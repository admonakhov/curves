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
        y_regr = list(map(lambda x:cor['intercept'] + x * cor['slope'], x))
        plt.plot(x, y_regr, usr['color'])
    plt.savefig(img, format = 'png')
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
    if len(X)>1:
        logX = list(map(np.log10, X))
        logY = list(map(np.log10, Y))
        cor = mymath.regression(logY, logX)
        lgy_regr = sorted(set(logY))
        lgx_regr = list(map(lambda x: cor['intercept'] + x * cor['slope'], lgy_regr))
        y_regr = list(map(lambda i: 10 ** i, lgy_regr))
        x_regr = list(map(lambda i: 10 ** i, lgx_regr))
        plt.plot(x_regr, y_regr, prof['color'])
        plt.text(max(X)*0.8, max(Y)*0.95, 'm: {0}\nC: {1}'.format(round(cor['slope'],2), round(cor['intercept'],2)), fontsize=12)
    plt.savefig(img, format = 'png')
    plt.close()
    p = base64.b64encode(img.getvalue()).decode()
    return p
