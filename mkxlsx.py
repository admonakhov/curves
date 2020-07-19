import xlsxwriter
import random
import mymath
import numpy as np
import os


colors = ['red', 'blue', 'green', 'yellow', 'magenta', 'purple', 'orange']
markers = ['square', 'diamond', 'triangle', 'x', 'star', 'circle', 'plus']
it = 0  # итератор цветов и маркеров
dkeys = ['stress', 'count', 'rstress', 'rcount', 'slope', 'intercept']
ALLOWED_EXTENSIONS = set(['txt', 'xlsx', 'xls'])


def allowed_file(extension):
    return extension in ALLOWED_EXTENSIONS


def mk_book(data):
    try:
        os.remove('tmp.xlsx')
    except:
        pass

    global colors
    global markers
    global it
    global dkeys
    with xlsxwriter.Workbook('tmp.xlsx') as wb:

        chart_all = wb.add_chart({'type': 'scatter'})
        chart_all.set_x_axis({
            'name': 'Долговечность, Цикл',
            'name_font': {'size': 12},
            'log_base': 10,
            'major_gridlines': {
                'visible': True,
                'line': {'width': 1.25, 'dash_type': 'dash'}
            }
        })
        chart_all.set_y_axis({
            'name': 'Напряжения, МПа',
            'name_font': {'size': 12}
        })
        for ws in data.keys():
            chart = wb.add_chart({'type': 'scatter'})
            chart.set_legend({'none': True})

            chart.set_title({
                'name': ws,
                'overlay': True
            })
            try:
                if mymath.round_less_div(min(list(map(float, data[ws]['count'])))) > mymath.round_less_div(
                        min(list(map(float, data[ws]['rcount'])))):
                    min_x = mymath.round_less_div(min(list(map(float, data[ws]['rcount']))))
                else:
                    min_x = mymath.round_less_div(min(list(map(float, data[ws]['count']))))
                if mymath.round_greater_div(max(list(map(float, data[ws]['count'])))) < mymath.round_greater_div(
                        max(list(map(float, data[ws]['count'])))):
                    max_x = mymath.round_greater_div(max(list(map(float, data[ws]['count']))))
                else:
                    max_x = mymath.round_greater_div(max(list(map(float, data[ws]['count']))))
                min_y = mymath.round_less_div(min(list(map(float, data[ws]['stress']))))
                max_y = mymath.round_greater_div(max(list(map(float, data[ws]['stress']))))
            except:
                min_x = 0
                min_y = 0
                max_x = np.nan
                max_y = np.nan
            val = {'categories': '={0}!B2:B1000'.format(ws), 'values': '={0}!A2:A1000'.format(ws), 'name': ws,
                   'marker': {'type': markers[it], 'border': {'color': colors[it]}, 'fill': {'color': colors[it]}}}
            val_reg = {'categories': '={0}!D2:D1000'.format(ws), 'marker': {'type': 'none'},
                       'values': '={0}!C2:C1000'.format(ws), 'name': ws + ' reg', 'line': {'color': colors[it]}}
            it += 1
            if it == (len(markers) - 1) or it == (len(colors) - 1):
                shuffle()
            worksheet = wb.add_worksheet(ws)
            if list(data.keys())[0] == ws:
                firstws = worksheet
            chart.set_x_axis({
                'name': 'Долговечность, Цикл',
                'min': min_x, 'max': max_x,
                'name_font': {'size': 12},
                'log_base': 10,
                'major_gridlines': {
                    'visible': True,
                    'line': {'width': 1.25, 'dash_type': 'dash'}
                }
            })
            chart.set_y_axis({
                'name': 'Напряжения, МПа',
                'min': min_y, 'max': max_y,
                'name_font': {'size': 12}
            })
            for col, key in enumerate(dkeys):
                if type(data[ws][key]) == list:
                    worksheet.write(0, col, key)
                    worksheet.write_column(1, col, list(map(float, data[ws][key])))
                else:
                    worksheet.write(0, col, key)
                    worksheet.write(1, col, data[ws][key])
            chart.add_series(val)
            chart_all.add_series(val)
            chart.add_series(val_reg)
            chart_all.add_series(val_reg)
            worksheet.insert_chart('D10', chart)
        firstws.insert_chart('L10', chart_all)
    it = 0


def shuffle():
    global colors
    global markers
    global it
    markers = random.shuffle(markers)
    colors = random.shuffle(colors)
    it = 0
