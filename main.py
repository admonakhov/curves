from flask import Flask, render_template, request, redirect
import myplot
import config


app = Flask(__name__)
stress = []
count = []

@app.route('/')
def main_page():
    return render_template("main.html")


@app.route('/sncurve', methods=['POST', 'GET'])
def sn_page():
    global stress
    global count
    if request.method == "POST":
        if(('stress' in request.form) and ('count' in request.form)):
            stress.append(int(request.form['stress']))
            count.append(int(request.form['count']))
            p = myplot.sn(count, stress)
            return render_template("sncurve.html", stress=stress, count=count, lenght=range(len(stress)), plot=p)
        if 'del' in request.form:
            for i in request.form:
                if i.isdigit():
                    count.pop(int(i))
                    stress.pop(int(i))
            p = myplot.sn(count, stress)
            return render_template("sncurve.html", stress=stress, count=count, lenght=range(len(stress)), plot=p)
        if 'clear' in request.form:
            stress = []
            count = []
            return render_template("sncurve.html", plot=config.empty)

    else:
        return render_template("sncurve.html", plot=config.empty)


app.run(debug=True)
