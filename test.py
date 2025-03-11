import requests
from bs4 import BeautifulSoup
from web_scraper import * 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
import psycopg2

# # PostgreSQL connection details

# # Load environment variables from .env file
# load_dotenv()

# # Get database credentials from environment variables
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")


# # db = psycopg2.connect(
# #     dbname=DB_NAME,
# #     user=DB_USER,
# #     password=DB_PASSWORD,
# #     host=DB_HOST,
# #     port=DB_PORT
# #     )

# # cursor = db.cursor()

# # cursor.execute("ALTER TABLE prof_info ADD COLUMN difficulty FLOAT;")
# # cursor.execute("ALTER TABLE prof_info ADD COLUMN would_take_again INT;")

# # db.commit()

# def get_links():
#     webpage_links = []  # Initialize an empty list to store links

#     try:
#         # Connect to your PostgreSQL database
#         db = psycopg2.connect(
#             dbname=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             host=DB_HOST,
#             port=DB_PORT
#         )
#         cursor = db.cursor()

#         # Correct SQL query to get all links
#         cursor.execute("SELECT link FROM webpages;")

#         # Fetch all the links from the query result
#         webpage_links = cursor.fetchall()

#         print("Got web links successfully!")

#     except Exception as e:
#         print(f"Error getting links from database: {e}")
    
#     finally:
#         if cursor:
#             cursor.close()
#         if db:
#             db.close()
    
#     # Extract links from the fetched rows (since fetchall returns a list of tuples)
#     for link in webpage_links:
#         print(link[0]) 

# get_links()

