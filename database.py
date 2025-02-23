import sqlite3

# define connection and cursor, a cursor allows us to interact with daatbase thorugh sql commands
# Creates or opens a file called
db = sqlite3.connect('rate_my_prof.db')
cursor = db.cursor()

##########
# CREATE #
##########
cursor.execute('''
    CREATE TABLE IF NOT EXISTS webpages(
        prof_id INTEGER PRIMARY KEY,
        link TEXT
    )
''')
db.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS prof_info(
        prof_id INTEGER PRIMARY KEY,
        department TEXT,
        rating FLOAT,
        number_ratings INT,
        level_diffculty FLOAT,
        students_take_again FLOAT,
        top_tags TEXT,
        ratings TEXT
    )
''')
db.commit()

##########
# INSERT #
##########

def insert_prof_links(prof_id_dict):
    # Ensure that db is properly connected
    if not db:
        print("Database connection is not established.")
        return
    
    cursor = db.cursor()
    
    try:
        for key in prof_id_dict:
            prof_link = f"https://www.ratemyprofessors.com/professor/{key}"

            # Check if the prof_id already exists in the database
            cursor.execute('''SELECT prof_id FROM webpages WHERE prof_id = ?''', (key,))
            existing_prof_id = cursor.fetchone()  # Fetch one result
            
            if not existing_prof_id:
                cursor.execute('''INSERT INTO webpages(prof_id, link) VALUES(?, ?)''', (key, prof_link))
        
        db.commit()  # Commit the transaction after the loop
        
    except sqlite3.Error as e:
        print(f"Error while inserting data: {e}")
        db.rollback()  # Rollback any changes if an error occurs
    finally:
        cursor.close()  # Close the cursor to release resources


