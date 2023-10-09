import requests
from bs4 import BeautifulSoup


class LinkScrapper:

    def __init__(self, url):
        self.url = url

    def scrap_text(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            soup = soup.find("section", {"id": "content"})
            for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
                script.extract()
            text = " ".join(t.strip() for t in soup.stripped_strings)

            return text
        except requests.RequestException as e:
            return f"An error occurred while fetching the page: {e}"
