import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtCore import Qt

films = []
try:
    with open("films.txt", "r", encoding="utf-8") as file:
        for film in file.readlines():
            films.append(film.strip())
except FileNotFoundError:
    films = ['After', 'Ginny & Georgia', 'Kissing Booth', 'To All the Boys I have Loved', 'Through my window']

correct_film_names = {
    'after.jpg': 'After',
    'ginny-&-georgia.jpg': 'Ginny & Georgia',
    'kissing-booth.jpg': 'Kissing Booth',
    'to-all-the-boys-I-have-loved.jpg': 'To All the Boys I have Loved',
    'through-my-window.jpg': 'Through my window',
    'hidden-love.jpg': 'Hidden love',
    'true-beauty.jpg': 'True beauty',
    'xo-kitty.jpg': 'XO, Kitty',
    'my-fault.jpg': 'My fault',   
    'k.c.-undercover.jpg': 'K.C. undercover'
}

class FilmQuizApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setFixedSize(1070, 700)
        self.setWindowTitle('The film quiz')
        self.setWindowIcon(QIcon('images/icon.png'))
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.film_label = QLabel(self)
        self.main_layout.addWidget(self.film_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.message_label = QLabel('', self)
        self.message_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.main_layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.answer_buttons = []
        
        self.next_button = QPushButton('Следующий фильм', self)
        self.next_button.setStyleSheet("""
            QPushButton {
                margin-top: 50px;
                background-color: coral; 
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: brown; }
            QPushButton:pressed { background-color: darkred; }
        """)
        self.next_button.clicked.connect(self.show_next_film)
        self.main_layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.init_game()
        
    def init_game(self):
        self.message_label.setText('')
        self.next_button.setEnabled(False)
        
        for btn in self.answer_buttons:
            self.main_layout.removeWidget(btn)
            btn.deleteLater()
        self.answer_buttons.clear()
        
        image_name = random.choice(list(correct_film_names.keys()))
        film_pixmap = QPixmap(f'images/{image_name}')
        self.film_label.setPixmap(film_pixmap.scaledToHeight(300))
        
        correct_answer = correct_film_names[image_name]
        wrong_films = random.sample([film for film in films if film != correct_answer], min(3, len(films)))
        
        all_films = wrong_films + [correct_answer]
        random.shuffle(all_films)
        
        next_btn_index = self.main_layout.indexOf(self.next_button)
        
        for film in all_films:
            button = QPushButton(film, self)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 16px;
                    border: none;
                    border-radius: 10px;
                    padding: 10px;
                    min-width: 200px;
                }
                QPushButton:hover { background-color: #45a049; }
                QPushButton:pressed { background-color: #388E3C; }
                QPushButton:disabled { background-color: #A9A9A9; color: #7D7D7D; }
            """)
            button.clicked.connect(lambda _, f=film, img=image_name: self.check_answer(f, img))
            
            self.main_layout.insertWidget(next_btn_index, button, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.answer_buttons.append(button)

    def check_answer(self, chosen_film, image_name):
        if chosen_film == correct_film_names[image_name]:
            self.message_label.setText('Верно!')
        else:
            self.message_label.setText('Неверно :(')
            
        for btn in self.answer_buttons:
            btn.setEnabled(False)
            
        self.next_button.setEnabled(True)

    def show_next_film(self):
        self.init_game()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        background_pixmap = QPixmap('images/background.jpg')
        if not background_pixmap.isNull():
            painter.drawPixmap(self.rect(), background_pixmap)
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    quiz_app = FilmQuizApp()
    quiz_app.show()
    sys.exit(app.exec()) 
