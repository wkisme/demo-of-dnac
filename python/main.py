import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QWidget, QLineEdit,\
    QPushButton, QApplication, QMessageBox, QComboBox
from dnac_nbapi_mission.mission import nextui

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Login'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500
        self.log_interface()

    def log_interface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.dnac = QLineEdit(self)
        self.dnac.setPlaceholderText('dnac center')
        self.dnac.move(100, 100)
        self.user = QLineEdit(self)
        self.user.setPlaceholderText('User Name')
        self.user.move(100, 150)
        self.pw = QLineEdit(self)
        self.pw.setPlaceholderText('Password')
        self.pw.move(100, 200)
        self.combo = QComboBox(self)
        for i in ['https://sandboxdnac.cisco.com/' ,'https://sandboxdnac2.cisco.com/']:
            self.combo.addItem(i)
        self.combo.move(250, 100)
        self.combo.activated[str].connect(self.onchanged)

        self.combo1 = QComboBox(self)
        for i in ['devnetuser']:
            self.combo1.addItem(i)
        self.combo1.move(250, 150)
        self.combo1.activated[str].connect(self.onchanged1)

        self.combo2 = QComboBox(self)
        for i in ['Cisco123!']:
            self.combo2.addItem(i)
        self.combo2.move(250, 200)
        self.combo2.activated[str].connect(self.onchanged2)

        btn = QPushButton('Click to login', self)
        btn.move(100, 300)
        btn.clicked.connect(self.login)

        self.show()

    def onchanged(self, text):
        self.dnac.setText(text)
        self.dnac.adjustSize()
    def onchanged1(self, text):
        self.user.setText(text)
        self.user.adjustSize()
    def onchanged2(self, text):
        self.pw.setText(text)
        self.pw.adjustSize()


    def login(self):
        nextui(self.dnac.text(), self.user.text(), self.pw.text())
        self.SW = SecondWindow(self.dnac.text(), self.user.text(), self.pw.text())
        self.SW.show()

import sys
from PyQt5.QtWidgets import QWidget, QLineEdit,\
    QPushButton, QApplication, QMessageBox, QComboBox
from function.get_device_list_demo import get_device_list


class SecondWindow(QWidget):
    def __init__(self, dnac, user, pwd):
        super().__init__()
        self.title = 'path trace'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500
        self.dnac = dnac
        self.user = user
        self.pwd = pwd
        self.main_interface()

    def main_interface(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.source_port = QLineEdit(self)
        self.source_port.setPlaceholderText('source_port')
        self.source_port.move(100, 100)

        self.des_port = QLineEdit(self)
        self.des_port.setPlaceholderText('des_port')
        self.des_port.move(100, 200)
        self.combo = QComboBox(self)
        self.combo1 = QComboBox(self)
        combo_port = get_device_list(self.dnac, self.user, self.pwd)
        for i in combo_port:
            self.combo.addItem(i)
        self.combo.move(250, 100)
        self.combo.activated[str].connect(self.onchanged)

        for i in combo_port:
            self.combo1.addItem(i)
        self.combo1.move(250, 200)
        self.combo1.activated[str].connect(self.onchanged1)

        btn = QPushButton('Click to path traces', self)
        btn.move(100, 300)
        btn.clicked.connect(self.path_trace)

        self.show()

    def onchanged(self, text):
        self.source_port.setText(text)
        self.source_port.adjustSize()

    def onchanged1(self, text):
        self.des_port.setText(text)
        self.des_port.adjustSize()

    def path_trace(self):
        self.path_trace_window = path_trace_window(self.source_port.text(), self.des_port.text())
        self.path_trace_window.show()
import sys
from PyQt5.QtWidgets import QWidget, QLineEdit,\
    QPushButton, QApplication, QMessageBox, QComboBox, QLabel
from path_trace.path_trace import path_trace_main
class path_trace_window(QWidget):
    def __init__(self, source_port, des_port):
        super().__init__()
        self.title = 'path_trace_result'
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 1500
        self.source_port = source_port
        self.des_port = des_port
        self.result_interface()

    def result_interface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)

        # list1 = path_trace_main(self.source_port, self.des_port)

        self.outline = QLabel(self)
        self.outline.setText('path trace from \n' + self.source_port + ' to \n' + self.des_port)
        # self.outline.adjustSize()
        self.outline.move(0, 0)

        self.flow_analysis_lable = QLabel(self)
        self.flow_analysis_lable.setText('flow analysis: ')
        self.flow_analysis_lable.move(0, 100)

        self.hop1 = QLabel(self)
        self.hop1.setText('hop1')
        self.hop1.move(200, 100)

        self.hop2 = QLabel(self)
        self.hop2.setText('hop2')
        self.hop2.move(600, 100)

        self.hop3 = QLabel(self)
        self.hop3.setText('hop3')
        self.hop3.move(1000, 100)

        self.hop1_result = QLabel(self)
        self.hop1_result.setText('Hop 1: Network Device cat_9k_1.abc.inc' + '\n' +
                                 'Device IP: 10.10.22.66' + '\n' +
                                 'Device Role: ACCESS' + '\n' +
                                 'Ingress Interface' + '\n' +
                                 '--------------------' + '\n' +
                                 'Port Name: TenGigabitEthernet1/0/1' + '\n' +
                                 'Interface Type: Physical' + '\n' +
                                 'Admin Status: UP' + '\n' +
                                 'Operational Status: up' + '\n' +
                                 'Media Type: 100/1000/2.5G/5G/10GBaseTX' + '\n' +
                                 'Speed: 1000000' + '\n' +
                                 'Duplex Setting: FullDuplex' + '\n' +
                                 'Port Mode: access' + '\n' +
                                 'Interface VLAN: 1' + '\n' +
                                 'Voice VLAN: None' + '\n' +
                                 'Egress Interface' + '\n' +
                                 '--------------------' + '\n'
                                 )
        self.hop1_result.move(200, 200)

        self.hop2_result = QLabel(self)
        self.hop2_result.setText('Hop 2: Network Device cat_9k_1.abc.inc' + '\n' +
                                 'Device IP: 10.10.22.69' + '\n' +
                                 'Device Role: DISTRIBUTION' + '\n' +
                                 'Ingress Interface' + '\n' +
                                 '--------------------' + '\n' +
                                 'Port Name: TenGigabitEthernet1/1/2' + '\n' +
                                 'Interface Type: Physical' + '\n' +
                                 'Admin Status: UP' + '\n' +
                                 'Operational Status: up' + '\n' +
                                 'Media Type: SFP-10GBase-CX1' + '\n' +
                                 'Speed: 1000000' + '\n' +
                                 'Duplex Setting: FullDuplex' + '\n' +
                                 'Port Mode: routed' + '\n' +
                                 'Interface VLAN: None' + '\n' +
                                 'Voice VLAN: None' + '\n' +
                                 'Egress Interface' + '\n' +
                                 '--------------------' + '\n')
        self.hop2_result.move(600, 200)

        self.hop3_result = QLabel(self)
        self.hop3_result.setText('Hop 3: Network Device cat_9k_1.abc.inc' + '\n' +
                                 'Device IP: 10.10.22.70' + '\n' +
                                 'Device Role: ACCESS' + '\n' +
                                 'Ingress Interface' + '\n' +
                                 '--------------------' + '\n' +
                                 'Port Name: TenGigabitEthernet1/1/1' + '\n' +
                                 'Interface Type: Physical' + '\n' +
                                 'Admin Status: UP' + '\n' +
                                 'Operational Status: up' + '\n' +
                                 'Media Type: unknown' + '\n' +
                                 'Speed: 1000000' + '\n' +
                                 'Duplex Setting: FullDuplex' + '\n' +
                                 'Port Mode: routed' + '\n' +
                                 'Interface VLAN: None' + '\n' +
                                 'Voice VLAN: None' + '\n' +
                                 'Egress Interface' + '\n' +
                                 '--------------------' + '\n')
        self.hop3_result.move(1000, 200)



        self.show()

if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    app = QApplication(sys.argv)
    ex = Login()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
