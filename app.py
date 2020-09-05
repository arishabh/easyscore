from flask import Flask, render_template, request, redirect
from search import search_all
from general import credits_inv
from datetime import datetime

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        keyword = str(request.form['keyword'])
        dep = str(request.form['dept'])
        req = str(request.form['requirement'])
        sub = str(request.form['subject'])
        code = str(request.form['code'])
        inst = str(request.form['instrname'])
        cr = str(request.form['credit'])
        level = str(request.form['level'])
        timing = str(request.form['timing'])
        days = map(str, request.form.getlist("day"))
        next_sem = str(request.form['next_sem'])
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + dep + "\t" + req + "\t" + sub + "\t" + code + "\t" + inst + "\t" + cr + "\t" + level + "\t" + str(next_sem) + "\n")
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem, keyword, timing, days)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, int(next_sem), keyword, timing, days])
    else:
        return render_template('index.html')      

@app.route('/result', methods=['POST', 'GET'])
def output():
    if request.method == 'POST':
        keyword = str(request.form['keyword'])
        dep = str(request.form['dept'])
        req = str(request.form['requirement'])
        sub = str(request.form['subject'])
        code = str(request.form['code'])
        inst = str(request.form['instrname'])
        cr = str(request.form['credit'])
        level = str(request.form['level'])
        timing = str(request.form['timing'])
        days = map(str, request.form.getlist("day"))
        next_sem = str(request.form['next_sem'])
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + dep + "\t" + req + "\t" + sub + "\t" + code + "\t" + inst + "\t" + cr + "\t" + level + "\t" + str(next_sem) + "\n")
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem, keyword, timing, days)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, int(next_sem), keyword, timing, days])
    else:
        return render_template('result.html')

@app.route('/mobile', methods=['POST', 'GET'])
def mobile():
    if request.method == 'POST':
        keyword = str(request.form['keyword'])
        dep = str(request.form['dept'])
        req = str(request.form['requirement'])
        sub = str(request.form['subject'])
        code = str(request.form['code'])
        inst = str(request.form['instrname'])
        cr = str(request.form['credit'])
        level = str(request.form['level'])
        timing = str(request.form['timing'])
        days = map(str, request.form.getlist("day"))
        next_sem = str(request.form['next_sem'])
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + dep + "\t" + req + "\t" + sub + "\t" + code + "\t" + inst + "\t" + cr + "\t" + level + "\t" + str(next_sem) + "\n")
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem, keyword, timing, days)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('mobile_result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, int(next_sem), keyword, timing, days])
    else:
        return render_template('mobile.html')

@app.route('/mobile_result', methods=['POST', 'GET'])
def mobile_output():
    if request.method == 'POST':
        keyword = request.form['keyword']
        dep = request.form['dept']
        req = request.form['requirement']
        sub = request.form['subject']
        code = request.form['code']
        inst = request.form['instrname']
        cr = request.form['credit']
        level = request.form['level']
        timing = request.form['timing']
        days = request.form.getlist("day")
        next_sem = request.form['next_sem']
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + dep + "\t" + req + "\t" + sub + "\t" + code + "\t" + inst + "\t" + cr + "\t" + level + "\t" + str(next_sem) + "\n")
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem, keyword, timing, days)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('mobile_result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, int(next_sem), keyword, timing, days])
    else:
        return render_template('mobile_result.html') 

if __name__ == "__main__":
    app.run(debug=True)
