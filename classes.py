class Term:
    def __init__(self, name):
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

    def to_string2(self):
        return ("\z" + self.term + "|" + str(self.sect_desc) + "|" + str(self.total_students) + "|" + str(self.grades_perc) + "|" + str(self.grade_dist) + "|" + str(self.cum_gpa) + "|" + str(self.sect_gpa))
class Instructor:
    def __init__(self, name):
        self.name = name
        self.terms = []
        self.rating = 0
    
    def add_term(self, term):
        self.terms.append(term)

    def last_term(self):
        return self.terms[-1]

    def __lt__(self, other):
        return self.rating < other.rating
    """
    def rate(self):
        factor = 10
        diff = 96/11.0

        total = 0.0
        gpa_diff = 0
        grades = [0]*13

        for term in self.terms:
            grades = [(grades[j] + int(term.grade_dist[j])) for j in range(13)]
            total += term.total_students
            gpa_diff += term.sect_gpa-term.cum_gpa
        gpa_diff /= len(self.terms)
        self.rating = 100*grades[0]/total
        for i in range(12):
            self.rating += (96-(diff*i))*(grades[i+1]/total)
        self.rating += gpa_diff*factor
        self.rating = round(self.rating, 2)
    """
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
            if(int(term.term[-4:])>=(curr_year-grey)):
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
        if (self.rating>100): self.rating = 100
        elif (self.rating<0): self.rating = 0
    
    def to_string(self):
        out = "\t" + str(self.name) + " " + str(self.rating) + ":\n"
        for term in self.terms:
            out += term.to_string()
        return out

    def to_string2(self):
        out = "\t" + str(self.name) + "|" + str(self.rating)
        for term in self.terms:
            out += term.to_string2()
        return out
class Course:
    def __init__(self):
        self.sub = ""
        self.instructors = []
        self.desc = ""
        self.department = ""
        self.code = 0
        self.name = ""
        self.instructor_names = []
        self.credit = []
    
    def __lt__(self, other):
        return (self.instructors[0].rating < other.instructors[0].rating)

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
    
    def equals(course):
        flag = (self.department == c.department) and (self.name == c.name)

    def to_string(self):
        out = self.name + " " + self.desc + " " + str(self.credit) + ":\n"
        for inst in self.instructors:
            out += inst.to_string()
        return out

    def to_string2(self):
        out = self.department + "|" + self.sub + "|" + str(self.code) + "|" + self.desc + "|" + self.name + "|" + str(self.credit)
        for inst in self.instructors:
            out += inst.to_string2()
        out += "\n"
        return out

    
