![Tinder](Tinder_logo.png)

# Speed Dating - Analyse exploratoire

Projet réalisé dans le cadre du bloc 2 de la certification CDSD (Jedha).

---

## Contexte

Tinder observe une baisse du nombre de matchs sur sa plateforme et veut comprendre ce qui pousse deux personnes à vouloir se revoir après une première rencontre. Pour y répondre, l'équipe marketing a mis à disposition un dataset issu d'expériences de speed dating organisées entre 2002 et 2004. Chaque ligne représente un échange de 4 minutes entre deux participants, avec le résultat (match ou non) et une série de notes sur différents critères.

---

## Ce que j'ai fait

Analyse exploratoire pour répondre à 5 questions concrètes :

1. **Attributs les moins désirables** - Ce que chaque genre valorise ou au contraire ignore chez un partenaire
2. **Attractivité perçue vs réelle** - Les gens lui accordent beaucoup d'importance, mais est-ce vraiment ce qui fait la différence ?
3. **Intérêts partagés vs origine raciale** - Lequel des deux facteurs a le plus d'impact sur le match ?
4. **Auto-perception** - Les participants savent-ils comment les autres les perçoivent ?
5. **Effet de position** - Vaut-il mieux être le premier ou le dernier speed date de la nuit ?

---

## Stack

- Python - Pandas, Plotly Express

---

## Données

Dataset issu de Columbia Business School (speed dating 2002–2004) :
```
https://full-stack-assets.s3.eu-west-3.amazonaws.com/M03-EDA/Speed+Dating+Data.csv
```
Le dictionnaire des variables est disponible dans `docs/Speed+Dating+Data+Key.pdf`.

---

## Structure

```
Tinder/
├── data/
│   ├── raw/
│   │   └── Speed_Dating_Data.csv
│   └── processed/
├── docs/
│   ├── 01-Speed_Dating.ipynb         # Énoncé du projet
│   └── Speed+Dating+Data+Key.pdf     # Dictionnaire des variables
├── notebooks/
│   └── tinder.ipynb
├── reports/
│   └── figures/
│       ├── 01_missing_values.png
│       ├── 02_gender_pie.png
│       ├── 03_age_distribution.png
│       ├── 04_goal_sunburst.png
│       ├── 05_match_global_pie.png
│       ├── 06_match_by_gender.png
│       ├── 07_criteria_by_gender.png
│       ├── 08_attribute_impact.png
│       ├── 09_like_score_vs_match.png
│       ├── 10_interest_correlation.png
│       ├── 11_interests_vs_race.png
│       ├── 12_self_perception_vs_reality.png
│       ├── 13_match_prediction.png
│       └── 14_position_effect.png
└── README.md
```

---

Julien CHARLIER - [(Github : Atomik31)](https://github.com/Atomik31)
