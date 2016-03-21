from PyQt4 import QtGui, QtCore
import sys

import json



class Window(QtGui.QMainWindow):
    
    
    ## init
    def __init__(self):
        
        super(Window, self).__init__()
        self.main_widget = QtGui.QWidget(self)
        self.main_widget.setObjectName("main")
        self.setMinimumSize(1,1)

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
        
        panel = QtGui.QHBoxLayout()
        panel.addWidget(self.status_label)
        
        backbutton = BackButton()
        backbutton.setWindow(self)
        panel.addWidget(backbutton);
        
        
        layout.addLayout(panel)

        
        
        #search
        self.search = SearchField()
        self.search.setWindow(self)
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
        
        self.scroll = ScrollArea()
        
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
        
        self.hommat = json1_data.values()

        self.buttons = []
        self.taskbuttons = []
        
        ## Start with customer list
        self.populate_customers()
        self.populate_tasks()
        self.hide_tasks()
        
        #initialization
        self.current_button = None
        self.state = 'customer'
        
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
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape and self.state == 'tasks':
            try:
                self.show_customers()
                return QtGui.QMainWindow.keyPressEvent(self, event)
            except:
                pass
        
    
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
        return

    def hide_customers(self):
        for item in self.buttons:
            item.setVisible(False)

    def show_customers(self):
        for item in self.buttons:
            item.setVisible(True)
            
    def populate_customers(self):
        for item in self.lista:
            mypushbutton = PushButton()
            mypushbutton.setText(item)
            self.vbox.addWidget(mypushbutton)
            self.buttons.append(mypushbutton)
            mypushbutton.setWindow(self)


class SearchField(QtGui.QLineEdit):
    def __init__(self):
        QtGui.QLineEdit.__init__(self)
        self.setText("Not implemented!")
        self.setDisabled(True)

    
    
    def setWindow(self, window):
        self.window = window




class ScrollArea(QtGui.QScrollArea):
    def __init__(self):
        QtGui.QScrollArea.__init__(self)
   
   
   
class BackButton(QtGui.QPushButton):
    def __init__(self):
        QtGui.QPushButton.__init__(self)
        self.setText("Back")
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
    
    def mousePressEvent(self, event):
        if self.window.state == 'tasks':
            try:
                self.window.show_customers()
                return QtGui.QLineEdit.mousePressEvent(self, event)
            except TypeError:
                pass
    
    def setWindow(self, window):
        self.window = window
    
#END class BackButton
    
class PushButton(QtGui.QPushButton):
    def __init__(self):
        QtGui.QPushButton.__init__(self)
        self.inactivate()


    def setWindow(self, window):
        self.window = window
        
        
    def enterEvent(self, event):
        self.activate()
        try:
            return QtGui.QPushButton.enterEvent(self, event)
        except TypeError:
            pass

    def leaveEvent(self, event):
        self.inactivate()
        try:
            return QtGui.QPushButton.leaveEvent(self, event)
        except TypeError:
            pass

    def mousePressEvent(self, event):
        self.window.hide_customers()
        self.window.state = 'tasks'
        try:
            return QtGui.QPushButton.mousePressEvent(self, event)
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

#END class PushButton

app = QtGui.QApplication(sys.argv)
window = Window()


sys.exit(app.exec_())