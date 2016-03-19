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
    

        self.status_label = QtGui.QLabel('Valitse asiakas ja tehtava', self)
        self.status_label.setStyleSheet("""
        
            font-size: 14px;
            font-family:calibri;
            font-style: italic;
            height: 40px;
            max-height: 40px;

        """)
        layout.addWidget(self.status_label)

        
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



        #### Internal variables
        
        self.current_selection = 0

        self.hommat = json1_data.values()
        self.state = "customer"
        self.buttons = []
        self.taskbuttons = []
        
        ## Start with customer list
        self.populate_customers()
        self.populate_tasks()
        self.hide_tasks()
        
        
        self.initUI()
        
    def centerWindow(self):
        self.setGeometry(500, 200, 450, 400)
        
    def initUI(self):
        self.centerWindow()
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

    
    def __icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.show()
            self.sysTray.setVisible(False)
    
    
    def windowToTray(self):
        self.sysTray.setVisible(True)
        self.hide()
    
    


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
            max-height:70px;
        }
        """); 


    


    def hide_tasks(self):
        for item in self.taskbuttons:
            item.setVisible(False)

    def show_tasks(self):
        for item in self.taskbuttons:
            item.setVisible(True)

    def populate_tasks(self):
        print self.hommat
        for item in self.hommat[0]:
            mypushbutton = MyPushButton(self, len(self.taskbuttons))
            mypushbutton.setText(item)
            self.vbox.addWidget(mypushbutton)
            self.taskbuttons.append(mypushbutton)
        
        self.taskbuttons[0].activate()

    def hide_customers(self):
        for item in self.buttons:
            item.setVisible(False)

    def show_customers(self):
        for item in self.buttons:
            item.setVisible(True)
            
    def populate_customers(self):
        for item in self.lista:
            mypushbutton = MyPushButton(self, len(self.buttons))
            mypushbutton.setText(item)
            self.vbox.addWidget(mypushbutton)
            self.buttons.append(mypushbutton)
                
        self.buttons[0].activate()


class SearchField(QtGui.QLineEdit):
    def setWindow(self, window):
        self.window = window
 

class MyScrollArea(QtGui.QScrollArea):
    
    def setWindow(self, window):
        self.window = window
        
    def keyPressEvent(self, event):
        self.window.keyPressEvent(event)
    
    
    
class MyPushButton(QtGui.QPushButton):
    def __init__(self, window, order):
        QtGui.QPushButton.__init__(self)
        self.inactivate()
        self.window = window
        self.order = order
    
    def enterEvent(self, *args, **kwargs):
        self.activate()
        self.window.selection = self.order
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



app = QtGui.QApplication(sys.argv)
window = Window()


sys.exit(app.exec_())