from pandas import read_csv
from classes import *
from requests import get
from bs4 import BeautifulSoup as bs
from time import time
from statistics import mean, median, stdev
from ast import literal_eval
import json

VERSION = "v11"

credits = {'A&H Breadth of Inquiry credit':0,
        'Diversity in U.S. credit':1,
        'S&H Breadth of Inquiry credit':2,
        'N&M Breadth of Inquiry credit':3,
        'World Culture credit':4,
        'Public Oral Communication credit':5,
        'English Composition credit':6,
        'Mathematical Modeling credit':7,
        '300+':8,
        '400+':9,
        'Grad':10,
        'Intensive Writing credit':11,
        '100-299':12,
        'Honors': 13}

credits_inv = ['A&H credit',
        'Diversity in U.S. credit',
        'S&H credit',
        'N&M credit',
        'World Culture credit',
        'Public Oral Communication credit',
        'English Composition credit',
        'Mathematical Modeling credit',
        '300+',
        '400+',
        'Grad',
        'Intensive Writing credit',
        '100-299',
        'Honors']

path = "info/"
raw_data_file = path+"raw_data/"
main_file = path+"data/data_"+VERSION+".txt"
stat_file = path+"stat/stat_"+VERSION+".txt"
final_file = path+"final/final_"+VERSION+".json"
scrape_file = path+"scrape/scrape_"+VERSION+".json"
black_list_file = path+"misc/black_list.txt"
teachers_name_file = path+"misc/teachers_name.txt"
searches_file = "info/misc/search.txt"
search_excel_file = "info/misc/searches.xls"
courses_folder_path='info/courses'

next_sem = ["https://utilities.registrar.indiana.edu/course-browser/prl/soc4212/", ".shtml"]
last_sem = ["https://utilities.registrar.indiana.edu/course-browser/prl/soc4208/", ".shtml"]
last_last_sem = ["https://utilities.registrar.indiana.edu/course-browser/prl/soc4205/", ".shtml"]
next_sem_name = "Spring 2021"
