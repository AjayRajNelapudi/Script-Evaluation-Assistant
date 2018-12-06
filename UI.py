from tkinter import *
from contextlib import suppress
import mysql
import runtime
import spreadsheets
import setup
import os

separator = "/"
if os.name == 'nt':
    separator = "\\"

class Exec_Helper:
    process = None
    def get_script_output():
        roll_no = regid_var.get()
        path = mysql.get_script_path(roll_no)
        script_name = script_var.get()
        script_id = mysql.get_script_id(script_name)
        input_text = input_entry.get()
        if input_text == '***':
            input_text = mysql.get_input_text(script_id)
        language = mysql.get_script_runtime(script_id)
        execution = exec_type.get()
        with suppress(Exception):
            os.chdir(path)
            os.system('rm a.out')

        if execution == 'static':
            if runtime.static_execute(script_name, language, path, input_text) == 0:
                file = open(path + '/op.txt', 'r')
                output = file.read()
                file.close()
            else:
                output = 'ERROR!'
            output_text.delete('1.0', END)
            output_text.insert(INSERT, output)
        else:
            output_text.delete('1.0', END)
            try:
                Exec_Helper.process = runtime.GCC_Dynamic_Execute(script_name, path, output_text)
            except:
                # display message = "Compile Time Error"
                pass

def enter_command(data):
    Exec_Helper.process.set_input()

def award_grade():
    try:
        roll_no = int(regid_var.get())
    except:
        return

    feedback = feedback_entry.get()
    script_name = script_var.get()
    script_id = mysql.get_script_id(script_name)
    grade = grade_entry.get()
    mysql.award_grade(roll_no, script_id, grade)

def display_spreadsheets_ui():
    spreadsheets.display()

def display_setup_ui():
    setup.display()

def display_script(script_name):
    code_text.delete('1.0', END)
    roll_no = regid_var.get()
    path = mysql.get_script_path(roll_no)

    with open(path + separator + script_name) as code_file:
        code_text.insert(INSERT, code_file.read())

def weekno_command(week_no):
    global script_names, script_var, scriptname_optionmenu
    script_names = mysql.get_script_names_for_week(week_no)
    script_var.set(script_names[0])
    scriptname_optionmenu = OptionMenu(window, script_var, *script_names, command = display_script)
    scriptname_optionmenu.place(x = 1120, y = 100, height = 30, width = 200)

def update_week_script(week_no):
    weekno_command(week_no)
    display_script(script_var.get())

def save_file():
    roll_no = regid_var.get()
    path = mysql.get_script_path(roll_no)
    code = code_text.get('1.0', END)
    script_name = script_var.get()
    if code != 'Select Script':
        file = open(path + separator + script_name, 'w')
        file.write(code)
        file.close()


mysql.initialise_database()

window = Tk()
window.geometry('1366x768')
window.title('Script Evaluation Assistant')
window.configure(background = 'light blue')

menubar = Menu(window)

file_menu = Menu(menubar)
file_menu.add_command(label='Save', command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Quit', command=exit)

view_menu = Menu(menubar)
view_menu.add_command(label='Setup', command=display_setup_ui)
view_menu.add_command(label='SpreadSheets', command=display_spreadsheets_ui)
view_menu.add_command(label='Insights')

about = Menu(menubar)
about.add_command(label='Application')
about.add_command(label='Team')

menubar.add_cascade(label='File', menu=file_menu)
menubar.add_cascade(label='View', menu=view_menu)
menubar.add_cascade(label='About', menu=about)

'''masthead = Label(window, text = 'Desiged and Developed by Shazam')
masthead.place(x = 450, y = 700, height = 50, width = 500)'''

window.bind('<Return>', enter_command)

code_label = Label(window, text = 'CODE', relief = RAISED)
code_label.place(x = 30, y = 50, height = 30, width = 100)
code_text = Text(window, font = ('Monaco', 14))
code_text.place(x = 30, y = 80, height = 400, width = 700)

output_title = Label(window, text = 'OUTPUT', relief = RAISED)
output_title.place(x = 30, y = 500, height = 30, width = 100)

output_text = Text(window, font = ('Monaco', 14))
output_text.place(x = 30, y = 530, height = 200, width = 700)

rollno_label = Label(window, text = 'Roll No', relief = RAISED)
rollno_label.place(x = 900, y = 50, height = 30, width = 100)

reg_ids = mysql.get_student_regids()
regid_var = StringVar(window)
regid_var.set(reg_ids[0])
rollno_optionsmenu = OptionMenu(window, regid_var, *reg_ids)
rollno_optionsmenu.place(x = 1020, y = 50, height = 30, width = 150)

script_spec = Label(window, text = 'Week & Script', relief = RAISED)
script_spec.place(x = 900, y = 100, height = 30, width = 100)

weeks = mysql.get_weeks_list()
week_var = StringVar(window)
week_var.set(weeks[0])
week_no = OptionMenu(window, week_var, *weeks, command = update_week_script)
week_no.place(x = 1020, y = 100, height = 30, width = 70)

script_names = mysql.get_script_names_for_week('1')
script_var = StringVar(window)
script_var.set(script_names[0])
scriptname_optionmenu = OptionMenu(window, script_var, *script_names, command = display_script)
scriptname_optionmenu.place(x = 1120, y = 100, height = 30, width = 200)

input_label = Label(window, text = 'Input', relief = RAISED)
input_label.place(x = 900, y = 150, height = 30, width = 100)

input_entry = Entry(window)
input_entry.place(x = 1020, y = 150, height = 100, width = 300)

exec_type = StringVar()
static_exec = Radiobutton(window, text = 'Static', variable = exec_type, value = 'static')
static_exec.place(x = 1020, y = 270)
dynamic_exec = Radiobutton(window, text = 'Dynamic', variable = exec_type, value = 'dynamic')
dynamic_exec.place(x = 1100, y = 270)

execute_button = Button(window, text = 'Execute', command = Exec_Helper.get_script_output)
execute_button.place(x = 1020, y = 320, height = 30, width = 140)

grade_label = Label(window, text = 'Grade', relief = RAISED)
grade_label.place(x = 900, y = 400, height = 30, width = 100)

grade_entry = Entry(window)
grade_entry.place(x = 1020, y = 400, height = 30, width = 120)

feedback_label = Label(window, text = 'Feedback', relief = RAISED)
feedback_label.place(x = 900, y = 450, height = 30, width = 100)

feedback_entry = Entry(window)
feedback_entry.place(x = 1020, y = 450, height = 100, width = 300)

grade_button = Button(window, text = 'Post Grade & Feedback', command = award_grade)
grade_button.place(x = 1020, y = 600, height = 30, width = 180)

window.config(menu = menubar)
window.mainloop()