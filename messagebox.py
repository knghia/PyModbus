import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Messagebox(QDialog):

    wid = 300
    hei = 280

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pos_x = int((QDesktopWidget().screenGeometry().width()-self.wid)/2)
        pos_y = int((QDesktopWidget().screenGeometry().height()-self.hei)/2)

        self.setGeometry(pos_x, pos_y, self.wid, self.hei)
        self.setAutoFillBackground(False)
        self.setWindowFlags(Qt.Dialog|Qt.FramelessWindowHint)

        self.create_winbar()
        self.create_info()

    def create_winbar(self):
        self.title_frame = QFrame(self)
        self.title_frame.setGeometry(0, 0, 300, 40)
        self.title_frame.setStyleSheet('background-color:#F4D03F')

        self.logo = QLabel(self.title_frame)
        self.logo.setGeometry(5, 5, 30, 30)
        self.logo.setPixmap(QPixmap('image/message_30px.png'))

        self.close_win_bt = QPushButton(self.title_frame)
        self.close_win_bt.setGeometry(265, 5, 30, 30)
        self.close_win_bt.setStyleSheet('border:flat')
        self.close_win_bt.setIcon(
            QIcon(QPixmap('image/close_window_40px.png')))
        self.close_win_bt.setIconSize(QSize(30, 30))
        self.close_win_bt.clicked.connect(self.close_win)

    def create_info(self):

        self.info_frame = QFrame(self)
        self.info_frame.setGeometry(0, 40, 300, 240)
        self.info_frame.setStyleSheet('background-color:#2471A3')

        self.status_la = QLabel(self.info_frame, text='STATUS')
        self.status_la.setGeometry(30, 10, 90, 30)
        self.status_la.setFont(QFont('Consolas', 12, QFont.Bold))

        self.status_icon = QLabel(self.info_frame)
        self.status_icon.setGeometry(50, 35, 50, 30)

        self.codes_la = QLabel(self.info_frame, text='CODE')
        self.codes_la.setGeometry(210, 10, 70, 30)
        self.codes_la.setFont(QFont('Consolas', 12, QFont.Bold))

        self.codes_icon = QLabel(self.info_frame)
        self.codes_icon.setGeometry(210, 35, 60, 30)
        self.codes_icon.setFont(QFont('Consolas', 12, QFont.Bold))
        self.codes_icon.setStyleSheet(
            'background-color:#FDFEFE;padding-left: 2px')

        self.contents = QPlainTextEdit(self.info_frame)
        self.contents.setGeometry(20, 80, 260, 100)
        self.contents.setFont(QFont('Consolas', 12, QFont.Bold))
        self.contents.setStyleSheet(
            'background-color:#FDFEFE;padding-left: 2px')

        self.close_bt = QPushButton(self, text='OK')
        self.close_bt.setGeometry(100, 230, 100, 30)
        self.close_bt.setFont(QFont('Consolas', 12, QFont.Bold))
        self.close_bt.setStyleSheet('background-color: #F4D03F;border:flat')
        self.close_bt.clicked.connect(self.close_win)

    @pyqtSlot()
    def close_win(self):
        self.close()

    def key_press_event(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()

    def show_info(self, *args, **kwargs):
        if (kwargs['status'] == True):
            self.status_icon.setPixmap(QPixmap('image/checkmark_30px.png'))
        else:
            self.status_icon.setPixmap(QPixmap('image/error_30px2.png'))

        self.login_la = QLabel(self.title_frame, text=kwargs['title'])
        self.login_la.setGeometry(40, 5, 70, 30)
        self.login_la.setFont(QFont('Consolas', 10, QFont.Bold))

        self.codes_icon.setText(kwargs['codes'])
        self.contents.insertPlainText(kwargs['contents'])
        self.show()
        


if __name__ == '__main__':

    app = QApplication(sys.argv)
    my_app = Messagebox()
    my_app.show_info(status=True, codes='1', contents='Finish !')
    app.exec_()
