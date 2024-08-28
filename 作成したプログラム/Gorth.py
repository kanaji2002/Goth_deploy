import sys
import os
import re
import asyncio
import aiohttp
import threading
import xml.etree.ElementTree as ET
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import QWebEngineProfile
import yt_dlp

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QPoint


#類似度を計算するためのモジュール
from difflib import SequenceMatcher

# htmlからpyhonにデータを渡すためのモジュール
from PySide6.QtWebChannel import QWebChannel
import sys

#音楽を再生するためのモジュール
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class LinkHandler(QObject):
    @Slot(str,str)
    def handleLinkClick(self, url,name):
        print(f"Link clicked: URL={url}, Name={name}")
        # Add a new tab with the clicked URL
        # window.add_new_tab()
        url = QUrl(url)
        window.add_pin_stop(url, name)
        window.add_new_tab(url, "New Tab")

# リソースパスを解決する関数を追加
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QMainWindow):
    # tab_id_title_list = []
    # tab_id_title_list.append({'id': 0, 'title': 'Home'})
    
    tab_id_title_list=[
            {'id': 0, 'title': 'Home'}
        ]

    ## ここに，3Dモデルを格納するオブジェクトを追加する．
    
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.handler = LinkHandler()
        self.vertical_bar = QToolBar("Vertical Bar")
        self.vertical_bar.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.vertical_bar)
        self.tabs = QTabWidget(self)
        self.vertical_bar.setFixedWidth(150)
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.resize(960, 540)
        

        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        self.setup_shortcuts()

    

           # ボタンを作成してタブバーの右上に配置
        self.add_tab_button = QPushButton("newタブ")
        self.add_new_tab(QUrl('https://kanaji2002.github.io/Goth-toppage/top_page.html'), 'Homepage')
        # self.showMaximized()
        # ボタンがクリックされたときに、新しいタブを開くように設定
        self.add_tab_button.clicked.connect(lambda: self.add_new_tab())
        #self.add_tab_button.clicked.connect(self.add_new_tab())



        self.add_tab_button.setStyleSheet("background-color: white; color: black;")
        
        self.tabs.setCornerWidget(self.add_tab_button, Qt.TopRightCorner)
        
      
        #self.add_tab_button.setStyleSheet("background-color: gray; color: white;")
        # ボタンがクリックされたときに、新しいタブを開くように設定
        self.add_tab_button.clicked.connect(self.add_new_tab)


        
        self.tabs.tabCloseRequested.connect(self.close_tab)

        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        print(self.status)
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)
        self.load_shortcuts()
        # アプリケーションの起動時にピン留めされたショートカットをロード
        self.load_shortcuts_pin()

        back_btn = QAction("<", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)
        next_btn = QAction(">", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
        reload_btn = QAction("○", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        self.toolbar = QToolBar("Actions")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.star_button = QAction("☆", self)
        self.star_button.setStatusTip("Add shortcut to vertical bar")
        self.star_button.setCheckable(True)  # チェック可能に設定
        self.star_button.triggered.connect(self.toggle_star)
        self.toolbar.addAction(self.star_button)

        self.cl_cache_button = QAction("cache", self)
        self.cl_cache_button.setStatusTip("clear cache")
        self.cl_cache_button.triggered.connect(self.clear_cache)
        self.toolbar.addAction(self.cl_cache_button)
       
        self.room2 = QAction("room2", self)
        self.room2.setStatusTip("go to room2")
        self.room2.triggered.connect(lambda: self.add_new_tab(QUrl('https://kanaji2002.github.io/Goth-toppage/room2.html')))
        self.toolbar.addAction(self.room2)

        self.room3 = QAction("room3", self)
        self.room3.setStatusTip("go to room3")
        self.room3.triggered.connect(lambda: self.add_new_tab(QUrl('https://kanaji2002.github.io/Goth-toppage/room3.html')))
        self.toolbar.addAction(self.room3)

        self.room4 = QAction("room4", self)
        self.room4.setStatusTip("go to room4")
        self.room4.triggered.connect(lambda: self.add_new_tab(QUrl('https://kanaji2002.github.io/Goth-toppage/room4.html')))
        self.toolbar.addAction(self.room4)

        self.room5 = QAction("room5", self)
        self.room5.setStatusTip("go to room5")
        self.room5.triggered.connect(lambda: self.add_new_tab(QUrl('https://kanaji2002.github.io/Goth-toppage/room5.html')))
        self.toolbar.addAction(self.room5)

        self.room6 = QAction("room6", self)
        self.room6.setStatusTip("go to room6")
        self.room6.triggered.connect(lambda: self.add_new_tab(QUrl('https://kanaji2002.github.io/Goth-toppage/room6.html')))
        self.toolbar.addAction(self.room6)

        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        # self.play_button = QAction("Play music")
        # self.play_button.setIcon(QIcon("parts/saisei.png"))
        # self.play_button.setStatusTip("play music")
        # self.play_button.triggered.connect(self.toggle_music)
        # #self.play_button.clicked.connect(self.toggle_music)
        # self.toolbar.addAction(self.play_button)


        ## 実行ファイル用のリソースパスを解決する関数を追加
        # 修正: リソースパス関数を使用して画像のパスを取得
        self.play_button = QAction("Play music")
        self.play_button.setIcon(QIcon(resource_path("parts/saisei.png")))
        self.play_button.setStatusTip("play music")
        self.play_button.triggered.connect(self.toggle_music)
        self.toolbar.addAction(self.play_button)

   


        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
        navtb.addSeparator()
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        # QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_downloadRequested)
        stop_btn = QAction("X", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
        # self.add_new_tab(QUrl('https://kanaji2002.github.io/Goth-toppage/top_page.html'), 'Homepage')
        self.delete_bookmark = QToolBar("delete bookmark")
        self.delete_bookmark.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.delete_bookmark)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        self.setWindowTitle("")
        self.setStyleSheet("background-color: gray; color: white;")  # 背景色を黒に変更
        self.tabs.setStyleSheet("QTabBar::tab { color: white; }")



        # ウィンドウアイコンの設定（アイコンファイルのパスを指定）
        self.setWindowIcon(QIcon("parts/icon.ico"))
        

        
       
        """ initialize 終わり """


    def toggle_music(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setIcon(QIcon("parts/saisei.png"))
        else:
            # 音楽ファイルのURLを設定（ローカルファイルの場合は "file:///フルパス" の形式で指定）
            self.player.setSource(QUrl("https://kanaji2002.github.io/Goth-toppage/mititeyuku_free.mp3"))
            self.player.play()
            self.play_button.setIcon(QIcon("parts/stop.png"))



    
    def close_tab(self, i):
        
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

        
        print ("-------close_tab end--------")
        print(f"Current tab list: {self.tab_id_title_list}")

    def setup_shortcuts(self):
        # Ctrl+W で現在のタブを閉じる
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)

        # Ctrl+r で現在のタブ＋次（右隣り）を閉じる(右隣りがないときはそのタブだけを閉じる)
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+r"), self)
        close_tab_shortcut.activated.connect(self.close_two_tab)

        # Ctrl+Space で現在のタブを閉じる
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+Space"), self)
        close_tab_shortcut.activated.connect(self.close_related_tab)

        # Ctrl+T で新しいタブを開く
        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+t"), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)
        # self.add_tab_button.clicked.connect(lambda: self.add_new_tab(qurl=None, label="ブランク"))

        # Ctrl+Q でアプリケーションを終了する
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)

        # Alt+LeftArrow で前のタブに移動する
        prev_tab_shortcut = QShortcut(QKeySequence(Qt.ALT | Qt.Key_Left), self)
        prev_tab_shortcut.activated.connect(self.prev_tab)

        # Alt+RightArrow で次のタブに移動する
        next_tab_shortcut = QShortcut(QKeySequence(Qt.ALT | Qt.Key_Right), self)
        next_tab_shortcut.activated.connect(self.next_tab)

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.tabs.removeTab(current_index)

    def close_two_tab(self):
        
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.tabs.removeTab(current_index)
            self.tabs.removeTab(current_index)
            
            
    def close_related_tab(self):
            print(f'現在格納されているリストは，{self.tab_id_title_list}')
            current_index = self.tabs.currentIndex()
            delete_tab_index_list = []

            if current_index != -1 and self.tabs.count() > 1:
                print(f'現在のタブは{current_index}')   
                print(f'現在のタブの数は{self.tabs.count()}')

                tem_list=self.tab_id_title_list
                tem=tem_list[current_index]['title']
                print(f'現在のタブのtitleは{tem}')


                for i in range(len(self.tab_id_title_list)):
                    s = SequenceMatcher(None, self.tab_id_title_list[current_index]['title'], self.tab_id_title_list[i]['title'])
                    # if s.ratio() > 0 and i!=current_index:
                    #     print('類似度：{0}%，{1}.tabのIDは，{2}です．'.format(round(s.ratio()*100,1), self.tab_id_title_list[i]['title'],i))
                    #     delete_tab_index_list.append(i)

                    # current_tabも削除対象に含めル．つまり，類似度は　100%でOK
                    print('tabのID{0}の類似度：{1}%.タイトルは，{2}です．'.format(i,round(s.ratio()*100,1), self.tab_id_title_list[i]['title']))
                    if s.ratio() > 0.8 :
                        delete_tab_index_list.append(i)
                    print(f'削除対象のタブは，{delete_tab_index_list}')


                    # 関連するタブのindexをリストに追加していき，最後に，まとめて削除
                for i in reversed(delete_tab_index_list):
                    if self.tabs.count() > 1:
                        print(f'{i}番目のタブを削除します.タイトルは，{self.tab_id_title_list[i]["title"]}です．')
                        self.tabs.removeTab(i)
                        delete_tab_index_list.remove(i)
            print ("-------close_related_tab end--------")
            print(f"Current tab list: {self.tab_id_title_list}")
                

    def prev_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index > 0:
            self.tabs.setCurrentIndex(current_index - 1)

    def next_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index < self.tabs.count() - 1:
            self.tabs.setCurrentIndex(current_index + 1)

    def clear_cache(self):
        profile = QWebEngineProfile.defaultProfile()
        
        profile.clearHttpCache()  # HTTPキャッシュをクリア
        print("HTTPキャッシュがクリアされました。")
        
        # すべてのクッキーを削除
        cookie_store = profile.cookieStore()
        cookie_store.deleteAllCookies()
        print("すべてのクッキーが削除されました。")
        
        profile.clearAllVisitedLinks()  # すべての訪問リンクをクリア
        print("すべての訪問リンクがクリアされました。")
        
       

    def add_new_tab(self, qurl=None, label="ブランク"):
        profile = QWebEngineProfile.defaultProfile()
        # profile.clearHttpCache()  # HTTPキャッシュをクリア  


        self.update_star_icon()
        if qurl is None:
            qurl = QUrl('https://kanaji2002.github.io/Goth-toppage/room2.html')    
        elif isinstance(qurl, str):
            qurl = QUrl(qurl)  # 文字列からQUrlに変換する

        browser = QWebEngineView()
       
        # WebChannelを設定する
        channel = QWebChannel()  # 新しいチャンネルを作成
        handler = LinkHandler()  # 新しいハンドラを作成
        channel.registerObject("linkHandler", handler)
        browser.page().setWebChannel(channel)  # 新しいブラウザページにチャンネルを設定


        # ページのロードが完了したら、JavaScriptコードをインジェクトしてWebChannelを設定する
        browser.page().loadFinished.connect(lambda: browser.page().runJavaScript('''
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.linkHandler = channel.objects.linkHandler;
            });
        '''))
        
        browser.setUrl(qurl)


        i = self.tabs.addTab(browser, label)
        print(f'{i}番目のタブを開いたよ')
        self.tabs.setCurrentIndex(i)
        new_title = browser.page().title()
        if new_title == '':
            new_title = 'Document'
            
            
            
        # タイトルとIDのリストを更新
        found = False
        
        
        for tab_info in self.tab_id_title_list:
            if tab_info['id'] == i:
                tab_info['title'] = new_title
                found = True
                break
        
        if not found:
            # 空いているIDを探す
            available_id = None
            for idx in range(self.tabs.count()):
                if not any(tab_info['id'] == idx for tab_info in self.tab_id_title_list):
                    available_id = idx
                    break
            
            if available_id is not None:
                self.tab_id_title_list.insert(available_id, {'id': available_id, 'title': new_title})
            else:
                self.tab_id_title_list.append({'id': i, 'title': new_title})

        print(f"New tab opened: ID={i}, Title={new_title}")
        
        # タイトル変更時に on_title_changed を呼び出す
        browser.titleChanged.connect(lambda new_title, i=i: self.on_title_changed(new_title, i))
        
        # タブのIDとタイトルをリストに追加
        
        
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        
        browser.loadFinished.connect(lambda _, i=i, : self.tabs.setTabText(i, browser.page().title()[:7] if len(browser.page().title()) > 7 else browser.page().title().ljust(7)))
        browser.iconChanged.connect(lambda _, i=i, browser=browser: self.tabs.setTabIcon(i, browser.icon()))
        
        
        print ("-------add_new_tab end--------")
        print(f"Current tab list: {self.tab_id_title_list}")

        
        
    def on_title_changed(self, new_title, i):
        self.update_star_icon()
        # タイトルが変更されたらリストを更新
        for tab_info in self.tab_id_title_list:
            if tab_info['id'] == i:
                tab_info['title'] = new_title
                break

        # self.tab_id_title_list.append({i: new_title})
        #print(f"Tab updated: ID={i}, Title={new_title}")
        print(f"Current tab list: {self.tab_id_title_list}")
               
    

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()
            self.update_star_icon()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())
        self.update_star_icon()


    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        # title = browser.page().title()
        title=self.tabs.currentWidget().page().title()
        formatted_title = title[:7] if len(title) > 7 else title.ljust(7)
        print(formatted_title)
        self.setWindowTitle("%s Goth" % formatted_title)
    
        self.tabs.setTabText(self.tabs.currentIndex(), formatted_title)
        if title is not None:
            print(title)
        else:
            print("Noneだよ")
        

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://kanaji2002.github.io/Goth-toppage/room1.html"))

    def navigate_to_url(self):
        url = self.urlbar.text()
        if "google.com/search?q=" in url:
            self.tabs.currentWidget().setUrl(QUrl(url))
        else:
            google_search_url = "https://www.google.com/search?q=" + url
            self.tabs.currentWidget().setUrl(QUrl(google_search_url))

    def update_urlbar(self, q, browser=None):
        # 現在開いているタブのみみ受け付ける．
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


    
    
    def toggle_star(self):
        """☆ボタンをクリックするたびに☆と★を切り替える"""
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            
            if self.star_button.isChecked():
                self.star_button.setText("★")
                self.add_shortcut()
            else:
                self.star_button.setText("☆")
                self.remove_bookmark()

    def update_star_icon(self):
        """現在のタブのURLがブックマークされているかどうかで☆と★を切り替える"""

        
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            url = current_tab.page().url().toString()
            tree = ET.parse('shortcuts.xml')
            root = tree.getroot()
            bookmarked = any(shortcut.find('url').text == url for shortcut in root.findall('shortcut'))
            if bookmarked:
                self.star_button.setChecked(True)
                self.star_button.setText("★")
            else:
                self.star_button.setChecked(False)
                self.star_button.setText("☆")
                for action in self.vertical_bar.actions():
                    self.vertical_bar.removeAction(action)
                self.load_shortcuts()


    def add_shortcut(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            url = current_tab.page().url().toString()
            title = current_tab.page().title()
            shortcut_button = QAction("", self)
            shortcut_button.setText(current_tab.page().title())
            shortcut_button.setToolTip(url)
            
            shortcut_button.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl(url)))
            
            self.vertical_bar.addAction(shortcut_button)
            # self.tabs.currentWidget().setUrl(QUrl(url))
            self.save_shortcut_to_xml(title, url)

    def save_shortcut_to_xml(self, title, url):
        # self.force_star()
        if not os.path.exists('shortcuts.xml'):
            root = ET.Element("shortcuts")
            tree = ET.ElementTree(root)
            tree.write('shortcuts.xml')
            
        tree = ET.parse('shortcuts.xml')
        root = tree.getroot()
        for shortcut in root.findall('shortcut'):
            if shortcut.find('url').text == url:
                
                print("Bookmark already exists.")
            
                return
        shortcut = ET.SubElement(root, 'shortcut')
        ET.SubElement(shortcut, 'title').text = title
        ET.SubElement(shortcut, 'url').text = url
        tree.write('shortcuts.xml')

    def remove_bookmark(self):
        current_tab = self.tabs.currentWidget()
        # 現在のタブが QWebEngineView のインスタンスかどうかを確認
        if isinstance(current_tab, QWebEngineView):
            url = current_tab.page().url().toString()
            actions_to_remove = []  # 削除するアクションを一時的に保存するリスト

            # vertical_bar からアクションを探して削除
            for action in self.vertical_bar.actions():
                if hasattr(action, 'url') and action.url == url:
                    actions_to_remove.append(action)

            # すべての該当するアクションを削除
            for action in actions_to_remove:
                self.vertical_bar.removeAction(action)

            # XML からもショートカットを削除
            self.delete_shortcut_from_xml(url)

        # お気に入りの星アイコンを更新
        self.update_star_icon()


    def delete_shortcut_from_xml(self,url):
        if not os.path.exists('shortcuts.xml'):
            return
        tree = ET.parse('shortcuts.xml')
        root = tree.getroot()
        for shortcut in root.findall('shortcut'):
            if shortcut.find('url').text == url:
                root.remove(shortcut)
                tree.write('shortcuts.xml')
                break
    

    def load_shortcuts(self):
        if not os.path.exists('shortcuts.xml'):
            return
        tree = ET.parse('shortcuts.xml')
        root = tree.getroot()
        added_urls = set()
        for shortcut in root.findall('shortcut'):
            title = shortcut.find('title').text
            url = shortcut.find('url').text
            if url not in added_urls:
                self.add_website_shortcut(url, title)
                added_urls.add(url)

    def add_website_shortcut(self, url, name):
        name = name[:23] + '...' if len(name) > 23 else name
        shortcut_button = QAction(name, self)
        shortcut_button.url = url
        view = QWebEngineView()
        view.load(QUrl(url))
        view.iconChanged.connect(lambda icon, button=shortcut_button: button.setIcon(icon))
        shortcut_button.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl(url)))
        shortcut_button.triggered.connect(self.update_star_icon)  # ショートカットを開く時に☆を更新
        self.vertical_bar.addAction(shortcut_button)
        self.save_shortcut_to_xml(name, url)

    def create_database(self):
        if not os.path.exists('shortcuts.xml'):
            root = ET.Element("shortcuts")
            tree = ET.ElementTree(root)
            tree.write('shortcuts.xml')


    ## ここからが，pin度目を，xmlに保存していくコード

    def add_pin_stop(self, url, name):
        print("add_pin_stop")
        print(f"{url=}, {name=}in add_pin_stop")
        self.save_pin_to_xml(name, url.toString())

    def save_pin_to_xml(self, name, url):
        # XMLファイルが存在しない場合は作成する
        if not os.path.exists('shortcuts_pin.xml'):
            root = ET.Element("shortcuts")
            tree = ET.ElementTree(root)
            tree.write('shortcuts_pin.xml')

        tree = ET.parse('shortcuts_pin.xml')
        root = tree.getroot()

        # 同じURLが既に存在するかチェック
        for shortcut in root.findall('shortcut'):
            if shortcut.find('url').text == url:
                print("pin is already exists.")
                return

        # 新しいショートカットを追加
        shortcut = ET.SubElement(root, 'shortcut')
        ET.SubElement(shortcut, 'title').text = name
        ET.SubElement(shortcut, 'url').text = url
        tree.write('shortcuts_pin.xml')



    # def remove_pin(self):
       # ピン止めをはずす関数．これはまだ実装しなくてもいいかも．
    
    # def delete_shortcut_from_xml(self,url):


    def add_website_shortcut_pin(self, url, title):
        # ショートカットのボタンを作成
        shortcut_button = QAction(title, self)  # タイトルをボタンに設定
        shortcut_button.url = url

        # ショートカットのアイコン設定（URLのアイコンを設定するなど）
        view = QWebEngineView()
        view.load(QUrl(url))
        view.iconChanged.connect(lambda icon, button=shortcut_button: button.setIcon(icon))

        # ボタンがクリックされたときに新しいタブでURLを開く
        shortcut_button.triggered.connect(lambda: self.add_new_tab(QUrl(url), title))

        # ショートカットボタンをツールバーまたは任意の場所に追加
        self.vertical_bar.addAction(shortcut_button)

    def load_shortcuts_pin(self):
        if not os.path.exists('shortcuts_pin.xml'):
            return
        tree = ET.parse('shortcuts_pin.xml')
        root = tree.getroot()
        added_urls = set()
        for shortcut in root.findall('shortcut'):
            title = shortcut.find('title').text
            url = shortcut.find('url').text
            print(f"{title=}, {url=}")
            # URL文字列をQUrlに変換してからショートカットを追加
            qurl = QUrl(url)  # QUrlオブジェクトに変換
            # if url not in added_urls:
            #     self.add_website_shortcut_pin(qurl, title)  # QUrlオブジェクトを渡す
            #     added_urls.add(url)

        

app = QApplication(sys.argv)
app.setApplicationName("Goth")
app.setWindowIcon(QIcon("icon.ico")) 
window = MainWindow()
window.create_database()
# ページを描画
window.show()


# マウス等のイベントを監視
app.exec()









