from PyQt4 import QtGui

class Window(QtGui.QWidget):
    def __init__(self, val):
        QtGui.QWidget.__init__(self)
        mygroupbox = QtGui.QGroupBox('this is my groupbox')
        myform = QtGui.QFormLayout()
        labellist = []
        for i in range(val):
            labellist.append(QtGui.QLabel('mylabel'))
            myform.addRow(labellist[i])
        mygroupbox.setLayout(myform)
        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(scroll)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window(25)
    window.setGeometry(500, 300, 300, 400)
    window.show()
    sys.exit(app.exec_())