# create a https://arxiv.org/ webscrapper.
# 1. It asks the user what do they want to search.
# 2. after user enter their query
# 3. the scrapper searches for all the latest researches available
# 4. It shows user all the results it founds
# 5. then it asks which latest research paper they want to download.
# 6. it then downloads the latest available pdf file of the research.
# 7. then it asks if the user wants to continue
# 8. If yes continue and ask what do they want to search
# 9. If not quit

import requests
from bs4 import BeautifulSoup


# function to get the query from the user
def get_query():
    query = input("Enter your query: ")
    return query


# function to get the url of the query
def get_url(query):
    url = "https://arxiv.org/search/?query=" + query + "&searchtype=all&source=header"
    return url


# function to get the html of the url
def get_html(url):
    html = requests.get(url)
    return html


# function to get the soup of the html
def get_soup(html):
    soup = BeautifulSoup(html.text, "html.parser")
    return soup


# function to get the list of all the researches
def get_researches(soup):
    researches = soup.find_all("li", class_="arxiv-result")
    return researches


# function to get the title of the research
def get_title(research):
    title = research.find("p", class_="title is-5 mathjax").text
    return title


# function to get the authors of the research
def get_authors(research):
    authors = research.find("p", class_="authors").text
    return authors


# function to get the abstract of the research
def get_abstract(research):
    abstract = research.find(
        "span", class_="abstract-full has-text-grey-dark mathjax"
    ).text
    return abstract


# function to get the pdf link of the research
def get_pdf_link(research):
    pdf_link = research.find("a", class_=None)["href"].replace("abs", "pdf")
    return pdf_link



# function to show the results to the user
def show_results(researches):
    for i in range(len(researches)):
        print(f"{i+1}. {get_title(researches[i])}")
        print(f"   {get_authors(researches[i])}")
        print(f"   {get_abstract(researches[i])}")
        print(f"   {get_pdf_link(researches[i])}")
        print()


# function to get the index of the research the user wants to download
def get_index(researches):
    index = int(input("Enter the index of the research you want to download: "))
    return index


# function to run the program
def run():
    query = get_query()
    url = get_url(query)
    html = get_html(url)
    soup = get_soup(html)
    researches = get_researches(soup)
    show_results(researches)
    index = get_index(researches)
    pdf_link = get_pdf_link(researches[index - 1])
    pdf = requests.get(pdf_link)
    with open(f"{get_title(researches[index-1])}.pdf", "wb") as f:
        f.write(pdf.content)
    print("File downloaded successfully")


# main function
if __name__ == "__main__":
    while True:
        run()
        choice = input("Do you want to continue? (y/n): ")
        if choice == "n":
            break
