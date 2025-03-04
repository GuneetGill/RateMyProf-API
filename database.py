import psycopg2
import os
from dotenv import load_dotenv

# PostgreSQL connection details

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def initialize_database():
    """Ensures the required tables exist before inserting data."""
    try:
        db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = db.cursor()
        
        # Create tables if they do not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS webpages(
                prof_id INTEGER PRIMARY KEY,
                link TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prof_info(
                prof_id INTEGER PRIMARY KEY,
                department TEXT,
                rating FLOAT,
                number_ratings INT,
                level_difficulty FLOAT,
                students_take_again FLOAT,
                top_tags TEXT,
                ratings TEXT
            )
        ''')
        
        db.commit()
        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def insert_prof_links(prof_id_dict):
    """Inserts professor IDs and links into the database."""
    try:
        # Ensure the database is initialized before inserting data
        initialize_database()

        db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = db.cursor()
        
        for key in prof_id_dict:
            prof_link = f"https://www.ratemyprofessors.com/professor/{key}"

            # Check if prof_id exists
            cursor.execute("SELECT prof_id FROM webpages WHERE prof_id = %s", (key,))
            existing_prof_id = cursor.fetchone()

            if not existing_prof_id:
                cursor.execute("INSERT INTO webpages(prof_id, link) VALUES (%s, %s)", (key, prof_link))
        
        db.commit()
        print("Professor links inserted successfully!")

    except psycopg2.Error as e:
        print(f"Error while inserting data: {e}")
        db.rollback()
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# This ensures the database is initialized when the script is first run.
if __name__ == "__main__":
    initialize_database()
