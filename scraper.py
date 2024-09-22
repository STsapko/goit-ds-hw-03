import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "http://quotes.toscrape.com"

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

# Функция для сбора цитат со всех страниц
def scrape_quotes():
    quotes = []
    page = 1
    while True:
        url = f"{BASE_URL}/page/{page}/"
        soup = get_soup(url)
        quote_elements = soup.select(".quote")
        
        if not quote_elements:  # Если нет больше цитат, заканчиваем цикл
            break

        for quote in quote_elements:
            text = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all(class_="tag")]
            quotes.append({
                "quote": text,
                "author": author,
                "tags": tags
            })

        page += 1
    return quotes

# Функция для сбора информации об авторах
def scrape_authors():
    authors = []
    visited_authors = set()
    page = 1

    while True:
        url = f"{BASE_URL}/page/{page}/"
        soup = get_soup(url)
        quote_elements = soup.select(".quote")
        
        if not quote_elements:
            break

        for quote in quote_elements:
            author_name = quote.find(class_="author").get_text()
            if author_name not in visited_authors:
                visited_authors.add(author_name)
                author_url = BASE_URL + quote.find("a")["href"]
                author_soup = get_soup(author_url)
                born_date = author_soup.find(class_="author-born-date").get_text()
                born_location = author_soup.find(class_="author-born-location").get_text()
                description = author_soup.find(class_="author-description").get_text().strip()

                authors.append({
                    "fullname": author_name,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                })

        page += 1
    return authors

# Сохранение данных в файлы JSON
def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    quotes = scrape_quotes()
    authors = scrape_authors()

    save_to_json(quotes, "quotes.json")
    save_to_json(authors, "authors.json")

    print("Скрапинг завершен. Данные сохранены в quotes.json и authors.json.")
