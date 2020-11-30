from classes import *
from general import *

filtered = []
with open(final_file, "r") as f:
    filtered = json.load(f)["courses"]

def search_all(credit_fulfill='', level='', cr='', next_sem='', keyword='', timings='', days=[], filtered=filtered):
    all_courses = []
    start = time()
    if(timings or days): next_sem = '1'
    
    # keyword search: Course name, course code, instructor (first and last) name
    if keyword:
        new_filtered = []
        words = keyword.lower().split()
        for course in filtered:
            for word in words:
                word = word.strip()
                if not((word in course["name"].lower()) or (word in course["full_code"].lower()) or any(word in i["name"] for i in course["instructors"])):
                    break
            else: new_filtered.append(course)
        filtered = new_filtered

    if(credit_fulfill and credit_fulfill != 'ANY'): 
        filtered = list(filter(lambda d: (int(credit_fulfill) in d["credits_fulfilled"]), filtered))

    if(level and level != 'ANY'): 
        filtered = list(filter(lambda d: (int(level) in d["credits_fulfilled"]), filtered))

    if(cr and cr != "ANY"):
        if(float(cr) < 7):
            filtered=list(filter(lambda x: x["credits"] == float(cr), filtered))
        else:
            filtered=list(filter(lambda x: x["credits"] >= 7, filtered))

    if(next_sem == '1'):
        filtered=list(filter(lambda x: (x["taught_next_semester"] == 1), filtered))
        filtered2 = []
        for d in filtered:
            filtered_inst = list(filter(lambda x: (x["is_teaching_next_semester"] == 1), d["instructors"]))
            if not filtered_inst: continue
            d["instructors"] = filtered_inst
            filtered2.append(d)
        filtered = filtered2

        if(timings and timings != 'ANY'):
            filtered2 = []
            for d in filtered:
                f = list(filter(lambda x: (int(timings) in x["timings"][0]), d["instructors"]))
                if not f: continue
                d["instructors"] = f
                filtered2.append(d)
            filtered = filtered2

        if(days != [] and days != 'ANY'):
            filtered2 = []
            for d in filtered:
                f = list(filter(lambda x: (any(y in x["timings"][1] for y in days)), d["instructors"]))
                if not f: continue
                d["instructors"] = f
                filtered2.append(d)
            filtered = filtered2
    
    print("Time taken: " + str(time()-start)," Len: ", len(filtered))
    return {"courses": filtered}
