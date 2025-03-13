import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import database
import concurrent.futures
'''
File Overview: 
This script scrapes professor information from RateMyProfessors.com using multithreading to improve efficiency.
It uses a connection pool to manage database connections across multiple threads, ensuring thread safety
and optimal performance. The script extracts details such as professor names, ratings, departments, and
other metrics, then stores this information in a PostgreSQL database.

General Steps:
1. Get all links from prof_link table and store as a list
2. Go through the list and perform Web scraping with requests and BeautifulSoup
3. Update prof_info database with new info 

Key components: 
- Multithreaded execution with ThreadPoolExecutor
- Database operations with connection pooling to maintain ACID properties 
- Error handling and data validation
'''


def main():
     # Initialize the connection pool
    database.initialize_connection_pool()
    
    webpage_links = database.get_links()  # Get the list of webpage links from the database

    # Using ThreadPoolExecutor to scrape and save data concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Each thread runs scrape_and_save_data(link), which:
        # Calls get_data(link) to scrape data.
        # Saves the data using database.save_data_prof_info_table(scraped_data).
        # Submit scrape_and_save_data function to the executor for each link
        futures = [executor.submit(scrape_and_save, link) for link in webpage_links]
        
        # Optionally: Wait for all tasks to complete
        # This ensures that any errors in individual threads do not crash the whole program.
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Will raise exceptions if any occurred
            except Exception as e:
                print(f"Error occurred during scraping: {e}")

def scrape_and_save(link):
    """
    Scrapes data from the professor page and saves it to the database.
    This scrapes a single webpage link and saves data for a singular prof
    """
    scraped_data = get_data(link)
    if scraped_data:
        database.save_data_prof_info_table(scraped_data)

def get_data(url):
    """
    This scrapes data from a prof webapge gathering key info and returns a dict with key values
    from the webpage
    """
    prof_id = url.split('/')[4]
    
    # Initialize all values with default values in case extraction fails
    prof_name = ''
    rating = 0.0
    number_of_ratings = 0
    department = ''
    would_take_again = ''
    difficulty = 0.0
    top_tags = []
    
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Extracting the name
        name_element = soup.find('h1', class_='NameTitle__NameWrapper-dowf0z-2 fEoACI')
        if name_element:
            prof_name = name_element.get_text(" ", strip=True)
        
        # Extracting the Rating
        rating_element = soup.find("div", class_="RatingValue__Numerator-qw8sqy-2 liyUjw")
        if rating_element:
            rating = float(rating_element.get_text(strip=True))
        
        # Extracting the number of ratings
        ratings_element = soup.find("a", href="#ratingsList")
        if ratings_element:
            number_of_ratings = int(ratings_element.text.strip().split()[0])
        
        # Extracting Department
        department_element = soup.find("b")
        if department_element:
            department = department_element.text.split("department")[0].strip()
        
        # Extracting Would Take Again Rating
        would_take_again_element = soup.find("div", class_="FeedbackItem__FeedbackNumber-uof32n-1 kkESWs")
        if would_take_again_element:
            would_take_again = would_take_again_element.get_text(strip=True)
        
        # Extracting Difficulty
        difficulty_element = soup.find_all("div", class_="FeedbackItem__FeedbackNumber-uof32n-1 kkESWs")
        if difficulty_element:
            difficulty = float(difficulty_element[1].text.strip())
        
        # Extracting Teacher Tags
        tags_list = soup.find("div", class_="TeacherTags__TagsContainer-sc-16vmh1y-0 cgUwDc")
        if tags_list:
            top_tags = [tag.text.strip() for tag in tags_list.find_all("span", class_="Tag-bs9vf4-0 hHOVKF")]
    
    except Exception as e:
        print(f"Error extracting data: {e}")

    # Return the data with defaults for any missing values
    return {
        "prof_id": int(prof_id),
        "prof_name": prof_name,
        "department": department,
        "rating": rating,
        "number_of_ratings": number_of_ratings,
        "would_take_again": would_take_again,
        "difficulty": difficulty,
        "top_tags": top_tags
    }


'''
Program entry point:
Sets up the Selenium webdriver with headless mode (for background operation),
initializes the required components, and calls the main function to start the scraping process.
Ensures proper cleanup by closing the database connection pool and quitting the webdriver
when the scraping is complete. This provides clean entry and exit points for the application.

we can also run thiss script many times to get the latest most up to date info for each prof 
'''
if __name__ == "__main__":
    print("starting ")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    service = Service(executable_path="./chromedriver") 
    driver = webdriver.Chrome(service=service, options=chrome_options)

    main()
    database.close_pool()
    driver.quit()
