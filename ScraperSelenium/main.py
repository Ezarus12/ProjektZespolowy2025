import requests
from bs4 import BeautifulSoup

def scrape_dblp(query: str):
    url = f"https://dblp.org/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Błąd podczas pobierania strony")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    publications = []
    
    for entry in soup.find_all("li", class_="entry"):  # Szukanie wpisów
        title_tag = entry.find("span", class_="title")
        authors = [a.text for a in entry.find_all("span", itemprop="author")]
        year_tag = entry.find("span", itemprop="datePublished")
        pagination_tag = entry.find("span", itemprop="pagination")
        
        if title_tag and year_tag:
            publications.append({
                "title": title_tag.text,
                "authors": authors,
                "year": year_tag.text,
                "pagination": pagination_tag.text if pagination_tag else "N/A"
            })
    
    with open("dblp_authors_titles_years.txt", "w", encoding="utf-8") as file:
        for pub in publications:
            file.write(f"Tytuł: {pub['title']}\n")
            file.write(f"Autorzy: {', '.join(pub['authors'])}\n")
            file.write(f"Rok: {pub['year']}\n")
            file.write(f"Strony: {pub['pagination']}\n")
            file.write("-" * 40 + "\n")
    
    print("Dane zapisane do pliku dblp_authors_titles_years.txt")
    return publications

if __name__ == "__main__":
    query = "5G:2024"
    results = scrape_dblp(query)
    
    for pub in results:
        print(f"Tytuł: {pub['title']}")
        print(f"Autorzy: {', '.join(pub['authors'])}")
        print(f"Rok: {pub['year']}")
        print(f"Strony: {pub['pagination']}")
        print("-" * 40)