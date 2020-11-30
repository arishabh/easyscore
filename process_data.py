from general import *
from os import listdir

all_courses = []
all_course_names = []
data = []

def add_instructor(data, course):
    new_inst = Instructor(data[9])
    new_inst = add_term(data, new_inst)
    course.add_inst(new_inst)
    return course

def add_term(data, inst):
    for t in inst.terms:
        if(t.term == data[0]): return inst
    new_term = Term(data[0])
    new_term.set_all(data[15:19], data[13], data[12], data[10], data[20:33], data[2])
    inst.add_term(new_term)
    return inst

for csv_file in listdir(raw_data_file):
    info = read_csv(raw_data_file+csv_file, low_memory=False, header=0).values
    for raw_data in info:
        data=[]
        for elem in raw_data:
            try:
                data.append(elem.strip())
            except:
                data.append(elem)
        name = data[5]+str(data[6])
        if type(data[9]) == float: continue
        if(data[10]>5):
            if(name not in all_course_names):
                all_course_names.append(name)
                new_course = Course()
                new_course.set_all(data[4], data[5], data[6], data[8], name)
                new_course = add_instructor(data, new_course)
                all_courses.append(new_course)

            else:
                ind = all_course_names.index(name)
                c = all_courses[ind]
                if(data[9] not in c.instructor_names):
                    all_courses[ind] = add_instructor(data, all_courses[ind])
                else:
                    ind2 = c.instructor_names.index(data[9])
                    all_courses[ind].instructors[ind2] = add_term(data, all_courses[ind].instructors[ind2])
