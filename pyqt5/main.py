import sys
from pyqt5.design import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

regexdata = re.compile(r'^(\d{2})[-.\/](\d{2})[-.\/](\d{4})$')
regexvalor = re.compile(r'(\d)*')

form_data = '%d/%m/%Y'

class MyCalculadora(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.pushDias.clicked.connect(self.dias)
        self.pushMeses.clicked.connect(self.meses)
        self.pushAnos.clicked.connect(self.anos)
        self.pushHoje.clicked.connect(self.hoje)

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
            if opcao == 'D':
                data_final_date = data1_date + relativedelta(days=int(valor))
            # the_timedelta = data1_date - data2_date
            elif opcao == 'M':
                data_final_date = data1_date + relativedelta(months=+int(valor))
            elif opcao == 'A':
                data_final_date = data1_date + relativedelta(years=int(valor))
            data_final_str = datetime.strftime(data_final_date, form_data)
            return data_final_str

        if operacao == '-':
            if opcao == 'D':
                data_final_date = data1_date - relativedelta(days=int(valor))
            # the_timedelta = data1_date - data2_date
            elif opcao == 'M':
                data_final_date = data1_date - relativedelta(months=int(valor))
            elif opcao == 'A':
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

    def dias(self):
        print('hoje')
        operacao = self.lineOperacao.text()
        print('operacao:',operacao)
        op = self.strip_operacao(operacao=operacao)
        print('op:',op)
        if op == 'ERRO':
            self.lineResultado.setText('Operação inválida.')
        else:
            print('chegou no resultado')
            resultado = self.calcula(op[0], op[1], op[2], 'D')
            self.lineResultado.setText(resultado)
        print(operacao)
        # self.lineResultado.setText(operacao)

    def meses(self):
        print('hoje')
        operacao = self.lineOperacao.text()
        print('operacao:',operacao)
        op = self.strip_operacao(operacao=operacao)
        print('op:',op)
        if op == 'ERRO':
            self.lineResultado.setText('Operação inválida.')
        else:
            print('chegou no resultado')
            resultado = self.calcula(op[0], op[1], op[2], 'M')
            self.lineResultado.setText(resultado)
        print(operacao)
        # self.lineResultado.setText(operacao)

    def anos(self):
        print('hoje')
        operacao = self.lineOperacao.text()
        print('operacao:',operacao)
        op = self.strip_operacao(operacao=operacao)
        print('op:',op)
        if op == 'ERRO':
            self.lineResultado.setText('Operação inválida.')
        else:
            print('chegou no resultado')
            resultado = self.calcula(op[0], op[1], op[2], 'A')
            self.lineResultado.setText(resultado)
        print(operacao)
        # self.lineResultado.setText(operacao)

    def hoje(self):
        self.lineOperacao.setText(datetime.strftime(date.today(), form_data))


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    calc = MyCalculadora()
    calc.show()
    qt.exec_()