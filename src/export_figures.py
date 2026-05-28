import pandas as pd
import plotly.express as px
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "reports" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Chargement ──────────────────────────────────────────────────────────────
df = pd.read_csv(
    Path(__file__).resolve().parents[1] / "data" / "raw" / "Speed_Dating_Data.csv",
    encoding="latin-1"
)

# Labels
df["gender"]      = df["gender"].replace({1: "Hommes", 0: "Femmes"})
df["match_label"] = df["match"].map({0: "No Match", 1: "Match"})
df["race_label"]  = df["race"].map({
    1: "Black/African Am.", 2: "Européen/Caucasien",
    3: "Latino/Hispanic",   4: "Asiatique",
    5: "Natif Américain",   6: "Autre"
})
df["goal_label"] = df["goal"].map({
    1: "Se divertir",          2: "Rencontrer des gens",
    3: "Obtenir un RDV",       4: "Relation sérieuse",
    5: "Pour l'expérience",    6: "Autre"
})

# Normalisation
attr_cols = ["attr1_1", "sinc1_1", "intel1_1", "fun1_1", "amb1_1", "shar1_1"]
def normalize_row(row):
    total = row[attr_cols].sum()
    if total == 0:
        return row[attr_cols]
    return (row[attr_cols] / total) * 100
df[attr_cols] = df[attr_cols].apply(normalize_row, axis=1)

def save(fig, name):
    path = OUTPUT_DIR / f"{name}.png"
    fig.write_image(str(path))
    print(f"  {path.name}")


print("Export des figures...")

# 01 — Valeurs manquantes
missing_data = df.isnull().mean().sort_values(ascending=False).reset_index()
missing_data.columns = ["Variable", "Pct_manquants"]
missing_data = missing_data[missing_data["Pct_manquants"] > 0]
fig = px.bar(missing_data, x="Pct_manquants", y="Variable", orientation="h",
             title="Pourcentage de valeurs manquantes par variable",
             color="Pct_manquants", color_continuous_scale="Reds", height=1200)
save(fig, "01_missing_values")

# 02 — Répartition par genre
gender_counts = df.groupby("gender")["gender"].count().reset_index(name="count")
fig = px.pie(gender_counts, values="count", names="gender",
             title="Répartition par genre",
             color_discrete_sequence=["#636EFA", "#EF553B"],
             width=600, height=400)
save(fig, "02_gender_pie")

# 03 — Distribution de l'âge
fig = px.histogram(df, x="age", color="gender",
                   title="Distribution de l'âge par genre",
                   labels={"age": "Âge", "gender": "Genre"},
                   nbins=20, width=750, height=450)
fig.add_vline(x=df["age"].mean(), line_dash="dash", line_color="black",
              annotation_text=f"Moy. {df['age'].mean():.1f} ans",
              annotation_position="top right")
save(fig, "03_age_distribution")

# 04 — Objectifs et résultats (sunburst)
df_sun = df.groupby(["goal_label", "match_label"]).size().reset_index(name="nombre")
fig = px.sunburst(df_sun, path=["goal_label", "match_label"], values="nombre",
                  color="goal_label",
                  title="Objectif de la soirée et résultat obtenu",
                  width=750, height=750)
fig.update_traces(textinfo="label+percent parent", insidetextorientation="radial")
save(fig, "04_goal_sunburst")

# 05 — Taux de match global (pie)
match_counts = df["match"].value_counts().reset_index()
match_counts["label"] = match_counts["match"].map({0: "No Match", 1: "Match"})
fig = px.pie(match_counts, values="count", names="label",
             title=f"Taux de match global — {df['match'].mean()*100:.1f}% de matchs",
             color="label",
             color_discrete_map={"Match": "#2ecc71", "No Match": "#e74c3c"},
             width=600, height=400)
save(fig, "05_match_global_pie")

# 06 — Taux de match par genre
taux_genre = df.groupby("gender")["match"].mean().reset_index()
taux_genre.columns = ["Genre", "Taux de match"]
taux_genre["Taux de match"] = (taux_genre["Taux de match"] * 100).round(1)
fig = px.bar(taux_genre, x="Genre", y="Taux de match",
             title="Taux de match par genre (%)", text="Taux de match",
             color="Genre", width=600, height=400)
fig.update_traces(texttemplate="%{text}%", textposition="outside")
fig.update_layout(showlegend=False)
save(fig, "06_match_by_gender")

# 07 — Q1 : Critères par genre
attr_labels = {
    "attr1_1": "Attractivité", "sinc1_1": "Sincérité",  "intel1_1": "Intelligence",
    "fun1_1":  "Fun",           "amb1_1":  "Ambition",   "shar1_1":  "Intérêts communs"
}
attr_by_gender = df.groupby("gender")[attr_cols].mean()
attr_by_gender.columns = [attr_labels[c] for c in attr_cols]
attr_long = attr_by_gender.reset_index().melt(id_vars="gender", var_name="Critère", value_name="Poids moyen")
fig = px.bar(attr_long, x="Critère", y="Poids moyen", color="gender", barmode="group",
             title="Ce que chaque genre recherche chez un partenaire (sur 100 points)",
             labels={"Poids moyen": "Poids moyen (pts)", "Critère": "", "gender": "Genre"},
             color_discrete_sequence=["#636EFA", "#EF553B"],
             width=800, height=500)
save(fig, "07_criteria_by_gender")

# 08 — Q2 : Impact réel des attributs sur le match
attributs = ["attr_o", "sinc_o", "intel_o", "fun_o", "amb_o", "shar_o"]
attr_names = {
    "attr_o": "Attractivité", "sinc_o": "Sincérité",  "intel_o": "Intelligence",
    "fun_o":  "Fun",           "amb_o":  "Ambition",   "shar_o":  "Intérêts partagés"
}
comp = df.groupby("match")[attributs].mean().T
comp.columns = ["No Match", "Match"]
comp["Différence"] = comp["Match"] - comp["No Match"]
comp = comp.reset_index()
comp["index"] = comp["index"].map(attr_names)
comp = comp.sort_values("Différence", ascending=False)
fig = px.bar(comp, x="index", y="Différence",
             title="Écart de score entre Match et No Match — impact réel de chaque attribut",
             labels={"index": "Attribut", "Différence": "Différence (Match − No Match)"},
             color="Différence", color_continuous_scale="Blues", width=750, height=500)
save(fig, "08_attribute_impact")

# 09 — Q2 : Score like_o selon le résultat
like_comp = df.groupby(["gender", "match_label"])["like_o"].mean().reset_index()
fig = px.bar(like_comp, x="gender", y="like_o", color="match_label", barmode="group",
             title='"J\'ai apprécié cette personne" — score moyen selon le résultat',
             labels={"like_o": "Score moyen (sur 10)", "gender": "Genre", "match_label": "Résultat"},
             color_discrete_map={"Match": "#2ecc71", "No Match": "#e74c3c"},
             width=700, height=450)
save(fig, "09_like_score_vs_match")

# 10 — Q3 : Corrélation d'intérêts vs match
int_corr_comp = df.groupby("match_label")["int_corr"].mean().reset_index()
fig = px.bar(int_corr_comp, x="match_label", y="int_corr",
             title="Corrélation des intérêts entre participants selon le résultat",
             labels={"int_corr": "Corrélation moyenne", "match_label": "Résultat"},
             color="match_label",
             color_discrete_map={"Match": "#2ecc71", "No Match": "#e74c3c"},
             width=600, height=400)
save(fig, "10_interest_correlation")

# 11 — Q3 : Intérêts partagés vs origine raciale
taux_global = df["match"].mean() * 100
comparison_df = pd.DataFrame({
    "Facteur": ["Intérêts partagés\nélevés (score ≥ 8)", "Même origine\nraciale"],
    "Taux de match (%)": [
        round(df[df["shar_o"] >= 8]["match"].mean() * 100, 1),
        round(df[df["samerace"] == 1]["match"].mean() * 100, 1)
    ]
})
fig = px.bar(comparison_df, x="Facteur", y="Taux de match (%)",
             title="Taux de match : intérêts partagés vs même origine raciale",
             text="Taux de match (%)", color="Facteur", width=650, height=450)
fig.update_traces(texttemplate="%{text}%", textposition="outside")
fig.add_hline(y=taux_global, line_dash="dash", line_color="grey",
              annotation_text=f"Moyenne : {taux_global:.1f}%",
              annotation_position="top right")
save(fig, "11_interests_vs_race")

# 12 — Q4 : Auto-perception vs réalité
self_vs_real = df[["gender", "attr3_1", "attr_o"]].dropna()
fig = px.scatter(self_vs_real, x="attr3_1", y="attr_o", color="gender",
                 trendline="ols",
                 title="Auto-évaluation vs note réellement reçue (attractivité)",
                 labels={"attr3_1": "Comment je me note", "attr_o": "Comment les autres me notent", "gender": "Genre"},
                 opacity=0.25, width=700, height=500)
fig.add_shape(type="line", x0=1, y0=1, x1=10, y1=10,
              line=dict(color="black", dash="dot", width=1))
save(fig, "12_self_perception_vs_reality")

# 13 — Q4 : Prédiction du match (prob_o)
prob_comp = df.groupby("match_label")["prob_o"].mean().reset_index()
fig = px.bar(prob_comp, x="match_label", y="prob_o",
             title="Probabilité de match estimée par le partenaire vs résultat réel",
             labels={"prob_o": "Probabilité estimée (sur 10)", "match_label": "Résultat réel"},
             color="match_label",
             color_discrete_map={"Match": "#2ecc71", "No Match": "#e74c3c"},
             text="prob_o", width=600, height=400)
fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
save(fig, "13_match_prediction")

# 14 — Q5 : Effet de la position dans la soirée
match_by_order = df.groupby("order")["match"].mean().reset_index()
match_by_order.columns = ["Position", "Taux de match"]
match_by_order["Taux de match"] = (match_by_order["Taux de match"] * 100).round(2)
fig = px.line(match_by_order, x="Position", y="Taux de match",
              title="Taux de match (%) selon la position dans la soirée",
              markers=True, labels={"Taux de match": "Taux de match (%)"},
              width=750, height=480)
fig.add_hline(y=df["match"].mean() * 100, line_dash="dash", line_color="red",
              annotation_text=f"Moyenne : {df['match'].mean()*100:.1f}%",
              annotation_position="top right")
save(fig, "14_position_effect")

print(f"\nDone — 14 figures exportées dans {OUTPUT_DIR}")
