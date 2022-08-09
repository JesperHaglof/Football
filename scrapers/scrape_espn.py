from bs4 import BeautifulSoup
import requests
import pandas as pd

class espnScraper:
    def __init__(self, league_link):
        self.roster_end_links = None
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

    def _scrape_roster_end_links(self):

        # Scrape ESPN
        team_page_soup = self.get_soup(self.link)
        # Get all tables from team page
        tables = team_page_soup.find_all('div', class_="mod-container mod-open-list mod-no-footer mod-teams-list-small")
        # loop through to access all roster links
        for line in tables:
            print(line)
            elements = line.find_all('a')
            for element in elements:
                if "padding-top" in str(element):
                    roster_link = str(element).split('href="')[1].split('" ')[0]
                    print(roster_link)
                    self.roster_end_links.append(roster_link)

    def scrape(self):

        # Step 1: Get roster end links from team page
        self._scrape_roster_end_links()





if __name__ == '__main__':

    url = 'http://www.espn.com/nfl/players'
    Scraper = espnScraper(url)
    Scraper.scrape()

