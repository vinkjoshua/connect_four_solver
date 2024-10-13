# Connect Four Solver

This application is a Streamlit-based web interface for solving Connect Four game states and tracking player rankings. It uses a custom Connect Four solver algorithm and stores results in a Google Cloud SQL database.

## Features

- Upload and analyze Connect Four game states from text files
- Solve games and display results
- Store game results in a Google Cloud SQL database
- View player rankings and statistics

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- Google Cloud Platform account with Cloud SQL set up
- Google Cloud SDK installed and configured

## Installation

1. Clone the repository:
   ```
   git clone https://your-repository-url.git
   cd connect-four-solver
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Google Cloud SQL instance and note down the connection details.

4. Set the following environment variables with your database connection details:
   ```
   export DB_USER='your-db-user'
   export DB_PASS='your-db-password'
   export DB_NAME='your-db-name'
   export INSTANCE_CONNECTION_NAME='your-project-id:your-region:your-instance-name'
   ```

## Database Setup

1. Connect to your Google Cloud SQL instance.

2. Create the necessary table and views:

   ```sql
   CREATE TABLE game_results (
       id SERIAL PRIMARY KEY,
       player_id INTEGER,
       result VARCHAR(4),
       moves INTEGER
   );

   CREATE VIEW player_stats AS
   SELECT 
       player_id,
       COUNT(*) as games_played,
       SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as won,
       SUM(CASE WHEN result = 'draw' THEN 1 ELSE 0 END) as draws,
       SUM(CASE WHEN result = 'loss' THEN 1 ELSE 0 END) as lost,
       ROUND(SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 2) as win_percentage
   FROM 
       game_results
   GROUP BY 
       player_id;

   CREATE VIEW player_rankings AS
   SELECT 
       ROW_NUMBER() OVER (ORDER BY win_percentage DESC) as player_rank,
       player_id,
       games_played,
       won,
       lost,
       win_percentage as "win%"
   FROM 
       player_stats
   ORDER BY 
       win_percentage DESC;
   ```

## Running the Application

1. Navigate to the project directory:
   ```
   cd path/to/connect-four-solver
   ```

2. Run the Streamlit app:
   ```
   streamlit run streamlit/app.py
   ```

3. Open your web browser and go to `http://localhost:8501` (or the URL provided in the terminal).

## Using the Application

1. **Solve Connect Four**:
   - Select "Solve Connect Four" from the navigation sidebar.
   - Upload a text file containing the Connect Four game state.
   - Click "Solve and save results to db" to analyze the game and store the results.

2. **View Player Rankings**:
   - Select "Player Rankings" from the navigation sidebar to view the current rankings and statistics.

## File Format for Game States

The input text file should represent the Connect Four board state. For example:
```
......
......
......
......
...R..
...RB.
```
Where:
- `.` represents an empty cell
- `R` represents a red piece
- `B` represents a black piece

## Troubleshooting

- If you encounter database connection issues, ensure your environment variables are set correctly and that your IP is whitelisted in the Google Cloud SQL instance settings.
- For any other issues, check the Streamlit error messages in the browser or the console output.

## Contributing

Contributions to the Connect Four Solver are welcome. Please ensure you follow the coding style and add unit tests for any new features.

## License

[Specify your license here, e.g., MIT, GPL, etc.]

## Contact

If you have any questions or feedback, please contact [Your Name/Email/Contact Information].