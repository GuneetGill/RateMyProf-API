'''
add info to prof_info db 
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

'''
go to first table: prof webpage one and open each prof page link
once opened gather all the info from webpage 
update other database and add info to table 
use multithreading to scrape data so it doesnt take foreever 
'''
