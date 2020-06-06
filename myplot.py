import matplotlib.pyplot as plt
import matplotlib
import mymath
import config
import numpy as np
import base64
import io

matplotlib.use('Agg')


def plot(X, Y, usr=config.deafault_prof):
    img = io.BytesIO()
    plt.plot(X, Y, usr['color'] + usr['line'] + usr['dots'])
    if usr['Xlog']:
        plt.semilogx()
    if usr['grid']:
        plt.grid()
    if usr['regr']:
        cor = mymath.regression(X, Y)
        x = sorted(set(X))
        y_regr = list(map(lambda x: cor['intercept'] + x * cor['slope'], x))
        plt.plot(x, y_regr, usr['color'])
    plt.savefig(img, format='png')
    plt.close()
    p = base64.b64encode(img.getvalue()).decode()
    return p


def sn(X, Y, prof=config.sn_prof):
    img = io.BytesIO()
    plt.plot(X, Y, prof['color'] + prof['line'] + prof['dots'])
    plt.semilogx()
    plt.grid(which="both")
    plt.xlabel("Долговечность")
    plt.ylabel("Напряжение")
    if len(X) > 1:
        sn_data = mymath.reg_data(X, Y)
        plt.plot(sn_data['x'], sn_data['y'], prof['color'])
        plt.text(max(X) * 0.8, max(Y) * 0.95,
                 'm: {0}\nC: {1}'.format(round(sn_data['slope'], 2), round(sn_data['intercept'], 2)), fontsize=12)
    plt.savefig(img, format='png')
    plt.close()
    p = base64.b64encode(img.getvalue()).decode()
    return p
