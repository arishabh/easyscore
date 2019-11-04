from classes import *
from ast import literal_eval
from time import time
from general import *

all_courses = []
raw_data = []
filtered = []
with open(scrape_file, "r") as f:
    for lines in f:
        raw_data.append(lines[:-1])

def search_all(dep='', sub='', code='', inst='', credit='', cr='', next_sem=''):
    all_courses = []
    start = time()
    filtered = raw_data
    sub = str.upper(sub)
    print(cr)
    if(dep != '' and dep != 'ANY'): filtered = list(filter(lambda d: (d.split('|')[0] == dep), filtered))
    if(sub != ''): 
        if(len(sub) > 2):
            filtered = list(filter(lambda d: (d.split('|')[1] == sub), filtered))
        else:
            filtered = list(filter(lambda d: (d.split('|')[1][-1] == sub), filtered))
    if(code != ''): filtered = list(filter(lambda d: (d.split('|')[2] == code), filtered))
    if(credit != '' and credit != 'ANY'):
        filtered = list(filter(lambda d: (credits[credit] in list(map(int, literal_eval(d.split('\t')[0].split('|')[5])))), filtered))
    if(inst != ''):
        filtered2=[]
        inst = "".join((char if char.isalpha() else " ") for char in inst).split()
        for d in filtered:
            f=list(filter(lambda x: all((str.upper(word) in str.upper(x.split('|')[0])) for word in inst), d.split('\t')[1:]))
            if f != []:
                filtered2.append(d.split('\t')[0] + '\t' + f[0])
        filtered = filtered2
    if(cr != '' and cr != "ANY"): filtered=list(filter(lambda x: (int(x.split('|')[10]) >= int(cr)), filtered))
    print(str(next_sem))
    if(next_sem == ['1']): filtered=list(filter(lambda x: (x.split('|')[11].split('\t')[0] == '1'), filtered))
    for raw in filtered:
        raw1 = raw.split('\t')
        c = raw1[0].split('|')
        new_course = Course()
        new_course.set_all(c[0], c[1], int(c[2]), c[3], c[4])
        new_course.credit = list(map(int, literal_eval(c[5])))
        new_course.rating = float(c[6])
        new_course.sems = int(c[7])
        new_course.preq = c[8]
        new_course.url = c[9]
        new_course.cr = int(c[10])
        for i in range(len(raw1)-1):
            raw2 = raw1[i+1].split('\\z')
            i = raw2[0].split('|')
            new_inst = Instructor(i[0])
            new_inst.rating = float(i[1])
            new_inst.avg_grades = list(map(float, literal_eval(i[2])))
            new_inst.range = i[3]
            new_inst.sems = int(i[4])
            new_inst.avg_std = float(i[5])
            for j in range(len(raw2)-1):
                t = raw2[j+1].split('|')
                new_term = Term(t[0])
                new_term.set_all(list(map(float, literal_eval(t[3]))), t[-2], t[-1], t[2], list(map(int, literal_eval(t[4]))), t[1])
                new_inst.add_term(new_term)
            new_course.add_inst(new_inst)
        all_courses.append(new_course)
    all_courses.sort(reverse=True)
    with open(search_op_file, "w+") as f:
        for c in all_courses:
            f.write(c.to_string())
    print("Time taken: " + str(time()-start))
    return all_courses


