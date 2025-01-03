from helpers.nfj_url import create_url
from selenium.webdriver.common.by import By
from sites.nofluffjobs.analyze_offers import analyze 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import re
from selenium.webdriver.common.action_chains import ActionChains

def scrape(driver, categories, exp, requirements):
    path = create_url(categories, requirements, exp)
    driver.get(path)
    offers_count = 0
    
    try:
        offers_count = driver.find_element(By.CSS_SELECTOR, '[listname="search"] .list-title > span').text
        offers_count = int(re.search(r'\d+', offers_count).group())
    except:
        offers_count = 0
    
    button_locator = (By.CSS_SELECTOR, "button[nfjloadmore]")
        
    if offers_count > 0:
        try:
            load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button_locator))
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            actions = ActionChains(driver)
            actions.move_to_element(load_more_button).perform()
            driver.execute_script("arguments[0].click();", load_more_button)
        except TimeoutException:
            print("TimeoutException")

        except StaleElementReferenceException:
            print("StaleElementReferenceException")
            
    links = driver.find_elements(By.CSS_SELECTOR, '[listname="search"] [nfj-postings-item]')
    offers = get_offers(links)
    
    return analyze(driver, offers)


def get_offers(links: list) -> list:
    offers = []
    for link in links:
        url = link.get_attribute("href")
        if("pl/job" in url):
            offers.append(url)
            
    return offers