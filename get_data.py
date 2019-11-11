#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : get_data.py
# Author            : Rishabh Agrawal <rishabhagrawal41@gmail.com>
# Date              : 27.10.2019
# Last Modified Date: 28.10.2019

from process_data import all_courses
from general import *

a = []
black = []
black_file = open(black_list_file, 'w')
credit_file = open("info/misc/course_credits2.txt", "w") 
def get_cred(b):
    b = b[1].get_text().split("\r\n")
    b = [a.strip() for a in b]
    for cont in b:
        if (cont.startswith("COLL (CASE)")):
                if cont not in a:
                    return cont
"""

print(len(all_courses))
for i in range(len(all_courses)):
    c = all_courses[i]
    for i in range(len(url)):
        u = url[i][0] + c.department + "/" + c.name + url[i][1]
        b = bs(get(u).content, "lxml").findAll("pre")
        if (b != []):break
        elif(i == (len(url)-1)):
            black_list_file.write(c.name+"\n")
    print(all_courses.index(c))

"""
print(len(all_courses))
for i in range(len(all_courses)):
    flag = False
    c = all_courses[i]
    credit = []
    preq = ''
    instruct = {}
    seen = []
    if(c.code >= 100 and c.code <= 299): credit.append(credits['100-299'])
    elif(c.code >= 300 and c.code <= 399): credit.append(credits['300+'])
    elif(c.code >= 400 and c.code <= 499): credit.append(credits['400+'])
    elif(c.code >= 500): credit.append(credits['Grad']) 
    for i in range(len(url)):
        u = url[i][0] + c.department + "/" + c.name + url[i][1]
        b = bs(get(u).content, "lxml").findAll("pre")
        if (b != []):
            flag = True
            cr = int(b[1].findChild().get_text()[-5])
            b = b[1].get_text().split("\r\n")
            for cont in b:
                st = cont.strip()
                st2 = st.split()
                try:
                    int(st2[-1]); int(st2[-2]); int(st2[-3])
                    inst = st2[-5:-3]
                    if(inst not in seen):
                        seen.append(inst)
                        for i in c.instructors:
                            if(inst[0] in i.name and inst[1] in i.name): 
                                instruct[i.name] = 1
                                break;
                except: instruct = instruct
                if('HONORS' in st): credit.append(13)
                if('A&H' in st): credit.append(0)
                elif('N&M' in st): credit.append(3)
                elif('Diversity in U.S.' in st): credit.append(1)
                elif('S&H' in st): credit.append(2)
                elif('Global Civ' in st or 'World Culture' in st): credit.append(4)
                elif('Pubic Oral Communication' in st): credit.append(5)
                elif('English Composition' in st): credit.append(6)
                elif('Mathematical Modelling' in st): credit.append(7)
                elif('Intensive Writing' in st): credit.append(11)
                if ((st.startswith(c.sub[-1] + " " + str(c.code))) or (st.startswith(c.sub[-1] + str(c.code) + ":"))) and (preq == ""):
                    st2 = ":".join(st.split(':')[1:])
                    preq = st2[1:]
                    n = b[b.index(cont)+1].strip()
                    try:
                        if (str.islower(n[0]) or (type(st2[-1]) == int) or (st2.endswith('or')) or (st2.endswith('and'))):
                            preq += ' ...'
                    except: preq = preq
            
            break
    if(not flag): black_file.write(c.name + "\n")
    sem = 1 if(u.split('/')[4] in url[0][0]) else 0
    credit_file.write(c.name + '\t' + str(list(set(credit))) + "\t" + preq + "\t" + u + "\t" + str(cr) + "\t" + str(sem) + "\t" + str(instruct) +"\n")
    print(all_courses.index(c))
