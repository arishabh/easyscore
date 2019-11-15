#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : process_data.py
# Author            : Rishabh Agrawal <rishabhagrawal41@gmail.com>
# Date              : 22.10.2019
# Last Modified Date: 28.10.2019

from general import *
start = time()

all_courses = []
all_course_names = []
data = []
black_list = []
course_credits = {}
course_preqs = {}
course_urls = {}
course_cr = {}
course_next_sem = {}
instruct = {}
all_scores = []

with open(course_file, "r") as f:
    for line in f:
        d = line[:-1].split('\t')
        course_credits[d[0]] = literal_eval(d[1])
        course_preqs[d[0]] = d[2]
        course_urls[d[0]] = d[3]
        course_cr[d[0]] = d[4]
        course_next_sem[d[0]] = d[5]
        instruct[d[0]] = literal_eval(d[6])

with open(black_list_file, "r") as f:
    black_list = [l.strip("\n") for l in f]

def add_instructor(data, course):
    new_inst = Instructor(data[9])
    new_inst = add_term(data, new_inst)
    course.add_inst(new_inst)
    return course

def add_term(data, inst):
    for t in inst.terms:
        if(t.term == data[0]): return inst
    new_term = Term(data[0])
    new_term.set_all(data[15:19], data[13], data[12], data[10], data[20:33], data[3])
    inst.add_term(new_term)
    return inst

for i in range(1, total_files+1):
    info = read_csv(raw_data_file+str(i)+".csv", low_memory=False, header=0).values
    for raw_data in info:
        for elem in raw_data:
            try:
                data.append(elem.strip())
            except:
                data.append(elem)
        name = data[5]+str(data[6])
        if(data[10]>5) and (name not in black_list):
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
        data = []

for c in all_courses:
    for i in c.instructors:
        i.calc_data()
        all_scores.append(i.rating)
        c.sems += len(i.terms)
        if(i.name in instruct[c.name]): i.next_sem = 1
    c.credit = course_credits[c.name]
    c.preq = course_preqs[c.name]
    c.url = course_urls[c.name]
    c.cr = course_cr[c.name]
    c.next_sem = course_next_sem[c.name]
    if(instruct[c.name] == []): c.new_teacher = 1
    c.instructors.sort(reverse=True)
    c.rate()

"""
all_scores.sort()

for c in all_courses:
    for i in c.instructors:
        ind = all_scores.index(i.rating)
        i.rating = round(100*ind/len(all_scores),2)
        all_scores[ind] = i.rating
    c.instructors.sort(reverse=True)
"""

with open(stat_file, "w+") as f:
    f.write("Mean: " + str(mean(all_scores)) + "\n")
    f.write("Max: " + str(max(all_scores)) + "\n")
    f.write("Min: " + str(min(all_scores)) + "\n")
    f.write("Median: " + str(median(all_scores)) + "\n")
    f.write("Stardard Deviation: " + str(stdev(all_scores)) + "\n")
    f.write("Time taken for program: " + str(time()-start)) 

with open(main_file, "w+") as f:
    for course in all_courses:
        f.write(course.to_string())

with open(scrape_file, "w+") as f:
    for course in all_courses:
        f.write(course.to_string2())
    
print("time taken: " +str(time()-start))
