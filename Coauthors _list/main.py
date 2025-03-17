import os
import json
from pathlib import Path

def process_json_file(file_path, output_folder):
    """
    Function proccesses given JSON file and based on it creates new .txt file with the same name.
    Function goes through every entry in the JSON file (article with the list of author and the year) and adds 1
    to every pair of coauthors who worked on the article.
    After filling the coauthor_cout dictionary function outputs results in the file

    Args: 
    file_path : path to the JSON file containg articles data
    output_folder : path to the folder in which the .txt file will be saved

    Returns:

    
    """
    with open(file_path, 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)
        
    coauthor_count = {}  # Dictionary to store coauthor pairs and their counts
    
    for entry in data: # Iterate each of the entries (article) in the JSON file
        authors = entry.get("authors", [])  # Get the list of authors
        year = entry.get("year", "0")  # Get the year
        
        # If the year is a range, take the first year from the range (few articles in the json file could have range instead of the year in written in the DBLP website)
        if isinstance(year, str) and '-' in year:
            year = year.split('-')[0]
        
        year = int(year)  # Convert the year to an integer
        
        # Create pairs of coauthors
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                author1, author2 = sorted([authors[i], authors[j]])  # Sort authors
                coauthor_count.setdefault((author1, author2), {}).setdefault(year, 0)
                coauthor_count[(author1, author2)][year] += 1  # Increment coauthor count for each pair of authors
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate the output file name based on the file_path and save results to it
    output_file_name = os.path.join(output_folder, os.path.basename(file_path).replace(".json", "_coauthors.txt"))
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        for (author1, author2), years in coauthor_count.items():
            for year, count in years.items():
                output_file.write(f"{year};{author1};{author2};{count}\n")

if __name__ == "__main__":

    project_folder = Path(__file__).parent.parent  # Parent folder where the script is located
    folder_path = project_folder / "ScraperSelenium" / "scrapped_data"  # Path to the folder containing input data
    output_folder = Path(__file__).parent / "Coauthors_data"  # Path to the folder where output files will be saved
    
    # List all the JSON files in the input folder
    file_names = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    if not file_names:
        raise FileNotFoundError(f"Error: No JSON files found in '{folder_path}'")
    
    # Process each file
    for file_name in file_names:
        process_json_file(os.path.join(folder_path, file_name), output_folder)
