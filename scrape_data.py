from process_data import all_courses
import json
from general import *

a = []
black = []
black_file = open(black_list_file, 'w')
urls = [next_sem, last_sem, last_last_sem]
courses_data = {}

print(len(all_courses))
online = 'ARR'
for i, c in enumerate(all_courses):
    flag = False
    credit = []
    notes = ''
    instruct = []
    seen = []
    cr = 0
    timings = {}
    sem = 0
    if(c.code >= 100 and c.code <= 299): credit.append(credits['100-299'])
    elif(c.code >= 300 and c.code <= 399): credit.append(credits['300+'])
    elif(c.code >= 400 and c.code <= 499): credit.append(credits['400+'])
    elif(c.code >= 500): credit.append(credits['Grad'])
    for i, url in enumerate(urls):
        u = url[0] + c.department + "/" + c.name + url[1]
        b = bs(get(u).content, "lxml").findAll("pre")
        if (b != []):
            timing_flag = True
            flag = True
            # with open(courses_folder_path+c.name, "w+") as f: f.write(b[1].get_text())
            sem = 1 if(url[0].split('/')[-2] in u) else 0
            cr = float(b[1].findChild().get_text().split('(')[1][:-4].split('-')[-1])
            b = b[1].get_text().split("\r\n")
            for cont in b:
                st = cont.strip()
                st2 = st.split()
                if(url[0].split('/')[-2] in u):
                    try:
                        int(st2[-1]); int(st2[-2]); int(st2[-3])
                        inst = st2[-5:-3]
                        for i in c.instructors:
                            if(inst[0] in i.name and inst[1] in i.name):
                                if(inst not in seen):
                                    seen.append(inst)
                                    instruct.append(i.name)
                                time = st2[-9]
                                if(time != online):
                                    days = list(st2[-8]) if ('D' not in st2[-8]) else (list('MTWRF') + st2[-8][1:])
                                    full = time.split('-')[0]
                                    time = int(full[:2])
                                    if(full[-1] == 'A'):
                                        if(time >= 6 and time <= 10): 
                                            try: 
                                                timings[i.name][0].append(1)
                                                timings[i.name][1] += days
                                            except: timings[i.name] = [[1], days]
                                        elif(time >= 11):
                                            try: 
                                                timings[i.name][0].append(2)
                                                timings[i.name][1] += days
                                            except: timings[i.name] = [[2], days]
                                    elif(full[-1] == 'P'):
                                        if(time <= 4):
                                            try: 
                                                timings[i.name][0].append(2)
                                                timings[i.name][1] += days
                                            except: timings[i.name] = [[2], days]
                                        elif(time >= 5 and time <= 11):
                                            try: 
                                                timings[i.name][0].append(3)
                                                timings[i.name][1] += days
                                            except: timings[i.name] = [[3], days]
                                    timings[i.name][0] = list(set(timings[i.name][0]))
                                    timings[i.name][1] = list(set(timings[i.name][1]))
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
                elif('Mathematical Modeling' in st): credit.append(7)
                elif('Intensive Writing' in st): credit.append(11)
                if ((st.startswith(c.sub[-1] + " " + str(c.code))) or (st.startswith(c.sub[-1] + str(c.code) + ":"))) and (notes == ""):
                    st2 = ":".join(st.split(':')[1:])
                    notes = st2[1:]
                    n = b[b.index(cont)+1].strip()
                    try:
                        if (str.islower(n[0]) or (type(st2[-1]) == int) or (st2.endswith('or')) or (st2.endswith('and'))):
                            notes += ' ...'
                    except: notes = notes
            
            break
    if(not flag): black_file.write(c.name + "\n")

    output = {"credits_fulfilled": list(set(credit)), 
            "notes": notes, "url": u, 
            "number_credits": cr, 
            "next_sem": sem, 
            "instructors": instruct, 
            "timings": timings} # making dictionary for the json output
    courses_data[c.name] = output

    print(all_courses.index(c))

with open(scrape_file) as f:
    json.dump(courses_data, f, indent=4, sort_keys=True)
