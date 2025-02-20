from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os

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
    '''
    Website scrolling - disabled for the test purposes
    for _ in range(50):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Przewinięto stronę {_ + 1}/{50} razy")
        time.sleep(2)  # Poczekaj, aż nowe elementy się załadują
        '''

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
    #folder_name = query.split(":")[0] #Used for creating the folder for each of the topics
    folder_path = os.path.join("Dane")  # Ścieżka do folderu
    os.makedirs(folder_path, exist_ok=True)

    filename = query.replace(":", "_") + ".txt"
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        for pub in publications:
            file.write(f"Tytuł: {pub['title']}\n")
            file.write(f"Autorzy: {', '.join(pub['authors'])}\n")
            file.write(f"Rok: {pub['year']}\n")
            file.write("\n")

    print("Dane zapisane do pliku: ", file_path)
    return publications

if __name__ == "__main__":
    topics = ["artificial intelligence", "distributed systems", "5G", "manet", 
    "swarm intelligence", "quantum computing", "graphs", "temporal networks", "deep learning"]
    
    for topic in topics:
        for i in range(2022, 2023): #Change to 1980, 2024 for a full range
            temp_query = f"{topic}:{i}"
            print(temp_query)
            results = scrape_dblp(temp_query)
    
    '''
    for pub in results:
        print(f"Tytuł: {pub['title']}")
        print(f"Autorzy: {', '.join(pub['authors'])}")
        print(f"Rok: {pub['year']}")
        print("\n")
    '''