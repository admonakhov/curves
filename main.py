from flask import Flask, render_template, request, jsonify
import myplot, mymath
import config
import json

app = Flask(__name__)
stress = []
count = []


@app.route('/')
def main_page():
    return render_template("main.html")


@app.route('/sncurve_front/post', methods=['POST'])
def sn_curve_ret():
    stress = list(map(int, request.form.getlist('stress')))
    count = list(map(int, request.form.getlist('count')))
    if (len(stress) == len(count)) and (len(stress) > 1):
        d = mymath.reg_data(count, stress)
        return json.dumps({'stress': d['y'], 'count': d['x'], 'intercept': d['intercept'], 'slope': d['slope']})
    else:
        return json.dumps({'stress': [], 'count': [], 'intercept': 0, 'slope': 0})


@app.route('/sncurve', methods=['POST', 'GET'])
def sn_page():
    global stress
    global count
    if request.method == "POST":
        if (('stress' in request.form) and ('count' in request.form)):
            if request.form['count'] and request.form['stress']:
                stress.append(int(request.form['stress']))
                count.append(int(request.form['count']))
            p = myplot.sn(count, stress)
            return render_template("sncurve.html", stress=stress, count=count, lenght=range(len(stress)), plot=p)
        if 'del' in request.form:
            l = sorted(request.form)[::-1]
            if len(l) > 1:
                for i in l:  # удаление с последнего элемента
                    if i.isdigit():
                        count.pop(int(i))
                        stress.pop(int(i))
            else:
                count = []
                stress = []
            p = myplot.sn(count, stress)
            return render_template("sncurve.html", stress=stress, count=count, lenght=range(len(stress)), plot=p)

    else:
        return render_template("sncurve.html", plot=config.empty)


@app.route('/sncurve_front', methods=['POST', 'GET'])
def sn_page_new():
    return render_template("sncurve_front.html", plot=config.empty)


app.run(host='192.168.100.13', port=8112)
#app.run()
