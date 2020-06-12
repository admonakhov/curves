from flask import Flask, render_template, request, jsonify, send_file, redirect
import mymath, config, mkxlsx
import config
import json

app = Flask(__name__)
stress = []
count = []


@app.route('/')
def main_page():
    return render_template("main.html")


@app.route('/sncurve/post', methods=['POST'])
def sn_curve_ret():
    if request.form['key'] == 'regression':

        stress = list(map(int, request.form.getlist('stress')))
        count = list(map(int, request.form.getlist('count')))

        if (len(stress) == len(count)) and (len(stress) > 1):
            if request.form['equation'] == 'pow':
                d = mymath.pow_equation(count, stress)
            if request.form['equation'] == 'mandell':
                d = mymath.mandell_pow_equation(count, stress)
            return json.dumps({'stress': d['y'], 'count': d['x'], 'intercept': d['intercept'], 'slope': d['slope'],
                               'key': 'regression'})
        else:
            return json.dumps({'stress': [], 'count': [], 'intercept': 0, 'slope': 0, 'key': 'regression'})
    elif request.form['key'] == 'mkxlsx':
        d = json.loads(request.form['data'])
        mkxlsx.mk_book(d)
        return json.dumps({'key': 'file'})


@app.route('/sncurve', methods=['GET'])
def sn_page():
    return render_template("sncurve.html")


@app.route('/sscurve', methods=['GET'])
def ss_page():
    return render_template("sscurve.html")


@app.route('/sscurve', methods=['POST'])
def ss_curve_pos():
    for file in request.files:
        f = request.files[file]
    for i in f:
        print(i)
    return 'Good'


@app.route('/xlsxdownload.xlsx', methods=['GET'])
def xlsxdownload():
    return send_file('tmp.xlsx')


@app.route('/resources', methods=['GET'])
def resources():
    return render_template("resources.html")


# app.run(host=config.loc_ip, port=8112)
app.run()
