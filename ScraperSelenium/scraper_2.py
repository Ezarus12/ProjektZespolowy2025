import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def create_driver(executable_path="chromedriver.exe"):
    """
    Tworzy i zwraca obiekt WebDriver z ustawionym user agentem.
    """
    chrome_options = Options()
    # Ustawiamy "normalny" user agent, aby strona załadowała się w pełnej wersji
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/108.0.5359.72 Safari/537.36"
    )

    service = Service(executable_path=executable_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scroll_page(driver, max_scrolls=140, sleep_time=2):
    """
    Przewija stronę w dół do momentu załadowania nowej treści
    (lub do osiągnięcia liczby max_scrolls).
    """
    scroll_attempts = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    while scroll_attempts < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No more content to load. Exiting scroll loop.")
            break

        last_height = new_height
        scroll_attempts += 1
        print(f"Scroll attempt {scroll_attempts}.")


def parse_and_write_data(driver, output_file):
    """
    Parsuje źródło strony, wyciąga dane (autorów i tytuły) i zapisuje do pliku.
    Jeśli nie znaleziono żadnych artykułów, funkcja kończy działanie.
    """
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    boxes = soup.select("cite.data.tts-content")  # Selektor CSS

    if not boxes:
        print("Brak artykułów do zapisania. Kończę działanie funkcji.")
        return

    with open(output_file, "w", encoding="utf-8") as file:
        for i, box in enumerate(boxes, start=1):
            # Autorzy
            authors_elems = box.select("span[itemprop='author'] span[itemprop='name']")
            authors_list = [auth.get_text(strip=True) for auth in authors_elems]
            authors_str = ", ".join(authors_list) if authors_list else "Brak autorów"

            # Tytuł
            title_elem = box.find("span", class_="title")
            title_str = title_elem.get_text(strip=True) if title_elem else "Brak tytułu"

            file.write(f"Artykuł {i}:\n")
            file.write(f"Autor(zy): {authors_str}\n")
            file.write(f"Tytuł: {title_str}\n")
            file.write("-" * 50 + "\n")

    print("Scraping completed successfully. Dane zapisano w pliku:", output_file)


def main(url, output_file):
    """
    Główna funkcja:
    1. Tworzy WebDriver,
    2. Otwiera podany URL,
    3. Przewija stronę (scroll_page),
    4. Parsuje dane i zapisuje je do pliku (parse_and_write_data),
    5. Zamyka przeglądarkę.
    """
    driver = create_driver(executable_path="chromedriver.exe")

    try:
        print(f"Opening page: {url}")
        driver.get(url)
        time.sleep(2)  # Czas na wstępne załadowanie strony

        # Scrollujemy stronę
        scroll_page(driver, max_scrolls=150, sleep_time=1)

        # Parsujemy i zapisujemy wyniki
        parse_and_write_data(driver, output_file=output_file)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    """
    Wywołanie skryptu z linii poleceń:
    python script.py "URL" "nazwa_pliku.txt"

    """
    subject = ["Artificial Intelligence","Distributed Systems","5G","manet"]


    if len(sys.argv) > 2:
        url = sys.argv[1]
        output_file = sys.argv[2]
    elif len(sys.argv) > 1:
        url = sys.argv[1]
        output_file = "2040.txt"
    for i in subject:
        year = 2025
        while(year>2020):
            query = i + ":" + str(year)
            url = f"https://dblp.org/search?q={query}"
            file =f"{str(year)}"
            output_file = i + str(year)
            main(url, output_file)
            year = year - 1