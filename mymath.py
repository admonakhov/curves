import numpy as np
import scipy.stats as stats

dtypes = [int, float, np.float64, np.int64]


def round_less_div(a):
    i = 0
    while a >= 10:
        a /= 10
        i += 1
    a = int(a) - 1
    a = a * (10 ** i)
    return a


def nearest(a, l):
    ost = a
    if a in l:
        return a
    else:
        for i in l:
            if abs(a - i) < ost:
                ost = abs(a - i)
                n = i
        return n


def round_greater_div(a):
    i = 0
    while a >= 10:
        a /= 10
        i += 1
    a = int(a) + 1
    a = a * (10 ** i)
    return a


def mean(arg):
    if len(arg) > 1:
        return sum(arg) / len(arg)
    else:
        return arg


def sko(arg):
    if len(arg) > 1:
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


def linear_regression(x, y):
    d = {}
    d['slope'], d['intercept'], d['r_value'], d['p_value'], d['std_err'] = stats.linregress(x, y)
    return d


def pow_equation(X, Y, regression=linear_regression):
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


def mandell_pow_equation(X, Y, regression=linear_regression):
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

def simple_nearest(a, l, p = 0.1): # Определение ближайшего числа с заданной точностью
    ost = a
    n=0
    if type(l) not in dtypes:
        if a in l:
            return a
        else:
            for i in l:
                if abs(a-i)<ost:
                    ost = abs(a-i)
                    n = i
    else:
        ost = abs(a-l)
        n = l
    if n*p > ost:
        return n

def simple_crosslines(lx1, ly1, lx2, ly2, nearest=simple_nearest, p = 0.005):
    if len(lx1)==len(ly1) and len(lx2)==len(ly2):
        for i in range(len(lx1)):
            for j in range(len(lx2)):
                if nearest(lx1[i], lx2[j], p) == lx2[j] and nearest(ly1[i],ly2[j], p) == ly2[j]:
                    return lx1[i], ly1[i]




def s_s_prop(strain, stress, start, end, regression=linear_regression, cross=simple_crosslines, nearest=simple_nearest):
    prop = {}
    prop['ultimate'] = round_1497(max(stress), 'stress')  # Определение предела прочности
    #     Индексы начала и конца определения Е модуля
    n1 = stress.index(nearest(start, stress))
    n2 = stress.index(nearest(end, stress))
    reg = regression(strain[n1:n2], stress[n1:n2])
    prop['slope'] = reg['slope']
    prop['intercept'] = reg['intercept']
    prop['modulus'] = round_1497(reg['slope'] / 10, 'modulus')  # Определение моудля упругости
    #     Определение нуля деформации
    zero = -reg['intercept'] / reg['slope']
    #     Определение предела текучести
    stress02 = np.linspace(0, max(stress))
    strain02 = ((stress02-prop['intercept'])/prop['slope'])+0.2
    prop['yield'] = round_1497(cross(strain, stress, strain02, stress02)[1], 'stress')
    #     Определение максимальной пластеской деформации
    prop['extension'] = round_1497(max(strain) - (stress[-1] - reg['intercept']) / reg['slope'], 'strain')
    #     Определение предела пропорциональности
    n = stress.index(max(stress))
    strainP = []
    stressP = []
    for i in range(len(stress[:n])):
        stressP.append(stress[i])
        strainP.append(((stress[i]-reg['intercept'])/(reg['slope']*0.67))-strain[i])
    prop['proportional'] = round_1497(stressP[strainP.index(max(strainP))],'stress')
    return prop


def round_step(num, step):  #  Округление с заданной точностью
    if num % step >= 0.5 * step:
        num = (num // step + 1) * step
    else:
        num = (num // step) * step
    return num


def round_1497(num, case='stress'):  # Округление по ГОСТ 1497
    if case == 'stress':
        if num >= 500:
            num = round_step(num, 10)
        elif num >= 100:
            num = round_step(num, 5)
        else:
            num = round_step(num, 1)
        return int(num)
    elif case == 'strain':
        if num >= 25:
            num = round_step(num, 1)
        elif num >= 10:
            num = round_step(num, 0.5)
        else:
            num = round_step(num, 0.1)
        return num
    elif case == 'modulus':
        num = round_step(num, 1)
        return int(num)


