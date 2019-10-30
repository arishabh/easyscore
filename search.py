from classes import *
from ast import literal_eval
from time import time

VERSION = "v5.1"

data_file = "info/scrape_"+VERSION+".txt"
search_op_file = "info/search_op_"+VERSION+".txt"

credits = {'A&H Breadth of Inquiry credit':0,
        'Diversity in U.S. credit':1,
        'S&H Breadth of Inquiry credit':2,
        'N&M Breadth of Inquiry credit':3,
        'Global Civ & Culture credit':4,
        'Public Oral Communication credit':5,
        'English Composition credit':6,
        'Mathematical Modeling credit':7,
        '300+':8,
        '400+':9}


all_courses = []
raw_data = []
filtered = []
with open(data_file, "r") as f:
    for lines in f:
        raw_data.append(lines[:-1])

def search_all(dep='', sub='', code='', inst='', credit=''):
    all_courses = []
    start = time()
    filtered = raw_data
    if(dep != ''): filtered = list(filter(lambda d: (d.split('|')[0] == dep), filtered))
    if(sub != ''): filtered = list(filter(lambda d: (d.split('|')[1] == sub), filtered))
    if(code != ''): filtered = list(filter(lambda d: (d.split('|')[2] == code), filtered))
    if(credit != ''):
        credit = credits[c]
        filtered = list(filter(lambda d: (credit not in list(map(int, literal_eval(d.split('\t')[0].split('|')[5])))), filtered))
    if(inst != ''):
        filtered2=[]
        for d in filtered:
            f=list(filter(lambda x: (x.split('|')[0] == inst), d.split('\t')[1:]))
            if f != []:
                filtered2.append(d.split('\t')[0] + '\t' + f[0])
        filtered = filtered2
    for raw in filtered:
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
    all_courses.sort(reverse=True)
    print(all_courses)
    with open(search_op_file, "w+") as f:
        for c in all_courses:
            f.write(c.to_string())
    print("Time taken: " + str(time()-start))
