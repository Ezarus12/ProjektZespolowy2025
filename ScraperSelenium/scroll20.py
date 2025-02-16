from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_dblp(query: str):
    url = f"https://dblp.org/search?q={query}"

    # Konfiguracja Selenium (dla Chrome)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Uruchamia w tle (opcjonalne)
    service = Service("chromedriver.exe")  # Podaj ścieżkę do chromedriver.exe
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    # Przewiń stronę, aby załadować wszystkie wpisy
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = last_height
    for _ in range(20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Przewinięto stronę {_ + 1}/{20} razy")
        time.sleep(2)  # Poczekaj, aż nowe elementy się załadują

    # Pobierz pełną stronę HTML
    page_source = driver.page_source
    driver.quit()

    # Parsowanie HTML
    soup = BeautifulSoup(page_source, 'html.parser')
    publications = []

    for entry in soup.find_all("li", class_="entry"):  # Szukanie wpisów
        title_tag = entry.find("span", class_="title")
        authors = [a.text for a in entry.find_all("span", itemprop="author")]
        year_tag = entry.find("span", itemprop="datePublished")

        if title_tag and year_tag:
            publications.append({
                "title": title_tag.text,
                "authors": authors,
                "year": year_tag.text,
            })

    # Zapisz dane do pliku
    with open("DBLP_Data.txt", "w", encoding="utf-8") as file:
        for pub in publications:
            file.write(f"Tytuł: {pub['title']}\n")
            file.write(f"Autorzy: {', '.join(pub['authors'])}\n")
            file.write(f"Rok: {pub['year']}\n")
            file.write("\n")

    print("Dane zapisane do pliku dblp_authors_titles_years.txt")
    return publications

if __name__ == "__main__":
    query = "5G:2024"
    results = scrape_dblp(query)

    for pub in results:
        print(f"Tytuł: {pub['title']}")
        print(f"Autorzy: {', '.join(pub['authors'])}")
        print(f"Rok: {pub['year']}")
        print("\n")