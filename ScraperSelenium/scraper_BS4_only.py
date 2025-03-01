import requests
from bs4 import BeautifulSoup

def scrape_dblp(query: str, year: str):
    url = f"https://dblp.org/search?q={query.replace("_", "%20")}:{year}"
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

    file_name = f"{query}_dblp_authors_titles_years.txt"

    with open(f"./scrapped_data/{file_name}", "w", encoding="utf-8") as file:
        for pub in publications:
            file.write(f"Tytuł: {pub['title']}\n")
            file.write(f"Autorzy: {', '.join(pub['authors'])}\n")
            file.write(f"Rok: {pub['year']}\n")
            file.write(f"Strony: {pub['pagination']}\n")
            file.write("-" * 40 + "\n")
    
    print(f"Dane zapisane do pliku {file_name}")
    return publications

if __name__ == "__main__":

    topics = [
        "5G", "manet", "swarm_intelligence", "quantum_computing", "graphs",
        "temporal_networks", "deep_learning"
    ]

    for pos, name in enumerate(topics):
        results = scrape_dblp(
            query=f"{topics[pos]}",
            year="2024"
        )
