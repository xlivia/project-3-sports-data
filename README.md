# Project 3 Fifa Analytics

### Table of Contents
1. [Project Proposal](#project-proposal)
2. [Data Source](#data-source)
3. [Project File Structure](#project-file-structure)
4. [Dependencies](#dependencies)
5. [Start Up](#development-start-up)

## Project Proposal
The aim of our project is to create a Sports Analytics Dashboard that provides users with statistics and visualizations for sports data, such as player performance, team rankings, and game outcomes.
The dashboard will allow users to explore and analyze the data based on different filters, enabling them to gain insights and make data-driven decisions.
The dashboard page will include multiple charts that update from the same data, providing users with a comprehensive view of the sports analytics.
We will utilize a Python Flask-powered API, HTML/CSS, JavaScript, and a database (e.g., SQL, MongoDB, SQLite) to develop an interactive and informative dashboard.

## Data Source
[Kaggle Fifa 20 Dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-20-complete-player-dataset?select=players_20.csv)

## Project File Structure
```
Project_3/
├── data/
│   ├── cleaned_data/
│   │   ├── players_15.csv
│   │   ├── players_16.csv
│   │   ├── players_17.csv
│   │   ├── players_18.csv
│   │   ├── players_19.csv
│   │   └── players_20.csv
│   ├── db/
│   │   └── database.db
│   ├── json/
│   │   ├── players_15.json
│   │   ├── players_16.json
│   │   ├── players_17.json
│   │   ├── players_18.json
│   │   ├── players_19.json
│   │   └── players_20.json
│   ├── raw_data/
│   │   ├── players_15.csv
│   │   ├── players_16.csv
│   │   ├── players_17.csv
│   │   ├── players_18.csv
│   │   ├── players_19.csv
│   │   ├── players_20.csv
│   │   └── teams_and_leagues.csv
│   └── clean_data.ipynb
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── map.js
│       ├── league.js
│       ├── player.js
│       └── logic.js
├── templates/
│   ├── map.html
│   ├── index.html
│   ├── league.html
│   └── player.html
├── app.py
└── README.md
```

## Dependencies
1. `pip install flask pandas sqlalchemy`

## Development Start Up
1. To start the server Flask app make sure you are in the root directory of the project and run `python app.py`
2. After running `python app.py` the server should be running on `http://127.0.0.1:5000`
3. Go to `http://127.0.0.1:5000` in your broswer and you should see the site.
    - The main page of the application (`index.html`) will display the player data fetched from the database.

[Back To Top](#project-3-fifa-analytics)