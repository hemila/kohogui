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
        #self.main_widget.resize(800, 500)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet("background-color:white;");
        
        self.setStyleSheet("""

        .QLabel {
            font-size: 20px;
            font-family:calibri;
            background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #ccf);
        }
        .QPushButton{
            background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fefefe, stop: 1 #ececec);
            border-radius: 5px;
            height:30px;
            border: 1px solid #ddd;
            text-align:left;
            padding-left:30px;
            padding-top:3px;
            font-size:14px;
            color: #666;
            width:30px;
        }

        """)

        layout = QtGui.QVBoxLayout(self.main_widget)
        layout.setAlignment(QtCore.Qt.AlignTop)

        ### Labels

        self.customer_label = QtGui.QLabel('No customer')
        self.task_label = QtGui.QLabel('No task')
        self.time_label = QtGui.QLabel('No session')



        layout.addWidget(self.customer_label)
        layout.addWidget(self.task_label)
        layout.addWidget(self.time_label)
        
        #Control buttons
        self.minimize_button = QtGui.QPushButton('Piilota')
        self.back_button = QtGui.QPushButton('Takaisin')
        self.stop_button = QtGui.QPushButton('Stop')
        
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.back_button)
        layout.addWidget(self.stop_button)
        
        #search
        self.search = SearchField('')
        self.search.setStyleSheet("""
            padding:5px;
            text-align:middle;
            border-radius:10px;
            border: 2px solid #aaa;
            color: #aaa;
            font-weight: bold;
        """)
        self.search.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.search)

        # Listings
        self.vbox = QtGui.QVBoxLayout()            
        self.mygroupbox = QtGui.QGroupBox()
        self.mygroupbox.setLayout(self.vbox)

        
        scroll = MyScrollArea(self)
        scroll.setWindow(self)
        scroll.setWidget(self.mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            background: white;
            border-radius: 5px;
            border: 1px solid #ddd;
            padding:0px;
        """)

        
        self.scroll_bar = scroll.verticalScrollBar()
        #self.scroll_bar.hide()
        #self.scroll_bar.parent().hide()

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
        self.customer_count = len(self.lista)

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
        self.populate_tasks()
        self.hide_tasks()
        
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(100, 100, 350, 400)
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
            #print 'Right'
            self.nextValue()
        elif event.key() == QtCore.Qt.Key_Left:
            #print 'Left'
            self.previousValue()
        elif event.key() == QtCore.Qt.Key_Up:
            #print 'Up'
            self.previousValue()
        elif event.key() == QtCore.Qt.Key_Down:
            #print 'Down'
            self.nextValue()
        elif event.key() == QtCore.Qt.Key_Enter:
            #print 'Enter'
            self.select()
        elif event.key() == QtCore.Qt.Key_Return:
            #print 'Enter'
            self.select()
        elif event.key() == QtCore.Qt.Key_Space:
            #print 'Space'  
            self.select()
        else:
            self.search.keyPressEvent(event)
            self.filter()
            #str = QtCore.QString( QtCore.QChar(event.key()) )
            #self.search.setText(self.search.getText + str)
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
            self.search.setText('')
        elif self.state == 'task':
            self.start_session()
            self.state = 'customer'
            self.start_time = datetime.datetime.now()
            self.hide_tasks()
            self.show_customers()
            self.search.setText('')
            #self.windowToTray()    
            #self.showMinimized()
            
    def start_session(self):
        self.customer_label.setText(self.lista[self.current_employer])  
        self.task_label.setText(self.hommat[0][self.current_task])  

    def filter(self):
        query = self.search.text().toLower()
        if self.state == 'customer':
            for item in self.buttons:
                if query in item.getText().lower():
                    item.setVisible(True)
                else:
                    item.setVisible(False)
        elif self.state == 'task':
            for item in self.taskbuttons:
                if query in item.getText().lower():
                    item.setVisible(True)
                else:
                    item.setVisible(False)


    def move(self, steps):
        if self.state == 'customer':
            self.buttons[self.current_employer].inactivate()
            self.current_employer = (self.current_employer + steps) % self.customer_count
            self.buttons[self.current_employer].activate()
            self.scroll_bar.setValue(self.buttons[self.current_employer].pos().y() - 100)

        elif self.state == 'task':
            self.taskbuttons[self.current_task].inactivate()
            self.current_task = (self.current_task + steps) % len(self.hommat[0])
            self.taskbuttons[self.current_task].activate()
            self.scroll_bar.setValue(self.buttons[self.current_task].pos().y() - 100)

            
    def nextValue(self):
        self.move(1)     
    
    def previousValue(self):
        self.move(-1)


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
            self.vbox.addWidget(mypushbutton)
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
            seconds = datetime.datetime.now() - self.start_time
            m, s = divmod(seconds.total_seconds(), 60)
            h, m = divmod(m, 60)
            time = "%d:%02d:%02d" % (h, m, s)
            self.time_label.setText(time)

class SearchField(QtGui.QLineEdit):
    def setWindow(self, window):
        self.window = window
 

class MyScrollArea(QtGui.QScrollArea):
    
    def setWindow(self, window):
        self.window = window
        
    def keyPressEvent(self, event):
        self.window.keyPressEvent(event)
    
    def wheelEvent(self, event):
        self.window.move(-int(event.delta()/8))
        event.ignore()
        
        

class MyPushButton(QtGui.QPushButton):
    def __init__(self):
        QtGui.QPushButton.__init__(self)
        #self.setStyleSheet("background-color: green;")
        self.inactivate()
        
    def getText(self):
        return self.text
    
    def setText(self, text):
        self.text = text
        return QtGui.QPushButton.setText(self, text)
        
    def activate(self):
        self.setStyleSheet("""
            background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fefffe, stop: 1 rgb(253, 227, 193));
            border-radius: 5px;
            height:30px;
            border: 1px solid #ddd;
            text-align:left;
            padding-left:30px;
            font-weight:bold;
            padding-top:3px;
            font-size:16px;
        """)

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



app = QtGui.QApplication(sys.argv)
window = Window()


sys.exit(app.exec_())