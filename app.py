from datetime import datetime
from ast import literal_eval
from flask import Flask, render_template, request, redirect
from search import search_all, search_course
from general import credits_inv, next_sem_name

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        days = list(map(str, request.form.getlist("day")))
        search_query = dict(request.form)
        search_query.pop('dept')
        search_query.pop('day', None)
        search_query['days'] = days
        search_query = str(search_query)[1:-1]

        search_query = search_query.replace(",", "&")
        search_query = search_query.replace(":", "=")
        search_query = search_query.replace(' ', '_')
        url = '/results&searchquery=' + search_query
        return redirect(url)
    return render_template('index.html', next_sem_name=next_sem_name)

@app.route('/results&searchquery=<query>', methods=['POST', 'GET'])
def output(query):
    if query:
        query = query.replace("&", ",")
        query = query.replace("=", ":")
        query = query.replace('_', ' ')
        elements = literal_eval("{" + query + "}")
        keyword = elements["keyword"]
        cr_fullfil = elements["requirement"]
        cr = elements["credit"]
        level = elements["level"]
        timing = elements["timing"]
        days = elements["days"]
        next_sem = elements["next sem"]
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + str(elements))
        all_courses = search_all(cr_fullfil, level, cr, next_sem, keyword, timing, days)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
    if request.method == 'POST':
        days = list(map(str, request.form.getlist("day")))
        search_query = dict(request.form)
        search_query.pop('dept')
        search_query.pop('day', None)
        search_query['days'] = days
        search_query = str(search_query)[1:-1]

        search_query = search_query.replace(",", "&")
        search_query = search_query.replace(":", "=")
        search_query = search_query.replace(' ', '_')
        url = '/results&searchquery=' + search_query
        return redirect(url)
    return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[cr_fullfil, cr, level, next_sem, keyword, timing, days], next_sem_name=next_sem_name)

@app.route('/results&jsonquery=<query>', methods=['GET'])
def json_output(query):
    if query:
        query = query.replace("&", ",")
        query = query.replace("=", ":")
        query = query.replace('_', ' ')
        elements = literal_eval("{" + query + "}")
        keyword = elements["keyword"]
        cr_fullfil = elements["requirement"]
        level = elements["level"]
        cr = elements["credit"]
        timing = elements["timing"]
        days = elements["days"]
        next_sem = elements["next sem"]
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + str(elements))
        all_courses = search_all(cr_fullfil, level, cr, next_sem, keyword, timing, days)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
    return all_courses

@app.route('/results&jsonquery/course=<query>', methods=['GET'])
def json_course_output(query):
    course = query.split("_")[0]
    return search_course(course)

if __name__ == "__main__":
    app.run(debug=True)
