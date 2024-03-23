import subprocess 
import os 
import platform
import errno

name = "brainbay.exe"

def find_program(program):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([program], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == errno.ENOENT:
            return False
    return True

if __name__ == "__main__":
    if find_program(name):
        if platform.system() == "Windows":
            cmd = "where"
        else:
            cmd = "which"
        print(subprocess.call([cmd, name]))