import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import SMOTE


def simular_partido(home_team, away_team, matches, team_summary):
    home_features = team_summary.loc[home_team]
    away_features = team_summary.loc[away_team]
    features = pd.DataFrame({
        'home_advantage': [1],
        'diff_goalsScored': [home_features['goalsScored'] - away_features['goalsScored']],
        'diff_goalsConceded': [home_features['goalsConceded'] - away_features['goalsConceded']]
    })
    result = best_model.predict(features)[0]
    if result == 1:
        return home_team
    elif result == 0:
        return away_team
    else:
        return np.random.choice([home_team, away_team])
    
def imprimir_llave(etapa, enfrentamientos):
    print(f"\n--- {etapa.upper()} ---")
    for i, (local, visitante, ganador) in enumerate(enfrentamientos, start=1):
        print(f"Partido {i}: {local} vs {visitante} -> Ganador: {ganador}")

def simular_torneo(teamsList, matches, team_summary):
    print("\nSIMULACIÓN DE LIGUILLA")
    print(f"Equipos clasificados: {', '.join(teamsList)}")
    ganador_7_8 = simular_partido(teamsList[6], teamsList[7], matches, team_summary)
    print(f"Partido Reclasificación 7-8: {teamsList[6]} vs {teamsList[7]} -> Ganador: {ganador_7_8}")
    
    ganador_9_10 = simular_partido(teamsList[8], teamsList[9], matches, team_summary)
    print(f"Partido Reclasificación 9-10: {teamsList[8]} vs {teamsList[9]} -> Ganador: {ganador_9_10}")
    
    segundo_repechaje = simular_partido(ganador_9_10, teamsList[7] if ganador_7_8 == teamsList[6] else teamsList[6], matches, team_summary)
    print(f"Partido Segundo Repechaje: {ganador_9_10} vs {teamsList[7] if ganador_7_8 == teamsList[6] else teamsList[6]} -> Ganador: {segundo_repechaje}")
    equipos_cuartos = [teamsList[0], teamsList[1], teamsList[2], teamsList[3], teamsList[4], teamsList[5], ganador_7_8, segundo_repechaje]
    cuartos_enfrentamientos = [
        (equipos_cuartos[0], equipos_cuartos[7]),
        (equipos_cuartos[1], equipos_cuartos[6]),
        (equipos_cuartos[2], equipos_cuartos[5]),
        (equipos_cuartos[3], equipos_cuartos[4]),
    ]
    ganadores_cuartos = []
    for local, visitante in cuartos_enfrentamientos:
        ganador = simular_partido(local, visitante, matches, team_summary)
        ganadores_cuartos.append(ganador)
    imprimir_llave("Cuartos de final", [(l, v, g) for (l, v), g in zip(cuartos_enfrentamientos, ganadores_cuartos)])
    semifinales_enfrentamientos = [
        (ganadores_cuartos[0], ganadores_cuartos[3]),
        (ganadores_cuartos[1], ganadores_cuartos[2]),
    ]
    ganadores_semifinales = []
    for local, visitante in semifinales_enfrentamientos:
        ganador = simular_partido(local, visitante, matches, team_summary)
        ganadores_semifinales.append(ganador)
    imprimir_llave("Semifinales", [(l, v, g) for (l, v), g in zip(semifinales_enfrentamientos, ganadores_semifinales)])
    final_enfrentamiento = (ganadores_semifinales[0], ganadores_semifinales[1])
    ganador_final = simular_partido(*final_enfrentamiento, matches, team_summary)
    imprimir_llave("Final", [(final_enfrentamiento[0], final_enfrentamiento[1], ganador_final)])
    print(f"\n¡CAMPEÓN: {ganador_final.upper()}!\n")

df_apertura = pd.read_csv('apertura_2024.csv')
teamsList = df_apertura['team'].values.tolist()
teamsList = teamsList[:10]
matches = pd.read_csv('matchess.csv')
matches = matches.dropna(subset=['score'])
matches['score'] = matches['score'].str.extract(r'(\d+–\d+)', expand=False)
matches[['home_goals', 'away_goals']] = matches['score'].str.split('–', expand=True)
matches['home_goals'] = pd.to_numeric(matches['home_goals'])
matches['away_goals'] = pd.to_numeric(matches['away_goals'])
local_summary = matches.groupby('home_team')['home_goals'].sum().reset_index()
local_summary.rename(columns={'home_team': 'team', 'home_goals': 'home_goals_total'}, inplace=True)
away_summary = matches.groupby('away_team')['away_goals'].sum().reset_index()
away_summary.rename(columns={'away_team': 'team', 'away_goals': 'away_goals_total'}, inplace=True)
local_conceded_summary = matches.groupby('home_team')['away_goals'].sum().reset_index()
local_conceded_summary.rename(columns={'home_team': 'team', 'away_goals': 'home_conceded'}, inplace=True)
away_conceded_summary = matches.groupby('away_team')['home_goals'].sum().reset_index()
away_conceded_summary.rename(columns={'away_team': 'team', 'home_goals': 'away_conceded'}, inplace=True)
team_summary_scored = pd.merge(local_summary, away_summary, on='team', how='outer').fillna(0)
team_summary_conceded = pd.merge(local_conceded_summary, away_conceded_summary, on='team', how='outer').fillna(0)
team_summary_complete = pd.merge(team_summary_scored, team_summary_conceded, on='team', how='outer').fillna(0)
team_summary_complete['goalsScored'] = team_summary_complete['home_goals_total'] + team_summary_complete['away_goals_total']
team_summary_complete['goalsConceded'] = team_summary_complete['home_conceded'] + team_summary_complete['away_conceded']
team_summary_complete = team_summary_complete.set_index("team")
matches['result'] = matches.apply(
    lambda row: 1 if row['home_goals'] > row['away_goals'] else (0 if row['home_goals'] < row['away_goals'] else -1),
    axis=1
)
matches = pd.merge(matches, team_summary_complete, left_on='home_team', right_index=True, how='left')
matches = pd.merge(matches, team_summary_complete, left_on='away_team', right_index=True, suffixes=('_home', '_away'), how='left')
matches['home_advantage'] = 1
matches['diff_goalsScored'] = matches['goalsScored_home'] - matches['goalsScored_away']
matches['diff_goalsConceded'] = matches['goalsConceded_home'] - matches['goalsConceded_away']
features = ['home_advantage', 'diff_goalsScored', 'diff_goalsConceded']
X = matches[features]
y = matches['result']
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)
param_grid = {
    'C': [0.01, 0.1, 1, 10, 100],
    'solver': ['liblinear', 'saga'],
    'max_iter': [100, 200, 300]
}
logreg = LogisticRegression(multi_class='ovr', random_state=42)
grid_search = GridSearchCV(logreg, param_grid, cv=5, scoring='accuracy', verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
simular_torneo(teamsList, matches, team_summary_complete)
