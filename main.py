import unittest  # импортируем библиотеку для создания unit-тестов
from io import BytesIO  # импортируем класс BytesIO для создания байтового потока

from app import app  # импортируем Flask-приложение, которое будем тестировать


class TestFindMostCommonWord(unittest.TestCase):  # создаем класс для тестирования

    def test_index(self):  # тестируем функцию, которая отвечает за главную страницу
        tester = app.test_client(self)  # создаем клиент для тестирования
        response = tester.get('/')  # отправляем GET-запрос на главную страницу
        self.assertEqual(response.status_code, 200)  # проверяем, что код ответа равен 200

    def test_upload_page(self):  # тестируем функцию, которая отвечает за страницу загрузки файлов
        tester = app.test_client(self)  # создаем клиент для тестирования
        response = tester.get('/find_most_common_word')  # отправляем GET-запрос на страницу загрузки файлов
        self.assertEqual(response.status_code, 200)  # проверяем, что код ответа равен 200

    def test_upload_invalid_file(self):  # тестируем функцию, которая отвечает за загрузку недопустимых файлов
        tester = app.test_client(self)  # создаем клиент для тестирования
        response = tester.post('/find_most_common_word', content_type='multipart/form-data',
                               data={'file': (BytesIO(b'test.jpg'), 'test.jpg')})  # отправляем POST-запрос на страницу
        # загрузки файлов с некорректным файлом
        self.assertIn('Ошибка! Поддерживаются только файлы формата .docx, .txt и .html', response.data.decode())
        # проверяем, что полученный ответ содержит сообщение об ошибке

    def test_docx_file(self):  # тестируем функцию, которая отвечает за обработку .docx файлов
        tester = app.test_client(self)  # создаем клиент для тестирования
        with open('test.docx', 'rb') as f:  # открываем тестовый .docx файл для чтения в бинарном режиме
            response = tester.post('/find_most_common_word', content_type='multipart/form-data', data={'file': f})
            # отправляем POST-запрос на страницу загрузки файлов с тестовым .docx файлом
            self.assertIn('Самое частое слово в файле: "арбуз"', response.data.decode())  # проверяем, что полученный
            # ответ содержит ожидаемый результат

    def test_txt_file(self):  # тестируем функцию, которая отвечает за обработку .txt файлов
        tester = app.test_client(self)  # создаем клиент для тестирования
        with open('test.txt', 'rb') as f:  # открываем тестовый .txt файл для чтения
            response = tester.post('/find_most_common_word', content_type='multipart/form-data', data={
                'file': f})  # отправляем POST-запрос на страницу загрузки файлов с тестовым .txt файлом
            self.assertIn('Самое частое слово в файле: "арбуз"',
                          response.data.decode())  # проверяем, что полученный ответ содержит ожидаемый результат

    def test_html_file(self):  # тестируем функцию, которая отвечает за обработку .html файлов
        tester = app.test_client(self)  # создаем клиент для тестирования
        with open('test.html', 'rb') as f:  # открываем тестовый .html файл для чтения
            response = tester.post('/find_most_common_word', content_type='multipart/form-data', data={
                'file': f})  # отправляем POST-запрос на страницу загрузки файлов с тестовым .html файлом
            self.assertIn('Самое частое слово в файле: "арбуз"',
                          response.data.decode())  # проверяем, что полученный ответ содержит ожидаемый результат


if __name__ == '__main__':
    unittest.main()  # запускаем все тесты




