'''
Initally populate prod_id's and webpage links to table within database.
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


#Helper funcitons 
def close_popup(driver):
    """
    Closes the popup if it appears on the page.
    
    Parameters:
    - driver: The Selenium WebDriver instance.
    """
    try:
        close_button = WebDriverWait(driver, 5, poll_frequency=0.2).until(
            #EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/img'))
            EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/button'))
        )
        close_button.click()
        print("Popup closed successfully!")
    except:
        print("no popup found")

def append_prof_id_db(soup):
    """
    Extracts unique professor IDs from the page and adds them to the professor_ids set.

    Parameters:
    - soup: BeautifulSoup object containing the parsed page content.
    """
    # Find all professor cards
    professor_cards = soup.find_all('a', class_='TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx')

    # Loop through each professor card and extract the number (ID)
    for card in professor_cards:
        # Extract the href attribute, which contains the link
        href = card['href']
        # href="/professor/246300
        
        # Extract the number after '/professor/'
        if '/professor/' in href:
            professor_id = href.split('/professor/')[1]
            professor_ids.add(professor_id) 
            
    print(len(professor_ids))


def load_profs(url):
    """
    parameters: url, this is a url for each page you want to gather prof info about
                for example, you could enter in all 3 campus page links here 
    
    loads all profs for given url, clicks load button until all entires are shown 
    """
    driver.get(url)
    # Wait for the page to load
    driver.implicitly_wait(10)
    print("done waiting ")
    
    close_popup(driver)
    #driver.execute_script("arguments[0].click();", button) use javascript to froce close it?
        
    # Send a GET request to fetch the page's HTML
    response = requests.get(url)
    print("gotten the response")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("we are now inside the if statement")
        
        time.sleep(2)
        print("after 2 second sleep")
    
        while True:
            try:
                # print("in the try block trying to get button ")
                # Wait until the button is clickable explicit wait (wait for my condition to be met)
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.glImpo"))
                )
                button.click()
          
                
            except Exception as e:
                print("button no longer found")
                break
        
        updated_html = driver.page_source  # Use the page source from Selenium after clicking
        soup = BeautifulSoup(updated_html, 'html.parser') 
        
        #now that all the profs are loaded onto the screen put all of them into db 
        append_prof_id_db(soup)
        
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


print("starting ")
chrome_options = Options()
chrome_options.add_argument("--headless=new")
service = Service(executable_path="./chromedriver") 
driver = webdriver.Chrome(service=service, options=chrome_options)

# url = 'https://www.ratemyprofessors.com/search/professors/1482?q=*' #burnaby 
# url = 'https://www.ratemyprofessors.com/search/professors/4267?q=*' #surrey
url = 'https://www.ratemyprofessors.com/search/professors/5788?q=*' #vancouver 
# List to store the professor IDs (numbers after /professor/)
professor_ids = set()

load_profs(url)
#add profs to database 
database.insert_prof_links(professor_ids)


driver.quit()

