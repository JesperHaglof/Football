from bs4 import BeautifulSoup
import requests
import pandas as pd

class espnScraper:
    def __init__(self, league_link):
        self.link = league_link
        self.urls = []
        self.df = pd.DataFrame(columns=['Team', 'Pos', 'Player', 'Age', 'Nationality', 'Market Value (mEuros)'])
        self.team_names = []
        self.base_link = "http://www.espn.com/"

    def get_soup(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        html_text = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup

    def scrape(self):

        # Scrape ESPN


if __name__ == '__main__':

    url = 'https://www.espn.com/nfl/team/roster/_/name/buf/buffalo-bills'
    Scraper = espnScraper(url)
    Scraper.scrape()

