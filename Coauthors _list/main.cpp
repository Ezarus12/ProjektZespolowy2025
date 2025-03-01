#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ifstream inputFile("5G_2022.txt"); // Plik z danymi wejściowymi
    ofstream outputFile("coauthors.txt"); // Plik wyjściowy

    map<pair<string, string>, map<int, int>> coauthorCount;
    string line, title, authorsLine;
    int year;

    while (getline(inputFile, line)) {
        if (line.rfind("Tytuł:", 0) == 0) {
            title = line.substr(7);
        }
        else if (line.rfind("Autorzy:", 0) == 0) {
            authorsLine = line.substr(9);
        }
        else if (line.rfind("Rok:", 0) == 0) {
            year = stoi(line.substr(5));

            // Przetwarzanie listy autorów
            vector<string> authors;
            stringstream ss(authorsLine);
            string author;
            while (getline(ss, author, ',')) {
                author.erase(0, author.find_first_not_of(" ")); // Usunięcie spacji na początku
                authors.push_back(author);
            }

            // Tworzenie par współautorów
            for (size_t i = 0; i < authors.size(); ++i) {
                for (size_t j = i + 1; j < authors.size(); ++j) {
                    string author1 = min(authors[i], authors[j]);
                    string author2 = max(authors[i], authors[j]);
                    coauthorCount[{author1, author2}][year]++;
                }
            }
        }
    }

    // Zapis wyników do pliku
    for (const auto& entry : coauthorCount) {
        for (const auto& yearCount : entry.second) {
            outputFile << yearCount.first << " " << entry.first.first << " "
                << entry.first.second << " " << yearCount.second << "\n";
        }
    }

    inputFile.close();
    outputFile.close();
    return 0;
}
