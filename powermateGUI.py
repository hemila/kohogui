from PyQt4 import QtGui, QtCore
import sys

import json
import datetime
from objc._objc import NULL



class Window(QtGui.QMainWindow):
    
    
    ## init
    def __init__(self):
        
        super(Window, self).__init__()
        self.main_widget = QtGui.QWidget(self)
        #self.grid = QtGui.QGridLayout(self.main_widget)
        #self.main_widget.setStyleSheet("background-color:black;");
        self.main_widget.resize(800, 500)
        #self.setCentralWidget(self.main_widget)


        self.vbox = QtGui.QVBoxLayout()


            
        mygroupbox = QtGui.QGroupBox()
        mygroupbox.setLayout(self.vbox)
        #mygroupbox.setGeometry(300, 300, 650, 300)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        #scroll.setFixedHeight(400)
        #scroll.setGeometry(300, 300, 650, 300)

        layout = QtGui.QVBoxLayout(self.main_widget)
        layout.addWidget(scroll)

            
        ### systray
        self.sysTray = QtGui.QSystemTrayIcon(self)
        self.sysTray.setIcon( QtGui.QIcon('koho.png') )
        self.connect(self.sysTray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.__icon_activated)

        json1_file = open('tehtavat.json')
        json1_str = json1_file.read()
        json1_data = json.loads(json1_str)
        self.data = json1_data
        self.lista = json1_data.keys()
        self.lista.sort()

        #### Timer
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.tick)
        self.my_timer.start(1000) #1 second interval

        #### Internal variables
        self.current_employer = 0
        self.current_task = 0
        self.hommat = json1_data.values()
        self.state = "customer"
        self.buttons = []
        self.taskbuttons = []
        self.start_time = NULL
        
        ## Start with customer list
        self.populate_customers()
        #self.populate_tasks()
        #self.hide_tasks()
        
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(200, 200, 850, 500)
        self.setWindowTitle("Koho")
        exit_action = QtGui.QAction(QtGui.QIcon('./exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)     
        
        self.show()
        
        #focus and bring front
        self.setFocus(True)
        self.activateWindow()
        self.raise_()
        self.show()  
    ### Listener   
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            print 'Right'
            self.nextValue()
        elif event.key() == QtCore.Qt.Key_Left:
            print 'Left'
            self.previousValue()
        elif event.key() == QtCore.Qt.Key_Up:
            print 'Up'
            self.previousValue()
        elif event.key() == QtCore.Qt.Key_Down:
            print 'Down'
            self.nextValue()
        elif event.key() == QtCore.Qt.Key_Enter:
            print 'Enter'
            self.select()
        elif event.key() == QtCore.Qt.Key_Return:
            print 'Enter'
            self.select()
        elif event.key() == QtCore.Qt.Key_Space:
            print 'Space'  
            self.select()
                      
        #else:
        #    print event.key()
        
        #event.accept() #stops propagation
        #event.ignore() #will propagate
    
    def __icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.show()
            self.sysTray.setVisible(False)
    
    
    def windowToTray(self):
        self.sysTray.setVisible(True)
        self.hide()
        
    
    def select(self):
        if self.state == 'customer':
            self.state = 'task'
            self.hide_customers()
            self.show_tasks()
        elif self.state == 'task':
            self.state = 'customer'
            self.start_time = datetime.datetime.now()
            self.hide_tasks()
            self.show_customers()
            #self.windowToTray()    

    def nextValue(self):
        if self.state == 'customer':
            self.buttons[self.current_employer].inactivate()
            if self.current_employer < len(self.lista) - 1:
                self.current_employer = self.current_employer + 1
            else:
                self.current_employer = 0
            self.buttons[self.current_employer].activate()
        elif self.state == 'task':
            self.taskbuttons[self.current_task].inactivate()
            if self.current_task < len(self.hommat[0]) - 1:
                self.current_task = self.current_task + 1
            else:
                self.current_task = 0
            self.taskbuttons[self.current_task].activate()
        
    
    def previousValue(self):
        if self.state == 'customer':
            self.buttons[self.current_employer].setStyleSheet("background-color: green")
            if self.current_employer == 0:
                self.current_employer = len(self.lista) - 1
            else:
                self.current_employer = self.current_employer - 1
                self.buttons[self.current_employer].setStyleSheet("background-color: red")
        if self.state == 'task':
            self.taskbuttons[self.current_task].inactivate()
            if self.current_task == 0:
                self.current_task = len(self.hommat[0]) - 1
            else:
                self.current_task = self.current_task - 1
                self.taskbuttons[self.current_task].activate()
        
    



    def hide_tasks(self):
        for item in self.taskbuttons:
            item.setVisible(False)

    def show_tasks(self):
        for item in self.taskbuttons:
            item.setVisible(True)

    def populate_tasks(self):
        for item in self.hommat[0]:
            mypushbutton = MyPushButton()
            mypushbutton.setText(item)
            self.grid.addWidget(mypushbutton)
            self.taskbuttons.append(mypushbutton)
        
        self.taskbuttons[self.current_task].activate()

    def hide_customers(self):
        for item in self.buttons:
            item.setVisible(False)

    def show_customers(self):
        for item in self.buttons:
            item.setVisible(True)
            
    def populate_customers(self):
        for item in self.lista:
            mypushbutton = MyPushButton()
            mypushbutton.setText(item)
            self.vbox.addWidget(mypushbutton)
            self.buttons.append(mypushbutton)
                
        self.buttons[self.current_employer].activate()

    def tick(self):
        if self.start_time != NULL:
            print datetime.datetime.now() - self.start_time

class MyPushButton(QtGui.QPushButton):
    def __init__(self):
        QtGui.QPushButton.__init__(self)
        self.setStyleSheet("background-color: green")
        
    def activate(self):
        self.setStyleSheet("background-color: red")

    def inactivate(self):
        self.setStyleSheet("background-color: green")


app = QtGui.QApplication(sys.argv)
window = Window()


sys.exit(app.exec_())