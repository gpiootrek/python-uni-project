from selenium.webdriver.common.by import By
import re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

def analyze(driver, urls: list):
    primary_requirements = []
    secondary_requirements = []
    salary_lower_ranges = []
    salary_upper_ranges = []
    
    for url in urls:
        driver.get(url)
        primary_elements = driver.find_elements(By.CSS_SELECTOR, '[branch="musts"] > ul > li > span')
        secondary_elements = driver.find_elements(By.CSS_SELECTOR, '[branch="nices"] > ul > li > span')
        salary_elements = driver.find_elements(By.CSS_SELECTOR, 'common-posting-salaries-list .salary')        
        
        if salary_elements:
            results = save_salary_data(driver)
            salary_lower_ranges.append(results[0])
            salary_upper_ranges.append(results[1])
        
        for el in primary_elements:
            primary_requirements.append(el.text)

        for el in secondary_elements:
            secondary_requirements.append(el.text)
            
    return {
        "primary_requirements": primary_requirements,
        "secondary_requirements": secondary_requirements,
        "offers_count": len(urls),
        "salary_lower_ranges": [x for xs in salary_lower_ranges for x in xs],
        "salary_upper_ranges": [x for xs in salary_upper_ranges for x in xs],
    }


def save_salary_data(driver) -> tuple:
    salary_lower_ranges = []
    salary_upper_ranges = []

    salary_ranges = WebDriverWait(driver, 1000, ignored_exceptions=ignored_exceptions)\
                .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'h4')))
    numbers = re.findall(r'\d[\s\d]*', salary_ranges.text)

    if len(numbers) >= 2:
        lower_range = int(numbers[0].replace(" ", ""))
        upper_range = int(numbers[1].replace(" ", ""))
        
        salary_lower_ranges.append(lower_range)
        salary_upper_ranges.append(upper_range)
        
    
    return (salary_lower_ranges, salary_upper_ranges) 