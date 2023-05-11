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

    def get_query(self):
        self.query = input("Enter your query: ")

    def get_url(self):
        self.url = "https://arxiv.org/search/?query=" + self.query + "&searchtype=all&source=header"

    def get_html(self):
        self.html = requests.get(self.url)

    def get_soup(self):
        self.soup = BeautifulSoup(self.html.text, "html.parser")

    def get_researches(self):
        self.researches = self.soup.find_all("li", class_="arxiv-result")

    def get_title(self, research):
        title = research.find("p", class_="title is-5 mathjax").text
        return title

    def get_authors(self, research):
        authors = research.find("p", class_="authors").text
        return authors

    def get_abstract(self, research):
        abstract = research.find("span", class_="abstract-full has-text-grey-dark mathjax").text
        return abstract

    def get_pdf_link(self, research):
        pdf_link = research.find("a", class_=None)["href"].replace("abs", "pdf")
        return pdf_link

    def show_results(self):
        for i, research in enumerate(self.researches):
            print(f"{i + 1}. {self.get_title(research)}")
            print(f"   {self.get_authors(research)}")
            print(f"   {self.get_abstract(research)}")
            print(f"   {self.get_pdf_link(research)}")
            print()

    def get_index(self):
        self.index = int(input("Enter the index of the research you want to download: "))

    def download_pdf(self):
        title = self.get_title(self.researches[self.index - 1]).strip()

        title = title.replace(" ", "_")

        pdf_link = self.get_pdf_link(self.researches[self.index - 1])

        pdf = requests.get(pdf_link)

        with open(title + ".pdf", "wb") as f:
            f.write(pdf.content)

        print("Downloaded Successfully!")

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
