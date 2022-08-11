from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from html.parser import HTMLParser as Parser
from bs4 import BeautifulSoup
import webbrowser
import qdarktheme
import sys
import re
import os


# Single Line HTML Parser
class HTMLParser(Parser):
    def __init__(self):
        super().__init__()
        self.resetValues()

    def resetValues(self):
        self.isComment = False
        self.tagPos = 0
        self.attr = []
        self.val = []

    def parseLine(self,data):
        self.resetValues()
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        self.tagPos = self.getpos()[1]+len(tag)
        pos = self.tagPos
        for a in attrs:
            self.attr.append(a[0])
            self.val.append(a[1])
        
    def handle_comment(self, data):
        self.isComment = True


class HTMLHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parser = HTMLParser()
        self.tagFMT = QTextCharFormat()
        self.tagFMT.setForeground(QBrush(QColor('#219ebc')))
        self.tagFMT.setFontCapitalization(True)
        self.tagFMT.setFontWeight(QFont.Bold)

        self.attrFMT = QTextCharFormat()
        self.attrFMT.setForeground(QBrush(QColor('#f72585')))
        # attrFMT.setFontCapitalization(False)
        # self.attrFMT.setFontWeight(QFont.Bold)
        # 
        self.valFMT = QTextCharFormat()
        self.valFMT.setForeground(QBrush(QColor('#FF7F50')))

        self.commentFMT = QTextCharFormat()
        self.commentFMT.setForeground(QBrush(QColor('#008000')))
        self.commentFMT.setFontItalic(True)

    def highlightBlock(self, text_block):
        for match in re.finditer(r'<[^>]+>', text_block):
            i=0
            start, end = match.span()
            line = match.group().replace('\n',' ')
            self.parser.parseLine(line)
            if self.parser.isComment:
                self.setFormat(start, end - start, self.commentFMT) #<html
            else:
                # if no attributes then simply set
                temp = line[1:-1].strip()
                if ' ' not in temp or temp.lower()=='!doctype html':
                    self.setFormat(start, end - start, self.tagFMT)
                else:
                    self.setFormat(start, self.parser.tagPos - start, self.tagFMT) 
                    for i in  self.parser.attr:
                        self.setFormat(start+line.find(i), len(i), self.attrFMT) 
                    for i in  self.parser.val:
                        if i is not None:
                            self.setFormat(start+line.find(i), len(i), self.valFMT) 
                    self.setFormat(end-1, 1, self.tagFMT) # >
                        


class HTMLEditor(QMainWindow):
    def __init__(self):
        super(HTMLEditor, self).__init__()
        self.setWindowTitle("HTML Editor")
        self.setWindowIcon(QIcon("html5.png"))
        self.savePath = None
        self.darkTheme = True

        newFile = QAction(QIcon('icons/notebook.png'), "New", self)
        openFile = QAction(QIcon('icons/open.png'), "Open", self)
        saveFile = QAction(QIcon('icons/save.png'), "Save", self)
        saveFileAs = QAction(QIcon('icons/saveAs.png'), "Save As", self)
        printFile = QAction(QIcon('icons/printer.png'), "Print", self)
        prettify = QAction(QIcon('icons/wand.png'), "Prettify", self)
        switchTheme = QAction(QIcon('icons/theme.png'), "Switch Theme", self)
        preview = QAction(QIcon('icons/run.png'), "Preview", self)
        runInBrowser = QAction(QIcon('icons/application-browser.png'), "Run in Browser", self)
        self.autoLoad = QCheckBox('Auto-reload', self)

        toolBar = self.addToolBar('Navigation')
        toolBar.setIconSize(QSize(16, 16))
        toolBar.addAction(newFile)
        toolBar.addAction(openFile)
        toolBar.addAction(saveFile)
        toolBar.addAction(saveFileAs)
        toolBar.addAction(printFile)
        toolBar.addAction(prettify)
        toolBar.addAction(switchTheme)
        toolBar.addAction(preview)
        toolBar.addAction(runInBrowser)
        toolBar.addSeparator()
        toolBar.addWidget(self.autoLoad)
        toolBar.setMovable(False)

        self.editor = QTextEdit()
        self.editor.setStyleSheet("border:none;padding:10px;font: 16px monospace")
        self.editor.setAcceptRichText(False)
        self.editor.setMinimumWidth(100)
        self.setCentralWidget(self.editor)
        # self.items.setFloating(True)
        self.highlighter=HTMLHighlighter()
        self.highlighter.setDocument(self.editor.document())

        self.viewer = QDockWidget("HTML Output", self)
        self.webview = QWebEngineView()
        self.webview.titleChanged.connect(lambda: self.viewer.setWindowTitle(self.webview.title()))
        self.viewer.setWidget(self.webview)

        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer)

        newFile.triggered.connect(self.newFile)
        openFile.triggered.connect(self.openFile)
        saveFile.triggered.connect(self.saveFile)
        saveFileAs.triggered.connect(self.saveFileAs)
        printFile.triggered.connect(self.printFile)
        prettify.triggered.connect(self.prettify)
        switchTheme.triggered.connect(self.switchTheme)
        preview.triggered.connect(self.preview)
        runInBrowser.triggered.connect(self.openBrowser)

        self.editor.textChanged.connect(lambda: self.autoLoad.isChecked() and self.preview())

        self.setExample()
        self.preview()
        self.updateTitle()

    def preview(self):
        self.webview.setHtml(self.editor.toPlainText(),QUrl(self.savePath or (QDir.currentPath()+'/')))

    def prettify(self):
        soup = BeautifulSoup(self.editor.toPlainText(),'html.parser')
        self.editor.setPlainText(soup.prettify())

    def switchTheme(self):
        self.darkTheme = not self.darkTheme
        self.setStyleSheet(qdarktheme.load_stylesheet(self.darkTheme and 'dark' or 'light'))

    def openBrowser(self):
        if not self.savePath:
            self.saveFileAs()
        if self.savePath:
            webbrowser.open(self.savePath)

    def newFile(self):
        self.savePath = None
        self.editor.setPlainText('')
        self.preview()
        self.updateTitle()

    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "HTML File (*.htm *.html);;"
                                                  "All files (*.*)")

        if path:
            with open(path, 'r') as f:
                html = f.read()
            self.savePath=path
            self.editor.setPlainText(html)
            self.preview()
            self.updateTitle()

    def saveFile(self):
        if not self.savePath:
            return self.saveFileAs()
        html = self.editor.toPlainText()
        with open(self.savePath, 'w') as f:
            f.write(html)
        self.preview()
        self.updateTitle()

    def saveFileAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File As", "",
                                                  "HTML File (*html *.htm);;"
                                                  "All files (*.*)")

        if filename:
            self.savePath=filename
            self.saveFile()

    def printFile(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def updateTitle(self):
        self.setWindowTitle(f"{(os.path.basename(self.savePath) if self.savePath else 'Untitled')} - HTML Editor")

    def setExample(self):
        self.editor.setPlainText("<!--Example HTML Code-->\n"
        "<!DOCTYPE html>\n"
        "<HTML>\n"
        "   <HEAD>\n"
        "      <title>Example</title>\n"
        "   </HEAD>\n"
        '   <BODY bgcolor = "lightblue">\n'
        '      <P align = "center">\n'
        "         HTML EDITOR<BR/>\n"
        '         <IMG src = "html5.png" alt = "Test Image" />\n'
        '      </P>\n'
        '   </BODY>\n'
        "</HTML>\n")

if __name__ == "__main__":
    sys.argv.append("--disable-web-security")
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    main = HTMLEditor()
    main.show()
    sys.exit(app.exec_())
