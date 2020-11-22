from datetime import datetime
from ast import literal_eval
from flask import Flask, render_template, request, redirect
from search import search_all
from general import credits_inv, next_sem_name
print(next_sem_name)

app = Flask(__name__)


@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        days = list(map(str, request.form.getlist("day")))
        search_query = dict(request.form)
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
        keyword = elements.get("keyword")
        dep = elements.get("dept")
        req = elements.get("requirement")
        elements["requirement"] = credits_inv[int(req)]
        sub = elements.get("subject")
        code = elements.get("code")
        inst = elements.get("instrname")
        cr = elements.get("level")
        level = elements.get("credit")
        timing = elements.get("timing")
        days = elements.get("days")
        next_sem = elements.get("next sem")
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + str(elements))
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem, keyword, timing, days)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
    if request.method == 'POST':
        days = list(map(str, request.form.getlist("day")))
        search_query = dict(request.form)
        search_query['days'] = days
        search_query = str(search_query)[1:-1]

        search_query = search_query.replace(",", "&")
        search_query = search_query.replace(":", "=")
        search_query = search_query.replace(' ', '_')
        url = '/results&searchquery=' + search_query
        return redirect(url)
    return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, int(next_sem), keyword, timing, days], next_sem_name=next_sem_name)

if __name__ == "__main__":
    app.run(debug=True)
