from pdf_from_nsu_vestnik import pdf_url_from_vestnik
from pdf_from_nsu_vestnik import pdf_from_link
from text_from_pdf import get_text
import os
import re

# Указываем путь к директории
directory = "C:\project2025\ScientificStyle\Articles"

# Находим на сайте Вестника НГУ ссылки на pdf-файлы с научными статьями с 2007 до указанного года
for link in pdf_url_from_vestnik(2007):  # Для 2007 и 2008 годов все работает
    # По ссылке на pdf-файл скачиваем файл в указанную папку
    pdf_from_link(link, directory)

# Получаем список файлов
files = os.listdir(directory)

