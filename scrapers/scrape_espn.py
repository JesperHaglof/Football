from bs4 import BeautifulSoup
import requests
import pandas as pd

class espnScraper:
    def __init__(self, league_link):
        self.player_links = []
        self.roster_end_links = []
        self.link = league_link
        self.urls = []
        self.df = pd.DataFrame(columns=['Team', 'Pos', 'Player', 'Age', 'Nationality', 'Market Value (mEuros)'])
        self.team_names = []
        self.base_link = "http://www.espn.com"
        self.df = pd.DataFrame(columns = ["Team", "Pos", "Nr", "First Name", "Last Name", "Birth Date", "Age",
                                          "Length", "Weight", "College", "First Season", "Draft Info", "Status"])


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
            elements = line.find_all('a')
            for element in elements:
                if "padding-top" in str(element):
                    roster_link = str(element).split('href="')[1].split('" ')[0]
                    self.roster_end_links.append(roster_link)

    def scrape(self):

        # Step 1: Get roster end links from team page
        self._scrape_roster_end_links()
        # Step 2: Get all player info from rosters
        self._scrape_rosters()

    def _scrape_rosters(self):

        # Function to scrape rosters from espn

        for end_link in self.roster_end_links:
            roster_link = self.base_link + end_link
            team_name = self._scrape_team_name(roster_link)
            print(team_name)
            # Find player links
            self._scrape_player_links(roster_link)
            # Scrape down player info, from profile page
            self._scrape_player_info(team_name)
            # Empty player links again
            self.player_links = []

    def _scrape_team_name(self, roster_link):

        roster_page_soup = self.get_soup(roster_link)
        title = roster_page_soup.find_all('h1', class_="headline headline__h1 dib")
        team_name = title[0].text.replace(' Roster', '')

        return team_name

    def _scrape_player_links(self, roster_link):

        roster_page_soup = self.get_soup(roster_link)
        players = roster_page_soup.find_all('a', class_="AnchorLink")
        for player in players:
            if "headshot inline-block relative" in str(player):
                player_link = str(player).split('href="')[1].split('" ')[0]
                self.player_links.append(player_link)

    def _scrape_player_info(self, team_name):

        # Scrape down player information from roster links
        for player_link in self.player_links:
            player_soup = self.get_soup(player_link)
            first_name = player_soup.find_all('span', class_="truncate min-w-0 fw-light")[0].text
            last_name = player_soup.find_all('span', class_="truncate min-w-0")[0].text

            bio = player_soup.find_all('div', class_= "PlayerHeader__Main_Aside min-w-0 flex-grow flex-basis-0")[0]
            if len(bio.find_all("li", class_="")) > 1:
                number = bio.find_all("li", class_="")[0].text.replace("#","")
                position = bio.find_all("li", class_="")[1].text
            else:
                position = bio.find_all("li", class_="")[0].text

            bio2 = player_soup.find_all('div', class_="fw-medium clr-black")
            info = []
            for line in bio2:
                info.append(line.text)
                print(line.text)
            length = info[0].split(", ")[0]
            weight = info[0].split(", ")[1]
            birth_date = info[1].split(" (")[0]
            if " (" in info[1]:
                year = info[1].split(" (")[1].replace(")","")
                if info[2] in ["Active", "Out"]:
                    status = info[2]
                else:
                    college = info[2]
                if "Rd" in info[3]:
                    first_season = info[3].split(": ")[0]
                    drafted_info = info[3].split(": ")[1]
                    status = info[4]
                else:
                    if "th" in info[3] or "nd" in info[3] or "rd" in info[3]:
                        exp = info[3].split("th")[0]
                        first_season =  2022 - int(exp) + 1
                    else:
                        status=info[3]
                    if len(info) > 4:
                        if info[4] == "Rookie":
                            first_season = 2022
                            drafted_info = "Undrafted"
                        else:
                            if "th" in info[4]:
                                exp = info[4].split("th")[0]
                                first_season = 2022 - int(exp) + 1
                            elif "rd" in info[4]:
                                exp = info[4].split("rd")[0]
                                first_season = 2022 - int(exp) + 1
                            elif "nd" in info[4]:
                                if "London" in info[4]:
                                    college = "London, England"
                                else:
                                    exp = info[4].split("nd")[0]
                                    first_season = 2022 - int(exp) + 1
                            else:
                                exp = 1
                                first_season = 2022
                            drafted_info = "Undrafted"
            else:
                college = info[1]
                status = info[2]
                if info[3] == "Rookie":
                    first_season = 2022
                    drafted_info = "Undrafted"
                else:
                    if "th" in info[3]:
                        exp = info[3].split("th")[0]
                    elif "rd" in info[3]:
                        exp = info[3].split("rd")[0]
                    elif "nd" in info[3]:
                        exp = info[3].split("rd")[0]
                    first_season = 2022 - int(exp) + 1
                    drafted_info = "Undrafted"

            row = [team_name, position, number, first_name, last_name, birth_date, year, length, weight, college, first_season, drafted_info, status]
            self.df.loc[len(self.df)] = row
            print(row)



if __name__ == '__main__':

    url = 'http://www.espn.com/nfl/players'
    Scraper = espnScraper(url)
    Scraper.scrape()

