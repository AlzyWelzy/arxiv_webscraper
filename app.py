# Import Flask and other necessary modules
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

# Create a new instance of Flask
app = Flask(__name__)


# Define the route for the home page
@app.route("/")
def home():
    # Render the home page template
    return render_template("home.html")


# Define the route for the search results page
@app.route("/results", methods=["POST"])
def results():
    # Get the search query from the user
    query = request.form["query"]

    # Build the URL for the Arxiv search
    url = "https://arxiv.org/search/?query=" + query + "&searchtype=all&source=header"

    # Get the HTML content from the Arxiv search page
    html = requests.get(url).text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all the researches on the search page
    researches = soup.find_all("li", class_="arxiv-result")

    # Render the results page template with the search results
    return render_template("results.html", researches=researches)


# Define the route for the download page
@app.route("/download", methods=["POST"])
def download():
    # Get the PDF link for the selected research
    pdf_link = request.form["pdf_link"]

    # Get the PDF content from the link
    pdf = requests.get(pdf_link)

    # Set the response headers to download the PDF file
    headers = {"Content-Disposition": "attachment; filename=arxiv_paper.pdf"}

    # Return the PDF file as a response with the appropriate headers
    return pdf.content, 200, headers


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
