from PyQt5.QtWidgets import (
    QWidget, QApplication,
    QHBoxLayout, QLabel,
    QPushButton, QVBoxLayout, 
    QFileDialog, QTextEdit, QProgressBar
)
from PyQt5.QtCore import (
    Qt, pyqtSlot, QSize,
    QPoint, pyqtSignal
)
from PyQt5.QtGui import (
    QIcon, QImage,
    QPixmap, QTextCursor
)
from Translator import FormatTranslator
from typing import Dict
import ctypes


class MainWindow(QWidget):
    centering_signal = pyqtSignal(QSize)

    def __init__(self) -> None:
        super().__init__()
        self.centering_signal.connect(self.resize_to_center)
        self.setup_ui()
    
    def setup_ui(self) -> None:
        self.setStyleSheet('background-color: #080808;')
        self.setWindowIcon(QIcon('icons/title_icon.png'))
        self.setWindowTitle(' ')
        self.setFixedSize(QSize(500, 500))
        
        self.parse_widget = ParseWidget(self)
        self.parse_widget.setVisible(False)
        self.menu_widget = MenuWidget(self, self.parse_widget)

        super_layout = QHBoxLayout()
        super_layout.addWidget(self.parse_widget)
        super_layout.addWidget(self.menu_widget)
        
        self.setLayout(super_layout)

    @pyqtSlot(QSize)
    def resize_to_center(self, size: QSize) -> None:
        self.setFixedSize(size)
        self.move(QPoint(QApplication.desktop().width() // 2 - self.width() // 2,
                         QApplication.desktop().height() // 2 - self.height() // 2))


class ParseWidget(QWidget):
    ''' Виджет для просмотра двух файлов после форматирования '''
    def __init__(self, parent: MainWindow) -> None:
        super().__init__()
        self.setup_iu(parent)

    def setup_iu(self, parent: MainWindow) -> None:
        text_layout = QHBoxLayout()

        self.neu_file = QTextEdit()
        self.neu_file.setStyleSheet('border: 0px; color: white; font-size: 15px; font-weight: bold;')
        self.neu_file.setAlignment(Qt.AlignCenter)
        self.neu_file.setReadOnly(True)

        self.aneu_file = QTextEdit()
        self.aneu_file.setStyleSheet('border: 0px; color: white; font-size: 15px; font-weight: bold;')
        self.aneu_file.setAlignment(Qt.AlignCenter)
        self.aneu_file.setReadOnly(True)

        text_layout.addWidget(self.neu_file)
        text_layout.addWidget(self.aneu_file)

        self.close_button = QPushButton('Закрыть')
        self.close_button.setFixedSize(QSize(150, 40))
        self.close_button.clicked.connect(lambda: self.close_files_view(parent))
        self.close_button.setStyleSheet(
            '''
            QPushButton {
                color: white;
                font-weight: bold;
                font-size: 25px;
                text-align: center;
                background-color: #ff073a;
                border-radius: 10px;
            }
            
            QPushButton:hover {
                background-color: #4169e1;
            }''')
        
        label_layout = QHBoxLayout()
        
        neu_label = QLabel('.neu')
        neu_label.setAlignment(Qt.AlignCenter)
        neu_label.setStyleSheet('background-color: #080808; color: white; font-size: 25px; font-weight: bold;')

        aneu_label = QLabel('.aneu')
        aneu_label.setAlignment(Qt.AlignCenter)
        aneu_label.setStyleSheet('background-color: #080808; color: white; font-size: 25px; font-weight: bold;')
        
        label_layout.addWidget(neu_label)
        label_layout.setAlignment(neu_label, Qt.AlignCenter)
        label_layout.addWidget(aneu_label)
        label_layout.setAlignment(aneu_label, Qt.AlignCenter)

        file_parse_layout = QVBoxLayout()
        file_parse_layout.addLayout(label_layout)
        file_parse_layout.addLayout(text_layout)
        file_parse_layout.addWidget(self.close_button)
        file_parse_layout.setAlignment(self.close_button, Qt.AlignCenter)

        all_text_layout = QHBoxLayout()
        all_text_layout.addLayout(file_parse_layout)
        all_text_layout.setAlignment(file_parse_layout, Qt.AlignRight)

        self.setLayout(all_text_layout)

    @pyqtSlot(MainWindow)
    def close_files_view(self, parent: MainWindow) -> None:
        self.setVisible(False)
        parent.centering_signal.emit(QSize(500, 500))


class MenuWidget(QWidget):
    def __init__(self, parent: MainWindow, parse_widget: ParseWidget) -> None:
        super().__init__()

        self.__cache: Dict[str, str] = {
            'neu_path': '',
            'aneu_path': '',
        }
        self.parse_widget = parse_widget
        self.setup_iu(parent)

    def setup_iu(self, parent: MainWindow) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(70)

        self.message = QLabel()
        self.message.setText(f'''Выберите <i><tt><span style="color: #ffbf00;">.neu</span></tt></i>
                              файл<br /> для его форматирования''')
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setStyleSheet('color: white; font-size: 25px;')

        self.chose_file_button = QPushButton('Выбрать файл')
        self.chose_file_button.setFixedSize(QSize(250, 40))
        self.chose_file_button.clicked.connect(self.chose_file)
        self.chose_file_button.setStyleSheet(
            '''
            QPushButton {
                color: white;
                font-weight: bold;
                font-size: 25px;
                text-align: center;
                background-color: #3cb371;
                border-radius: 10px;
            }
            
            QPushButton:hover {
                background-color: #4169e1;
            }
            
            QPushButton:disabled {
                background-color: #b4c4c3;
            }''')
        
        self.parse_files_button = QPushButton('Просмотр файлов')
        self.parse_files_button.setEnabled(False)
        self.parse_files_button.setFixedSize(QSize(250, 40))
        self.parse_files_button.clicked.connect(lambda: self.parse_files(parent))
        self.parse_files_button.setStyleSheet(
            '''
            QPushButton {
                color: white;
                font-weight: bold;
                font-size: 25px;
                text-align: center;
                background-color: #ff073a;
                border-radius: 10px;
            }

            QPushButton:hover {
                background-color: #4169e1;
            }
            
            QPushButton:disabled {
                background-color: #b4c4c3;
            }''')
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addWidget(self.chose_file_button)
        button_layout.setAlignment(self.chose_file_button, Qt.AlignCenter)

        button_layout.addWidget(self.parse_files_button)
        button_layout.setAlignment(self.parse_files_button, Qt.AlignCenter)
        
        image_layout = QHBoxLayout()
        image_layout.setAlignment(Qt.AlignCenter)
        image_layout.setSpacing(50)

        neu_image = QLabel()
        neu_image.setPixmap(QPixmap.fromImage(QImage('icons/neu_icon.png')))

        arrow_image = QLabel()
        arrow_image.setPixmap(QPixmap.fromImage(QImage('icons/arrow_icon.png')))

        aneu_image = QLabel()
        aneu_image.setPixmap(QPixmap.fromImage(QImage('icons/aneu_icon.png')))

        image_layout.addWidget(neu_image)
        image_layout.addWidget(arrow_image)
        image_layout.addWidget(aneu_image)

        main_layout.addLayout(image_layout)
        main_layout.addWidget(self.message)
        main_layout.addLayout(button_layout)
        main_layout.setAlignment(button_layout, Qt.AlignBottom)

        self.parse_widget.close_button.clicked.connect(lambda: self.chose_file_button.setEnabled(True))
        self.parse_widget.close_button.clicked.connect(lambda: self.parse_files_button.setEnabled(True))

        self.setLayout(main_layout)

    @pyqtSlot()
    def chose_file(self) -> None:
        self.__cache['neu_path'] = ''
        self.__cache['aneu_path'] = ''
        self.message.setText(f'''Выберите <i><tt><span style="color: #ffbf00;">.neu</span></tt></i>
                                файл<br /> для его форматирования''')
        self.message.setStyleSheet('color: white; font-size: 25px;')
        self.parse_files_button.setEnabled(False)
        file_system_manager = QFileDialog()
        file_system_manager.setDirectory(".")
        file_system_manager.setFileMode(QFileDialog.ExistingFile)
        file_system_manager.fileSelected.connect(self.select_neu_file)
        file_system_manager.exec()

    @pyqtSlot(str)
    def select_neu_file(self, file: str) -> None:
        try:
            if '.' in file:
                raise ValueError
            self.progress_bar = QProgressBar(self)
            self.progress_bar.setValue(0)
            self.progress_bar.setFixedSize(QSize(490, 65))
            self.progress_bar.setStyleSheet('color: white; font-size: 20px;')
            self.progress_bar.move((QPoint(self.width() // 2 - self.progress_bar.width() // 2,
                                    self.height() // 2 - self.progress_bar.height() // 2)))
            FormatTranslator(file).convert()
            self.progress_bar.setValue(self.progress_bar.value() + 10)
            self.__cache['neu_path'] = file
            self.__cache['aneu_path'] = file + '.aneu'
            self.progress_bar.show()
            self.__loda_files_content()
            self.progress_bar.hide()
        except ValueError:
            self.parse_files_button.setEnabled(False)
            self.message.setText(f'''Файл <i><tt><span style="color: white;">
                                {file.split("/")[-1]}</span></tt></i><br />нe .neu расширения''')
            self.message.setStyleSheet('color: #ff073a; font-size: 25px;')
        else:
            self.parse_files_button.setEnabled(True)
            self.message.setText(f'''Файл <i><tt><span style="color: white;">
                                 {file.split("/")[-1]}.neu</span></tt></i><br />успешно преобразован''')
            self.message.setStyleSheet('color: #77dd77; font-size: 25px;')

    @pyqtSlot(MainWindow)
    def parse_files(self, parent) -> None:
        self.parse_files_button.setEnabled(False)
        self.chose_file_button.setEnabled(False)
        parent.centering_signal.emit(QSize(1200, 500))
        self.parse_widget.setVisible(True)

    def __loda_files_content(self) -> None:
        with open(self.__cache['neu_path'], 'r') as neu_file_content,\
            open(self.__cache['aneu_path'], 'r') as aneu_file_content:
            
            self.parse_widget.aneu_file.clear()
            neu_str_content = neu_file_content.read()
            self.progress_bar.setMaximum(len(neu_str_content.split('\n')) + 10)
            self.parse_widget.neu_file.setText(neu_str_content)
            del neu_str_content

            line_numb: int = 0
            for line in aneu_file_content:
                if line_numb == 0:
                    info = line.strip('\n\r').split(' ')
                    line_numb = int(info[0])
                    self.parse_widget.aneu_file.append(str(line_numb) + ' ' \
                        + '<span style="color: red">' + str(info[1]) + '</span>' + '<br />')
                else:
                    self.parse_widget.aneu_file.append(line.replace('\n', '<br />'))
                    line_numb -= 1
                self.progress_bar.setValue(self.progress_bar.value() + 1)
            
            cursor = self.parse_widget.aneu_file.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.parse_widget.aneu_file.setTextCursor(cursor)


def main() -> None:
    myappid = u'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
