import os
import argparse
import sys, sqlite3
import socket
import threading
import cv2
import numpy as np
import re
from datetime import datetime
import time

import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2


import pywinauto as pwa

os.environ['KMP_DUPLICATE_LIB_OK']='True'

from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QDialog, QMessageBox, \
    QBoxLayout, QListWidgetItem, QListWidget, QInputDialog
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QIcon

first_ui = uic.loadUiType("ui/first.ui")[0]
sign_ui = uic.loadUiType("ui/signup.ui")[0]
enter_ui = uic.loadUiType("ui/enter.ui")[0]
createExam_ui = uic.loadUiType("ui/createExam.ui")[0]
beforeExam_ui = uic.loadUiType("ui/beforetakeexam.ui")[0]
prepareExam_ui = uic.loadUiType("ui/prepareexam2.ui")[0]
takeExam_ui = uic.loadUiType("ui/takeexam2.ui")[0]


# 로그인창
class Login(QWidget, first_ui):
    def __init__(self):
        super(Login, self).__init__()
        self.signUppage = None
        self.myStartpage = None
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.btn_signup.clicked.connect(self.create_signUp)
        self.btn_login.clicked.connect(self.create_start)
        self.idEdit.setPlaceholderText("id")

        self.label_id.setPixmap(QtGui.QPixmap('./icon/login.png').scaledToWidth(32))
        self.label_pw.setPixmap(QtGui.QPixmap('./icon/password.png').scaledToWidth(32))

        self.pwEdit.setPlaceholderText("password")
        self.label_4.setPixmap(QtGui.QPixmap("./image/logo_h.jpg"))

        self.btn_login.setStyleSheet('''
                    QPushButton{
                    background-color: rgb(245,245,245);
                    font: 57 20pt "에스코어 드림 5 Medium";
                    color: rgb(62, 74, 184);
                    border-color: rgb(62, 74, 184);
                    border-style: solid;
                    border-width: 1.5px;
                    }

                    QPushButton:hover{
                    background-color: rgb(62, 74, 184);
                    font: 57 20pt "에스코어 드림 5 Medium";
                    color: rgb(255, 255, 255);}
                ''')

    def create_signUp(self):
        if self.signUppage is None:
            self.signUppage = SignUp(self)

        self.signUppage.setFixedSize(1920, 1080)
        self.signUppage.showMaximized()

    def create_start(self):

        ###########################
        global uid2
        uid = self.idEdit.text()
        uid2= self.idEdit.text()
        pw = self.pwEdit.text()
        queue = []
        str = 'login@' + uid + '@' + pw

        thread_socket_login = thread_socket_GUI(self, server_socket, str, queue)
        thread_socket_login.start()
        time.sleep(0.5)

        result = queue.pop()

        if result == '1':
            print("로그인성공")
            w_login.hide()
            if self.myStartpage is None:
                self.myStartpage = myStart(self)
            self.myStartpage.setFixedSize(1920, 1080)
            self.myStartpage.showMaximized()
        else:
            print("로그인 실패")
            # QMessageBox.about(self, "로그인실패", "아이디와 비밀번호가 일치하지 않습니다")
            msg = QMessageBox()
            msg.setText("\n아이디와 비밀번호가 일치하지 않습니다\n")
            msg.setWindowTitle("로그인실패")
            msg.setStyleSheet("background-color: rgb(255, 255, 255);")
            msg.setStyleSheet("QPushButton{background-color: rgb(225,225,225);}")
            msg.exec_()


# 회원가입창
class SignUp(QDialog, sign_ui):
    def __init__(self, *args, **kwargs):
        super(SignUp, self).__init__(*args, **kwargs)
        self.sqlConnect()
        self.initUI()

    def sqlConnect(self):
        try:
            self.conn = sqlite3.connect("test1.db")
        except:
            print("DB연동에 문제가 생겼습니다ㅠㅠ")
            exit(1)

    def initUI(self):
        self.setupUi(self)

        self.btn_signUp.clicked.connect(self.signUp)

    def signUp(self):

        ###########################
        uid = self.edit_id.text()
        pw = self.edit_pw.text()
        phoneNum = self.edit_phonenum.text()
        str = 'signUp@' + uid + '@' + pw + '@' + phoneNum

        thread_socket_signUp = thread_socket_GUI(self, server_socket, str, None)
        thread_socket_signUp.start()
        time.sleep(0.3)

        self.hide()
        ###########################

    def closeEvent(self, QCloseEvent):
        print("프로그램 close!")
        self.conn.close()


# 로그인 성공시 메인창
class myStart(QDialog, enter_ui):
    def __init__(self, *args, **kwargs):
        super(myStart, self).__init__(*args, **kwargs)
        self.createExampage = None
        self.takeExampage = None
        # self.sqlConnect()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.label.setPixmap(QtGui.QPixmap("./image/logo_v.png"))
        self.btn_prepare.setStyleSheet('''
                             QPushButton{

                             background-color: rgb(255,255,255);
                             font: 57 15pt "에스코어 드림 5 Medium";
                             color: rgb(62, 74, 184);
                             border-color: rgb(62, 74, 184);
                             border-style: solid;
                             icon: url(./icon/prepare.png);
                             border-radius: 5px;
                             border-width: 1.5px;
                             }

                             QPushButton:hover{
                             background-color: rgb(62, 74, 184);
                             font: 57 15pt "에스코어 드림 5 Medium";
                             icon: url(./icon/prepare_w.png);
                             border-radius: 5px;
                             color: rgb(255, 255, 255);}
                         ''')

        self.btn_enter.setStyleSheet('''
                             QPushButton{
                             background-color: rgb(255,255,255);
                             font: 57 15pt "에스코어 드림 5 Medium";
                             color: rgb(62, 74, 184);
                             icon: url(./icon/enter.png);
                             border-color: rgb(62, 74, 184);
                             border-style: solid;
                             border-width: 1.5px;
                             border-radius: 5px;
                             }

                             QPushButton:hover{
                             background-color: rgb(62, 74, 184);
                             font: 57 15pt "에스코어 드림 5 Medium";
                             icon: url(./icon/enter_w.png);
                             border-radius: 5px;
                             color: rgb(255, 255, 255);}
                         ''')

        self.btn_prepare.clicked.connect(self.createExam)
        self.btn_enter.clicked.connect(self.enterExam)

    def createExam(self):
        print("시험출제")
        if self.createExampage is None:
            self.createExampage = createExam(self)
        self.createExampage.setFixedSize(1920, 1080)
        self.createExampage.showMaximized()

    def enterExam(self):
        global beforeExamNum;
        print("시험응시")
        global eid

        text, ok = QInputDialog.getInt(self, "시험코드", "시험코드를 입력하세요.")
        queue = []
        string = 'enterExam@' + str(text)

        thread_socket_enter = thread_socket_GUI(self, server_socket, string, queue)
        thread_socket_enter.start()
        time.sleep(0.5)

        result = queue.pop()

        # 1이면 감독관, 0이면 응시자, -1이면 시험코드 잘못됨
        if result == '1':
            receive_webcam_thread = threading.Thread(target=thread_receive_webcam, args=(server_socket,))
            receive_webcam_thread.start()
            receive_webcam_thread.join()

        elif result == '0':
            eid = str(text)
            beforeExamNum = 0;
            #self.enterExampage = takeExam(self)
            #self.enterExampage.show()

            if self.takeExampage is None:
                self.takeExampage = takeExam(self)
            self.takeExampage.setFixedSize(1920, 1080)
            self.takeExampage.showMaximized()

        else:
            pass

    def closeEvent(self, QCloseEvent):
        print("프로그램 close!")
        self.conn.close()


# 시험생성_eid생성
class createExam(QDialog, createExam_ui):
    def __init__(self, *args, **kwargs):
        super(createExam, self).__init__(*args, **kwargs)
        self.prepareExampage = None
        self.sqlConnect()
        self.initUI()

    def sqlConnect(self):
        try:
            self.conn = sqlite3.connect("test1.db")
        except:
            print("DB연동에 문제가 생겼습니다ㅠㅠ")
            exit(1)

    def initUI(self):
        self.setupUi(self)
        self.btn_create.clicked.connect(self.createEid)

    def createEid(self):
        global eid
        print("eid생성 성공")
        self.cur = self.conn.cursor()
        sql = "insert into Exam(eid,startdate,enddate,starttime,endtime,uid) values (?,?,?,?,?,?)"
        a = self.startTime.date().toString("yyyyMMdd")
        b = self.endTime.date().toString("yyyyMMdd")
        c = self.startTime.time().toString("HHmmss")
        d = self.endTime.time().toString("HHmmss")
        eid = self.eid_Edit.text()
        self.cur.execute(sql, (eid, a, b, c, d, "uid"))

        string = 'createExam@' + str(eid) + '@' + a + '@' + c + '@' + b + '@' + d
        print(string)
        thread_socket_createExam = thread_socket_GUI(self, server_socket, string, None)
        thread_socket_createExam.start()

        time.sleep(0.3)

        self.hide()
        if self.prepareExampage is None:
            self.prepareExampage = prepareExam(self)
        self.prepareExampage.setFixedSize(1920, 1080)
        self.prepareExampage.showMaximized()

    def closeEvent(self, QCloseEvent):
        print("프로그램 close!")
        self.conn.close()


# 시험문제출제
class prepareExam(QDialog, prepareExam_ui):
    def __init__(self, *args, **kwargs):
        super(prepareExam, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        global problemNum
        problemNum = 1

        self.setupUi(self)

        self.next_btn.clicked.connect(self.next)
        self.done_btn.clicked.connect(self.done)
        self.label_pic.setPixmap(QtGui.QPixmap("./image/logo_h.jpg"))

    def next(self):
        print("다음문제")
        global problemNum

        self.conn = sqlite3.connect("test1.db")
        self.cur = self.conn.cursor()
        sql = "insert into " + eid + "(problemNum,question,answer) values (?,?,?)"
        question = self.question_Edit.text()
        answer = self.answer_Edit.text()

        string = 'newProblem@' + str(problemNum) + '@' + question + '@' + answer

        thread_socket_problem = thread_socket_GUI(self, server_socket, string, None)
        thread_socket_problem.start()
        time.sleep(0.3)

        item = QListWidgetItem(self.listWidget)
        custom_widget = Item()
        item.setSizeHint(custom_widget.sizeHint())
        self.listWidget.setItemWidget(item, custom_widget)
        self.listWidget.addItem(item)

        problemNum = problemNum + 1
        self.question_Edit.clear()
        self.answer_Edit.clear()

    def done(self):
        print("시험출제완료")

        thread_socket_complete = thread_socket_GUI(self, server_socket, 'complete@', None)
        thread_socket_complete.start()
        time.sleep(0.3)

        self.hide()

    def closeEvent(self, QCloseEvent):
        print("프로그램 close!")
        self.conn.close()

class Item(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        pbtext = "Q." + str(problemNum)
        self.pb = QPushButton(pbtext)
        layout.addWidget(self.pb)
        layout.setSizeConstraint(QBoxLayout.SetFixedSize)
        self.setLayout(layout)
        self.pb.clicked.connect(self.changePos)

    def changePos(self):
        global nowpos
        nowpos = int(self.pb.text().replace("Q.", "")) - 1
        global questionBrowser
        global result
        questionBrowser.setText(result[nowpos][1])


class beforeExam(QDialog,beforeExam_ui):
    def __init__(self, *args, **kwargs):
        global beforeExamNum;
        beforeExamNum=1;
        super(beforeExam, self).__init__(*args, **kwargs)
        self.takeExampage = None

        ######################################
        # thread_send_webcam 에서 frame을 imageStack에 저장
        self.imageStack = []
        ######################################
        self.queue = None
        self.isTimeOut = False
        self.i = 0
        #self.initUI()

        self.setupUi(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2.setAlignment(Qt.AlignCenter)

        # timer
        self.timer = QTimer(self)
        self.timer.start(100)
        self.timer.timeout.connect(self.timeout)

    def timeout(self):

        if(len(self.imageStack) > 0):
            frame = self.imageStack.pop()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # add circle
            cv2.circle(frame, (320, 240), 150, (255, 0, 0), 2)
            h,w,c = frame.shape
            qImg = QImage(frame.data, w, h, w*c, QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.label_2.setPixmap(pixmap)

        self.i += 1
        if(self.i > 100):
            self.timer.stop()
            self.queue.append(1)
            self.close()


# 시험응시창
class takeExam(QDialog, takeExam_ui):
    def __init__(self, *args, **kwargs):
        super(takeExam, self).__init__(*args, **kwargs)
        self.beforeExampage = None
        self.queue = []
        self.imageStack = []
        self.initUI()

    def initUI(self):
        global problemNum
        global nowpos
        nowpos = 0
        problemNum = 1

        self.setupUi(self)

        result = []
        problemInfo = server_socket.recv(1024).decode(encoding='ISO-8859-1')
        while problemInfo is not '0':
            messages = problemInfo.split('@')
            num = messages[0]
            problem = messages[1]
            answer = messages[2]

            a = [num, problem, answer]
            result.append(a)
            print(result)

            server_socket.send('1'.encode(encoding='ISO-8859-1'))
            problemInfo = server_socket.recv(1024).decode(encoding='ISO-8859-1')

        self.result = result

        for i in range(1, len(self.result) + 1):
            item = QListWidgetItem(self.listWidget)
            custom_widget = Item()
            item.setSizeHint(custom_widget.sizeHint())
            self.listWidget.setItemWidget(item, custom_widget)
            self.listWidget.addItem(item)
            problemNum = problemNum + 1

        self.answer = []

        global questionBrowser
        questionBrowser = self.questionBrowser
        self.questionBrowser.append(self.result[nowpos][1])

        #testtime = '1'

        #self.timer.setDigitCount(8)
        #self.timer.display(str(testtime))

        #self.timer = QTimer(self)
        #self.timer.setInterval(1000)
        #self.timer.timeout.connect(self.updateCounter)
        #self.timer.start()

        self.timer2 = QTimer(self)
        self.timer2.setInterval(10)
        self.timer2.timeout.connect(self.noother)
        self.timer2.start()

        self.pre_btn.clicked.connect(self.pre)
        self.next_btn.clicked.connect(self.next)
        self.submit_btn.clicked.connect(self.submit)

        send_webcam_thread = threading.Thread(target=thread_send_webcam, args=(server_socket, self.queue, self.imageStack))
        send_webcam_thread.start()


        if beforeExamNum==0:

            self.beforeExampage = beforeExam(self)
            self.beforeExampage.imageStack = self.imageStack
            self.beforeExampage.queue = self.queue
            self.beforeExampage.setFixedSize(1920, 1080)
            self.beforeExampage.showMaximized()

    def noother(self):
        t = u'Anti-Cheating_Test.*'
        # t = u'스융 졸프.*'
        app = pwa.application.Application()
        print('find title : ' + str(t))

        try:
            handle = pwa.findwindows.find_windows(title_re=t)[0]
            app.connect(handle=handle)
            print('title: ' + str(t) + 'handle: ' + str(handle) + ' Setted')
        except:
            print('No title exist on window ')

        # 어플리케이션의 window를 가져옴
        window = app.window(handle=handle)
        try:
            # 해당 윈도우를 탑으로 설정
            window.set_focus()
            # 버튼 눌리면 while문 빠져나가게끔
        except Exception as e:
            print('[error]setFocuse : ' + str(e))


    def updateCounter(self):
        remaining = self.bbb - datetime.now()
        #remaining = self.bbb - self.timer.remainingTime()

        print(remaining.seconds)
        print(type(self.timer.remainingTime()))
        hours = int(remaining.seconds / 3600)
        mins = int((remaining.seconds - hours * 3600) / 60)
        secs = int(remaining.seconds % 60)
        self.label_3.setText("%d:%02d:%02d" % (hours, mins, secs))


        #if self.bbb > datetime.now():
        #    print(remaining.seconds)
        #    print(type(self.timer.remainingTime()))
        #    hours = int(remaining.seconds / 3600)
        #    mins = int((remaining.seconds - hours * 3600) / 60)
        #    secs = int(remaining.seconds % 60)
        #    self.label_3.setText("%d:%02d:%02d" % (hours, mins, secs))
        #else:
        #    print(self.bbb)
        #    print(datetime.now())
        #    self.submit()

    def pre(self):
        print("이전")
        global nowpos
        if nowpos > 0:
            nowpos = nowpos - 1
            self.answer_Edit.clear()
            self.questionBrowser.setText(self.result[nowpos][1])
        else:
            QMessageBox.about(self, "알림", "첫 문제")

    def next(self):
        global nowpos
        self.answer.append(self.answer_Edit.text())
        print("다음")
        if nowpos < len(self.result) - 1:
            nowpos = nowpos + 1
            self.answer_Edit.clear()
            self.questionBrowser.setText(self.result[nowpos][1])
        else:
            QMessageBox.about(self, "알림", "마지막 문제")

    def submit(self):
        print("제출")

        self.queue.append(1)
        print("len(self.queue)", len(self.queue))

        print("웹캠 전송 종료, 답안 전송")
        server_socket.send('0'.encode(encoding='ISO-8859-1'))

        # 답안 저장
        print(self.answer)

        global uid2
        string = 'submit@' + str(uid2)
        for i in range(0, len(self.answer)):
            string = string + '@' + str(self.answer[i])
        print(string)

        thread_socket_problem = thread_socket_GUI(self, server_socket, string, None)
        thread_socket_problem.start()
        time.sleep(0.3)

        self.hide()


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

######################################
# argument imageStack 추가
def thread_send_webcam(server_socket, queue, imageStack):
    print("USER : CANDIDATE")
    capture = cv2.VideoCapture(0)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    while len(queue) < 2:

        ret, frame = capture.read()

        imageStack.append(frame)

        if ret == False:
            continue

        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        imgData = np.array(imgencode).tobytes()

        try:

            # -------------------------------------------------------
            # beforeExam 에서 전송하는 이미지는 cheatDetector 안쓰게 하고 싶어서 케이스 나눔
            # beforeExam 끝나면 (10초 지나면) queue에 값 하나 추가해서 값 바뀜

            if(len(queue) == 0):
                server_socket.send('2'.encode(encoding='ISO-8859-1'))
                server_socket.send(str(len(imgData)).ljust(16).encode(encoding='ISO-8859-1'))
                server_socket.send(imgData)
                server_socket.recv(1).decode(encoding='ISO-8859-1')

            else:
                server_socket.send('1'.encode(encoding='ISO-8859-1'))
                server_socket.send(str(len(imgData)).ljust(16).encode(encoding='ISO-8859-1'))
                server_socket.send(imgData)
                server_socket.recv(1).decode(encoding='ISO-8859-1')

            # -------------------------------------------------------

        except ConnectionResetError as e:
            break

        except ConnectionAbortedError as e:
            break

    server_socket.send('0'.encode(encoding='ISO-8859-1'))
    queue.append(1)


def thread_receive_webcam(server_socket):
    print("USER : SUPERVISOR")

    screen_rect = app.desktop().screenGeometry()
    screen_w, screen_h = screen_rect.width(), screen_rect.height()
    window_dict = {}
    cheat_memory = 0

    while True:
        try:
            uid = server_socket.recv(1024).decode(encoding='ISO-8859-1')

            if not uid:
                break

            length = server_socket.recv(16).decode(encoding='ISO-8859-1')
            stringData = recvall(server_socket, int(length))
            server_socket.send('1'.encode(encoding='ISO-8859-1'))

            imgData, cheatData = stringData[:-1], stringData[-1]
            data = np.frombuffer(imgData, dtype='uint8')
            decimg = cv2.imdecode(data, 1)
            decimg = cv2.flip(decimg, 1)
            cheat_info = int(cheatData)  # Cheat info: 0 Normal 1 Cheat 2 NoFace

            if True:  # DEBUG
                if cheat_info == 0:
                    cheat_memory = 0
                elif cheat_info == 1:
                    cv2.putText(decimg, 'CHEAT : Upper Left', (decimg.shape[1] // 4, decimg.shape[0] // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                elif cheat_info == 2:
                    cv2.putText(decimg, 'CHEAT : Lower Left', (decimg.shape[1] // 4, decimg.shape[0] // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                elif cheat_info == 3:
                    cv2.putText(decimg, 'CHEAT : Upper Right', (decimg.shape[1] // 4, decimg.shape[0] // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                elif cheat_info == 4:
                    cv2.putText(decimg, 'CHEAT : Lower Right', (decimg.shape[1] // 4, decimg.shape[0] // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                elif cheat_info == 5:
                    cv2.putText(decimg, 'No Face', (decimg.shape[1] // 4, decimg.shape[0] // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                elif cheat_info == 6:
                    cheat_memory = cheat_memory + 1
                    print(cheat_memory)
                    if cheat_memory > 10:
                        cv2.putText(decimg, 'CHEAT : Left', (decimg.shape[1] // 4, decimg.shape[0] // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                elif cheat_info == 7:
                    cheat_memory = cheat_memory + 1
                    print(cheat_memory)
                    if cheat_memory > 10:
                        cv2.putText(decimg, 'CHEAT : Right', (decimg.shape[1] // 4, decimg.shape[0] // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                elif cheat_info == 8:
                    cv2.putText(decimg, 'CHEAT : Too Far', (decimg.shape[1] // 4, decimg.shape[0] // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            print("@@decimg {}".format(decimg.shape))
            window_name = str(uid)
            print("@@@ {}".format(window_name))
            x = int(re.findall("\d+", window_name)[-1])
            print("#### {}".format(x))
            print("window dict  :{}".format(window_dict))
            cv2.namedWindow(window_name)

            if window_name not in window_dict.keys():
                window_x = (screen_w - (640 * 2)) // 2
                window_y = (screen_w - (480 * 1)) // 2
                window_x = window_x if window_x > 0 else 0
                window_y = window_y if window_y > 0 else 0

                window_x += len(window_dict.keys()) * 640
                while window_x > screen_w - 640:
                    window_x -= 640
                    window_y += 480
                while window_y > screen_h - 480:
                    window_y -= 380

                window_dict[window_name] = (window_x, window_y)

            wx = window_dict[window_name][0]
            wy = window_dict[window_name][1]

            # window_name = str(uid)
            # x = int(re.findall("\d+", window_name)[-1])
            # cv2.namedWindow(window_name)
            # cv2.moveWindow(window_name, x*600, 100)

            cv2.moveWindow(window_name, wx, wy)
            cv2.imshow(window_name, decimg)

            key = cv2.waitKey(1)
            if key == ord('q'):  # press q to exit
                break

        except ConnectionAbortedError as e:
            break


class thread_socket_GUI(QThread):
    # parent = MainWidget을 상속 받음.

    socket = None
    str = None
    result_queue = None

    def __init__(self, parent, socket, str, result_queue):
        super().__init__(parent)
        self.socket = socket
        self.str = str
        self.result_queue = result_queue

    def run(self):
        self.socket.send(self.str.encode(encoding='ISO-8859-1'))
        result = self.socket.recv(1024).decode(encoding='ISO-8859-1')
        print("recv:", result)

        if self.result_queue is not None:
            self.result_queue.append(result)
            print(self.result_queue)
        else:
            print("result_queue is none")


# 메인창
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # socket connection
    host = '192.168.219.100'
    # host = '122.43.117.171'
    # host = '127.0.0.1'
    # host = '183.97.17.205'

    port = 7777
    is_supervisor = False

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))

    w_login = Login()
    w_login.setFixedSize(1920, 1080)
    w_login.showMaximized()

    sys.exit(app.exec_())
