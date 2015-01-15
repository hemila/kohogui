from PyQt4 import QtGui, QtCore
import sys

import json



class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.main_widget = QtGui.QWidget(self)
        self.grid = QtGui.QGridLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)


        
        
        self.sysTray = QtGui.QSystemTrayIcon(self)
        self.sysTray.setIcon( QtGui.QIcon('koho.png') )
        self.connect(self.sysTray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.__icon_activated)

   

        json1_file = open('tehtavat.json')
        json1_str = json1_file.read()
        json1_data = json.loads(json1_str)
        self.data = json1_data
        self.lista = json1_data.keys()
        self.lista.sort()

        employers = ""
        for item in self.lista:
            employers = employers + item + ' \n'

        
        
        self.current_employer = 0
        self.current_task = 0
        
        self.hommat = json1_data.values()
        
        
        self.state = "customer"
        
        self.buttons = []
        self.taskbuttons = []
        
        
        for item in self.lista:
            mypushbutton = MyPushButton()
            mypushbutton.setText(item)
            mypushbutton.setStyleSheet("background-color: green")
            self.grid.addWidget(mypushbutton)
            self.buttons.append(mypushbutton)
        
        self.connect(self.grid, QtCore.SIGNAL("RightPressed"), self.nextValue)
        self.connect(self.buttons[0], QtCore.SIGNAL("LeftPressed"), self.previousValue)
        self.connect(self.buttons[0], QtCore.SIGNAL("clicked()"), self.rollClickedEmployer)
        
        
        self.buttons[0].setStyleSheet("background-color: red")
        
        for item in self.hommat[0]:
            mypushbutton = MyPushButton()
            mypushbutton.setText(item)
            mypushbutton.setStyleSheet("background-color: green")
            mypushbutton.setVisible(False)
            self.grid.addWidget(mypushbutton)
            self.taskbuttons.append(mypushbutton)
         
        for item in self.taskbuttons:
            self.connect(item, QtCore.SIGNAL("clicked()"), self.rollClickedTask) 
        
        
        self.initUI()
    
    
    def __icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.show()
            self.sysTray.setVisible(False)
        self.setState()
    
    
    def setState(self):
        print "setState started"
        if self.state == "customer":
            
            self.grid = QtGui.QGridLayout(self.main_widget)
            self.buttons = []
            for item in self.lista:
                mypushbutton = MyPushButton()
                mypushbutton.setText(item)
                mypushbutton.setStyleSheet("background-color: green")
                self.grid.addWidget(mypushbutton)
                self.buttons.append(mypushbutton)
            self.buttons[0].setStyleSheet("background-color: red")
            self.connect(self.buttons[0], QtCore.SIGNAL("RightPressed"), self.nextValue)
            self.connect(self.buttons[0], QtCore.SIGNAL("LeftPressed"), self.previousValue)
            self.connect(self.buttons[0], QtCore.SIGNAL("clicked()"), self.rollClickedEmployer)
            print "connects made"
    
    
    def windowToTray(self):
        self.sysTray.setVisible(True)
        self.hide()
        
        
    
    def rollClickedEmployer(self):
        for item in self.buttons:
            item.setVisible(False)
        for item in self.taskbuttons:
            item.setVisible(True)
        #self.disconnect(self.buttons[0], QtCore.SIGNAL("RightPressed"), self.nextValue)
            
    
    def rollClickedTask(self):
        for item in self.taskbuttons:
            item.setVisible(False)
       
        #self.connect(self.buttons[0], QtCore.SIGNAL("RightPressed"), self.nextValue)
        self.setState()
        #self.windowToTray()
    

    def nextValue(self):
        self.buttons[self.current_employer].setStyleSheet("background-color: green")
        if self.current_employer < len(self.lista) - 1:
            self.current_employer = self.current_employer + 1
        else:
            self.current_employer = 0
        self.buttons[self.current_employer].setStyleSheet("background-color: red")
        print "nextValue triggered"
    
    
    def previousValue(self):
        self.buttons[self.current_employer].setStyleSheet("background-color: green")
        if self.current_employer == 0:
            self.current_employer = len(self.lista) - 1
        else:
            self.current_employer = self.current_employer - 1
        self.buttons[self.current_employer].setStyleSheet("background-color: red")
    
    

    def initUI(self):
        self.setGeometry(300, 300, 650, 300)
        self.setWindowTitle("Koho")
        exit_action = QtGui.QAction(QtGui.QIcon('./exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)     
        
        self.show()



    def event(self, event):
        if (event.type()== QtCore.QEvent.KeyPress) and (event.key()== QtCore.Qt.Key_Right):
            self.emit(QtCore.SIGNAL("RightPressed"))
            print "right pressed"
            return True
        if (event.type()== QtCore.QEvent.KeyPress) and (event.key()== QtCore.Qt.Key_Left):
            self.emit(QtCore.SIGNAL("LeftPressed"))
            return True
        if (event.type()== QtCore.QEvent.KeyPress) and (event.key()== QtCore.Qt.Key_Space):
            self.emit(QtCore.SIGNAL("SpacePressed"))
            return True
        return QtGui.QMainWindow.event(self, event)
    


class MyPushButton(QtGui.QPushButton):
    def __init__(self):
        QtGui.QPushButton.__init__(self)
        
        
    def event(self, event):
        if (event.type()== QtCore.QEvent.KeyPress) and (event.key()== QtCore.Qt.Key_Right):
            self.emit(QtCore.SIGNAL("RightPressed"))
            #print "right pressed"
            return True
        if (event.type()== QtCore.QEvent.KeyPress) and (event.key()== QtCore.Qt.Key_Left):
            self.emit(QtCore.SIGNAL("LeftPressed"))
            return True
        if (event.type()== QtCore.QEvent.KeyPress) and (event.key()== QtCore.Qt.Key_Space):
            self.emit(QtCore.SIGNAL("SpacePressed"))
            return True
        return QtGui.QPushButton.event(self, event)    
        

app = QtGui.QApplication(sys.argv)
window = Window()


sys.exit(app.exec_())