from subprocess import run, PIPE, Popen
from contextlib import suppress
import time
import os
import threading

from tkinter import *

separator = "/"
if os.name == 'nt':
    separator = "\\"

def static_execute(script, runtime, path, input_data):
    '''
    :param script: A string with the script to be executed
    :param path: A string og the path in which the script is present
    :param input_data: A string of the data to be passed as input to the script
    :return: 0 if exec successfully, 1 if not.

    Executes the given script as a seperate subprocess and stores its output in a file
    The inputs are given in advance and collected after the process finishes execution
    '''
    file = open(path + separator + 'op.txt', 'r+')
    file.truncate(0)
    file.close()

    if runtime == 'gcc':
        Popen(['gcc', script], cwd=path).wait()
        command = './a.out'
    else:
        command = ['python3', script]

    with open(path + '/op.txt', 'w') as output_file:
        start = time.time()
        status = run(command,
                                cwd=path,
                                input=input_data,
                                encoding='ascii',
                                stdout=output_file)
        stop = time.time()
        output_file.write('Time Taken: ' + str(stop - start) + 's\n')
    return status.returncode

class GCC_Dynamic_Execute:
    def __init__(self, script, path, output):
        if script is None or path is None or output is None: return
        with open(path + separator + script, 'r') as script_file:
            code = script_file.readlines()

        with open(path + separator + script, 'w') as script_file:
            for line in code:
                if "printf" in line and '/**/' not in line:
                    script_file.write(line[:-1] + ' printf("\\n"); fflush(stdout); /**/' + '\n')
                else:
                    script_file.write(line)

        Popen(['gcc', script], cwd = path).wait()

        self.proc = Popen('./a.out',
                     cwd=path,
                     stdin=PIPE,
                     stdout=PIPE,
                     shell=False)

        self.output = output
        self.console_display = 'None'
        self.read = True
        self.get_output()
        reader_thread = threading.Thread(target = self.reader)
        reader_thread.start()

    def __del__(self):
        self.read = False

    def set_input(self):
        if self.proc.poll(): return
        new_console = self.output.get('1.0', END)
        new_console = new_console.replace('\n', '')
        input_data = new_console.replace(self.console_display, '')
        self.write_input(input_data)

    def write_input(self, input_line):
        if self.proc.poll(): return
        input_line = input_line + '\n'
        self.proc.stdin.write(input_line.encode())
        with suppress(Exception):
            self.proc.stdin.flush()

    def get_output(self):
        self.proc.stdout.flush()
        stdout = self.proc.stdout.readline()
        stdout = stdout.decode()
        self.output.insert(INSERT, stdout)
        self.console_display = self.output.get('1.0', END)
        self.console_display = self.console_display.replace('\n', '')

    def reader(self):
        while self.read:
            self.get_output()
            time.sleep(0.1)