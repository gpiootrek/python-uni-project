from helpers.pracujpl_url import create_url
from selenium.webdriver.common.by import By
from sites.pracujpl.analyze_offers import analyze

def scrape(driver, category: str, exp: str, skills: str):
    path = create_url(category, exp, skills)
    driver.get(path)
    
    links = driver.find_elements(By.CSS_SELECTOR, '[data-test="default-offer"] [data-test="link-offer"]')
    offers = get_offers(links)
    
    return analyze(driver, offers)


def get_offers(links: list) -> list:
    offers = []
    for link in links:
        url = link.get_attribute("href")
        if("praca/" in url):
            offers.append(url)
            
    return offers