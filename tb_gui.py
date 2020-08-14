import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.Qt import *
import qtawesome as qta
from tb_week import *

class SpiderGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.m_flag = False
        self.dir = ""
        self.initUI()


    def initUI(self):
        do_nothing = QAction(qta.icon('fa.gear', color='#FDE1E4'), 'decoration', self)
        title = QLabel('爬虫图形化程序', self)
        title.setFont(QFont("Microsoft YaHei"))
        title.setStyleSheet("QLabel{color: #ffffff}")
        # do_nothing = QAction(QIcon('_.png'), 'Exit', self)

        toolbar = self.addToolBar('a')
        toolbar.addAction(do_nothing)
        toolbar.addWidget(title)
        toolbar.setStyleSheet("QToolBar:top{background-color:#8E9AAF}")

        icon_exit = qta.icon('fa.window-close-o', scale_factor=1.3, color='#CBC0D3')
        btn_exit = QPushButton(icon_exit, '', self)
        broadcaster = QLabel('选择直播间：', self)
        # 设置下拉框
        self.combo = QComboBox(self)
        # bc_name = read_txt()
        bc_name = ["李佳琦", "薇娅", "盒马鲜生"]
        for n in bc_name:
            self.combo.addItem(n)
        # self.combo.addItem("李佳琦")
        # self.combo.addItem("薇娅")
        lbl_cookie = QLabel('Cookie:', self)
        lbl_dir = QLabel("存储路径：", self)
        dirEdit = QLineEdit(self)
        btn_dir = QPushButton(qta.icon('fa.folder-open', scale_factor=1.3, color='#e4c1f9'), '', self)


        cookieEdit = QTextEdit(self)
        btn_submit = QPushButton("提交", self)


        broadcaster.setFont(QFont("Microsoft YaHei"))
        self.combo.setFont(QFont("Microsoft YaHei"))
        lbl_cookie.setFont(QFont("Microsoft YaHei"))
        cookieEdit.setFont(QFont("Microsoft YaHei"))
        btn_submit.setFont(QFont("Microsoft YaHei"))
        lbl_dir.setFont(QFont("Microsoft YaHei"))
        btn_dir.setFont(QFont("Microsoft YaHei"))
        dirEdit.setFont(QFont("Microsoft YaHei"))

        btn_exit.setStyleSheet(#"QPushButton{background: transparent}"
                                "QPushButton{border: none !important}"
                                "QPushButton{font-size:0}"
                                "QPushButton{padding: 0 0}")
        btn_submit.setStyleSheet("QPushButton{background-color: #DEE2FF}"
                             "QPushButton{color: #231942}"
                             "QPushButton{font-size: 10pt}"
                             "QPushButton:hover{background-color:#FEEAFA}"
                            "QPushButton{border-radius:4px}"
                            "QPushButton{padding:2rem 4rem}")
        btn_submit.setCursor(QtCore.Qt.PointingHandCursor)
        btn_dir.setStyleSheet(#"QPushButton{background: transparent}"
                            "QPushButton{border: none !important}"
                            "QPushButton{border-radius:4px}"
                            "QPushButton{padding:1rem 2rem}")
        btn_dir.setCursor(QtCore.Qt.PointingHandCursor)

        # grid = QGridLayout()
        # grid.setSpacing(10)
        btn_exit.resize(40, 30)
        btn_exit.move(360, 5)
        lbl_cookie.move(20, 60)
        cookieEdit.resize(280, 100)
        cookieEdit.move(80, 60)
        broadcaster.move(20, 180)
        self.combo.move(100, 180)
        btn_submit.resize(50, 30)
        btn_submit.move(180, 300)
        lbl_dir.move(20, 240)
        dirEdit.resize(280, 30)
        dirEdit.move(80, 240)
        btn_dir.resize(50, 30)
        btn_dir.move(320, 240)

        # 将带监听器的变量设置为成员变量
        self.cookieEdit = cookieEdit
        self.dirEdit = dirEdit

        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor(196, 183, 205))  # 设置背景颜色
        self.setPalette(palette1)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setLayout(grid)
        self.setGeometry(750, 300, 400, 375)

        # 绑定事件
        btn_exit.clicked.connect(self.on_exit)
        btn_submit.clicked.connect(self.on_submit)
        btn_dir.clicked.connect(self.on_select)

        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def on_exit(self):
        """
        关闭窗口
        """
        self.close()

    def on_submit(self):
        '''
        提交Cookies
        在Console输出Cookies
        '''
        cookie = self.cookieEdit.toPlainText()
        print(cookie)
        broadcaster = self.combo.currentText()
        main(cookie, broadcaster, self.dir)

    def on_select(self):
        dir = QFileDialog.getExistingDirectory(self, "爬虫数据保存路径", "./")
        self.dir = dir
        self.dirEdit.setText(dir)
        print(dir)

    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

def read_txt():
    bc = []
    with open(os.path.join(app_path(), 'inbc.txt'), 'r') as f:
        while True:
            bc_name = f.readline().split()
            if not bc_name:
                break
            bc.append(bc_name[0])
        f.close()

    return bc

if __name__ == "__main__":
    app = QApplication(sys.argv)


    ex = SpiderGUI()
    sys.exit(app.exec_())
