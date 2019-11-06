from flask import Flask, render_template, request, redirect
from search import search_all
from general import credits_inv

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
        next_sem = request.form.getlist('next_sem')
        kw = request.form['keywords']
        all_courses = search_all(dep, sub, code, inst, req, cr, next_sem, kw)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv)
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
        next_sem = request.form.getlist('next_sem')
        all_courses = search_all(dep, sub, code, inst, req, cr, next_sem)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv)
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
        next_sem = request.form.getlist('next_sem')
        print(next_sem)
        all_courses = search_all(dep, sub, code, inst, req, cr, next_sem)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('mobile_result.html', all_courses=all_courses, credits_inv=credits_inv)
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
        next_sem = request.form.getlist('next_sem')
        all_courses = search_all(dep, sub, code, inst, req, cr, next_sem)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('mobile_result.html', all_courses=all_courses, credits_inv=credits_inv)
    else:
        return render_template('mobile_result.html') 

if __name__ == "__main__":
    app.run(debug=True)