'''
    Manga Reader with PySide6 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import sys,re,requests,json,sqlite3

from PySide6.QtGui import QStandardItem,QStandardItemModel,QPixmap,QImage,QIcon,QMovie,QCloseEvent
from PySide6.QtCore import Qt,QObject,QThread,Signal,Slot
from PySide6.QtWidgets import *
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow
from bs4 import BeautifulSoup

DEFAULT_ANIME='Dragon Ball'

# internet is crucial for our app, if no internet exit program
def noInternet():
    try:
        r = requests.head('https://google.com', timeout=1)
        return False
    except :
        return True

# convert AnimE-2.0 Name to AnimE_20_Name (for server)
def codeName(name):
    return re.sub(' +', ' ',''.join(e for e in name if e.isalnum() or e==' ' or e=='-')).replace(' ','_').replace('-','_').lower()

# get image from data (from internet)
def PhotoImage(data):
    qimg=QImage()
    qimg.loadFromData(data)
    page = QLabel()
    page.setPixmap(QPixmap(qimg))
    return page

# Common Framework for All Threads
class WorkerSignals(QObject):
    progressed = Signal(object)
    finished = Signal()

# Our Image Loader Thread, sends signals to add image when loaded
class ImageLoader(QThread):
    def __init__(self,name,chapter,pages) -> None:
        super().__init__()
        self.pages=pages
        self.name=name
        self.chapter=chapter
        self.killThread=False
        self.signals=WorkerSignals()

    @Slot(None,result=None)
    def run(self):
        for i in range(self.pages):
            if self.killThread:
                # print('THREAD KILLED')
                return
            data=requests.get(
                f'https://images.mangafreak.net/mangas/{self.name}/{self.name}_{self.chapter}/{self.name}_{self.chapter}_{i+1}.jpg'
            ).content
            self.signals.progressed.emit(data)
        self.signals.finished.emit()

    def stop(self):
        self.killThread=True
        self.wait()

# Framework to interact with database
class AnimeDB():
    def __init__(self):
        self.conn = sqlite3.connect("animelist.db")
        self.cursor = self.conn.cursor()
        if not self.dbExists(): 
            self.createAnimeDB()
        if not self.recordExists():
            self.addAnime(DEFAULT_ANIME)
    def dbExists(self):
        rows = self.cursor.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='anime'; """).fetchall()
        return len(rows) != 0
    def recordExists(self):
        return len(self.getAnimeList())!=0
    def createAnimeDB(self):
        self.cursor.execute("CREATE TABLE anime (name TEXT, chapters TEXT)")
    def getAnimeList(self):
        return self.cursor.execute("SELECT * FROM anime").fetchall()
    def animeExist(self,name):
        return len(self.getAnime(name))!=0
    def getAnime(self,name):
        return self.cursor.execute(f"SELECT * FROM anime WHERE name='{name}'").fetchall()
    def getChapterList(self,name):
        return self.getAnime(name)[0][1]
    def updateChapterList(self,name,chapters):
        chapters=json.dumps(chapters)
        self.cursor.execute(f"UPDATE anime SET chapters='{chapters}' WHERE name='{name}'").fetchall()
        self.conn.commit()
    # magical function to add anime ; just enter name like Dragon Ball
    def addAnime(self,name):
        if self.animeExist(name): # prevent duplicate entries
            return
        chapters=json.dumps(self.getChapters(name))
        # print('Adding Anime to Database')
        self.cursor.execute(f"INSERT INTO anime VALUES ('{name}', '{chapters}')")
        self.conn.commit()
        return chapters
    def getChapters(self,name):
        chapters={}
        name=codeName(name) # Anime Name to anime_name
        response=requests.get(f"https://w13.mangafreak.net/Manga/{name}")
        soup=BeautifulSoup(response.content,'html.parser')
        a=soup.find(name="div",class_="manga_series_list")
        for i in a.find_all('tr'):
            chapter=re.findall("[0-9]+",i.find('a').text)[0]
            # sometimes chapter names can be like 1a, 1b which are mostly irrelevant
            if chapter not in chapters:
                chapters[chapter]=0 # 0 means yet to be calculated
        return chapters
    def getPages(self,name,chapter):
        name=codeName(name) # Anime Name to anime_name
        response=requests.get(f"https://w13.mangafreak.net/Read1_{name}_{chapter}")
        soup=BeautifulSoup(response.content,'html.parser')
        div=soup.find('div',{'class':'read_selector'}) # no of pages in chapter
        return re.findall("[0-9]+",div.contents[2])[0] 
    # check if anime exists on server
    def checkAnime(self,name):
        name=codeName(name) # Anime Name to anime_name
        response=requests.get(f"https://w13.mangafreak.net/Manga/{name}",allow_redirects=False)
        return response.status_code==200

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if noInternet():
            QMessageBox.critical(self,'Error','No Internet Connection!')
            quit()

        self.setWindowTitle("Manga Reader")
        self.setWindowIcon(QIcon('icon.ico'))
        self.db=AnimeDB()

        self.treeModel = QStandardItemModel()
        addBtn = QPushButton('Add Anime')
        
        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeView.setModel(self.treeModel)
        self.animeList = self.db.getAnimeList()

        # SET TREE VIEW
        for row in self.animeList:
            self.treeAddAnime(row[0],row[1])

        self.treeView.expand(self.treeModel.indexFromItem(self.treeModel.item(0,0))) # Expand first node
        self.treeView.doubleClicked.connect(self.treeDoubleClicked)
        treeLayout = QVBoxLayout()
        treeLayout.addWidget(self.treeView)
        treeLayout.addWidget(addBtn)
        treeFrame = QFrame()
        treeFrame.setLayout(treeLayout)
        self.anime=QDockWidget('Anime',self)
        self.anime.setWidget(treeFrame)
        self.anime.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.anime)
        addBtn.clicked.connect(self.addAnimeClicked)
        self.setAnime()

    # first show buffering then load anime as per requirement
    def setAnime(self,name=DEFAULT_ANIME,chapter=None,pages=0):
        self.loading = True # is anime being loaded? 
        self.scrollArea = QScrollArea(self)
        self.frame = QFrame()
        self.layout = QVBoxLayout()
        if pages<=0: # pages not calculated
            chapters=json.loads(self.db.getChapterList(name))
            if chapter is None:
                chapter=next(iter(chapters)) # get first chapter available
            pages=int(self.db.getPages(name,chapter))
            chapters[chapter]=pages
            self.db.updateChapterList(name,chapters)
        
        name = codeName(name) # Anime Name to anime_name

        buffering = QLabel()
        buffering.setStyleSheet('background:none')
        movie=QMovie('buffering.gif' )
        buffering.setMovie(movie)
        movie.start()

        self.layout.addWidget(buffering,0,Qt.AlignCenter)

        self.frame.setLayout(self.layout)
        self.scrollArea.setWidget(self.frame)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.scrollArea)

        # load images via thread
        self.imgLoader=ImageLoader(name,chapter,pages)
        self.imgLoader.signals.finished.connect(self.onPageLoad)
        self.imgLoader.signals.finished.connect(buffering.deleteLater)
        self.imgLoader.signals.progressed.connect(self.updatePage)
        self.imgLoader.start()
    
    def updatePage(self,data):
        # add last second widget (last is always buffering)
        self.layout.insertWidget(self.layout.count()-1,PhotoImage(data),0,Qt.AlignCenter)
        self.scrollArea.widget().adjustSize()

    def onPageLoad(self):
        self.loading=False

    def treeDoubleClicked(self,index):
        if self.loading: 
            self.imgLoader.stop()
            self.loading=False
            return # TODO figure a way to stop threads immediately without using return
        clickedItem=self.treeView.selectedIndexes()[0].model().itemFromIndex(index)
        if clickedItem.anime: # is a chapter
            self.setAnime(clickedItem.anime,re.findall("[0-9]+",clickedItem.text())[0],clickedItem.pages)
        else: # is an anime itself
            self.setAnime(clickedItem.text(),1,clickedItem.pages)

    def treeAddAnime(self,name,chapters):
        parent = QStandardItem(name) # anime name
        parent.setEditable(False)
        chapters=json.loads(chapters)
        parent.anime = None # chapters have anime, anime doesn't have anime xD
        parent.pages = next(iter(chapters)) # get first chapter available
        for j in chapters:
            child = QStandardItem(f'Chapter {j}')
            child.anime = name # data variable; will come in use later
            child.pages = chapters[j]
            child.setEditable(False)
            parent.appendRow(child)
        self.treeModel.appendRow(parent)

    def addAnimeClicked(self):
        name, ok = QInputDialog.getText(self, 'Add Anime', 'Anime Name:')
        if name and ok:
            if self.db.checkAnime(name):
                chapters=self.db.addAnime(name)
                self.treeAddAnime(name,chapters)
            else:
                QMessageBox.critical(self,'Error',f"Anime '{name}' not found on server!")
                
    def closeEvent(self, event: QCloseEvent) -> None:
        self.imgLoader.stop()
        return super().closeEvent(event)



if __name__=='__main__':
    app=QApplication(sys.argv)
    dark(app)
    win=ModernWindow(MainWindow())
    win.setWindowIcon(QIcon('icon.ico'))
    win.show()
    sys.exit(app.exec_())