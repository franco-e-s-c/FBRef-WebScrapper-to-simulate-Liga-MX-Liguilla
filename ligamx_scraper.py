from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

res = requests.get("https://fbref.com/es/comps/31/2019-2020/horario/Marcadores-y-partidos-de-2019-2020-Liga-MX")
comm = re.compile("<!--|-->")
soup = BeautifulSoup(comm.sub("",res.text),'lxml')
all_tables = soup.findAll("tbody")
liguilla = soup.findAll("div", class_="matchup")
matches_table = soup.find("table", id="sched_all")
liguilla_features = [
    'Instance', 
    'Match Date', 
    'Home Team', 
    'Result', 
    'Away Team',
    'Winner', 
    'Note'
]
liguilla_apertura = liguilla[0:4]
liguilla_clausura = liguilla[4:8]
league_table = all_tables[0]
league_features = [
    "games",
    "wins",
    "ties",
    "losses",
    "goals_for",
    "goals_against",
    "goal_diff",
    "points",
    "points_avg",
    "xg_for",
    "xg_against",
    "xg_diff",
    "xg_diff_per90",
    "attendance_per_g",
    "top_team_scorers",
    "top_keeper"
]
league_ha_table = all_tables[1]
league_ha_features = [
    "home_games",
    "home_wins",
    "home_ties",
    "home_losses",
    "home_goals_for",
    "home_goals_against",
    "home_goal_diff",
    "home_points",
    "home_points_avg",
    "home_xg_for",
    "home_xg_against",
    "home_xg_diff",
    "home_xg_diff_per90",
    "away_games",
    "away_wins",
    "away_ties",
    "away_losses",
    "away_goals_for",
    "away_goals_against",
    "away_goal_diff",
    "away_points",
    "away_points_avg",
    "away_xg_for",
    "away_xg_against",
    "away_xg_diff",
    "away_xg_diff_per90"
]
league_apertura = all_tables[2]
league_apertura_features =[
    "games",
    "wins",
    "ties",
    "losses",
    "goals_for",
    "goals_against",
    "goal_diff",
    "points",
    "points_avg",
    "xg_for",
    "xg_against",
    "xg_diff",
    "xg_diff_per90",
    "notes"
]
league_clausura = all_tables[3]
league_clausura_features = [
    "games",
    "wins",
    "ties",
    "losses",
    "goals_for",
    "goals_against",
    "goal_diff",
    "points",
    "points_avg",
    "xg_for",
    "xg_against",
    "xg_diff",
    "xg_diff_per90",
    "notes"
]
partidos_features = [
    "dayofweek",
    "home_team",
    "score",
    "away_team"
]
links = [
    "https://fbref.com/es/comps/31/2019-2020/horario/Marcadores-y-partidos-de-2019-2020-Liga-MX",
    "https://fbref.com/es/comps/31/2020-2021/horario/Marcadores-y-partidos-de-2020-2021-Liga-MX",
    "https://fbref.com/es/comps/31/2021-2022/horario/Marcadores-y-partidos-de-2021-2022-Liga-MX",
    "https://fbref.com/es/comps/31/2022-2023/horario/Marcadores-y-partidos-de-2022-2023-Liga-MX",
    "https://fbref.com/es/comps/31/2023-2024/horario/Marcadores-y-partidos-de-2023-2024-Liga-MX",
    "https://fbref.com/es/comps/31/2018-2019/horario/Marcadores-y-partidos-de-2018-2019-Liga-MX",
    "https://fbref.com/es/comps/31/2017-2018/horario/Marcadores-y-partidos-de-2017-2018-Liga-MX",
    "https://fbref.com/es/comps/31/2016-2017/horario/Marcadores-y-partidos-de-2016-2017-Liga-MX",
    "https://fbref.com/es/comps/31/2015-2016/horario/Marcadores-y-partidos-de-2015-2016-Liga-MX",
    "https://fbref.com/es/comps/31/2014-2015/horario/Marcadores-y-partidos-de-2014-2015-Liga-MX",
    "https://fbref.com/es/comps/31/2013-2014/horario/Marcadores-y-partidos-de-2013-2014-Liga-MX",
    "https://fbref.com/es/comps/31/2012-2013/horario/Marcadores-y-partidos-de-2012-2013-Liga-MX",
    "https://fbref.com/es/comps/31/2011-2012/horario/Marcadores-y-partidos-de-2011-2012-Liga-MX",
    "https://fbref.com/es/comps/31/2010-2011/horario/Marcadores-y-partidos-de-2010-2011-Liga-MX",
    "https://fbref.com/es/comps/31/2009-2010/horario/Marcadores-y-partidos-de-2009-2010-Liga-MX",
    "https://fbref.com/es/comps/31/2008-2009/horario/Marcadores-y-partidos-de-2008-2009-Liga-MX",
    "https://fbref.com/es/comps/31/2007-2008/horario/Marcadores-y-partidos-de-2007-2008-Liga-MX",
    "https://fbref.com/es/comps/31/2006-2007/horario/Marcadores-y-partidos-de-2006-2007-Liga-MX",
    "https://fbref.com/es/comps/31/2005-2006/horario/Marcadores-y-partidos-de-2005-2006-Liga-MX",
    "https://fbref.com/es/comps/31/2004-2005/horario/Marcadores-y-partidos-de-2004-2005-Liga-MX",
    "https://fbref.com/es/comps/31/2003-2004/horario/Marcadores-y-partidos-de-2003-2004-Liga-MX",
]


def genTable(league_table, features_wanted):
    pre_df = {feature: [] for feature in features_wanted}
    rows_squad = league_table.find_all('tr')
    for row in rows_squad:
        if(row.find('th',{"scope":"row"}) != None):
            pos = row.find('th',{"data-stat":"rank"}).text.strip().encode().decode("utf-8")
            name = row.find('td',{"data-stat":"team"}).text.strip().encode().decode("utf-8")
            if 'rank' in pre_df:
                pre_df['rank'].append(pos)
            else:
                pre_df['rank'] = [pos]
            if 'team' in pre_df:
                pre_df['team'].append(name)
            else:
                pre_df['team'] = [name]
            for f in features_wanted:
                cell = row.find("td",{"data-stat": f})
                a = cell.text.strip().encode()
                text=a.decode("utf-8")
                pre_df[f].append(text)
    df_squad = pd.DataFrame.from_dict(pre_df)
    return df_squad[["rank", "team"] + [col for col in features_wanted]]

def genLiguilla(liguilla, features_wanted):
    pre_df_matchup = {feature: [] for feature in features_wanted}
    instance = soup.findAll("h3")
    instance = instance[0:4]
    i=0
    for matchup in liguilla:
        insta = instance[i].text.strip()
        i=i+1
        match_summary = matchup.find_all('div', recursive=False)
        for matches_sum in match_summary:
            match_date = matches_sum.find(class_='match-date').text.strip()
            
            teams = matches_sum.find_all(class_='matchup-team')
            team1 = teams[0].text.strip().split("\n")[-1].strip()
            score = matches_sum.find(class_='match-detail').text.strip()
            team2 = teams[1].text.strip().split("\n")[0].strip()

            team1_winner = 'winner' in teams[0].attrs.get('class', [])
            team2_winner = 'winner' in teams[1].attrs.get('class', [])
            
            note = matches_sum.find(class_='matchup-note').text.strip()

            pre_df_matchup['Instance'].append(insta)
            pre_df_matchup['Match Date'].append(match_date)
            pre_df_matchup['Home Team'].append(team1)
            pre_df_matchup['Result'].append(score)
            pre_df_matchup['Away Team'].append(team2)
            pre_df_matchup['Note'].append(note)
            pre_df_matchup['Winner'].append(team1 if team1_winner else (team2 if team2_winner else "Draw"))

            matches_container = matches_sum.find_all(class_="matches")
            if matches_container:
                for matches in matches_container:
                    match_ind = matches.find_all('div', recursive=False)
                    j=0
                    for match in match_ind:
                        leg = ("First Leg" if j == 0 else "Second Leg")
                        j=j+1
                        match_date_individual = match.find(class_="match-date").small.get_text()
                        teams_individual = match.find_all(class_='matchup-team')
                        team1_individual = teams_individual[0].text.strip()
                        team2_individual = teams_individual[1].text.strip()
                        score_individual = match.find(class_='match-detail').text.strip()

                        team1_winner_individual = 'winner' in teams_individual[0].attrs.get('class', [])
                        team2_winner_individual = 'winner' in teams_individual[1].attrs.get('class', [])

                        note_individual = ""

                        pre_df_matchup['Instance'].append(leg)
                        pre_df_matchup['Match Date'].append(match_date_individual)
                        pre_df_matchup['Home Team'].append(team1_individual)
                        pre_df_matchup['Result'].append(score_individual)
                        pre_df_matchup['Away Team'].append(team2_individual)
                        pre_df_matchup['Note'].append(note_individual)
                        pre_df_matchup['Winner'].append(team1_individual if team1_winner_individual else (team2_individual if team2_winner_individual else "Draw"))
                        
    
    df_matchup = pd.DataFrame.from_dict(pre_df_matchup)
    return df_matchup[['Instance', 'Match Date', 'Home Team', 'Result', 'Away Team', 'Note', 'Winner']]

def genPartidos(matches_table, features_wanted):
    pre_df = {feature: [] for feature in features_wanted}
    matches_body = matches_table.find('tbody')
    matches_rows = matches_body.find_all('tr', class_=lambda class_value: not (class_value and any(c in ["spacer" "partial_table" "result_all", "thead"] for c in class_value)))
    for row in matches_rows:
        if(row.has_attr('class')):
            continue

        for feature in features_wanted:
            cell = row.find("td",{"data-stat": feature})
            a = cell.text.strip().encode()
            text=a.decode("utf-8")
            pre_df[feature].append(text)
    df_match = pd.DataFrame.from_dict(pre_df)
    return df_match[[col for col in features_wanted]]

def genAllDataPartidos(links, features_wanted, output_csv):
    all_matches = []

    for link in links:
        res = requests.get(link)
        comm = re.compile("<!--|-->")
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        matches_table = soup.find("table", id="sched_all")
        if matches_table:
            print(link)
            season_matches = genPartidos(matches_table, features_wanted)
            all_matches.append(season_matches)
        else:
            print(f"No se encontró la tabla en el enlace: {link}")


    if all_matches:
        final_df = pd.concat(all_matches, ignore_index=True)
        final_df.to_csv(output_csv, encoding="utf-8-sig", index=False)
        print(f"Archivo guardado como {output_csv}")
    else:
        print("No se encontraron datos en los enlaces proporcionados.")


genAllDataPartidos(links, partidos_features, "matchess.csv")

df_liguilla = genLiguilla(liguilla_apertura, liguilla_features)
df_liguilla.to_csv("liguilla.csv", encoding="utf-8-sig")

df_apertura = genTable(league_apertura, league_apertura_features)
df_apertura.to_csv("apertura_2019.csv", encoding="utf-8-sig")

df_clausura = genTable(league_clausura, league_clausura_features)
df_clausura.to_csv("clausura_2020.csv", encoding="utf-8-sig")

df_HomeAway = genTable(league_ha_table, league_ha_features)
df_HomeAway.to_csv("HomeAwayResults_2018_2019.csv", encoding="utf-8-sig")