from classes import *
from ast import literal_eval
from time import time
from general import *

data_file = "info/scrape/scrape_"+VERSION+".txt"

start = time()

all_courses = []
raw_data = []
with open(data_file, "r") as f:
    for lines in f:
        raw_data.append(lines[:-1])

for raw in raw_data:
    raw1 = raw.split('\t')
    c = raw1[0].split('|')
    new_course = Course()
    new_course.set_all(c[0], c[1], int(c[2]), c[3], c[4])
    new_course.credit = list(map(int, literal_eval(c[5])))
    for i in range(len(raw1)-1):
        raw2 = raw1[i+1].split('\\z')
        i = raw2[0].split('|')
        new_inst = Instructor(i[0])
        new_inst.rating = float(i[1])
        for j in range(len(raw2)-1):
            t = raw2[j+1].split('|')
            new_term = Term(t[0])
            new_term.set_all(list(map(float, literal_eval(t[3]))), t[-2], t[-1], t[2], list(map(int, literal_eval(t[4]))), t[1])
            new_inst.add_term(new_term)
        new_course.add_inst(new_inst)
    all_courses.append(new_course)

print("Time taken: " + str(time()-start))
