import sys
from pyqt5.design import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import numpy as np
import locale

r"""
Calculadora de datas em PyQT5
Interface gráfica criada no QT Designer (https://build-system.fman.io/qt-designer-download)
Conversão da interface pelo comando 'pyuic5 .\design.ui >> design.py' (windows powershell)
Na importação do módulo, acontece um erro relacionado ao arquivo design.py conter caracteres
inválidos. Para driblar o erro eu usei o Notepad++ para substituir estes caracteres por vazio.
É necessário buscar por \x00 marcando a caixa "expressão regular" no canto inferior esquerdo.
Depois disso o arquivo volta a funcionar normalmente, a menos que o design seja alterado no 
QT Designer, o que torna todo o processo necessário novamente.

Outra dificuldade que pode ser enfrentada é no caso do debug do código no PyCharm (não sei se
ocorre em outras IDEs). Durante o percurso de debug ocorre uma falha na biblioteca numpy que
interrompe o processo. O único modo que encontrei de mitigar o erro foi desabilitar o
import da biblioteca temporariamente (comentando a linha).
"""


locale.setlocale(locale.LC_ALL, '')

regexdata = re.compile(r'^(\d{2})[-.\/](\d{2})[-.\/](\d{4})$')
regexvalor = re.compile(r'(\d)*')

form_data = '%d/%m/%Y'

class MyCalculadora(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.label.setStyleSheet('font-size:14px; font-weight: 700')
        self.txtOperacao.setFocus()
        self.txtOperacao.setStyleSheet('font:bold 14px;')
        self.txtResultado.setStyleSheet('font:bold 14px;')
        self.botaoDias.setStyleSheet('background: #095177; color: #fff; font-weight: 700')
        self.botaoMeses.setStyleSheet('background: #095177; color: #fff; font-weight: 700')
        self.botaoAnos.setStyleSheet('background: #095177; color: #fff; font-weight: 700')
        self.botaoHoje.setStyleSheet('background: #095177; color: #fff; font-weight: 700')
        self.botaoUteis.setStyleSheet('background: #095177; color: #fff; font-weight: 700')
        self.botaoDiaSemana.setStyleSheet('background: #095177; color: #fff; font-weight: 700')
        self.botaoDiferenca.setStyleSheet('background: #095177; color: #fff; font-weight: 700')
        self.botaoSair.setStyleSheet('background: #095177; color: #fff; font-weight: 700')
        self.botaoDias.clicked.connect(self.dias)
        self.botaoMeses.clicked.connect(self.meses)
        self.botaoAnos.clicked.connect(self.anos)
        self.botaoHoje.clicked.connect(self.hoje)
        self.botaoUteis.clicked.connect(self.diasuteis)
        self.botaoDiaSemana.clicked.connect(self.diasemana)
        self.botaoDiferenca.clicked.connect(self.diferenca)
        self.botaoSair.clicked.connect(self.sair)

    def strip_datas(self, datas):
        datas = datas.replace(" ", "")
        if datas == '':
            return 'ERRO'
        elif datas.find('-') == -1:
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
                return 'ERRO'
            else:
                return strings

    def calcula(self, data1, valor, operacao, opcao):
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

    def valida(self, data, valor):
        print(data, valor)
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

    def strip_operacao(self, operacao=''):
        op_limpo = operacao.replace(" ", "")
        print(op_limpo)
        if op_limpo.find('+') != -1:
            strings = op_limpo.split('+')
            if not self.valida(data=strings[0], valor=strings[1]):
                return 'ERRO'
            else:
                return strings[0], int(strings[1]), '+'
        elif op_limpo.find('-') != -1:
            strings = op_limpo.split('-')
            if not self.valida(data=strings[0], valor=strings[1]):
                return 'ERRO'
            else:
                return strings[0], int(strings[1]), '-'
        else:
            return 'ERRO'
    # EDITANDO
    def dma_func(self, dma):
        tmp = self.strip_datas(self.txtOperacao.text())
        if tmp != 'ERRO':
            data1 = datetime.strptime(tmp[0], form_data)
            data2 = datetime.strptime(tmp[1], form_data)
            timedelta = data1 - data2
            if dma == 'DIAS':
                resultado = str(timedelta.days)
            elif dma == 'MESES':
                resultado = str(round(timedelta.days / 30))
            elif dma == 'ANOS':
                resultado = str(round((timedelta.days / 365), 2))
            self.txtResultado.setText(resultado)
        else:
            op = self.strip_operacao(self.txtOperacao.text())
            if op == 'ERRO':
                self.txtResultado.setText('data inválida')
            else:
                resultado = self.calcula(op[0], op[1], op[2], dma)
                self.txtResultado.setText(resultado)

    def dias(self):
        self.dma_func('DIAS')
        # print('hoje')
        # operacao = self.txtOperacao.text()
        # print('operacao:',operacao)
        # op = self.strip_operacao(operacao=operacao)
        # print('op:',op)
        # if op == 'ERRO':
        #     self.txtResultado.setText('Operação inválida.')
        # else:
        #     print('chegou no resultado')
        #     resultado = self.calcula(op[0], op[1], op[2], 'D')
        #     self.txtResultado.setText(resultado)
        # print(operacao)
        # # self.txtResultado.setText(operacao)

    def meses(self):
        self.dma_func('MESES')
        # print('hoje')
        # operacao = self.txtOperacao.text()
        # print('operacao:',operacao)
        # op = self.strip_operacao(operacao=operacao)
        # print('op:',op)
        # if op == 'ERRO':
        #     self.txtResultado.setText('Operação inválida.')
        # else:
        #     print('chegou no resultado')
        #     resultado = self.calcula(op[0], op[1], op[2], 'M')
        #     self.txtResultado.setText(resultado)
        # print(operacao)
        # # self.txtResultado.setText(operacao)

    def anos(self):
        self.dma_func('ANOS')
        # print('hoje')
        # operacao = self.txtOperacao.text()
        # print('operacao:',operacao)
        # op = self.strip_operacao(operacao=operacao)
        # print('op:',op)
        # if op == 'ERRO':
        #     self.txtResultado.setText('Operação inválida.')
        # else:
        #     print('chegou no resultado')
        #     resultado = self.calcula(op[0], op[1], op[2], 'A')
        #     self.txtResultado.setText(resultado)
        # print(operacao)
        # # self.txtResultado.setText(operacao)

    def hoje(self):
        self.txtOperacao.setText(datetime.strftime(date.today(), form_data))
        self.txtResultado.setText('')

    def diasuteis(self):
        tmp = self.strip_datas(self.txtOperacao.text())
        print('TMP: ', tmp)
        if tmp == 'ERRO':
            print('As datas devem ser inseridas da seguinte forma: 00/00/0000-00/00/0000')
        else:
            print('TMP 0 and 1', tmp[0], tmp[1])
            data1 = datetime.strptime(tmp[0], form_data)
            data2 = datetime.strptime(tmp[1], form_data)
            res = np.busday_count(data1.strftime('%Y-%m-%d'), data2.strftime('%Y-%m-%d'))
            self.txtResultado.setText(str(res) + ' dias')

    def diasemana(self):
        tmp = self.txtOperacao.text()
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
            self.txtResultado.setText(tmp)
        else:
            self.txtResultado.setText('Operação inválida.')

    def diferenca(self):
        tmp = self.strip_datas(self.txtOperacao.text())
        print('TMP: ', tmp)
        if tmp == 'ERRO':
            print('As datas devem ser inseridas da seguinte forma: 00/00/0000-00/00/0000')
            self.txtResultado.setText('Operação inválida.')
        else:
            data1 = datetime.strptime(tmp[0], form_data)
            data2 = datetime.strptime(tmp[1], form_data)
            timedelta = data1 - data2
            self.txtResultado.setText(str(abs(timedelta.days)) + ' dias')

    def sair(self):
        QApplication.quit()

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    calc = MyCalculadora()
    calc.show()
    qt.exec_()