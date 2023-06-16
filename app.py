from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, inspect
import pandas as pd
import os
import json
import requests
import csv

app = Flask(__name__)

def get_nationalities_with_coordinates():
    # Check if the JSON file already exists
    json_file_path = "data/json/player_nationalities.json"
    if os.path.exists(json_file_path):
        return  # Skip creating the file if it already exists
    # Create a dictionary to store nationalities and their coordinates
    nationalities = {}
    # Loop through all tables in the database
    for year in range(15, 21):
        table_name = f"players_{year}"
        # Load the table as a DataFrame
        df = pd.read_csv(f"data/cleaned_data/{table_name}.csv")
        # Create a dictionary to store the count of players and the list of players for each country
        country_data = {}
        # Loop through each row in the DataFrame
        for _, row in df.iterrows():
            nationality = row["nationality"]
            if nationality not in country_data:
                country_data[nationality] = {"count": 0, "players": []}
            country_data[nationality]["count"] += 1
            country_data[nationality]["players"].append(row["short_name"])
        # Add the country data to the nationalities dictionary
        for country, data in country_data.items():
            if country not in nationalities:
                nationalities[country] = {"country": country, "longitude": "", "latitude": ""}
            nationalities[country][f"20{year}"] = {"count": data["count"], "players": data["players"]}
    # Save the nationalities dictionary as a JSON file
    json_file_path = "data/json/player_nationalities.json"
    with open(json_file_path, "w") as json_file:
        json.dump(list(nationalities.values()), json_file, indent=4)

def csv_to_json():
    csv_folder_path = "data/cleaned_data/"
    json_folder_path = "data/json/"
    csv_files = ['players_15.csv', 'players_16.csv', 'players_17.csv', 'players_18.csv', 'players_19.csv', 'players_20.csv']
    for csv_file in csv_files:
        csv_file_path = os.path.join(csv_folder_path, csv_file)
        json_file_path = os.path.join(json_folder_path, f"{csv_file.split('.')[0]}.json")
        # Check if the JSON file already exists
        if os.path.exists(json_file_path):
            continue  # Skip this iteration and proceed to the next CSV file
        # Read the CSV file with different encodings
        encodings = ['utf-8', 'latin1']
        for encoding in encodings:
            try:
                with open(csv_file_path, "r", encoding=encoding) as csv_file:
                    csv_data = csv.DictReader(csv_file)
                    json_data = [row for row in csv_data]
                break  # Stop trying encodings if successful
            except UnicodeDecodeError:
                pass  # Try the next encoding
        else:
            print(f"Failed to read the CSV file: {csv_file}")
            continue  # Skip this iteration if the CSV file cannot be read
        # Write the JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

def load_csv_to_database():
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('sqlite:///data/db/database.db')
    inspector = inspect(engine)
    # Get a list of all CSV files in the data directory
    csv_files = [file for file in os.listdir('data/cleaned_data') if file.endswith('.csv')]
    # Load each CSV file into the database
    for file in csv_files:
        table_name = file.split('.')[0]
        # Check if the table already exists in the database
        if not inspector.has_table(table_name):
            csv_file = os.path.join('data/cleaned_data', file)
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file)
            # Insert the DataFrame into the database table
            df.to_sql(table_name, engine, if_exists='replace', index=False)

@app.route('/')
def index():
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('sqlite:///data/db/database.db')
    # Query the required columns from all the tables
    tables = ['players_15', 'players_16', 'players_17', 'players_18', 'players_19', 'players_20']
    # Fetch the results from each table and concatenate them
    players = []
    for table in tables:
        query = f"SELECT * FROM {table} LIMIT 100"
        results = engine.execute(query)
        players += [dict(row) for row in results]
    # Render the index.html template and pass the players data to it
    return render_template('index.html', players=players)

@app.route('/player')
def player():
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('sqlite:///data/db/database.db')
    # Query the required columns from all the tables
    tables = ['players_15', 'players_16', 'players_17', 'players_18', 'players_19', 'players_20']
    # Fetch the results from each table and concatenate them
    players = []
    for table in tables:
        # Query the unique values from the `short_name` column of the `players` table
        query = f"SELECT DISTINCT short_name FROM {table}"
        results = engine.execute(query)
        players = [row[0] for row in results]
    # Render the player.html template and pass the players data to it
    return render_template('player.html', players=players)

@app.route('/league')
def league():
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('sqlite:///data/db/database.db')
    # Query the required columns from all the tables
    tables = ['players_15', 'players_16', 'players_17', 'players_18', 'players_19', 'players_20']
    # Fetch the results from each table and concatenate them
    players = []
    for table in tables:
        # Query the unique values from the `short_name` column of the `players` table
        query = f"SELECT DISTINCT short_name FROM {table}"
        results = engine.execute(query)
        players = [row[0] for row in results]
    # Render the player.html template and pass the players data to it
    return render_template('league.html', players=players)

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/data')
def get_table_data():
    table = request.args.get('table', 'players_15')  # Get the table parameter from the query string, default to 'players_15'
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('sqlite:///data/db/database.db')
    # Query the required columns from the specified table
    query = f"SELECT * FROM {table} LIMIT 100"
    results = engine.execute(query)
    players = [dict(row) for row in results]
    # Return the table data as a JSON response
    return jsonify(players)

@app.route('/player_info')
def get_player_info():
    table = request.args.get('table', 'players_15')  # Get the table parameter from the query string, default to 'players_15'
    selectedPlayer = request.args.get('selectedPlayer', '')  # Get the selectedPlayer parameter from the query string
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('sqlite:///data/db/database.db')
    # Query the required columns from the specified table
    query = f"SELECT short_name, age, nationality, club FROM {table} WHERE short_name = '{selectedPlayer}'"
    results = engine.execute(query)
    players = [dict(row) for row in results]
    # Return the table data as a JSON response
    return jsonify(players)

@app.route('/league_info')
def get_league_info():
    table = request.args.get('table', 'players_15')  # Get the table parameter from the query string, default to 'players_15'
    selectedPlayer = request.args.get('selectedPlayer', '')  # Get the selectedPlayer parameter from the query string
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('sqlite:///data/db/database.db')
    # Query the required columns from the specified table
    query = f"SELECT short_name, nationality, club, team_position, age FROM {table} WHERE short_name = '{selectedPlayer}'"
    results = engine.execute(query)
    leagues = [dict(row) for row in results]
    # Return the table data as a JSON response
    return jsonify(leagues)

@app.route('/map_data')
def get_map_data():
    table = request.args.get('table', 'players_15')  # Get the table parameter from the query string, default to 'players_15'
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('sqlite:///data/db/database.db')
    # Query the required columns from the specified table
    query = f"SELECT * FROM {table}"
    results = engine.execute(query)
    players = [dict(row) for row in results]
    # Return the player data as a JSON response
    return jsonify(players)

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    load_csv_to_database() # Load all the CSV files into the database
    csv_to_json() # Convert all the CSV files into json files
    get_nationalities_with_coordinates()
    app.run(debug=True) # Run the Flask application