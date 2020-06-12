from process_data import all_courses
from general import *

a = []
black = []
black_file = open(black_list_file, 'w')
credit_file = open(course_file, 'w')
url = [next_sem, last_sem, last_last_sem]

print(len(all_courses))
for i in range(len(all_courses)):
    flag = False
    online = 'ARR'
    c = all_courses[i]
    credit = []
    preq = ''
    instruct = []
    seen = []
    cr = 0
    timings = {}
    sem = 0
    if(c.code >= 100 and c.code <= 299): credit.append(credits['100-299'])
    elif(c.code >= 300 and c.code <= 399): credit.append(credits['300+'])
    elif(c.code >= 400 and c.code <= 499): credit.append(credits['400+'])
    elif(c.code >= 500): credit.append(credits['Grad'])
    for i in range(len(url)):
        u = url[i][0] + c.department + "/" + c.name + url[i][1]
        b = bs(get(u).content, "lxml").findAll("pre")
        if (b != []):
            timing_flag = True
            flag = True
            # with open(courses_folder_path+c.name, "w+") as f: f.write(b[1].get_text())
            sem = 1 if(url[0][0].split('/')[-2] in u) else 0
            cr = b[1].findChild().get_text().split('(')[1][:-4].split('-')[-1]
            b = b[1].get_text().split("\r\n")
            for cont in b:
                st = cont.strip()
                st2 = st.split()
                if(url[0][0].split('/')[-2] in u):
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
    credit_file.write(c.name + '\t' + str(list(set(credit))) + "\t" + preq + "\t" + u + "\t" + str(cr) + "\t" + str(sem) + "\t" + str(instruct) + "\t" + str(timings) + "\n")
    print(all_courses.index(c))

