from flask import Flask, render_template, request, redirect
from search import search_all
from general import credits_inv
from datetime import datetime

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        dep = request.form['dept']
        req = request.form['requirement']
        sub = request.form['subject']
        code = request.form['code']
        inst = request.form['instrname']
        cr = request.form['cr']
        level = request.form['level']
        next_sem = request.form.getlist('next_sem')
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + dep + "\t" + req + "\t" + sub + "\t" + code + "\t" + inst + "\t" + cr + "\t" + level + "\t" + str(next_sem) + "\n")
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, 1 if next_sem!=[] else 0])
    else:
        return render_template('index.html')      

@app.route('/result', methods=['POST', 'GET'])
def output():
    if request.method == 'POST':
        dep = request.form['dept']
        req = request.form['requirement']
        sub = request.form['subject']
        code = request.form['code']
        inst = request.form['instrname']
        cr = request.form['cr']
        level = request.form['level']
        next_sem = request.form.getlist('next_sem')
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + dep + "\t" + req + "\t" + sub + "\t" + code + "\t" + inst + "\t" + cr + "\t" + level + "\t" + str(next_sem) + "\n")
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, 1 if next_sem!=[] else 0])
    else:
        return render_template('result.html')

@app.route('/mobile', methods=['POST', 'GET'])
def mobile():
    if request.method == 'POST':
        dep = request.form['dept']
        req = request.form['requirement']
        sub = request.form['subject']
        code = request.form['code']
        inst = request.form['instrname']
        cr = request.form['cr']
        level = request.form['level']
        next_sem = request.form.getlist('next_sem')
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem)
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + dep + "\t" + req + "\t" + sub + "\t" + code + "\t" + inst + "\t" + cr + "\t" + level + "\t" + str(next_sem) + "\n")
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('mobile_result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, 1 if next_sem!=[] else 0])
    else:
        return render_template('mobile.html')

@app.route('/mobile_result', methods=['POST', 'GET'])
def mobile_output():
    if request.method == 'POST':
        dep = request.form['dept']
        req = request.form['requirement']
        sub = request.form['subject']
        code = request.form['code']
        inst = request.form['instrname']
        cr = request.form['cr']
        level = request.form['level']
        next_sem = request.form.getlist('next_sem')
        all_courses = search_all(dep, sub, code, inst, req, level, cr, next_sem)
        with open("info/misc/search.txt", "a+") as f:
            f.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + dep + "\t" + req + "\t" + sub + "\t" + code + "\t" + inst + "\t" + cr + "\t" + level + "\t" + str(next_sem) + "\n")
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('mobile_result.html', all_courses=all_courses, credits_inv=credits_inv, inp=[dep, req, sub, code, inst, cr, level, 1 if next_sem!=[] else 0])
    else:
        return render_template('mobile_result.html') 

if __name__ == "__main__":
    app.run(debug=True)