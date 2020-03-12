import os
import subprocess
from avatar2 import *

WORK_DIR = "/home/ss/work/vxafl"
HOME = "/home/ss"
QEMU_VERSION = "2.10.0"
CPU_TARGET = "i386"
VXWORKS_VERSION = "6.6"
IMAGE_PATH = f"{HOME}/work/vxworks{VXWORKS_VERSION}/MS-DOS.vmdk"
VXWORKS_PATH = f"{HOME}/work/vxworks{VXWORKS_VERSION}/vxWorks"
QEMU_EXEC = f"{WORK_DIR}/qemu-{QEMU_VERSION}/{CPU_TARGET}-softmmu/qemu-system-i386 -hda {IMAGE_PATH} -s -nographic -vxafl-img {VXWORKS_PATH} -vxafl-entry CrashFunc -net tap,ifname=tap0 -net nic,model=pcnet"
cmdline = QEMU_EXEC.split(' ')
print(cmdline)
avatar = Avatar(arch=archs.X86)
target = avatar.add_target(GDBTarget, gdb_port=1234)

subprocess.Popen(cmdline, pass_fds=(199, 198))
# subprocess.Popen(cmdline)

target.init()  # connect the target
target.set_breakpoint("*{}".format(0x30d4d0))
in_the_entry = False

while True:
    target.cont()
    target.wait()
    if not in_the_entry:
        target.set_breakpoint("*{}".format(0x3189e0)) # excStub
        target.set_breakpoint("*{}".format(0x40cb30))
        target.set_breakpoint("*{}".format(0x40a250))
        target.set_breakpoint("*{}".format(0x312d50)) #excPanicShow
        target.set_breakpoint("*{}".format(0x00318a50)) # excStub1
        in_the_entry = True
    # esp = target.read_register('esp')
    # arg_addr = target.read_memory(esp+4, 4)
    # input_file = open(f"{WORK_DIR}/fuzzout/.cur_input", "rb")
    # test_case = input_file.read()
    # input_file.close()
    # arg_value_addr = target.read_memory(arg_addr, 4)
    # print(f"arg_addr:{arg_value_addr}")
    # target.write_memory(arg_value_addr, len(test_case), test_case)
    print("complete one")

