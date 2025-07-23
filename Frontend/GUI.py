from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if lines.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):

    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "why", "which", "whose", "whom", "can you", "what's", "what's", "how's"]
    
    if any(word + " " in new_query for word in question_words ):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"

    else:
        
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(Command)


def GetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status    


def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(Status)


def GetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitailed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicDirectoryPath(Filename):
    Path = rf'{GraphicsDirPath}\{Filename}'
    return Path

def TempDirectoryPath(Filename):
    Path = rf'{TempDirPath}\{Filename}'
    return Path

def ShowTexttoScreen(Text):
    with open(rf'{TempDirPath}\Response.data', "w", encoding='utf-8') as file:
        file.write(Text)

class ChatSection(QWidget):

    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        self.chat_text_edit= QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.serSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_Lable.setStyleSheet("border: none;")
        movie = QMovie(GraphicDirectoryPath('Jarvis.gif'))
        max_gif_sizw_W = 480
        max_gif_sizw_H = 270
        movie.setScaledSize(QSize(max_gif_sizw_W, max_gif_sizw_H))
        self.gif_lable.setAlingnment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_lable.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_lable)
        self.lable.setStyleSheet("color: white; font size: 16px; margin-right: 195px; border: none; margin-top: -30px;")
        self.lable.setAlignment(Qt.AlignRight)
        layout.addWidget(self.lable)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_lable)
        font = QFont
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessage)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
                           QScrollbar:vertical{
                           border: none;
                           background: black;
                           width: 10px;
                           margin: 0px 0px 0px 0px
                           }
                           
                           QScrollbar:: handel:vertical{
                           background: white;
                           min-height: 20px;
                           }
                           
                           QScrollbar:: add-line:vertical{
                           background: black;
                           subcontrol-position: bottom;
                           subcontrol-origin: margin;
                           height: 10px;
                           }
                           
                           QScrollbar:: sub-line: vertical{
                           background: black;
                           subcontrol-position: top;
                           subcontrol-origin: margin;
                           height: 10px;
                           }
                           
                           QScrollbar:: up-arrow:vertical, QScrollbar::down-arrow:vertical{
                           border: none;
                           color: none;
                           }
                           
                           QScrollbar::add-page:vertical, QScrollbar::sub-page:vertical{
                           background: none;
                           }
                    """)
        def loadMessage(self):

            global old_chat_message

            with open(TempDirectoryPath('Response.data'), 'r', encoding='utf-8')as file:
                messages = file.read()

                if None ==  messages:
                    pass

                elif len(messages)<1:
                    pass

                elif str(old_chat_message)==str(messages):
                    pass

                else:
                    self.addMessage(message=messages, color = 'White')
                    old_chat_message = messages

        def SpeechRcogText(self):
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8')as file:
                message = file.read()
                self.lable.setText(message)

        def loadIcon(self, path, width=60, height=60 ):
                pixmap = QPixmap(path)
                new_pixmap = pixmap.scaled(width, height)
                self.icon_lable.setPixmap(new_pixmap)

        def toggle_icon(self, event=None):
                
                if self.toggled:
                    self.load_icon(GraphicDirectoryPath('voice.png'),60, 60)
                    MicButtonInitailed()

                else:
                    self.load_icon(GraphicDirectoryPath('mic png'), 60, 60)
                    MicButtonClosed()

                self.toggled = not self.toggled

        def addMessage(self, message, color):
                cursor = self.chat_text_edit.textCursor
                format = QTextCharFormat()
                formatm = QTextBlockFormat()
                formatm.setTopMargin(10)  
                formatm. setLeftMargin(10)
                format.setForeground(QColor(color))
                cursor.setCharFormat(format)
                cursor.setBlockFormat(formatm)
                cursor.insertText(message + "\n")
                self.chat_text_edit.setTextCursor(cursor)

class InitialScreen(QWidget):

    def __init__(self, parent= None):
          super().__init__(parent)
          desktop = QApplication.desktop()
          screen_width = desktop.screenGeometry().width()
          screen_height = desktop.screenGeometry().height()
          content_layout = QVBoxLayout()
          content_layout.setContentsMargins(0, 0, 0, 0)
          gif_lable = QLabel()
          movie = QMovie(GraphicDirectoryPath('Jarvis.gif'))
          gif_lable.setMovie(movie)
          max_gif_size_H = int(screen_width / 16*9)
          movie.setScaledSize(QSize(screen_width, max_gif_size_H))
          gif_lable.setAlignment(Qt.AlignCenter)
          movie.start()
          gif_lable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
          self.icon_lable = QLabel()
          pixmap = QPixmap(GraphicDirectoryPath('Mic_on png'))
          new_pixmap = pixmap.scaled(60,60)
          self.icon_lable.setPixmap(new_pixmap)
          self.icon_lable.setFixedSize(150, 150)
          self.icon_lable.setAlignment(Qt.AlignCenter)
          self.toggle = True
          self.toggle_icon()
          self.icon_lable.mousePressEvent = self.toggle_icon
          self.lable = QLabel("")
          self.lable.setStyleSheet("color: white; font-size: 16px; margin-bottom:0;" )
          content_layout.addWidget(gif_lable, alignment=Qt.AlignCenter)
          content_layout.addWidget(self.lable, alignment=Qt.ALignCenter)
          content_layout.addWidget(self.icon_lable, alignment=Qt.ALignCenter)
          content_layout.setContentsMargins(0, 0, 0, 150)
          self.setLayout(content_layout)
          self.setFixedHeight(screen_height)
          self.setFixedWidth(screen_width)
          self.timer.timeout.connect(self.SpeechRecogText)
          self.timer.start(5)

    def SppechRcogText(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            message = file.read()
            self.lable.setText(message)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_lable.setPixmap(new_pixmap)

    def toggle_icon(self, event = None):

        if self.toggled:
             self.load_icon(GraphicDirectoryPath('Mic_on png'), 60, 60)
             MicButtonInitailed()
        else:

            self.load_icon(GraphicDirectoryPath('Mic_on png'), 60, 60)
            MicButtonClosed()

        self.toggled = not self.toggled

class MessageScreen(QWidget):

        def __init__(self, parent = None):
            super().__init__(parent)
            desktop = QApplication.desktop()
            screen_width = desktop.screenGeometry().width()
            screen_height = desktop.screenGeometry().height()
            layout = QVBoxLayout()
            lable = QLabel("")
            layout.addWidget(lable)
            chat_section = ChatSection()
            layout.addWidget(chat_section)
            self.setLayout(layout)
            self.setStyleSheet("background-color: black;")
            self.setFixedHeight(screen_height)
            self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):

     def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.intiUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget

     def  intiUI(self):
         self.setFixedHeight(50)
         layout = QHBoxLayout(self)
         layout.setAlignment(Qt.AligRight)
         home_button = QPushButton()
         home_icon = QIcon(GraphicDirectoryPath('Home.png'))
         home_button.setIcon(home_icon)
         home_button.setText(" Home")
         home_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color:black")
         message_button = QPushButton()
         message_icon = QIcon(GraphicDirectoryPath("Chat.png"))
         message_button.setIcon(message_icon)
         message_button.setText(" Chat")
         message_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color: black")
         minimize_button = QPushButton()
         minimize_icon = QIcon(GraphicDirectoryPath('Minimize2.png'))
         minimize_button.setIcon("background-color:white")
         minimize_button.setStyleSheet.connect(self.minimizeWindow)
         self.maximize_button = QPushButton()
         self.maximize_icon = QIcon(GraphicDirectoryPath('Maximaize.png'))
         self.restore_icon = QIcon(GraphicDirectoryPath('Minimize.png'))
         self.maximize_button.setIcon(self.maximize_icon)
         self.maximize_button.setFlat(True)
         self.maximize_button.setStyleSheet("background-color:white")
         self.maximize_button.clicked.connect("self.maximizeWindow")
         close_button = QPushButton()
         close_icon = QIcon(GraphicDirectoryPath('Close.png'))
         close_button.setIcon(close_icon)
         close_button.setStyleSheet("background-color:white")
         close_button.clicked.connect(self.closeWindow)
         line_Frame = QFrame()
         line_Frame.setFixedHeight(1)
         line_Frame.setFrameShadow(QFrame.HLine)
         line_Frame.setFrameShape(QFrame.Sunken)
         line_Frame.setStyleSheet("border-color: black;")
         title_lable = QLabel(f"{str(Assistantname).capitalize()}AI   ")
         title_lable.setStyleSheet("color:black; font-size: 18px; background-color:white")
         home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
         message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
         layout.addWidget(title_lable)
         layout.addStretch(1)
         layout.addWidget(home_button)
         layout.addStretch(1)
         layout.addWidget(minimize_button)
         layout.addWidget(self.maximize_button)
         layout.addWidget(close_button)
         layout.addWidget(line_Frame)
         self.draggable = True
         self.offset = None

     def paintEvent(self, event):
         painter = QPainter(self)
         painter.fillRect(self.rect(), Qt.white)
         super().paintEvent(event)

     def minimizeWindow(self):
         self.parent().showMinimized()

     def maximizeWindow(self):
         if self.parent().isMaximized():
                 self.parent().showNormal()
                 self.maximize_button.setIcon(self.maximize_icon)

         else:
             
             self.parent().showMaximized()
             self.maximize_button.setIcon(self.restore_icon)


     def closeWindow(self):
         self.parent().close()

     def mousePressEvent(self, event):
         if self.draggable:
                 self.offset = event.pos()

     def mouseMoveEvent(self, event):
         if self.draggable and self.offset:
                new_pos = event.globalPos() - self.offset
                self.parent().move(new_pos)

     def showMessageScreen(self):
          if self.current_screen is not None:
                  self.current_screen.hide()


          message_screen = MessageScreen(self)
          layout = self.parent().layout()
          if layout is not None:
               layout.addwidget(message_screen)
          self.current_screen = message_screen

     def showInitialScreen(self):
          if self.current_screen is not None:
                  self.current_screen()
            
          message_screen = MessageScreen(self)
          layout = self.parent().layout()
          if layout is not None:
                  layout.addWidget(message_screen)
          self.current_screen = message_screen

     def showInitialScreen(self):
          if self.current_screen is not None:
                 self.current_screen.hide()

          intial_screen = InitialScreen(self)
          layout = self.parent().layout()
          if layout is not None:
                 layout.addWidget(intial_screen)
          self.current_screen = intial_screen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()  # <- call to correct function name

    def initUI(self):  # <- EXACT same name!
        # your code here
        pass

def initUI(self):
          desktop = QApplication.desktop()
          screen_width= desktop.screenGeometry().width()
          screen_height= desktop.screenGeometry().height()
          stacked_widget = QStackedWidget(self)
          initial_screen = MessageScreen()
          stacked_widget.addWidget(initial_screen)
          stacked_widget.addwidget(message_screen)
          self.setGeometry(0, 0, screen_width, screen_height)
          self.setStyleSheet("background-color: black;")
          self.setMenuWidget(top_screen)
          self.setCentralWidget(stacked_widget)


def GrphicalUserInterface():
     app = QApplication(sys.argv)
     window = MainWindow()
     window.show()
     sys.exit(app.exec())

if __name__ == "__main__":
     GrphicalUserInterface()        

# end program   