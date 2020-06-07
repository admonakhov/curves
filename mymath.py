import numpy as np


def round_less_div(a):
    i = 0
    while a >= 10:
        a /= 10
        i += 1
    a = int(a) - 1
    a = a * (10 ** i)
    return a


def round_greater_div(a):
    i = 0
    while a >= 10:
        a /= 10
        i += 1
    a = int(a) + 1
    a = a * (10 ** i)
    return a

def mean(arg):
    if len(arg)>1:
        return sum(arg) / len(arg)
    else:
        return arg


def sko(arg):
    if len(arg)>1:
        m = mean(arg)
        lsum = 0
        for n in arg:
            lsum += (n - m) ** 2
        return (lsum / (len(arg) - 1)) ** 0.5
    else:
        return 0


def cv(arg):
    return round(100 * sko(arg) / mean(arg), 5)


def median(arg):
    tmp = sorted(arg)
    if len(tmp) % 2 == 0:
        return (tmp[int(len(tmp) / 2)] + tmp[int(len(tmp) / 2) - 1]) / 2
    else:
        return tmp[int(len(tmp) / 2)]


def regression(x, y):
    cor = {}
    m_x = mean(x)

    m_y = mean(y)
    s_y = sko(y)
    s_x = sko(x)
    cor['cov'] = 0
    for i in range(len(x)):
        cor['cov'] += (x[i] - m_x) * (y[i] - m_y)
    cor['cov'] /= (len(x) - 1)
    try:
        cor['regression'] = cor['cov'] / (s_y * s_x)
        cor['slope'] = (s_y / s_x) * (cor['regression'])
        cor['intercept'] = m_y - (cor['slope'] * m_x)
    except Exception:
        cor['regression'] = 0
        cor['slope'] = 0
        cor['intercept'] = 0
    return cor


def pow_equation(X, Y):
    if len(X) > 1:
        try:
            data = {}
            logX = list(map(np.log10, X))
            logY = list(map(np.log10, Y))
            cor = regression(logY, logX)
            lgy_regr = sorted(set(logY))
            lgx_regr = list(map(lambda x: cor['intercept'] + x * cor['slope'], lgy_regr))
            y_regr = list(map(lambda i: 10 ** i, lgy_regr))
            x_regr = list(map(lambda i: 10 ** i, lgx_regr))
            data['x'] = x_regr
            data['y'] = y_regr
            data['intercept'] = cor['intercept']
            data['slope'] = cor['slope']
            return data
        except:
            print('Something wrong')
            data['x'] = [0]
            data['y'] = [0]
            data['intercept'] = 0
            data['slope'] = 0
            return data

def mandell_pow_equation(X, Y):
    if len(X) > 1:
        try:
            data = {}
            logX = list(map(np.log10, X))
            cor = regression(Y, logX)
            y_regr = sorted(set(Y))
            lgx_regr = list(map(lambda x: cor['intercept'] + x * cor['slope'], y_regr))
            x_regr = list(map(lambda i: 10 ** i, lgx_regr))
            data['x'] = x_regr
            data['y'] = y_regr
            data['intercept'] = cor['intercept']
            data['slope'] = cor['slope']
            return data
        except:
            print('Something wrong')
            data['x'] = [0]
            data['y'] = [0]
            data['intercept'] = 0
            data['slope'] = 0
            return data