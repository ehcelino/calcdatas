import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang import Builder
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from kivy.uix.textinput import TextInput
import re
import numpy as np
import locale
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Window.size = (300, 550)
Window.clearcolor = (1, 1, 1, 1)

regexdata = re.compile(r'^(\d{2})[-.\/](\d{2})[-.\/](\d{4})$')
regexvalor = re.compile(r'(\d)*')

locale.setlocale(locale.LC_ALL, '')


class CDataApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('CData.kv')

    # def teste_texto(self, instance, value):
    #     print('The widget', instance, 'have:', value)
    #     return value

    def build(self):
        pass
        # return Button(text='Hello World')


    def valida_data(self, data):
        resultado =  False
        try:
            tmp = bool(datetime.strptime(data, '%d/%m/%Y'))
            resultado = True
        except ValueError:
            resultado = False
        return resultado

    def strip_datas(self, datas):
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

    def valida(self, data, valor):
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

    def strip_operacao(self, operacao=''):
        op_limpo = operacao.replace(" ", "")
        if op_limpo.find('+') != -1:
            strings = op_limpo.split('+')
            if not self.valida(strings[0], strings[1]):
                return 'ERRO'
            else:
                return strings[0], int(strings[1]), '+'
        elif op_limpo.find('-') != -1:
            strings = op_limpo.split('-')
            if not self.valida(strings[0], strings[1]):
                return 'ERRO'
            else:
                return strings[0], int(strings[1]), '-'
        else:
            return 'ERRO'

    # def ler_operacao(self):
    #     resultado = None
    #     texto = self.root.ids.ti_operacao.text
    #     # texto = self.screen.ids.ti_operacao.text
    #     print(texto)
    #     texto_limpo = texto.replace(" ", "")
    #     if re.fullmatch(regexdata, texto_limpo):
    #         if self.valida_data(texto_limpo):
    #             resultado = texto_limpo
    #     elif texto_limpo.find('+') != -1:
    #         strings = texto_limpo.split('+')
    #         if self.valida_data(strings[0]) and re.fullmatch(regexvalor, strings[1]):
    #             resultado = (strings[0], strings[1], '+')
    #         else:
    #             resultado = 'ERRO'
    #     elif texto_limpo.find('-') != -1:
    #         strings = texto_limpo.split('-')
    #         if self.valida_data(strings[0]) and re.fullmatch(regexvalor, strings[1]):
    #             resultado = (strings[0], strings[1], '-')
    #         elif self.valida_data(strings[0]) and self.valida_data(strings[1]):
    #             resultado = (strings[0], strings[1])
    #         else:
    #             resultado = 'ERRO'
    #     else:
    #         resultado = 'ERRO'
    #     print('Resultado: ', resultado)
    #     return resultado

    def calcula(self, data1, valor, operacao, opcao):
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

    def botao_dias(self):
        tmp = self.strip_operacao(self.root.ids.ti_operacao.text)
        if tmp == 'ERRO':
            print(tmp)
            print('Operação inválida.')
            self.root.ids.ti_resultado.text = 'Operação inválida.'
        else:
            result = self.calcula(tmp[0], tmp[1], tmp[2], 'D')
            self.root.ids.ti_resultado.text = result
            historico = self.root.ids.ti_historico.text
            self.root.ids.ti_historico.text = \
                historico + '\n' + tmp[0] + ' ' + tmp[2] + ' ' + str(tmp[1]) + ' dias' + '\n= ' + result

    def botao_meses(self):
        tmp = self.strip_operacao(self.root.ids.ti_operacao.text)
        if tmp == 'ERRO':
            print(tmp)
            print('Operação inválida.')
            self.root.ids.ti_resultado.text = 'Operação inválida.'
        else:
            result = self.calcula(tmp[0], tmp[1], tmp[2], 'D')
            self.root.ids.ti_resultado.text = result
            historico = self.root.ids.ti_historico.text
            self.root.ids.ti_historico.text = \
                historico + '\n' + tmp[0] + ' ' + tmp[2] + ' ' + str(tmp[1]) + ' meses' + '\n= ' + result


    def botao_anos(self):
        tmp = self.strip_operacao(self.root.ids.ti_operacao.text)
        if tmp == 'ERRO':
            print(tmp)
            print('Operação inválida.')
            self.root.ids.ti_resultado.text = 'Operação inválida.'
        else:
            result = self.calcula(tmp[0], tmp[1], tmp[2], 'D')
            self.root.ids.ti_resultado.text = result
            historico = self.root.ids.ti_historico.text
            self.root.ids.ti_historico.text = \
                historico + '\n' + tmp[0] + ' ' + tmp[2] + ' ' + str(tmp[1]) + ' anos' + '\n= ' + result


    def botao_hoje(self):
        self.root.ids.ti_operacao.text = datetime.strftime(date.today(), '%d/%m/%Y')

    def botao_dias_uteis(self):
        # tmp = self.ler_operacao()
        tmp = self.strip_datas(self.root.ids.ti_operacao.text)
        print('TMP: ', tmp)
        if tmp == 'ERRO':
            print('As datas devem ser inseridas da seguinte forma: 00/00/0000-00/00/0000')
            self.root.ids.ti_resultado.text = 'Operação inválida.'
        # elif tmp[2] not in ('+', '-'):
        #     print('Operação inválida.')
        else:
            print('TMP 0 and 1', tmp[0], tmp[1])
            data1 = datetime.strptime(tmp[0], '%d/%m/%Y')
            data2 = datetime.strptime(tmp[1], '%d/%m/%Y')
            tmp2 = np.busday_count(data1.strftime('%Y-%m-%d'), data2.strftime('%Y-%m-%d'))
            self.root.ids.ti_resultado.text = str(abs(tmp2)) + ' dias'
            historico = self.root.ids.ti_historico.text
            self.root.ids.ti_historico.text = \
                historico + '\nEntre ' + tmp[0] + ' e ' + tmp[1] + ' há\n' + str(abs(tmp2)) + ' dias úteis.'

    def botao_dia_semana(self):
        # tmp = self.ler_operacao()
        tmp = self.root.ids.ti_operacao.text
        tmp3 = tmp.replace(" ", "")
        if tmp3 != '' and re.fullmatch(regexdata, tmp3):
            try:
                tmp2 = bool(datetime.strptime(tmp3, '%d/%m/%Y'))
            except ValueError:
                tmp2 = False
        else:
            tmp2 = False

        if tmp2:
        # print('TMP: ', tmp)
        # if tmp == 'ERRO':
        #     print('As datas devem ser inseridas da seguinte forma: 00/00/0000-00/00/0000')
        #     self.root.ids.ti_resultado.text = 'Operação inválida.'
        # else:
            dt_tmp = datetime.strptime(tmp3, '%d/%m/%Y')
            tmp2 = datetime.strftime(dt_tmp, '%A')
            self.root.ids.ti_resultado.text = tmp2
            historico = self.root.ids.ti_historico.text
            self.root.ids.ti_historico.text = \
                historico + '\n' + 'Dia ' + tmp + ' = ' + tmp2
        else:
            self.root.ids.ti_resultado.text = 'Operação inválida.'

    def botao_diferenca(self):
        # tmp = self.ler_operacao()
        tmp = self.strip_datas(self.root.ids.ti_operacao.text)
        print('TMP: ', tmp)
        if tmp == 'ERRO':
            print('As datas devem ser inseridas da seguinte forma: 00/00/0000-00/00/0000')
            self.root.ids.ti_resultado.text = 'Operação inválida.'
        # elif tmp[2] not in ('+', '-'):
        #     print('Operação inválida.')
        else:
            data1 = datetime.strptime(tmp[0], '%d/%m/%Y')
            data2 = datetime.strptime(tmp[1], '%d/%m/%Y')
            timedelta = data1 - data2
            self.root.ids.ti_resultado.text = str(abs(timedelta.days)) + ' dias'
            historico = self.root.ids.ti_historico.text
            self.root.ids.ti_historico.text = \
                historico + '\n' + tmp[0] + ' - ' + tmp[1] + ' = ' + str(abs(timedelta.days)) + ' dias'

    def close(self):
        self.stop()

if __name__ == '__main__':
    CDataApp().run()