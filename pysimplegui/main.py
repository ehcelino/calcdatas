"""
Calculadora de datas - versão PySimpleGUI
Copyright (c) 2022 Eduardo C.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import PySimpleGUI as sg
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re
import locale
import numpy as np

locale.setlocale(locale.LC_ALL, '')

regexdata = re.compile(r'^(\d{2})[-.\/](\d{2})[-.\/](\d{4})$')
regexvalor = re.compile(r'(\d)*')
# re.fullmatch(regex, valor)

sg.theme('SystemDefaultForReal')

form_data = '%d/%m/%Y'

def valida(data, valor):
    tmp = True
    if not re.fullmatch(regexdata, data):
        tmp = False
    try:
        tmp = bool(datetime.strptime(data, form_data))
    except ValueError:
        tmp = False
    if not re.fullmatch(regexvalor, valor):
        tmp = False
    return tmp


def strip_operacao(operacao=''):
    op_limpo = operacao.replace(" ", "")
    if op_limpo.find('+') != -1:
        strings = op_limpo.split('+')
        if not valida(strings[0], strings[1]):
            return 'ERRO'
        else:
            return strings[0], int(strings[1]), '+'
    elif op_limpo.find('-') != -1:
        strings = op_limpo.split('-')
        if not valida(strings[0], strings[1]):
            return 'ERRO'
        else:
            return strings[0], int(strings[1]), '-'
    else:
        return 'ERRO'


def strip_datas(datas):
    result = True
    datas = datas.replace(" ", "")
    if datas == '':
        result = False
        return 'ERRO'
    elif datas.find('-') == -1:
        result = False
        return 'ERRO'
    else:
        strings = datas.split('-')
        print(strings)
        try:
            tmp = bool(datetime.strptime(strings[0], form_data))
            tmp = bool(datetime.strptime(strings[1], form_data))
        except ValueError as err:
            print('erro: ', err)
            return 'ERRO'
        if not re.fullmatch(regexdata, strings[0]) or not re.fullmatch(regexdata, strings[1]):
            result = False
            return 'ERRO'
        else:
            return strings


def calcula(data1, valor, operacao, opcao):
    """
    faz o cálculo entre duas datas
    :param data1: string
    :param valor: string
    :param operacao: string (+,-)
    :param opcao: string (D, M, A)
    :return: string
    """
    data1_date = datetime.strptime(data1, form_data)
    # data2_date = datetime.strptime(data2, form_data)
    if operacao == '+':
        if opcao == 'DIAS':
            data_final_date = data1_date + relativedelta(days=int(valor))
        # the_timedelta = data1_date - data2_date
        elif opcao == 'MESES':
            data_final_date = data1_date + relativedelta(months=+int(valor))
        elif opcao == 'ANOS':
            data_final_date = data1_date + relativedelta(years=int(valor))
        data_final_str = datetime.strftime(data_final_date, form_data)
        return data_final_str

    if operacao == '-':
        if opcao == 'DIAS':
            data_final_date = data1_date - relativedelta(days=int(valor))
        # the_timedelta = data1_date - data2_date
        elif opcao == 'MESES':
            data_final_date = data1_date - relativedelta(months=int(valor))
        elif opcao == 'ANOS':
            data_final_date = data1_date - relativedelta(years=int(valor))
        data_final_str = datetime.strftime(data_final_date, form_data)
        return data_final_str


def janela_calculadora():
    b = (6, 1)
    mensagem = 'Para calcular, digite a data no formato 00/00/0000 + ou - a quantidade de dias/meses/anos.'
    mensagem2 = 'Para diferença, digite as duas datas: 00/00/0000-00/00/0000.'
    mensagem3 = 'Para dia da semana, digite a data: 00/00/0000.'
    mensagem4 = 'Para dias úteis entre datas, digite as duas datas: 00/00/0000-00/00/0000.'
    mensagem5 = 'Para diferença entre datas (em dias), digite as duas datas: 00/00/0000-00/00/0000.'
    mensagem6 = 'Clique em "como usar" para voltar.'
    frame_layout = [
        [sg.Multiline(k='-SAIDA-', s=(29, 8), border_width=0, do_not_clear=True)],
        [sg.T('Operação:')],
        [sg.I(k='-INPUT1-', s=(20, 1), border_width=0, focus=True, font='_ 14 bold',
              tooltip='Para ajuda clique no botão "Como usar".'
              , enable_events=True)],
        # [sg.I(k='-INPUT2-', s=(26, 1), border_width=0, justification='right')],
        # [sg.I(k='-OPERACAO-', s=(26, 1), border_width=0, justification='right')],
        [sg.T('Resultado:')],
        [sg.I(k='-OUTPUT-', s=(20, 1), border_width=0, font='_ 14 bold')],
        [sg.Multiline(k='-OUTPUT2-', s=(20, 2), border_width=0, font='_ 14 bold', no_scrollbar=True)],
        # [sg.B('+', k='-+-', s=b), sg.B('-', k='---', s=b)],
        [sg.B('DIAS', k='-DIAS-', s=b), sg.B('MESES', k='-MESES-', s=b),
         sg.B('ANOS', k='-ANOS-', s=b)],
        [sg.B('HOJE', k='-HOJE-', s=b)],
        [sg.B('DIA DA SEMANA', k='-DIASEM-')],
        [sg.B('DIAS ÚTEIS ENTRE DATAS', k='-DIASUTEIS-')],
        [sg.B('DIFERENÇA ENTRE DATAS', k='-DIFERENCA-')],
    ]

    frame_layout2 = [
        [sg.T('Como usar a calculadora:')],
        [sg.T(mensagem, s=(27, 4))],
        [sg.T(mensagem2, s=(27, 4))],
        [sg.T(mensagem3, s=(27, 4))],
        [sg.T(mensagem4, s=(27, 4))],
        [sg.T(mensagem5, s=(27, 4))],
        [sg.T(mensagem6, s=(27, 4))],
    ]
    layout = [
        [sg.T('Calculadora de datas')],
        [sg.Frame('', frame_layout, element_justification='center', visible=True, k='-FRAME1-', s=(240, 480)),
         sg.Frame('', frame_layout2, visible=False, k='-FRAME2-', s=(240, 480))],
        [sg.Push(), sg.B('COMO USAR', k='-AJUDA-'), sg.B('SAIR', k='-SAIR-')]
    ]

    return sg.Window('Calculadora de datas', layout, finalize=True)


class calculadora:

    def __init__(self):
        self.comousar = False
        self.mensagem = 'Para calcular, digite a data no formato 00/00/0000 + ou - a quantidade de dias/meses/anos. ' \
                        'Para diferença, digite as duas datas 00/00/0000-00/00/0000. ' \
                        'Para dia da semana, digite a data 00/00/0000.'
        self.values = None
        self.event = None
        self.window = janela_calculadora()
        # self.operacao = False

    def dma_func(self, dma):
        tmp = strip_datas(self.values['-INPUT1-'])
        if tmp != 'ERRO':
            data1 = datetime.strptime(tmp[0], form_data)
            data2 = datetime.strptime(tmp[1], form_data)
            timedelta = data1 - data2
            if dma == 'DIAS':
                resultado = timedelta.days
            elif dma == 'MESES':
                resultado = round(timedelta.days / 30)
            elif dma == 'ANOS':
                resultado = round((timedelta.days / 365), 2)
            self.window['-OUTPUT-'].update(value=resultado)
            self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' ' + dma)
            self.window['-SAIDA-'].print('= ' + str(resultado) + ' ' + dma)
            self.window['-OUTPUT2-'].update(value='')
        else:
            op = strip_operacao(self.values['-INPUT1-'])
            if op == 'ERRO':
                self.window['-OUTPUT-'].update(value='data inválida')
            else:
                self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' ' + dma)
                resultado = calcula(op[0], op[1], op[2], dma)
                self.window['-OUTPUT-'].update(value=resultado)
                self.window['-SAIDA-'].print('= ' + resultado)
                extenso = datetime.strftime(datetime.strptime(resultado, form_data), '%A, %d de %B de %Y')
                self.window['-OUTPUT2-'].update(value=extenso)
                # self.operacao = False

    def run(self):
        while True:
            self.event, self.values = self.window.read()

            if self.event == '-INPUT1-' and self.values['-INPUT1-'] and\
                    self.values['-INPUT1-'][-1] not in ('0123456789/-+'):
                self.window['-INPUT1-'].update(self.values['-INPUT1-'][:-1])

            if self.event == '-AJUDA-':
                # sg.popup(self.mensagem)
                if not self.comousar:
                    self.window['-FRAME1-'].update(visible=False)
                    self.window['-FRAME2-'].update(visible=True)
                    self.comousar = True
                else:
                    self.window['-FRAME1-'].update(visible=True)
                    self.window['-FRAME2-'].update(visible=False)
                    self.comousar = False
            # if self.event == '-+-':
            #     self.window['-OPERACAO-'].update(value='+')
            #     self.operacao = True

            if self.event == '-DIFERENCA-':
                tmp = strip_datas(self.values['-INPUT1-'])
                print('TMP: ', tmp)
                if tmp == 'ERRO':
                    sg.popup('As datas devem ser inseridas da seguinte forma: 00/00/0000-00/00/0000')
                else:
                    data1 = datetime.strptime(tmp[0], form_data)
                    data2 = datetime.strptime(tmp[1], form_data)
                    timedelta = data1 - data2
                    self.window['-OUTPUT-'].update(value=str(abs(timedelta.days)) + ' dias')
                    self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' DIFERENÇA')
                    self.window['-SAIDA-'].print('= ' + str(abs(timedelta.days)))

            if self.event == '-DIASUTEIS-':
                tmp = strip_datas(self.values['-INPUT1-'])
                print('TMP: ', tmp)
                if tmp == 'ERRO':
                    sg.popup('As datas devem ser inseridas da seguinte forma: 00/00/0000-00/00/0000')
                else:
                    print('TMP 0 and 1', tmp[0], tmp[1])
                    data1 = datetime.strptime(tmp[0], form_data)
                    data2 = datetime.strptime(tmp[1], form_data)
                    res = np.busday_count(data1.strftime('%Y-%m-%d'), data2.strftime('%Y-%m-%d'))
                    self.window['-OUTPUT-'].update(value=str(res) + ' dias')
                    self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' DIAS ÚTEIS')
                    self.window['-SAIDA-'].print('= ' + str(res))

            if self.event == '-DIASEM-':
                tmp = self.values['-INPUT1-']
                tmp3 = tmp.replace(" ", "")
                if tmp3 != '' and re.fullmatch(regexdata, tmp3):
                    try:
                        tmp2 = bool(datetime.strptime(tmp3, form_data))
                    except ValueError:
                        tmp2 = False
                else:
                    tmp2 = False

                if tmp2:
                    dt_tmp = datetime.strptime(tmp3, form_data)
                    tmp = datetime.strftime(dt_tmp, '%A')
                    self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' DIA DA SEMANA')
                    self.window['-OUTPUT-'].update(value=tmp)
                    self.window['-SAIDA-'].print('= ' + tmp)
                else:
                    self.window['-OUTPUT-'].update(value='data inválida')

            if self.event == '-DIAS-':
                self.dma_func('DIAS')

            if self.event == '-MESES-':
                self.dma_func('MESES')

            if self.event == '-ANOS-':
                self.dma_func('ANOS')

            if self.event == '-HOJE-':
                self.window['-INPUT1-'].update(value=datetime.strftime(date.today(), form_data))
                self.window['-OUTPUT-'].update(value='')
                extenso = datetime.strftime(date.today(), '%A, %d de %B de %Y')
                self.window['-OUTPUT2-'].update(value=extenso)

            if self.event in (sg.WIN_CLOSED, '-SAIR-'):
                break
        self.window.close()


if __name__ == '__main__':
    calculadora().run()
