from PyQt4 import QtGui

class Window(QtGui.QWidget):
    def __init__(self, val):
        QtGui.QWidget.__init__(self)
        mygroupbox = QtGui.QGroupBox('Here are the customers')
        myform = QtGui.QFormLayout()
        labellist = []
        for i in range(val):
            labellist.append(MyPushButton())
            myform.addRow(labellist[i])
        mygroupbox.setLayout(myform)
        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(scroll)


class MyPushButton(QtGui.QPushButton):
    def __init__(self):
        QtGui.QPushButton.__init__(self)
        self.inactivate()
        self.setText("Customer")
        
    
    def enterEvent(self, *args, **kwargs):
        self.activate()
        try:
            return QtGui.QPushButton.enterEvent(self, *args, **kwargs)
        except TypeError:
            pass

    def leaveEvent(self, *args, **kwargs):
        self.inactivate()
        try:
            return QtGui.QPushButton.leaveEvent(self, *args, **kwargs)
        except TypeError:
            pass

    def inactivate(self):
        self.setStyleSheet("""
            background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fefefe, stop: 1 #ececec);
            border-radius: 5px;
            height:30px;
            border: 1px solid #ddd;
            text-align:left;
            padding-left:30px;
            padding-top:3px;
            font-size:14px;
            color: #666;
        """)
        
    def activate(self):
        self.setStyleSheet("""
            background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(234, 156, 0), stop: 1 rgb(221, 138, 0));
            border-radius: 5px;
            height:30px;
            border: 1px solid rgb(183, 121, 0);
            text-align:left;
            padding-left:30px;
            padding-top:3px;
            font-size:14px;
            color: white;
        """)


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window(25)
    window.setGeometry(500, 300, 300, 400)
    window.show()
    sys.exit(app.exec_())