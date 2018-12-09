-- creating database --
create database MultiuserSea;
-- uaing multiuser database --
use MultiuserSea;
-- creating student database --
create table Student (
	reg_id char(12) primary key,
	section char(1) not null,
	name char(50) not null,
	files_path char(50) not null
);
-- creating faculty database --
create table Faculty (
	faculty_id char(10) primary key,
	faculty_name char(50) not null,
	faculty_password char(20) not null
);
-- creating semester database --
create table Semester (
	reg_id_year char(12) not null,
	year char(1) not null,
	semester char(1) not null,
	section char(1) not null,
	faculty_A char(10) not null,
	faculty_B char(10) not null
);
-- adding faculty_A_FK --
alter table Semester
add constraint faculty_A_Semester_FK foreign key(faculty_A)
references Faculty(faculty_id);
-- adding faculty_B_FK --
alter table Semester
add constraint faculty_B_Semester_FK foreign key(faculty_B)
references Faculty(faculty_id);
-- creating programs table --
create table Script (
    script_id char(8) primary key,
    script_name varchar(20) unique not null,
    script_week integer not null,
    script_desc varchar(100),
    script_input varchar(100),
    script_runtime varchar(20) not null
);
-- creating grading table --
create table Grade (
	reg_id char(12) not null,
	script_id char(8) not null,
	grade integer not null
);
-- adding reg_id_Grade_FK keys --
alter table Grade
add constraint reg_id_Grade_FK foreign key(reg_id)
references Student(reg_id);
-- adding script_id_Grade_FK keys --
alter table Grade
add constraint script_id_Grade_FK foreign key(script_id)
references Script(script_id);


