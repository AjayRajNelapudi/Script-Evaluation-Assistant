from subprocess import Popen, PIPE
from contextlib import suppress
import time

def execute(command):
    proc = Popen(command, stdin = PIPE, stdout = PIPE, shell = True)
    while proc.poll() is None:
        stdout = proc.stdout.readline().decode()
        print(stdout, end = ' ')
        proc.stdin.write(b'5\n')
        with suppress(Exception):
            proc.stdin.flush()
        import time
        time.sleep(3)

    stdout = proc.stdout.readline().decode()
    print(stdout, end = ' ')
        
try:
    Popen(['gcc', 'DisplayN.c']).wait()
    execute('./a.out')
except:
    print('error')