from flask import Flask, render_template, request  # Импортирование нужных библиотек
from bs4 import BeautifulSoup  # Импортирование функции для парсинга HTML
import docx  # Импортирование модуля для работы с документами Word
import re  # Импортирование модуля для работы с регулярными выражениями

app = Flask(__name__)  # Создание объекта приложения Flask


@app.route('/')  # Определение маршрута "/" (главная страница)
def index():
    return render_template('main_page.html')  # Отображение шаблона "source.html"


@app.route('/find_most_common_word', methods=['GET', 'POST'])  # Определение маршрута "/find_most_common_word"
def find_most_common_word():
    if request.method == 'POST':  # Если запрос методом POST
        file = request.files['file']  # Получение загруженного файла
        if file and allowed_file(file.filename):  # Если файл допустимого формата
            filename = file.filename  # Получение имени файла
            if filename.endswith('.docx'):  # Если файл формата .docx
                doc = docx.Document(file)  # Создание объекта документа Word из файла
                words = []
                for para in doc.paragraphs:  # Для каждого абзаца в документе
                    words.extend(para.text.split())  # Добавление слов из абзаца в список слов
            elif filename.endswith('.txt'):  # Если файл формата .txt
                words = file.read().decode('utf-8').split()  # Чтение содержимого файла и разделение на слова
            elif filename.endswith('.html'):  # Если файл формата .html
                soup = BeautifulSoup(file, 'html.parser')  # Создание объекта BeautifulSoup для парсинга HTML
                words = soup.get_text().split()  # Получение текстового содержимого HTML и разделение на слова
            else:
                return render_template('upload_page.html',
                                       error='Ошибка! Поддерживаются только файлы формата .docx, .txt и .html')
                # Отображение сообщения об ошибке, если файл не допустимого формата
            words = [re.sub(r'[^\w\s]', '', word) for word in words if re.search(r'[a-zA-Zа-яА-Я]', word)]
            # Удаление знаков препинания
            word_counts = {}
            for word in words:  # Для каждого слова в списке слов
                if word in word_counts:
                    word_counts[word] += 1  # Увеличение счетчика для этого слова
                else:
                    word_counts[word] = 1  # Добавление нового слова в словарь
            most_common_word = max(word_counts, key=word_counts.get)  # Нахождение слова с максимальным количеством
            # повторений в словаре word_counts и присвоение его переменной most_common_word.
            return render_template('result_page.html', most_common_word=most_common_word)  # Отображение шаблона "main.html" и
            # передача самого часто встречающегося слова в качестве аргумента.
        else:
            return render_template('upload_page.html',
                                   error='Ошибка! Поддерживаются только файлы формата .docx, .txt и .html')  # В случае,
            # если загруженный файл не является допустимым, отображается шаблон "upload.html" с сообщением об ошибке.
    return render_template('upload_page.html')  # Отображение шаблона "upload.html", который содержит форму для загрузки
    # файла и кнопку "Найти самое часто встречающееся слово".


def allowed_file(filename):  # Функция, которая проверяет, является ли расширение загруженного файла допустимым.
    # Если да, функция возвращает True, иначе False.
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'docx', 'txt', 'html'}


if __name__ == '__main__':  # запуск программы
    app.run()
