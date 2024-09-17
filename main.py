from web_scraper import * 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time 

#global varibles 
service = Service(executable_path="chromedriver")
driver = webdriver.Chrome(service=service)
driver.get('https://www.ratemyprofessors.com')

# List of universities and professors
profs = ["Simon Ford","Toby Donaldson", "Billy Bob", "Bob Gill"]

#inital first search for prof 
close_popup(driver)
conduct_search(driver, profs[0], university_name="Simon Fraser University", initial_search=True)
time.sleep(5)

# Iterate over subsequent professors
for professor in profs[1:]:
    conduct_search(driver, professor, initial_search=False)
    time.sleep(5)

time.sleep(10)
driver.quit()