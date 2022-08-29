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


def valida(data, valor):
    tmp = True
    if not re.fullmatch(regexdata, data):
        tmp = False
    try:
        tmp = bool(datetime.strptime(data, '%d/%m/%Y'))
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
    data1_date = datetime.strptime(data1, '%d/%m/%Y')
    # data2_date = datetime.strptime(data2, '%d/%m/%Y')
    if operacao == '+':
        if opcao == 'D':
            data_final_date = data1_date + relativedelta(days=int(valor))
        # the_timedelta = data1_date - data2_date
        elif opcao == 'M':
            data_final_date = data1_date + relativedelta(months=+int(valor))
        elif opcao == 'A':
            data_final_date = data1_date + relativedelta(years=int(valor))
        data_final_str = datetime.strftime(data_final_date, '%d/%m/%Y')
        return data_final_str

    if operacao == '-':
        if opcao == 'D':
            data_final_date = data1_date - relativedelta(days=int(valor))
        # the_timedelta = data1_date - data2_date
        elif opcao == 'M':
            data_final_date = data1_date - relativedelta(months=int(valor))
        elif opcao == 'A':
            data_final_date = data1_date - relativedelta(years=int(valor))
        data_final_str = datetime.strftime(data_final_date, '%d/%m/%Y')
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
        [sg.Multiline(k='-SAIDA-', s=(29, 10), border_width=0, do_not_clear=True)],
        [sg.T('Operação:')],
        [sg.I(k='-INPUT1-', s=(20, 1), border_width=0, focus=True, font='_ 14 bold',
              tooltip='Digite a data (00/00/0000) + ou - a quantidade e clique em um dos botões.')],
        # [sg.I(k='-INPUT2-', s=(26, 1), border_width=0, justification='right')],
        # [sg.I(k='-OPERACAO-', s=(26, 1), border_width=0, justification='right')],
        [sg.T('Resultado:')],
        [sg.I(k='-OUTPUT-', s=(20, 1), border_width=0, font='_ 14 bold')],
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
        [sg.Frame('', frame_layout, element_justification='center', visible=True, k='-FRAME1-', s=(240, 440)),
         sg.Frame('', frame_layout2, visible=False, k='-FRAME2-', s=(240, 440))],
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

    def run(self):
        while True:
            self.event, self.values = self.window.read()

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
                    data1 = datetime.strptime(tmp[0], '%d/%m/%Y')
                    data2 = datetime.strptime(tmp[1], '%d/%m/%Y')
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
                    data1 = datetime.strptime(tmp[0], '%d/%m/%Y')
                    data2 = datetime.strptime(tmp[1], '%d/%m/%Y')
                    res = np.busday_count(data1.strftime('%Y-%m-%d'), data2.strftime('%Y-%m-%d'))
                    self.window['-OUTPUT-'].update(value=str(res) + ' dias')
                    self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' DIAS ÚTEIS')
                    self.window['-SAIDA-'].print('= ' + str(res))

            if self.event == '-DIASEM-':
                tmp = self.values['-INPUT1-']
                if tmp != '' and re.fullmatch(regexdata, tmp):
                    try:
                        tmp2 = bool(datetime.strptime(tmp, '%d/%m/%Y'))
                    except ValueError:
                        tmp2 = False
                else:
                    tmp2 = False

                if tmp2:
                    dt_tmp = datetime.strptime(tmp, '%d/%m/%Y')
                    tmp = datetime.strftime(dt_tmp, '%A')
                    self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' DIA DA SEMANA')
                    self.window['-OUTPUT-'].update(value=tmp)
                    self.window['-SAIDA-'].print('= ' + tmp)
                else:
                    self.window['-OUTPUT-'].update(value='data inválida')

            if self.event == '-DIAS-':
                op = strip_operacao(self.values['-INPUT1-'])
                if op == 'ERRO':
                    self.window['-OUTPUT-'].update(value='data inválida')
                else:
                    self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' DIAS')
                    resultado = calcula(op[0], op[1], op[2], 'D')
                    self.window['-OUTPUT-'].update(value=resultado)
                    self.window['-SAIDA-'].print('= ' + resultado)
                    # self.operacao = False

            if self.event == '-MESES-':
                op = strip_operacao(self.values['-INPUT1-'])
                if op == 'ERRO':
                    self.window['-OUTPUT-'].update(value='data inválida')
                else:
                    self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' MESES')
                    resultado = calcula(op[0], op[1], op[2], 'M')
                    self.window['-OUTPUT-'].update(value=resultado)
                    self.window['-SAIDA-'].print('= ' + resultado)
                    # self.operacao = False

            if self.event == '-ANOS-':
                op = strip_operacao(self.values['-INPUT1-'])
                if op == 'ERRO':
                    self.window['-OUTPUT-'].update(value='data inválida')
                else:
                    self.window['-SAIDA-'].print(self.values['-INPUT1-'] + ' ANOS')
                    resultado = calcula(op[0], op[1], op[2], 'A')
                    self.window['-OUTPUT-'].update(value=resultado)
                    self.window['-SAIDA-'].print('= ' + resultado)
                    # self.operacao = False

            if self.event == '-HOJE-':
                self.window['-INPUT1-'].update(value=datetime.strftime(date.today(), '%d/%m/%Y'))

            if self.event in (sg.WIN_CLOSED, '-SAIR-'):
                break
        self.window.close()


if __name__ == '__main__':
    calculadora().run()
