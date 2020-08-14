import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import messagebox as ms
import get_comport as gp
import serial


class MPort(QWidget):

    wid = 260
    hei = 380
    myconnect = serial.Serial()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pos_x = int((QDesktopWidget().screenGeometry().width()-self.wid)/2)
        pos_y = int((QDesktopWidget().screenGeometry().height()-self.hei)/2)

        self.setWindowTitle('PORT')
        self.setAutoFillBackground(False)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setGeometry(pos_x, pos_y, self.wid, self.hei)
        self.setWindowIcon(QIcon('image/rs-232_female_30px.png'))

        self.create_winbar()
        self.create_setup()

    def create_winbar(self):
        self.title_frame = QFrame(self)
        self.title_frame.setGeometry(0, 0, 260, 40)
        self.title_frame.setStyleSheet('background-color:#F4D03F')

        self.logo = QLabel(self.title_frame)
        self.logo.setGeometry(5, 5, 30, 30)
        self.logo.setPixmap(QPixmap('image/rs-232_female_30px.png'))

        self.login_la = QLabel(self.title_frame, text='PORT')
        self.login_la.setGeometry(40, 5, 70, 30)
        self.login_la.setFont(QFont('Consolas', 12, QFont.Bold))

        self.status_la = QLabel(self.title_frame)
        self.status_la.setGeometry(190, 5, 30, 30)
        self.status_la.setPixmap(QPixmap('image/crying_30px.png'))

        self.close_win_bt = QPushButton(self.title_frame)
        self.close_win_bt.setGeometry(225, 5, 30, 30)
        self.close_win_bt.setStyleSheet('border:flat')
        self.close_win_bt.setIcon(
            QIcon(QPixmap('image/close_window_40px.png')))
        self.close_win_bt.setIconSize(QSize(30, 30))
        self.close_win_bt.clicked.connect(self.close_win)

    def create_setup(self):
        self.setup_frame = QFrame(self)
        self.setup_frame.setGeometry(0, 40, 260, 380)
        self.setup_frame.setStyleSheet('background-color:#2471A3')

        self.port_la = QLabel(self, text='PORT')
        self.port_la.setGeometry(30, 80, 60, 30)
        self.port_la.setFont(QFont('Consolas', 12, QFont.Bold))
        self.port_la.setStyleSheet('background-color:#2471A3')

        self.port_cb = QComboBox(self)
        self.port_cb.setGeometry(110, 80, 120, 30)
        self.port_cb.setFont(QFont('Consolas', 12, QFont.Bold))
        self.port_cb.setStyleSheet('background-color:#FDFEFE;border:flat')
        self.port_cb.addItems(gp.get_ports())

        self.baud_la = QLabel(self, text='BAUD')
        self.baud_la.setGeometry(30, 120, 60, 30)
        self.baud_la.setFont(QFont('Consolas', 12, QFont.Bold))
        self.baud_la.setStyleSheet('background-color:#2471A3')

        self.baud_cb = QComboBox(self)
        self.baud_cb.setGeometry(110, 120, 120, 30)
        self.baud_cb.setFont(QFont('Consolas', 12, QFont.Bold))
        self.baud_cb.setStyleSheet('background-color:#FDFEFE;border:flat')
        self.baud_cb.addItems(['2400', '4800', '9600',
                               '14400', '19200', '38400', '56000', '57600', '115200'])
        self.baud_cb.setCurrentText('9600')

        self.data_la = QLabel(self, text='DATA')
        self.data_la.setGeometry(30, 160, 60, 30)
        self.data_la.setFont(QFont('Consolas', 12, QFont.Bold))
        self.data_la.setStyleSheet('background-color:#2471A3')

        self.data_cb = QComboBox(self)
        self.data_cb.setGeometry(110, 160, 120, 30)
        self.data_cb.setFont(QFont('Consolas', 12, QFont.Bold))
        self.data_cb.setStyleSheet('background-color:#FDFEFE;border:flat')
        # self.data_cb.view().setSelectioMode(2)
        self.data_cb.addItems(['8', '7', '6', '5'])

        self.parity_la = QLabel(self, text='PARITY')
        self.parity_la.setGeometry(30, 200, 100, 30)
        self.parity_la.setFont(QFont('Consolas', 12, QFont.Bold))
        self.parity_la.setStyleSheet('background-color:#2471A3')

        self.parity_cb = QComboBox(self)
        self.parity_cb.setGeometry(110, 200, 120, 30)
        self.parity_cb.setFont(QFont('Consolas', 12, QFont.Bold))
        self.parity_cb.setStyleSheet('background-color:#FDFEFE;border:flat')
        self.parity_cb.addItems(['none', 'even', 'odd'])

        self.stop_la = QLabel(self, text='STOP')
        self.stop_la.setGeometry(30, 240, 60, 30)
        self.stop_la.setFont(QFont('Consolas', 12, QFont.Bold))
        self.stop_la.setStyleSheet('background-color:#2471A3')

        self.stop_cb = QComboBox(self)
        self.stop_cb.setGeometry(110, 240, 120, 30)
        self.stop_cb.setFont(QFont('Consolas', 12, QFont.Bold))
        self.stop_cb.setStyleSheet('background-color:#FDFEFE;border:flat')
        self.stop_cb.addItems(['1', '2'])

        self.reload_bt = QPushButton(self, text='RELOAD')
        self.reload_bt.setGeometry(40, 310, 85, 30)
        self.reload_bt.setFont(QFont('Consolas', 12, QFont.Bold))
        self.reload_bt.setStyleSheet('background-color:#F4D03F')
        self.reload_bt.clicked.connect(self.reload_port)

        self.load_bt = QPushButton(self, text='LOAD')
        self.load_bt.setGeometry(140, 310, 85, 30)
        self.load_bt.setFont(QFont('Consolas', 12, QFont.Bold))
        self.load_bt.setStyleSheet('background-color:#F4D03F')
        self.load_bt.clicked.connect(self.load_connect)

    @staticmethod
    def get_parity(str_parity):
        if str_parity == 'even':
            return 'E'
        elif str_parity == 'odd':
            return 'O'
        elif str_parity == 'none':
            return 'N'

    @pyqtSlot()
    def load_connect(self):
        if (self.port_cb.currentIndex() == -1):
            ms.Messagebox(self).show_info(title='INFO',
                status=False, codes='0', contents='Error: empty !')
        else:
            if (self.myconnect.isOpen() == False):
                try:
                    self.load_port()
                except serial.SerialException as exp:
                    ms.Messagebox(self).show_info(title='INFO',
                        status=False, codes='0', contents='Error !'+exp)
            else:
                self.close_port()

    @pyqtSlot()
    def reload_port(self):
        if self.myconnect.isOpen() == True:
            self.myconnect.close()
            self.status_la.setPixmap(QPixmap('image/crying_30px.png'))
            self.load_bt.setText("LOAD")
            self.load_bt.setStyleSheet('background-color:#F4D03F')
        self.port_cb.clear()
        self.port_cb.addItems(gp.get_ports())
        ms.Messagebox(self).show_info(title='INFO',
            status=True, codes='1', contents='Reloaded !')

    def load_port(self):
        self.myconnect.port = self.port_cb.currentText()
        self.myconnect.baudrate = int(self.baud_cb.currentText())
        self.myconnect.bytesize = int(self.data_cb.currentText())
        self.myconnect.parity = self.get_parity(self.parity_cb.currentText())

        if(self.myconnect.isOpen() == False):
            self.myconnect.open()
            ms.Messagebox(self).show_info(title='INFO',
                status=True, codes='1', contents='Finish !')
            self.status_la.setPixmap(QPixmap('image/wink_30px.png'))
        self.load_bt.setText("CANNEL")
        self.load_bt.setStyleSheet('background-color:#ff2b2b')

    def close_port(self):
        if (self.myconnect.isOpen() == True):
            self.myconnect.close()
            self.status_la.setPixmap(QPixmap('image/crying_30px.png'))
            self.load_bt.setText("LOAD")
            self.load_bt.setStyleSheet('background-color:#F4D03F')
            ms.Messagebox(self).show_info(title='INFO',
                status=True, codes='1', contents='Disconnected !')

    def close_win(self):
        if self.myconnect.isOpen():
            self.myconnect.close()
        self.close()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_Return:
            self.load_connect()

def main():
    app = QApplication(sys.argv)
    my_app = MPort()
    my_app.show()
    app.exec_()

if __name__ == '__main__':
    main()

