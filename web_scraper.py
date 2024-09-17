from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#close pop up that appears about data
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


#function to extract data from website 
def extract_text_from_xpath(driver, xpath, wait_time=10):
    """
    Extracts text from an element located by XPath.
    
    Parameters:
    - driver: The Selenium WebDriver instance.
    - xpath: The XPath of the element to locate.
    - wait_time: Maximum time to wait for the element.
    
    Returns:
    - The text of the element or None if not found.
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except Exception as e:
        print(f"Could not find element with XPath {xpath}: {e}")
        return None     

# gather data
def gather_data(driver):
    """
    Gathers data from the professor's page using predefined XPaths.
    
    Parameters:
    - driver: The Selenium WebDriver instance.
    
    Returns:
    - A dictionary containing the extracted data.
    """
    xpaths = {
        'rating': '//*[@id="root"]/div/div/div[3]/div[2]/div[1]/div[1]/div[1]/div/div[1]',
        'number_of_ratings': '//*[@id="root"]/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/a',
        'level_of_difficulty': '//*[@id="root"]/div/div/div[3]/div[2]/div[1]/div[3]/div[2]/div[1]',
        'would_take_again': '//*[@id="root"]/div/div/div[3]/div[2]/div[1]/div[3]/div[1]/div[1]'
    }

    # Extract data using the function
    data = {
        'rating': extract_text_from_xpath(driver, xpaths['rating']),
        'number_of_ratings': extract_text_from_xpath(driver, xpaths['number_of_ratings']),
        'level_of_difficulty': extract_text_from_xpath(driver, xpaths['level_of_difficulty']),
        'would_take_again': extract_text_from_xpath(driver, xpaths['would_take_again']),
        'link': driver.current_url
    }
    # Print the extracted data
    print(f"Overall Rating: {data['rating']}")
    print(f"Number of Ratings: {data['number_of_ratings']}")
    print(f"Level of Difficulty: {data['level_of_difficulty']}")
    print(f"Would Take Again: {data['would_take_again']}")
    print(f"Webpage link: {data['link']}")
    
    return data

def conduct_search(driver, professor_name, university_name=None, initial_search=False):
    """
    Conducts a search for a university (if initial) and professor on the website.
    
    Parameters:
    - driver: The Selenium WebDriver instance.
    - professor_name: The name of the professor to search for.
    - university_name: The name of the university to search for (used only for initial search).
    - initial_search: A boolean indicating whether it's the initial search (True) or subsequent search (False).
    """
    try:
        if initial_search:
            # Wait for the search input field to be visible
            search_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[3]/div[2]/input'))
            )
            # Clear the input field if necessary
            search_input.clear()
            
            # Enter the university name (replace 'University Name' with the actual search query)
            search_input.send_keys(university_name)
            time.sleep(2)
            search_input.send_keys(Keys.DOWN)
            search_input.send_keys(Keys.RETURN)

            # search prof
            search_input.send_keys(professor_name)
            time.sleep(2)
            search_input.send_keys(Keys.ENTER)
            
            print("Search conducted successfully!")
            time.sleep(2)
            
            #call func
            print("calling gather data for prof 0")
            data = gather_data(driver)
            print(" successfully called gather data for prof 0")
            return data
           
        else:
            # Wait for the search input field to be visible
            search_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/header/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[2]/input'))
            )
            time.sleep(1)
            
            # Clear the input field if necessary
            current_value = search_input.get_attribute("value")
            while len(current_value) > 0:
                search_input.send_keys(Keys.BACKSPACE)
                time.sleep(0.2)  # Adjust this delay if needed
                current_value = search_input.get_attribute("value")
            
            time.sleep(2)
            
            # search prof
            search_input.send_keys(professor_name)
            time.sleep(2)
            
            # Locate the dropdown container
            dropdown = driver.find_element(By.CLASS_NAME, 'SearchTypeahead__StyledSearchTypeaheadDropdown-sc-1i57108-0')
            time.sleep(1)
            # Find the first item in the dropdown list
            first_item = dropdown.find_element(By.CSS_SELECTOR, 'ul.TypeaheadItemList__StyledTypeaheadItemList-sc-1veot99-0 li')
            professor = first_item.find_element(By.CSS_SELECTOR, '.MenuItem__MenuItemHeader-h6a87s-0.lauWml').text
            print(professor)
            found = False
            if professor_name.lower() != professor.lower():
                print("no prof found")
                data = None
                return data
            
            # Click the first item
            first_item.click()

            # Optionally, wait to ensure the next page or popup loads
            time.sleep(2)
            print("Search for another prof conducted successfully!")
            
            #call func
            data = gather_data(driver)
            return data
           
                
    except Exception as e:
        print(f"Error conducting search: {e}")
