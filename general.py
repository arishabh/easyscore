
VERSION = "v9"

credits = {'A&H Breadth of Inquiry credit':0,
        'Diversity in U.S. credit':1,
        'S&H Breadth of Inquiry credit':2,
        'N&M Breadth of Inquiry credit':3,
        'Global Civ & Culture credit':4,
        'Public Oral Communication credit':5,
        'English Composition credit':6,
        'Mathematical Modeling credit':7,
        '300+':8,
        '400+':9,
        'Grad':10}

credits_inv = ['A&H Breadth of Inquiry credit',
        'Diversity in U.S. credit',
        'S&H Breadth of Inquiry credit',
        'N&M Breadth of Inquiry credit',
        'Global Civ & Culture credit',
        'Public Oral Communication credit',
        'English Composition credit',
        'Mathematical Modeling credit',
        '300+',
        '400+',
        'Grad']

path = "info/"
total_files = 10
raw_data_file = path+"raw_data/"
main_file = path+"data/data_"+VERSION+".txt"
stat_file = path+"stat/stat_"+VERSION+".txt"
scrape_file = path+"scrape/scrape_"+VERSION+".txt"
course_credit_file = path+"misc/course_credits.txt"
black_list_file = path+"misc/black_list.txt"
teachers_name_file = path+"misc/teachers_name.txt"
search_op_file = "info/search_op_"+VERSION+".txt"

next_sem = ["https://registrar.indiana.edu/browser/soc4202/", ".shtml"]
last_sem = ["https://registrar.indiana.edu/browser/soc4198/", ".shtml"]
last_last_sem = ["https://registrar.indiana.edu/browser/soc4195/", ".shtml"]
url = [next_sem, last_sem, last_last_sem]
