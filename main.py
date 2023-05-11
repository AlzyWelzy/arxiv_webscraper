import requests
from bs4 import BeautifulSoup


class ArxivScraper:
    def __init__(self):
        self.query = None
        self.url = None
        self.html = None
        self.soup = None
        self.researches = None
        self.index = None

    # function to get the query from the user
    def get_query(self):
        self.query = input("Enter your query: ")

    # function to get the url of the query
    def get_url(self):
        self.url = "https://arxiv.org/search/?query=" + self.query + "&searchtype=all&source=header"

    # function to get the html of the url
    def get_html(self):
        self.html = requests.get(self.url)

    # function to get the soup of the html
    def get_soup(self):
        self.soup = BeautifulSoup(self.html.text, "html.parser")

    # function to get the list of all the researches
    def get_researches(self):
        self.researches = self.soup.find_all("li", class_="arxiv-result")

    # function to get the title of the research
    def get_title(self, research):
        title = research.find("p", class_="title is-5 mathjax").text
        return title

    # function to get the authors of the research
    def get_authors(self, research):
        authors = research.find("p", class_="authors").text
        return authors

    # function to get the abstract of the research
    def get_abstract(self, research):
        abstract = research.find("span", class_="abstract-full has-text-grey-dark mathjax").text
        return abstract

    # function to get the pdf link of the research
    def get_pdf_link(self, research):
        pdf_link = research.find("a", class_=None)["href"].replace("abs", "pdf")
        return pdf_link

    # function to show the results to the user
    def show_results(self):
        for i, research in enumerate(self.researches):
            print(f"{i+1}. {self.get_title(research)}")
            print(f"   {self.get_authors(research)}")
            print(f"   {self.get_abstract(research)}")
            print(f"   {self.get_pdf_link(research)}")
            print()

    # function to get the index of the research the user wants to download
    def get_index(self):
        self.index = int(input("Enter the index of the research you want to download: "))

    # function to download the pdf file
    def download_pdf(self):
        pdf_link = self.get_pdf_link(self.researches[self.index - 1])
        pdf = requests.get(pdf_link)
        with open(f"{self.get_title(self.researches[self.index-1])}.pdf", "wb") as f:
            f.write(pdf.content)
        print("File downloaded successfully")

    # function to run the program
    def run(self):
        self.get_query()
        self.get_url()
        self.get_html()
        self.get_soup()
        self.get_researches()
        self.show_results()
        self.get_index()
        self.download_pdf()


if __name__ == "__main__":
    arxiv_scraper = ArxivScraper()
    while True:
        arxiv_scraper.run()
        choice = input("Do you want to continue? (y/n): ")
        if choice == "n":
            break
