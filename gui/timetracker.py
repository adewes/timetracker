#!/usr/bin/env python
# -*- coding: utf8 -*-
from PySide.QtGui import *
from PySide.QtCore import *
import sys
import math

class Task(object):
    
    def __init__(self,name):
        self._name = name
        
    @property
    def name(self):
        return self._name

    @name.setter
    def setName(self,name):
        self._name = name

class StatusWidget(QWidget):
    
    class NewItemEdit(QLineEdit):
        
        def __init__(self,parent = None):
            QLineEdit.__init__(self,parent)
        
        def reset(self):
            self.setText("")
            
    class StatusLabel(QLabel):
        
        def __init__(self,*args,**kwargs):
            QLabel.__init__(self,*args,**kwargs)
            self.setStyleSheet("background:#eeff00; padding:10px; padding-left:0")
                    
    
    def __init__(self,parent = None,*args,**kwargs):
        QWidget.__init__(self,parent,*args,**kwargs)
        self._mouseDown = False
        self._tasks = []
        self._tasks.append(Task("Test"))
        self._tasks.append(Task("Festplatte aufräumen"))
        self._taskWidgets = []
        self._stackedWidget = QStackedWidget()
        self._statusWidget = QWidget()
        self._emptyWidget = QWidget()
        self._stackedWidget.addWidget(self._statusWidget)
        self._stackedWidget.addWidget(self._emptyWidget)
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.newItemEdit = self.NewItemEdit()
        self.newItemEdit.setStyleSheet("border:1px solid #aaa;")
        self.connect(self.newItemEdit,SIGNAL("returnPressed()"),self.addItem)
        self.layout.addWidget(self.newItemEdit)
        self.layout.addItem(QSpacerItem(0,10))
        self._statusWidget.setLayout(self.layout)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.addWidget(self._stackedWidget)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.setFixedSize(20,20)
        self.setMinimumSize(0,0)
        self.setMaximumSize(1000,1000)
        self.setFixedWidth(300)
        self._stackedWidget.setCurrentWidget(self._statusWidget)
        self.updateGeometry()

    def addItem(self):
        print "Adding item: %s" % self.newItemEdit.text()
        label = self.StatusLabel(self.newItemEdit.text())
        self.layout.addWidget(label,0,0)
        self.newItemEdit.reset()
        
    def enterEvent(self,event):
        geometry = self.geometry()
        self.setMinimumSize(0,0)
        self.setMaximumSize(1000,1000)
        self.setFixedWidth(300)
        self._stackedWidget.setCurrentWidget(self._statusWidget)
        self.updateGeometry()
        newGeometry = self.geometry()
        print newGeometry
        self.move(geometry.bottomRight().x()-newGeometry.width()+1,geometry.bottomRight().y()-newGeometry.height()+1)
        self.update()
        event.accept()
    
    def leaveEvent(self,event):
        geometry = self.geometry()
        self._stackedWidget.setCurrentWidget(self._emptyWidget)
        self.setFixedSize(20,20)
        self.update()
        self.updateGeometry()
        self.ensurePolished()
        newGeometry = self.geometry()
        self.move(geometry.bottomRight().x()-newGeometry.width()+1,geometry.bottomRight().y()-newGeometry.height()+1)
        event.accept()

    def mousePressEvent(self,event):
        self._mouseDown = True
        self._dragPosition = event.globalPos()-self.frameGeometry().topLeft()
        
    def mouseReleaseEvent(self,event):
        self._mouseDown = False
    
    def mouseMoveEvent(self,event):
        print "move"
        if self._mouseDown:
            self.move(event.globalPos()-self._dragPosition)
    
def on_timeout():
    print QCursor.pos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont() 
    timer = QTimer()
    timer.setInterval(100)
    timer.start()
    timer.connect(SIGNAL("timeout()"),on_timeout)
    font.setFamily("Century Gothic")
    font.setPixelSize(20)
    app.setFont(font);
    # Create a Label and show it
    window = StatusWidget(None,Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    window.show()
    # Enter Qt application main loop
    app.exec_()
    sys.exit()