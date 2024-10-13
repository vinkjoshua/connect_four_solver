import os
from google.cloud.sql.connector import Connector
import sqlalchemy
import pg8000

os.environ['DB_USER'] = 'connect_four_user'  # The user you created
os.environ['DB_PASS'] = 'connect_four_123'  # The password you set for the user
os.environ['DB_NAME'] = 'postgres'  # The database name you created
os.environ['INSTANCE_CONNECTION_NAME'] = 'esoteric-state-438507-i4:europe-west1:connect-four-db'

connector = Connector()

def getconn() -> pg8000.Connection:
    """ Returns a connection to the database

    Returns:
        pg8000.Connection: Connection to the database
    """
    conn = connector.connect(
        os.environ['INSTANCE_CONNECTION_NAME'],
        "pg8000",
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        db=os.environ['DB_NAME']
    )
    return conn

engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

def write_to_database(result: list[str]) -> None:
    """ Writes the game results to the database

    Args:
        result (list[str]): List of game results
    """
    with engine.connect() as conn:
        for game_result in result:
            if "won" in game_result:
                winner, moves = game_result.split(" won in ")
                player_id = winner.split('_')[1]
                moves = int(moves.split()[0])
                conn.execute(sqlalchemy.text(
                    "INSERT INTO game_results (player_id, result, moves) VALUES (:player_id, 'win', :moves)"
                ), {"player_id": player_id, "moves": moves})
            elif "Draw" in game_result:
                players = game_result.split("Draw between ")[1].split(" and ")
                for player in players:
                    player_id = player.split('_')[1]
                    conn.execute(sqlalchemy.text(
                        "INSERT INTO game_results (player_id, result, moves) VALUES (:player_id, 'draw', NULL)"
                    ), {"player_id": player_id})
        conn.commit()
    return True



