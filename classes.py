import json

class Term:
    def __init__(self, name="", json_inp=''):
        if json_inp:
            self.from_json(json_inp)
        else:
            self.term = name
            self.cum_gpa = 0
            self.sect_gpa = 0
            self.grades_perc = []
            self.total_students = 0
            self.grade_dist = []
            self.sect_desc = ""

    def set_all(self, gr, cum_gpa, sect_gpa, tot, grade, desc):
        self.grades_perc = gr
        self.total_students = int(tot)
        self.grade_dist = grade
        self.cum_gpa = float(cum_gpa)
        self.sect_gpa = float(sect_gpa)
        self.sect_desc = desc

    def to_string(self):
        return ("\t\t" + self.term + " - " + str(self.sect_desc) + " - " + str(self.total_students) + " " + str(self.grades_perc) + " " + str(self.grade_dist) + " CGPA: " + str(self.cum_gpa) + " Sect: " + str(self.sect_gpa) + "\n")

    def to_json(self):
        output = {"term": self.term, 
                "section_description": self.sect_desc,
                "total_students": self.total_students,
                "grade_percentage": self.grades_perc,
                "grade_distribution": self.grade_dist,
                "cumilative_gpa": self.cum_gpa,
                "section_gpa": self.sect_gpa}
        return json.dumps(output)
    
    def from_json(self, inp):
        inp = json.loads(inp)
        self.term = inp.get("term")
        self.sect_desc = inp.get("section_description")
        self.total_students = inp.get("total_students")
        self.grades_perc = inp.get("grade_precentage")
        self.grade_dist = inp.get("grade_distribution")
        self.cum_gpa = inp.get("cumilative_gpa")
        self.sect_gpa = inp.get("section_gpa")

class Instructor:
    def __init__(self, name="", json_inp=''):
        if json_inp:
            self.from_json(json_inp)
        else:
            self.name = name
            self.terms = []
            self.rating = 0
            self.avg_grades = [0, 0, 0, 0]
            self.range = ""
            self.sems = 0
            self.avg_std = 0
            self.next_sem = 0
            self.timings = [[], []]

    def add_term(self, term):
        self.terms.append(term)

    def last_term(self):
        return self.terms[-1]

    def __lt__(self, other):
        latest_year = int(self.range.split("-")[-1])
        other_latest_year = int(other.range.split("-")[-1])
        if latest_year == other_latest_year:
            return self.rating < other.rating
        else:
            return latest_year < other_latest_year
    
    def __eq__(self, other):
        return other in self.name

    def rate(self):
        factor = 10
        diff = 96/11.0
        curr_year = 2019
        grey = 3
        latest_offset = 2/3.0
        old_offset = 1-latest_offset

        rating1 = 0
        rating2 = 0
        total1 = 0.0
        total2 = 0.0
        gpa_diff = 0
        grades1 = [0]*13
        grades2 = [0]*13
        for term in self.terms:
            if(int(term.term[-4:]) >= (curr_year-grey)):
                grades1 = [grades1[j] + int(term.grade_dist[j]) for j in range(13)]
                total1 += term.total_students
            else:
                grades2 = [grades2[j] + int(term.grade_dist[j]) for j in range(13)]
                total2 += term.total_students
            gpa_diff += term.sect_gpa-term.cum_gpa
        gpa_diff /= len(self.terms)
        if(total1 != 0):
            rating1 = 100*grades1[0]/total1
            for i in range(12):
                rating1 += (96-(diff*i))*(grades1[i+1]/total1)

        if(total2 != 0):
            rating2 = 100*grades2[0]/total2
            for i in range(12):
                rating2 += (96-(diff*i))*(grades2[i+1]/total2)
        if rating1 == 0: rating1 = rating2
        if rating2 == 0: rating2 = rating1
        self.rating = (latest_offset*rating1) + (old_offset*rating2)
        self.rating += gpa_diff*factor
        self.rating = round(self.rating, 2)
        self.rating = min(100, self.rating)
        self.rating = max(0, self.rating)

    def calc_data(self):
        lowest = 30000
        highest = 0
        self.sems = len(self.terms)
        for i in self.terms:
            self.avg_std += i.total_students
            year = int(i.term[-4:])
            if year>highest: highest=year
            if year<lowest: lowest=year
            self.avg_grades[0] += float(i.grades_perc[0])
            self.avg_grades[1] += float(i.grades_perc[1])
            self.avg_grades[2] += float(i.grades_perc[2])
            self.avg_grades[3] += float(i.grades_perc[3])
        if(lowest == highest): self.range=str(highest)
        else: self.range=str(lowest)+"-"+str(highest)
        for i in range(4):
            self.avg_grades[i] = round(self.avg_grades[i]/len(self.terms), 2)
        self.avg_std = round(self.avg_std/len(self.terms), 2)
        self.rate()
        if (self.avg_std < 10): self.rating = max(0, self.rating-(12-self.avg_std))
        if(self.sems < 3): self.rating = max(0, self.rating-(5-self.sems))
        if(self.sems > 7): min(100, self.rating+(self.sems-8))
        # elif(self.sems >= 4): min(100, self.rating+1)
        if(self.avg_std > 20): min(100, self.rating+(self.avg_std-20))
        self.rating = round(self.rating, 2)

    def to_string(self):
        out = "\t" + str(self.name) + " " + str(self.rating) + " " + str(self.avg_grades) + " " + self.range + " " + str(self.sems) + " sem." + str(self.avg_std) + ":\n"
        for term in self.terms:
            out += term.to_string()
        return out

    def to_json(self):
        output = {"name": self.name, 
                "rating": self.rating, 
                "average_grades": self.avg_grades, 
                "years_taught": self.range, 
                "semesters_taught": self.sems,
                "average_number_of_students": self.avg_std,
                "is_teaching_next_semester": self.next_sem,
                "timings": self.timings,
                "past_terms": []}
        for term in self.terms:
            output["past_terms"].append(json.loads(term.to_json()))
        
        return json.dumps(output)

    def from_json(self, inp):
        inp = json.loads(inp)
        self.name = inp.get("name")
        self.rating = inp.get("rating")
        self.avg_grades = inp.get("average_grades")
        self.range = inp.get("years_taught")
        self.sems = inp.get("semesters_taught")
        self.avg_std = inp.get("average_number_of_students")
        self.next_sem = inp.get("is_teaching_next_semester")
        self.timings = inp.get("timings")
        self.terms = [Term(json_inp=term) for term in inp.get("past_sems")]

class Course:
    def __init__(self, json_inp=''):
        if json_inp:
            self.from_json(json_inp)
        else:
            self.sub = ""
            self.instructors = []
            self.desc = ""
            self.department = ""
            self.code = 0
            self.name = ""
            self.instructor_names = []
            self.credit = []
            self.rating = 0
            self.sems = 0
            self.notes = ''
            self.url= ''
            self.cr = 0
            self.next_sem = 0
            self.new_instructor = 0
    
    def __lt__(self, other):
        if (self.rating == other.rating):
            return(self.sems < other.sems)
        else: return self.rating < other.rating

    def set_sub(self, sub):
        self.sub = sub
        self.name = self.sub + str(self.code)

    def set_code(self, code):
        self.code = code
        self.name = self.sub + str(self.code)

    def set_all(self, dep, sub, code, desc, name):
        self.department = dep
        self.sub = sub
        self.code = code
        self.name = name
        self.desc = desc

    def last_instructor(self):
        return self.instructors[-1]

    def add_inst(self, inst):
        self.instructors.append(inst)
        self.instructor_names.append(inst.name)

    def equals(self, course):
        flag = (self.department == course.department) and (self.name == course.name)
        return flag

    def to_string(self):
        out = self.name + " " + self.desc + " " + str(self.credit) + " " + str(self.rating) + " " + str(self.sems) + " " + self.notes + ":\n"
        for inst in self.instructors:
            out += inst.to_string()
        return out

    def to_json(self):
        output = {"full_code": self.name,
                "department": self.department,
                "subject": self.sub,
                "code": self.code,
                "name": self.desc,
                "credits": self.cr,
                "credits_fulfilled": self.credit,
                "rating": self.rating,
                "semesters_taught": self.sems,
                "notes": self.notes,
                "url": self.url,
                "taught_next_semester": self.next_sem,
                "new_instructor": self.new_instructor,
                "instructors": []}

        for inst in self.instructors:
            output["instructors"].append(json.loads(inst.to_json()))

    def from_json(self, inp):
        inp = json.loads(inp)
        self.sub = inp.get("subject")
        self.desc = inp.get("name")
        self.code = inp.get("code")
        self.department = inp.get("department")
        self.cr = inp.get("credits")
        self.name = inp.get("full_code")
        self.credit = inp.get("credits_fulfilled")
        self.rating = inp.get("rating")
        self.sems = inp.get("semesters_taught")
        self.notes = inp.get("notes")
        self.url = inp.get("url")
        self.next_sem = inp.get("taught_next_semester")
        self.new_instructor = inp.get("new_instructor")
        self.next_sem = [Instructor(json_inp=inst) for inst in inp.get("instructors")]

    def rate(self):
        total = 0
        for i in self.instructors: total += i.rating
        self.rating = round(total/len(self.instructors), 2) 
