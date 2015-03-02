from PyQt4 import QtGui, QtCore
import sys

import json
import datetime



class Window(QtGui.QMainWindow):
    
    
    ## init
    def __init__(self):
        
        super(Window, self).__init__()
        self.main_widget = QtGui.QWidget(self)
        self.main_widget.setObjectName("main")
        self.setMinimumSize(1,1)
        #self.grid = QtGui.QGridLayout(self.main_widget)
        #self.main_widget.resize(800, 500)
        self.setCentralWidget(self.main_widget)
        self.set_open()
        layout = QtGui.QVBoxLayout(self.main_widget)
    
    

        ## Controls
        #self.control_layout = QtGui.QHBoxLayout()
        #self.control_box = QtGui.QGroupBox()
        #self.control_box.setLayout(self.control_layout)
        #self.control_box.setStyleSheet("""
        #    margin: 0px;
        #    padding: 0px;
        #    border: 0px;
        #    background: red;
        #""")
        #layout.addWidget(self.control_box)

        self.status_label = QtGui.QLabel('Valitse asiakas ja tehtava', self)
        self.status_label.setStyleSheet("""
        
            font-size: 14px;
            font-family:calibri;
            font-style: italic;
            height: 40px;
            max-height: 40px;

        """)
        layout.addWidget(self.status_label)

        #self.info_button = MyPushButton()
        #self.info_button = QtGui.QPushButton()
        #self.info_button.setText('ESC')
        #self.info_button.setStyleSheet("""
        #
        #    background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fefefe, stop: 1 #ececec);
        #    border-radius: 5px;
        #    height:30px;
        #    border: 1px solid #ddd;
        #    text-align:left;
        #    padding-top:3px;
        #    font-size:14px;
        #    color: #666;
        #    width:70px;
        #    float:right;
        #    max-width:70px;
        #    text-align: middle;

        #""")
        #self.control_layout.addWidget(self.info_button)
        #self.info_button.resize(40, 30)

        
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
        
        self.scroll = MyScrollArea(self)
        self.scroll.setWindow(self)
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            background: red;
            background: white;
            border-radius: 5px;
            border: 1px solid #ddd;
            padding:0px;
        """)

        
        self.scroll_bar = self.scroll.verticalScrollBar()
        #self.scroll_bar.hide()
        #self.scroll_bar.parent().hide()

        layout.addWidget(self.scroll)
            
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
        self.start_time = None

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
        #self.send_to_background()

        #focus and bring front
        self.setFocus(True)
        self.activateWindow()
        self.raise_()
        self.show()  
  
  
    
    ### Listeners
    def mousePressEvent(self, event):
        if self.state == 'background':
            self.resume()
     
    def keyPressEvent(self, event):
        print self.state
        if self.state == 'background':
            self.resume()
        else:
            if event.key() == QtCore.Qt.Key_Right:
                #print 'Right'
                self.nextValue()
            elif event.key() == QtCore.Qt.Key_Escape:
                #print 'Esc'
                self.back()
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
            elif self.start_time != None and event.key() == QtCore.Qt.Key_Space:
                print 'Space'  
                self.stop_session()
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
    
    def back(self):   
        if self.state == 'customer':
            self.search.setText('')
            self.send_to_background()
        elif self.state == 'task':
            self.state = 'customer'
            self.hide_tasks()
            self.show_customers()
            self.search.setText('')
        self.focus_selected()
        
    def select(self):
        if self.state == 'customer':
            self.state = 'task'
            self.hide_customers()
            self.show_tasks()
            self.search.setText('')
        elif self.state == 'task':
            self.start_session()
            self.hide_tasks()

            self.search.setText('')
            self.send_to_background()
            #self.windowToTray()    
            #self.showMinimized()
            
        self.focus_selected()
        
    def resume(self):
        self.state = 'customer'
        self.mygroupbox.show()
        self.search.show()
        self.scroll.show()
        self.set_open()
        self.show_customers()
        self.setGeometry(100, 100, 350, 400)

        
    def send_to_background(self):
        self.state = 'background'
        self.setGeometry(1080, 740, 200, 60)
        self.mygroupbox.hide()
        self.search.hide()
        self.scroll.hide()
        self.set_closed()




    def set_open(self):
        self.main_widget.setStyleSheet("""
        #main{
            background-color:white;
            max-height:1000px;
        }
        """);
        
    def set_closed(self):
        self.main_widget.setStyleSheet("""
        #main{
            background-color:white;
            max-height:60px;
        }
        """); 


    def stop_session(self):
        self.customer_name = ''
        self.task_name = ''
        self.start_time = None

        
    def start_session(self):
        self.customer_name = self.lista[self.current_employer]
        self.task_name = self.hommat[0][self.current_task]
        self.start_time = datetime.datetime.now()


    def filter(self):
        query = self.search.text().toLower()
        if self.state == 'customer':
            first = True
            for item in self.buttons:
                item.inactivate()
                if query in item.getText().lower():
                    item.setVisible(True)
                    if first:
                        item.activate()
                        first = False
                        self.current_employer = self.lista.index(item.getText())
                else:
                    item.setVisible(False)
                    
                    
        elif self.state == 'task':
            first = True

            for item in self.taskbuttons:
                item.inactivate()
                if query in item.getText().lower():
                    item.setVisible(True)
                    if first:
                        item.activate()
                        first = False
                else:
                    item.setVisible(False)
        self.focus_selected()
        
    def focus_selected(self):
        if self.state == 'customer':
            self.scroll_bar.setValue(self.buttons[self.current_employer].pos().y() - 100)

        elif self.state == 'task':
            self.scroll_bar.setValue(self.buttons[self.current_task].pos().y() - 100)        

    def move(self, steps):
        print steps
        if self.state == 'customer':
            self.buttons[self.current_employer].inactivate()
            self.current_employer = max(min((self.current_employer + steps), self.customer_count - 1), 0)
            self.buttons[self.current_employer].activate()

        elif self.state == 'task':
            self.taskbuttons[self.current_task].inactivate()
            self.current_task = max(min((self.current_task + steps), len(self.hommat[0]) - 1), 0)
            self.taskbuttons[self.current_task].activate()

        self.focus_selected()
            
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
        if self.start_time != None:
            seconds = datetime.datetime.now() - self.start_time
            m, s = divmod(seconds.total_seconds(), 60)
            h, m = divmod(m, 60)
            time = "%d:%02d:%02d" % (h, m, s)
            self.status_label.setText(self.customer_name + ': ' + time+ "\n" + self.task_name )
        else:
            self.status_label.setText("Valitse asiakas ja tehtava")


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