from general import *
start = time()
from process_data import all_courses

final_courses = []
black_list = []
all_scores = []

all_info = []

with open(scrape_file, "r") as f:
    all_info = json.load(f)

with open(black_list_file, "r") as f:
    black_list = [l.strip("\n") for l in f]

for c in all_courses:
    if c.name in black_list: continue
    this_info = all_info[c.name]
    for i in c.instructors:
        i.calc_data()
        all_scores.append(i.rating)
        c.sems += len(i.terms)
        if(i.name in this_info["instructors"]): i.next_sem = 1
        try:
            i.timings = this_info["timings"][i.name] 
        except:
            i.timings = [[],[]]
    c.credit = this_info["credits_fulfilled"]
    c.preq = this_info["notes"]
    c.url = this_info["url"]
    c.cr = this_info["number_credits"]
    c.next_sem = this_info["next_sem"]
    if(this_info[c.name] == []): c.new_instructor = 1
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
    json.dump(json_data, f, indent=1)
    
print("time taken: " +str(time()-start))
