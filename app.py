from flask import Flask, render_template, url_for, request, redirect
from search import search_all

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        dep = request.form['dept']
        req = request.form['requirement']
        sub = request.form['subject']
        code = request.form['code']
        inst = request.form['instrname']
        all_courses = search_all(dep, sub, code, inst, req)
        return render_template('result.html', all_courses=all_courses)
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
        all_courses = search_all(dep, sub, code, inst, req)
        return render_template('result.html', all_courses=all_courses)
    else:
        return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)