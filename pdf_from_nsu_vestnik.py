from bs4 import BeautifulSoup
import requests

# По ссылке на pdf-файл скачиваем файл
def pdf_from_link(link):
    # Проверяем HTTP response status code
    response = requests.get(link)
    file_Path = "C:\project2025/ScientificStyle/Articles/" + str(link[-36:])
    if response.status_code == 200:
        # Создаем новый файл и сохраняем в нем файл по ссылке
        with open(file_Path, 'wb') as file:
            file.write(response.content)
    else:
        print('Failed to download file')

# Находим на сайте Вестника НГУ ссылки на pdf-файлы с научными статьями с 2007 до указанного года
def pdf_url_from_vestnik(year):
    pdf_links = []
    for year in range(2007, year + 1):
        # Получаем ссылку на выпуски определенного года
        year_url = 'https://vestnik.nsu.ru/historyphilology/' + str(year)
        page_year = requests.get(year_url)
        year_soup = BeautifulSoup(page_year.text, "html.parser")
        for year_issues in year_soup.find_all('div', class_='col-md-12'):
            year_issues_url = year_issues.find_all('a')
            for issue in year_issues_url:
                # Получаем ссылку на определенный выпуск
                issue_url = issue.get('href')
                page_issue = requests.get(issue_url)
                issue_soup = BeautifulSoup(page_issue.text, "html.parser")
                for issue_articles in issue_soup.find_all('div', class_='col-md-12'):
                    issue_article_url = issue_articles.find_all('a')
                    for article in issue_article_url:
                        # Получаем ссылку на определенную статью
                        article_url = article.get('href')
                        page_article = requests.get(article_url)
                        article_soup = BeautifulSoup(page_article.text, "html.parser")
                        for article_pdfs in article_soup.find_all('div', class_='col-md-12'):
                            article_pdf_url = article_pdfs.find_all('a')
                            for pdf_file in article_pdf_url:
                                # Получаем ссылки на файлы на данной странице
                                pdf_url = 'https://vestnik.nsu.ru' + pdf_file.get('href')
                                # Проверяем, что скачиваемый файл - именно pdf
                                if pdf_url[-3:] == "pdf":
                                    pdf_links.append(pdf_url)
    return pdf_links


for link in pdf_url_from_vestnik(2007):
    pdf_from_link(link)
