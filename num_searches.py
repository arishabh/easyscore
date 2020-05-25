from general import *
from datetime import datetime
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
            for j in range(len(data[0])):
                page.write(j+1,i, data[i][j])

	wb.save(search_excel_file)

with open(searches_file, 'r') as f:
    for lines in f:
        if(lines == '\n'): continue
        date = str(datetime.strptime(lines.split('\t')[0], '%d/%m/%Y %H:%M:%S').date())
        if(date in dates):
            count[dates.index(date)] += 1
        else:
            dates.append(date)
            count.append(1)

write_file(['Date', 'Number'], [dates, count])

import plotly.express as px
import pandas as pd

df = pd.read_excel(search_excel_file)

fig = px.line(df, x='Date', y='Number')
fig.show()
