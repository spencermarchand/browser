# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import os
import sys

class BookMarkToolBar(QtWidgets.QToolBar):
    bookmarkClicked = QtCore.pyqtSignal(QtCore.QUrl, str)

    def __init__(self, parent=None):
        super(BookMarkToolBar, self).__init__(parent)
        self.actionTriggered.connect(self.onActionTriggered)
        self.bookmark_list = []

    def setBookMarks(self, bookmarks):
        for bookmark in bookmarks:
            self.addBookMarkAction(bookmark["title"], bookmark["url"])

    def addBookMarkAction(self, title, url):
        bookmark = {"title": title, "url": url}
        fm = QtGui.QFontMetrics(self.font())
        if bookmark not in self.bookmark_list:
            text = fm.elidedText(title, QtCore.Qt.ElideRight, 150)
            action = self.addAction(text)
            action.setData(bookmark)
            self.bookmark_list.append(bookmark)

    @QtCore.pyqtSlot(QtWidgets.QAction)
    def onActionTriggered(self, action):
        bookmark = action.data()
        self.bookmarkClicked.emit(bookmark["url"], bookmark["title"])

# creating main window class
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
    
        window = QMainWindow()
        window.setWindowTitle("Toolbar Example")
        window.resize(400, 300)
        
        #Create a QtabWidget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True) #This is to make the tabs look like normal tabs
        self.tabs.setTabsClosable(True) #This is to make the tabs closable


        #adding action when the tab is changed
        self.tabs.currentChanged.connect(self.currentTabChanged)

        #adding action when the tab is closed
        self.tabs.tabCloseRequested.connect(self.closeCurrentTab)

        #create status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        #set the tabs as the central widget
        navigationBar = QToolBar('Navigation')
        self.addToolBar(navigationBar)


        #set the tabs as the central widget
        self.setCentralWidget(self.tabs)

        #adding action to the navigation bar
        backButton = QAction('Back', self)
        backButton.setStatusTip('Back to previous page')
        backButton.triggered.connect(lambda: self.tabs.currentWidget().back())
        navigationBar.addAction(backButton)

        #adding forward button to the navigation bar
        forwardButton = QAction('Forward', self)
        forwardButton.setStatusTip('Forward to next page')
        forwardButton.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navigationBar.addAction(forwardButton)

        #adding reload button to the navigation bar
        reloadButton = QAction('Reload', self)
        reloadButton.setStatusTip('Reload page')
        reloadButton.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navigationBar.addAction(reloadButton)
        self.reloadButtonShortcut = QShortcut(QKeySequence("Ctrl+r"), self)
        self.reloadButtonShortcut.activated.connect(lambda: self.tabs.currentWidget().reload())


        #adding home button to the navigation bar
        homeButton = QAction('Home', self)
        homeButton.setStatusTip('Go home')
        homeButton.triggered.connect(self.navigate_home)
        navigationBar.addAction(homeButton)
        self.HomeButtonShortcut = QShortcut(QKeySequence("Ctrl+h"), self)
        self.HomeButtonShortcut.activated.connect(self.navigate_home)
        
        #adding new tab button to the navigation bar
        newtabButton = QAction('New Tab', self)
        newtabButton.setStatusTip('Open a new tab')
        newtabButton.triggered.connect(self.addNewTabFromButton)
        navigationBar.addAction(newtabButton)
        self.newTabShortcut = QShortcut(QKeySequence("Ctrl+t"), self)
        self.newTabShortcut.activated.connect(self.addNewTabFromButton)

        
        #adding stop button to the navigation bar
        stopButton = QAction('Stop', self)
        stopButton.setStatusTip('Stop loading current page')
        stopButton.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navigationBar.addAction(stopButton)

        navigationBar.addSeparator()

        #adding a search bar to the navigation bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigationBar.addWidget(self.urlbar)

        #adding a search button to the navigation bar
        searchButton = QAction('Search', self)
        searchButton.setStatusTip('Search')
        searchButton.triggered.connect(self.navigate_to_url)
        navigationBar.addAction(searchButton)
        

        #adding a bookmark button to the navigation bar
        bookmarkButton = QAction('Bookmark', self)
        bookmarkButton.setStatusTip('Bookmark')
        bookmarkButton.triggered.connect(self.addFavoriteClicked)
        navigationBar.addAction(bookmarkButton)
        self.BookMarkshortcut = QShortcut(QKeySequence("Ctrl+b"), self)
        self.BookMarkshortcut.activated.connect(self.addFavoriteClicked)

        #adding a bookmark toolbar
        self.addToolBarBreak()
        self.bookmarkToolbar = BookMarkToolBar()
        self.bookmarkToolbar.bookmarkClicked.connect(self.addNewTab)
        self.addToolBar(self.bookmarkToolbar)
        #self.readSettings()
        self.bookmarkToolbar.addBookMarkAction("Google", QtCore.QUrl("http://www.google.com"))
        self.bookmarkToolbar.addBookMarkAction("Youtube", QtCore.QUrl("http://www.youtube.com"))
        self.bookmarkToolbar.addBookMarkAction("Reddit", QtCore.QUrl("http://www.reddit.com"))
        self.bookmarkToolbar.addBookMarkAction("Facebook", QtCore.QUrl("http://www.facebook.com"))
        self.bookmarkToolbar.addBookMarkAction("Twitter", QtCore.QUrl("http://www.twitter.com"))
        self.bookmarkToolbar.addBookMarkAction("Spencer's Github", QtCore.QUrl("https://github.com/spencermarchand?tab=overview&from=2023-04-01&to=2023-04-30"))
        self.bookmarkToolbar.addBookMarkAction("Instagram", QtCore.QUrl("http://www.instagram.com"))
        self.bookmarkToolbar.addBookMarkAction("StackOverflow", QtCore.QUrl("http://www.stackoverflow.com"))
        self.bookmarkToolbar.addBookMarkAction("Wikipedia", QtCore.QUrl("http://www.wikipedia.com"))
        self.bookmarkToolbar.addBookMarkAction("Spencer's LinkedIn", QtCore.QUrl("https://www.linkedin.com/in/spencer-marchand/"))

    def addFavoriteClicked(self):
        loop = QtCore.QEventLoop()

        def callback(resp):
            setattr(self, "title", resp)
            loop.quit()

        web_browser = self.tabs.currentWidget()
        web_browser.page().runJavaScript("(function() { return document.title;})();", callback)
        url = web_browser.url()
        loop.exec_()
        self.bookmarkToolbar.addBookMarkAction(getattr(self, "title"), url)

    # def readSettings(self):
    #     setting = QtCore.QSettings()
    #     self.defaultUrl = setting.value("defaultUrl", QtCore.QUrl('http://www.google.com'))
    #     self.addNewTab(self.defaultUrl, 'Home Page')
    #     self.bookmarkToolbar.setBookMarks(setting.value("bookmarks", []))
    
    # def saveSettins(self):
    #     settings = QtCore.QSettings()
    #     settings.setValue("defaultUrl", self.defaultUrl)
    #     settings.setValue("bookmarks", self.bookmarkToolbar.bookmark_list)
    
    def closeEvent(self, event):
        self.saveSettins()
        super(MainWindow, self).closeEvent(event)


    def addNewTabFromButton(self):
        label = 'Google'
        qurl = QUrl('http://www.google.com')
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser = browser: self.updateURL_Bar(qurl, browser))
        browser.loadFinished.connect(lambda _, i = i, browser = browser: self.tabs.setTabText(i, browser.page().title()))


    def addNewTab(self, qurl = None, label = "Blank"):

        if qurl is None:
            qurl = QUrl('http://www.google.com')
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        global i
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser = browser: self.updateURL_Bar(qurl, browser))
        browser.loadFinished.connect(lambda _, i = i, browser = browser: self.tabs.setTabText(i, browser.page().title()))
    
        
    def currentTabChanged(self, i):

        qurl = self.tabs.currentWidget().url()
        self.updateURL_Bar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def closeCurrentTab(self, i):
            
            if self.tabs.count() < 2:
                return
            
            self.tabs.removeTab(i)
        
    def update_title(self, browser):
            
            if browser != self.tabs.currentWidget():
                return
            
            title = self.tabs.currentWidget().page().title()
            self.setWindowTitle(str(title))
    


    def navigate_home(self):

        self.tabs.currentWidget().setUrl(QUrl('http://www.google.com'))
        

    def navigate_to_url(self):
         
        q = QUrl(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme('http')

        self.tabs.currentWidget().setUrl(q)
    
    def updateURL_Bar(self, q, browser = None):
         
        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())

        self.urlbar.setCursorPosition(0)

if __name__ == '__main__':
         
    app = QApplication(sys.argv)
    app.setApplicationName("Browser")

    window = MainWindow()

    window.showMaximized()

    window.addNewTab()

    app.exec_()

    