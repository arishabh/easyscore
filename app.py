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
        all_courses = search_all(dep, sub, code, inst, req, cr)
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
        all_courses = search_all(dep, sub, code, inst, req, cr)
        if len(all_courses)>40:
            all_courses = all_courses[:40]
        return render_template('result.html', all_courses=all_courses, credits_inv=credits_inv)
    else:
        return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)