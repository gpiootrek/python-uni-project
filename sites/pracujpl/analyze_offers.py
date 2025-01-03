from selenium.webdriver.common.by import By
import re


def analyze(driver, urls):
    primary_requirements = []
    secondary_requirements = []
    salary_lower_ranges = []
    salary_upper_ranges = []
    
    for url in urls:
        driver.get(url)
        primary_elements = driver.find_elements(By.CSS_SELECTOR, '[data-test="section-technologies-expected"] [data-test="aggregate-open-dictionary-model"] [data-test="item-technologies-expected"]')
        secondary_elements = driver.find_elements(By.CSS_SELECTOR, '[data-test="section-technologies-optional"] [data-test="aggregate-open-dictionary-model"] [data-test="item-technologies-optional"]')
        salary_element = driver.find_elements(By.CSS_SELECTOR, '[data-test="section-salary"] [data-test="text-earningAmount"]')
        salary_per_element = driver.find_elements(By.CSS_SELECTOR, '[data-test="section-salary"] [data-test="text-earningAmount"] + div')
        
        if salary_element and salary_per_element:
            results = save_salary_ranges(salary_element[0].text, salary_per_element[0].text)
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
        "salary_lower_ranges": salary_lower_ranges,
        "salary_upper_ranges": salary_upper_ranges,
    }


def save_salary_ranges(salary, unit) -> tuple:
    lower_range = 0
    upper_range = 0
    multiplier = 1
    
    if('godz' in unit):
        multiplier = 160
        
    numbers = re.findall(r'\d[\d\s]*(?:,\d+)?', salary)

    if len(numbers) >= 2:
        lower_range = clean_number(numbers[0])
        upper_range = clean_number(numbers[1])
        
    return (lower_range * multiplier, upper_range * multiplier)


def clean_number(num) -> int:
    if ',' in num:
        return int(num.split(',')[0])
    else:
        return int(num.replace(" ", ""))