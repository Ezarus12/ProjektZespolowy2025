#include <iostream>
#include <fstream>
#include <string>
#include <vector>

int main() {
    std::string file_path = "C:\\Users\\ezaru\\Desktop\\ProjektZespolowy\\Parser\\dblp-parser\\dane.xml";  // Podaj œcie¿kê do pliku

    // Zdefiniuj rok do filtrowania
    std::string filter_year = "2022";  // Przyk³ad: chcesz filtrowaæ tylko artyku³y z 2021 roku

    // Otwórz plik
    std::ifstream file(file_path);

    if (!file.is_open()) {
        std::cerr << "Nie mo¿na otworzyæ pliku: " << file_path << std::endl;
        return 1;
    }

    std::string line;
    std::string keyword = "beyond 5G";  // Zdefiniuj s³owo kluczowe
    int line_c = 0;
    bool inside_article = false;
    bool article_printed = false; // Flaga sprawdzaj¹ca, czy artyku³ ju¿ zosta³ wypisany
    std::string current_title;
    std::string current_year;
    std::vector<std::string> current_authors;
    std::string next_line; // Zmienna do przechowywania linii, która zawiera rok

    // Czytanie pliku linia po linii
    while (std::getline(file, line)) {
        line_c++;

        // Szukamy pocz¹tków i koñców tagów <article> i </article>
        if (line.find("<article") != std::string::npos) {
            inside_article = true;
            article_printed = false; // Zresetuj flagê przy rozpoczêciu nowego artyku³u
            current_title.clear();
            current_year.clear();
            current_authors.clear();
            next_line.clear();  // Resetuj zmienn¹ przechowuj¹c¹ kolejn¹ liniê
        }

        if (inside_article) {
            // Sprawdzamy tytu³ artyku³u
            if (line.find("<title>") != std::string::npos) {
                size_t start = line.find("<title>") + 7;
                size_t end = line.find("</title>");
                current_title = line.substr(start, end - start);
            }

            // Sprawdzamy autorów (uwzglêdniaj¹c ORCID, ale wypisujemy tylko imiê i nazwisko)
            if (line.find("<author") != std::string::npos) {
                size_t start = line.find(">") + 1;  // Wyszukujemy po ">"
                size_t end = line.find("</author>");
                std::string author = line.substr(start, end - start);

                // Zapisz imiê i nazwisko autora (pomijamy ORCID)
                current_authors.push_back(author);
            }

            // Jeœli napotkamy koniec artyku³u, sprawdzamy drug¹ liniê, ¿eby wyci¹gn¹æ rok
            if (line.find("<title>") != std::string::npos) {
                std::getline(file, next_line); // Odczytujemy nastêpn¹ liniê z tagiem <pages>
                std::getline(file, line); // Odczytujemy liniê z tagiem <year>

                // Szukamy roku w linii z tagiem <year>
                if (line.find("<year>") != std::string::npos) {
                    size_t start = line.find("<year>") + 6;
                    size_t end = line.find("</year>");
                    current_year = line.substr(start, end - start);
                }
            }

            // Jeœli linia zawiera s³owo kluczowe w tytule, sprawdzamy rok i wypisujemy artyku³
            if (!current_title.empty() && current_title.find(keyword) != std::string::npos && !article_printed) {
                // Sprawdzamy, czy rok pasuje do filtru
                if (current_year == filter_year) {
                    // Wypisz tytu³, autorów i rok artyku³u
                    std::cout << "Tytu³: " << current_title << std::endl;
                    std::cout << "Rok: " << (current_year.empty() ? "Brak roku" : current_year) << std::endl;
                    std::cout << "Autorzy: ";
                    for (const auto& author : current_authors) {
                        std::cout << author << "; ";
                    }
                    std::cout << std::endl;
                }
                article_printed = true; // Ustaw flagê, ¿e artyku³ zosta³ ju¿ wypisany
            }

            // Jeœli napotkamy koniec artyku³u
            if (line.find("</article>") != std::string::npos) {
                inside_article = false;
            }
        }

        // Wypisz numer linii co milion
        if (line_c % 10000000 == 0) {
            std::cout << line_c / 10000000 << std::endl;
        }
    }

    file.close();  // Zamknij plik po zakoñczeniu

    return 0;
}
