import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Configuration du driver Firefox
GECKO_DRIVER_PATH = "C:/Users/teoch/Desktop/Projet Code/sofascore-dashboard/webdriver/geckodriver.exe"  # Chemin vers geckodriver
options = Options()
options.add_argument("--headless")  # Mode sans interface graphique
driver = webdriver.Firefox(service=Service(GECKO_DRIVER_PATH), options=options)

# URL de la page de l'équipe
url = "https://www.sofascore.com/fr/equipe/football/manchester-united/35"

def scrape_manchester_united_stats():
    try:
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        team_data = soup.find("a", href="/fr/equipe/football/manchester-united/35")
        if not team_data:
            return {"error": "Impossible de trouver les données de l'équipe."}

        stats = team_data.find_all("div", class_="Box klGMtt")
        current_matchday = stats[0].text.strip()
        wins = stats[1].text.strip()
        draws = stats[2].text.strip()
        losses = stats[3].text.strip()
        goal_difference = stats[4].text.strip()
        goals = stats[5].text.strip()
        points = stats[6].text.strip()

        goals_scored, goals_conceded = 0, 0
        if ":" in goals:
            goals_scored, goals_conceded = map(int, goals.split(":"))

        last_matches_div = team_data.find("div", class_="Box Flex iwTzXB gBmRiB")
        last_matches = []
        if last_matches_div:
            match_divs = last_matches_div.find_all("div", class_="Box klGMtt")
            for match_div in match_divs:
                title = match_div.get("title")
                if title:
                    match_info = re.match(r"(\d{2}/\d{2}/\d{4}), (\d+ – \d+) (.+?) – (.+)", title)
                    if match_info:
                        date, score, home_team, away_team = match_info.groups()
                        last_matches.append({
                            "date": date,
                            "score": score,
                            "home_team": home_team,
                            "away_team": away_team
                        })

        return {
            "team_name": "Manchester United",
            "current_matchday": int(current_matchday),
            "wins": int(wins),
            "draws": int(draws),
            "losses": int(losses),
            "goal_difference": goal_difference,
            "goals_scored": goals_scored,
            "goals_conceded": goals_conceded,
            #"points": int(points),
            "last_matches": last_matches
        }

    finally:
        driver.quit()
