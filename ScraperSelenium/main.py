import json
import time

import requests
from bs4 import BeautifulSoup

def scrape_data(query, year):
    """
    Sends requests to the specified url and extracts data from the response
    until there is no more content available on the page
    Args:
        query: The name of category to search
    """
    page = 1
    all_publications = []
    start = time.time()
    print(f"Scraping data from the '{topic}' website...")
    while True:
        url = f"https://dblp.org/search/publ/inc?q={query.replace(' ', '%20')}%3A{year}&s=ydvspc&h=30&b={page}"
        response = requests.get(url=url)
        if response.status_code == 200:
            response_html_data = response.text
            soup = BeautifulSoup(response_html_data, 'html.parser')
            current_page_publications = search_for_publications(soup)
            if not current_page_publications:
                print(f"End of the '{topic}' website. Pages iterated: {page}")
                break
            all_publications.extend(current_page_publications)
            page += 1
        else:
            print(f"Error: {response.status_code}")
            break
    finish = time.time()
    print(f"Scraping the '{topic}' page took {finish - start:.5}s.")
    return all_publications

def search_for_publications(soup):
    """
    Looks for publications data in provided html content
    Args:
        soup: bs4 object of html content
    """
    publications = []
    for entry in soup.find_all("li", class_="entry"):
        title_tag = entry.find("span", class_="title")
        authors = [a.text for a in entry.find_all("span", itemprop="author")]
        year_tag = entry.find("span", itemprop="datePublished")

        if title_tag and year_tag:
            if title_tag.text != "(Withdrawn)": #skips empty tags
                publications.append({
                    "title": title_tag.text,
                    "authors": authors,
                    "year": year_tag.text,
                })
    return publications

def save_publications_to_file(publications, file_name, year):
    """
    Saves publications data to file with given name
    Args:
        publications: list of publications to save
        file_name: name of file to save data to
    """
    if len(publications) != 0:
        start = time.time()
        with open(f"scrapped_data/{file_name}_{year}.json", "w")as file:
            json.dump(publications, file, indent=4)
        finish = time.time()
        print(f"Data saved to file 'scrapped_data/{file_name}_{year}'.")
        print(f"Saving data to '{file_name}' file took {finish - start:.3f}s.\n\n")
    else:
        print(f"No data for {year} year.")


if __name__ == "__main__":
    topics = [
        "artificial intelligence", "distributed systems", "5G", "manet","swarm intelligence",
        "quantum computing", "graphs", "temporal networks", "deep learning"
    ]

    print("Program started.\n\n")
    start_of_whole_program = time.time()

    s_year = 1950
    f_year = 2005

    for topic in topics:
        for year in range(s_year, f_year):
            pubs = scrape_data(topic, year)
            save_publications_to_file(pubs, topic.replace(" ", "_").lower(), year)

    end_of_whole_program = time.time()
    whole_time = (end_of_whole_program - start_of_whole_program)/60
    print("Program finished.")
    print(f"It took {whole_time:.5f}s to scrape and save all the data.")
