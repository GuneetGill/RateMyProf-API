'''
every so often scrape the website for new profs and update exisitng prof data 

get list of existing profs from your func
get all profs from webpage 
compare and only add new ones

'''

import requests
from bs4 import BeautifulSoup
from web_scraper import * 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time 
from bs4 import BeautifulSoup
import database 
from selenium.webdriver.chrome.options import Options
import add_prof_id_db

if __name__ == "__main__":
    print("starting ")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    service = Service(executable_path="./chromedriver") 
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    #all 3 campus school url's 
    school_urls = ['https://www.ratemyprofessors.com/search/professors/1482?q=*','https://www.ratemyprofessors.com/search/professors/4267?q=*','https://www.ratemyprofessors.com/search/professors/5788?q=*' ]

    #get all current prof's in database
    set(database.get_prof_id())
    
    for school in school_urls:
        add_prof_id_db.load_profs(school)
        #load all the profs but it has a global varible 
        #
        
    
