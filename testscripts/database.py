import pymysql
import csv
import setup

notes = '''
This script will tell you how to format your queries accordingly.
You have to follow this pattern.
Add necessary triggers to CreateDatabase.sql file and make a pull request.
I will further update this file with more required queries and you can fill them.
'''

reg_id_year = None
year = None
semester = None
section = None

database = pymysql.connect('localhost', 'root', 'anitscse034')
database.autocommit(True)
db = database.cursor()

def initialise_database():
    '''
    :return: None
    Pareses CreateDatabase.sql and Operations.sql to fetch SQL statements and
    creates database
    creates tables
    adds constraints
    creates triggers and funcs
    '''
    db.execute("SHOW DATABASES")
    databases = db.fetchall()
    if ('SEA',) in databases:
        db.execute('USE SEA')
        return
    if ('sea',) in databases:
        db.execute('USE sea')
        return

    try:
        for file in ('CreateDatabase.sql', 'Operations.sql'):
            with open(file, 'r') as queries_file:
                queries = queries_file.read()
                query = queries.split('--')
                for i in range(0, len(query), 2):
                    new_query = query[i]
                    new_query = new_query.replace('\n', ' ')
                    new_query = new_query.replace('\t', ' ')
                    if new_query == '': continue
                    db.execute(new_query)
        setup.display()
    except:
        db.execute('DROP DATABASE SEA')

def validate_login(faculty_id, faculty_password):
    '''
    :return: None
    '''
    query = "SELECT * FROM Faculty WHERE faculty_id = '%s' and faculty_password = '%s'" % (faculty_id, faculty_password)
    data = db.fetchall()
    if len(data) == 0:
        pass #show on window
        return
    

def init_student_table(student_file):
    '''
    :param student_file: csv file containing students data
    :return: None

    Will insert the data from student_file to student table
    '''
    with open(student_file) as student_data:
        student_reader = csv.reader(student_data, delimiter = ',')
        for student in student_reader:
            query = "INSERT INTO Student VALUES ('%s', '%s', '%s')" % tuple(student)
            db.execute(query)

def init_scripts_table(scripts_file):
    '''
    :param scripts_file: csv file containing scripts data
    :return: None

    Will insert the data from scripts_file to script table
    '''
    with open(scripts_file) as script_data:
        script_reader = csv.reader(script_data, delimiter=',')
        for script in script_reader:
            query = "INSERT INTO Script VALUES ('%s', '%s', %s, '%s', '%s', '%s')" % tuple(script)
            db.execute(query)

def get_student_regids():
    '''
    :return: List of student reg_id
    '''
    global reg_id_year, section
    query = "SELECT reg_id from Student WHERE reg_id LIKE '%s%' and section = '%s'" % tuple(reg_id_year, section)
    db.execute(query)
    reg_ids = db.fetchall()
    reg_ids = [reg[0] for reg in reg_ids]
    if reg_ids == []:
        return ['Reg Id']
    return reg_ids

def get_script_runtime(script_id):
    '''
    :param script_id: The PK of the script
    :return: string of runtime of the script
    '''
    query = "SELECT script_runtime FROM Script WHERE script_id = '%s'" % (script_id)
    db.execute(query)
    runtime = db.fetchall()[0][0]
    return runtime

def get_weeks_list():
    '''
    :return: a list of the weeks
    '''
    global year, semester
    query = "SELECT DISTINCT script_week FROM Script WHERE script_id LIKE 'CSE%s%s%'" % (year, semester)
    db.execute(query)
    weeks = db.fetchall()
    weeks_list = [str(week[0]) for week in weeks]
    weeks_list.sort()
    if weeks_list == []:
        return ['week no']
    return weeks_list

def get_script_path(roll_no):
    '''
    :param roll_no: the roll no of the student
    :return: the path of his scripts
    '''
    global year, semester
    query = "SELECT dir FROM Student where reg_id = '%s'" % (roll_no)
    db.execute(query)
    data = db.fetchall()
    directory = data[0][0]
    return directory

def get_script_names():
    '''
    :return: Tuple of all script names
    '''
    global year, semester
    query = "SELECT script_name FROM Script WHERE script_id LIKE 'CSE%s%s%'" % (year, semester)
    db.execute(query)
    script_names = db.fetchall()
    return script_names

def get_script_names_for_week(week_no):
    '''
    :param week_no: The week in which the program has to be done
    :return: returns a tuple of all script names
    '''
    query = "SELECT script_name FROM Script WHERE script_week = %s AND WHERE script_id LIKE 'CSE%s%s%'" % (week_no, year, semester)
    db.execute(query)
    scripts = db.fetchall()
    script_names = [script[0] for script in scripts]
    script_names.sort()
    if script_names == []:
        return ['script name']
    return tuple(script_names)

def get_script(script_id):
    '''
    :param reg_id: Registration id of student
    :param script_id: Script id
    :return: The script_name
    '''
    query = "SELECT script_name FROM Script WHERE script_id = '%s'" % (script_id)
    db.execute(query)
    script = db.fetchall()
    return script[0][0]

def get_script_id(script_name):
    '''
    :param script_name: The name of the script
    :return: The id of the script
    '''

    query = "SELECT script_id FROM Script WHERE script_name = '%s'" % (script_name)
    db.execute(query)
    script_id = db.fetchall()[0][0]
    return script_id

def get_input_text(script_id):
    '''
    :param script_id: The script id of the script to extract the input text
    :return: The input text
    '''
    query = "SELECT script_input FROM Script WHERE script_id = '%s'" % (script_id)
    db.execute(query)
    input_text = db.fetchall()[0][0]
    return input_text

def award_grade(reg_id, script_id, grade):
    '''
    :param roll_no: The roll no of the student
    :param script_id: The script to be awarded
    :param grade: The grade to be awarded
    :return: None
    '''
    check_query = "SELECT * FROM Grade WHERE reg_id = '%s' and script_id = '%s'" % (reg_id, script_id)
    if db.execute(check_query) == 1:
        query = "UPDATE Grade SET grade = %s WHERE reg_id = '%s' and script_id = '%s'" % (grade, reg_id, script_id)
    else:
        query = "INSERT INTO Grade VALUES ('%s', '%s', %s, curdate())" % (reg_id, script_id, grade)
    db.execute(query)

def get_query_data(script_name, grade, bound):
    '''
    :param script_id: The script name for evaluation
    :param grade: A to F
    :param bound: >, = or < the grade
    :return: query data
    '''
    if bound == 'All':
        bound = '>='
        grade = 0

    if script_name == 'All':
        query = "SELECT S.reg_id, S.name, S.marks FROM Student S WHERE S.marks %s %s" % (bound, grade)
    else:
        scriptid_query = "SELECT script_id from Script where script_name = '%s'" % (script_name)
        db.execute(scriptid_query)
        script_id = db.fetchall()[0][0]
        query = "SELECT S.reg_id, S.name, S.marks FROM Student S, Grade G WHERE G.grade %s %s AND G.script_id = '%s' AND G.reg_id = S.reg_id" % (bound, grade, script_id)
    db.execute(query)
    query_data = db.fetchall()
    return query_data