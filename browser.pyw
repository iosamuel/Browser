#!/usr/bin/python
#-*- coding:ISO-8859-1 -*-

import sys
from PySide import QtGui, QtCore, QtWebKit

class Browser(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.setWindowTitle("Navegador BroWeb")
		
		self.statusBar().showMessage("Listo", 5000)

		self.progress = 0
		self.homeURL = "http://www.google.com/"

		self.view = QtWebKit.QWebView(self)
		self.view.load(QtCore.QUrl(self.homeURL))
		self.view.loadProgress.connect(self.setProgress)
		self.view.titleChanged.connect(self.setTextProgress)
		self.view.loadFinished.connect(self.adjustLocation)
		self.view.loadFinished.connect(self.finishLoading)

		self.urlEdit = QtGui.QLineEdit(self)
		self.urlEdit.returnPressed.connect(self.chLocation)

		toolbar = self.addToolBar("Navegacion")
		toolbar.addAction(self.view.pageAction(QtWebKit.QWebPage.Back))
		toolbar.addAction(self.view.pageAction(QtWebKit.QWebPage.Forward))
		toolbar.addWidget(self.urlEdit)
		toolbar.addAction(self.view.pageAction(QtWebKit.QWebPage.Reload))
		toolbar.addAction(self.view.pageAction(QtWebKit.QWebPage.Stop))

		closeAction = QtGui.QAction("&Salir", self)
		aboutAction = QtGui.QAction("&Acerca", self)
		closeAction.triggered.connect(self.close)
		aboutAction.triggered.connect(self.aboutMess)

		menubar = QtGui.QMenuBar()
		fileMenu = QtGui.QMenu("&Archivo")
		helpMenu = QtGui.QMenu("A&yuda")
		fileMenu.addAction(closeAction)
		helpMenu.addAction(aboutAction)
		menubar.addMenu(fileMenu)
		menubar.addMenu(helpMenu)
		self.setMenuBar(menubar)

		self.setCentralWidget(self.view)
	
	def aboutMess(self):
		QtGui.QMessageBox.information(self, "Acerca de BroWeb",
		                              "Este es un navegador web sencillo.\nVisita: http://samuelbr.com/",
		                              QtGui.QMessageBox.Ok)

	def setProgress(self, n):
		self.progress = n
		self.setTextProgress()
		self.adjustLocation()
	
	def setTextProgress(self):
		if 0 < self.progress < 100:
			self.setWindowTitle( "%s - BroWeb" % (self.view.title()) )
			self.statusBar().showMessage( "%s (%s%%)" % (self.view.url().toString(), self.progress) )
		else:
			self.setWindowTitle( "%s - BroWeb" % (self.view.title()) )
			self.statusBar().showMessage("Terminado")
	
	def adjustLocation(self):
		self.urlEdit.setText(self.view.url().toString())
		self.urlEdit.setCursorPosition(0)
	
	def finishLoading(self):
		self.progress = 100
		self.setTextProgress()
		self.adjustLocation()
	
	def chLocation(self):
		url = QtCore.QUrl.fromUserInput(self.urlEdit.text())
		self.view.load(url)
		self.view.setFocus()

app = QtGui.QApplication(sys.argv)
b = Browser()
b.showMaximized()
sys.exit(app.exec_())
