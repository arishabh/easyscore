#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : get_data.py
# Author            : Rishabh Agrawal <rishabhagrawal41@gmail.com>
# Date              : 27.10.2019
# Last Modified Date: 28.10.2019

from requests import get
from bs4 import BeautifulSoup as bs
from process_data import all_courses

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

next_sem = ["https://registrar.indiana.edu/browser/soc4202/", ".shtml"]
last_sem = ["https://registrar.indiana.edu/browser/soc4198/", ".shtml"]
last_last_sem = ["https://registrar.indiana.edu/browser/soc4195/", ".shtml"]
url = [next_sem, last_sem, last_last_sem]
a = []
black = []
credit_file = open("info/misc/course_credits.txt", "a") 
black = open("info/misc/black_list.txt", "w+") 
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
            black.write(c.name+"\n")
    print(all_courses.index(c))

"""
print(len(all_courses))
for i in range(3631,len(all_courses)):
    c = all_courses[i]
    credit = []
    if(c.code >= 300 and c.code <= 399): credit.append(credits['300+'])
    if(c.code >= 400 and c.code <= 499): credit.append(credits['400+'])
    for i in range(len(url)):
        u = url[i][0] + c.department + "/" + c.name + url[i][1]
        b = bs(get(u).content, "lxml").findAll("pre")
        if (b != []):
            b = b[1].get_text().split("\r\n")
            b = [a.strip() for a in b]
            for cont in b:
                if (cont.startswith("COLL (CASE)") and credits[cont[12:]] not in credit):
                            credit.append(credits[cont[12:]])
            i = len(url)
    credit_file.write(c.name + '\t' + str(credit) + "\n")
    print(all_courses.index(c))
