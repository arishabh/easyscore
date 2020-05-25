from process_data import *
from general import *
from xlwt import Workbook, Font, XFStyle

dates = []
count = []

def write_file(headers, data):
	wb = Workbook()
	font = Font()
	style = XFStyle()
	page = wb.add_sheet('All Data')
	for i in range(len(data)):
            font.bold = True
            style.font = font
            page.write(0,i, headers[i], style = style)
            for j in range(len(data[i])):
                page.write(j+1,i, data[i][j])

	wb.save('info/misc/rating_plot.xls')

ratings2 = [int(r.rating) for r in all_courses]
a = []
for i in all_courses: a += i.instructors
ratings = [int(r.rating) for r in a]
freq = []
freq2 = []
rating = []
for i in range(101):
    freq.append(ratings.count(i))
    #freq.append(ratings2.count(i))
    rating.append(i)

write_file(['Rating', 'Frequency'], [rating, freq])

import plotly.express as px
import pandas as pd

df = pd.read_excel('info/misc/rating_plot.xls')

fig = px.line(df, x='Rating', y='Frequency')
# fig.show()
fig.write_image("info/misc/scores_dist.png")
