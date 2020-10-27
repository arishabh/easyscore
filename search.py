#TODO session days timing search filter
from classes import *
from general import *

all_courses = []
raw_data = []
filtered = []
with open(scrape_file, "r") as f:
    for lines in f:
        raw_data.append(str(lines[:-1]))

def search_all(dep='', sub='', code='', inst='', credit='', level='', cr='', next_sem='', keyword='', timings='', days=[], raw_data=raw_data):
    all_courses = []
    start = time()
    filtered = raw_data
    if(timings != '' or days != []): next_sem = '1'
    if(dep != '' and dep != 'ANY'): filtered = list(filter(lambda d: (d.split('|')[0] == dep), filtered))
    if(sub != ''): 
        sub = str.upper(sub.strip())
        if(len(sub) > 2):
            filtered = list(filter(lambda d: (d.split('|')[1] == sub), filtered))
        else:
            filtered = list(filter(lambda d: (d.split('|')[1][-1] == sub), filtered))
    if(code != ''): filtered = list(filter(lambda d: (d.split('|')[2] == code.strip()), filtered))
    if(credit != '' and credit != 'ANY'): filtered = list(filter(lambda d: (int(credit) in list(map(int, literal_eval(d.split('\t')[0].split('|')[5])))), filtered))
    if(level != '' and level != 'ANY'): filtered = list(filter(lambda d: (int(level) in list(map(int, literal_eval(d.split('\t')[0].split('|')[5])))), filtered))
    if(inst != ''):
        filtered2=[]
        inst = "".join((char if char.isalpha() else " ") for char in inst).split()
        for d in filtered:
            f=list(filter(lambda x: all((str.upper(word) in str.upper(x.split('|')[0])) for word in inst), d.split('\t')[1:]))
            if f != []:
                filtered2.append(d.split('\t')[0] + '\t' + f[0])
        filtered = filtered2
    if(cr != '' and cr != "ANY"): 
        if(cr != '7'):
            filtered=list(filter(lambda x: (int(float(x.split('|')[10])) == int(cr)), filtered))
        else:
            filtered=list(filter(lambda x: (int(float(x.split('|')[10]) >= 7)), filtered))

    if(next_sem == '1'):
        filtered=list(filter(lambda x: (x.split('|')[11] == '1'), filtered))
        filtered2 = []
        for d in filtered:
            f = list(filter(lambda x: (x.split('|')[6] == '1'), d.split('\t')[1:]))
            if f == []: continue
            filtered2.append(d.split('\t')[0])
            for x in f: filtered2[-1] += '\t' + x
        filtered = filtered2
        print(len(filtered))

        if(timings != "" and timings != 'ANY'):
            filtered2 = []
            for d in filtered:
                f = list(filter(lambda x: (int(timings) in literal_eval(x.split('|')[7].split('\z')[0])[0]), d.split('\t')[1:]))
                if not f: continue
                filtered2.append(d.split('\t')[0])
                for x in f: filtered2[-1] += '\t' + x
            filtered = filtered2

        if(days != [] and days != 'ANY'):
            filtered2 = []
            for d in filtered:
                f = list(filter(lambda x: (any(y in literal_eval(x.split('|')[7].split('\z')[0])[1] for y in days)), d.split('\t')[1:]))
                if not f: continue
                filtered2.append(d.split('\t')[0])
                for x in f: filtered2[-1] += '\t' + x
            filtered = filtered2
    
    if(keyword != ''): 
        keyword = keyword.replace("-", " ") 
        filtered=list(filter(lambda x: (all(str.upper(word) in str.upper(x.split('|')[3]) or str.upper(word) in str.upper(x.split('|')[0]) or str.upper(word) in str.upper(x.split('|')[1])  or str.upper(word) in str.upper(x.split('|')[2])for word in keyword.split())), filtered))
    
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
        new_course.cr = float(c[10]) if float(c[10])%1 != 0 else int(c[10])
        new_course.next_sem = int(c[11])
        new_course.new_teacher = int(c[12])
        for i in range(len(raw1)-1):
            raw2 = raw1[i+1].split('\\z')
            i = raw2[0].split('|')
            new_inst = Instructor(i[0])
            new_inst.rating = float(i[1])
            new_inst.avg_grades = list(map(float, literal_eval(i[2])))
            new_inst.range = i[3]
            new_inst.sems = int(i[4])
            new_inst.avg_std = float(i[5])
            new_inst.next_sem = int(i[6])
            new_inst.timings = literal_eval(i[7])
            for j in range(len(raw2)-1):
                t = raw2[j+1].split('|')
                new_term = Term(t[0])
                new_term.set_all(list(map(float, literal_eval(t[3]))), t[-2], t[-1], t[2], list(map(int, literal_eval(t[4]))), t[1])
                new_inst.add_term(new_term)
            new_course.add_inst(new_inst)
        all_courses.append(new_course)
    all_courses.sort(reverse=True)
    print("Time taken: " + str(time()-start)," Len: ", len(all_courses))
    return all_courses


