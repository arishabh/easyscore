from general import *
start = time()
from process_data import all_courses

final_courses = []
black_list = []
course_credits = {}
course_notes = {}
course_urls = {}
course_cr = {}
course_next_sem = {}
instruct = {}
timings = {}
all_scores = []

all_info = []

with open(path+"scrape/scrape_v10.txt", "r") as f:
    for line in f:
        d = line[:-1].split('\t')
        all_info.append(d)
        course_credits[d[0]] = literal_eval(d[1])
        course_notes[d[0]] = d[2]
        course_urls[d[0]] = d[3]
        course_cr[d[0]] = float(d[4])
        course_next_sem[d[0]] = int(d[5])
        instruct[d[0]] = literal_eval(d[6])
        timings[d[0]] = literal_eval(d[7])

with open(black_list_file, "r") as f:
    black_list = [l.strip("\n") for l in f]

for c in all_courses:
    if c.name not in instruct: continue
    for i in c.instructors:
        i.calc_data()
        all_scores.append(i.rating)
        c.sems += len(i.terms)
        if(i.name in instruct[c.name]): i.next_sem = 1
        try:
            i.timings = timings[c.name][i.name] 
        except:
            i.timings = [[],[]]
    c.credit = course_credits[c.name]
    c.preq = course_notes[c.name]
    c.url = course_urls[c.name]
    c.cr = course_cr[c.name]
    c.next_sem = course_next_sem[c.name]
    if(instruct[c.name] == []): c.new_instructor = 1
    c.instructors.sort(reverse=True)
    c.rate()
    final_courses.append(c)

with open(stat_file, "w+") as f:
    f.write("Mean: " + str(mean(all_scores)) + "\n")
    f.write("Max: " + str(max(all_scores)) + "\n")
    f.write("Min: " + str(min(all_scores)) + "\n")
    f.write("Median: " + str(median(all_scores)) + "\n")
    f.write("Stardard Deviation: " + str(stdev(all_scores)) + "\n")
    f.write("Time taken for program: " + str(time()-start)) 

with open(final_file, "w+") as f:
    json_data = {"courses": []}
    for course in all_courses:
        json_data["courses"].append(json.loads(course.to_json()))
    json.dump(json_data, f, indent=2, sort_keys=True)
    
print("time taken: " +str(time()-start))
