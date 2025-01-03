import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sites.nofluffjobs.scraper import scrape as nfj_scrape
from sites.pracujpl.scraper import scrape as pracujpl_scrape
from functools import reduce
from collections import Counter
from statistics import mean

categories_options = ["Frontend", "Backend", "Data"]
skills_options = ["", "Java", "JavaScript", "SQL", "HTML", "Python"]
exp_options = ["trainee", "junior", "mid", "senior", "expert"]
categories_selection = None
exp_selection = None
skills_selection = None

def app() -> None:
    if 'disabled_analysis' not in st.session_state:
        st.session_state.disabled_analysis = True
        
    if 'loading' not in st.session_state:
        st.session_state.loading = False
        
    st.title("Analiza ofert pracy")
    setup_inputs()
    st.button(
        "Analizuj",
        type="primary",
        on_click=on_analyze_click,
        disabled=st.session_state.get("disabled_analysis", True) or st.session_state.get("loading", True)
    )


def setup_inputs() -> None:
    global categories_selection, exp_selection, skills_selection
    
    categories_selection = st.segmented_control(
        "Kategoria",
        categories_options,
        selection_mode="single",
        on_change=set_state,
        key="categories",
        disabled=st.session_state.get("loading", True)
    )
    exp_selection = st.pills(
        "Doświadczenie",
        exp_options,
        selection_mode="single",
        key="exp",
        on_change=set_state,
        disabled=st.session_state.get("loading", True)
    )
    skills_selection = st.selectbox(
        'Umiejętności',
        skills_options,
        on_change=set_state,
        disabled=st.session_state.get("loading", True)
    )


def on_analyze_click() -> None:
    results = []
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    st.session_state.loading = True
    
    with st.spinner('Scraping...'):
        pracujpl_results = pracujpl_scrape(driver, categories_selection, exp_selection, skills_selection)
        nfj_results = nfj_scrape(driver, categories_selection, exp_selection, skills_selection)
        results = [pracujpl_results, nfj_results]

    st.session_state.loading = False
    display_results(results)


def set_state() -> None:
    if st.session_state.categories and st.session_state.exp:
        st.session_state.disabled_analysis = (len(st.session_state.categories) < 1 and len(st.session_state.exp) < 1)
    else:
        st.session_state.disabled_analysis = True


def display_results(results: list) -> None:
    offers_count = reduce(lambda acc, x: acc + x['offers_count'], results, 0)
    st.write(f'Przeanalizowanych ofert: {offers_count}')
    primary_requirements = Counter([req for result in results for req in result["primary_requirements"]]).most_common()
    secondary_requirements = Counter([req for result in results for req in result["secondary_requirements"]]).most_common()
    primary_df = pd.DataFrame(primary_requirements, columns=["Umiejętność", "Liczba wystąpień"])
    secondary_df = pd.DataFrame(secondary_requirements, columns=["Umiejętność", "Liczba wystąpień"])
    
    st.write("Wymagane umiejętności")
    st.dataframe(primary_df)
    st.write("Mile widziane umiejętności")
    st.dataframe(secondary_df)
    
    salaries_lower_ranges = [lower for result in results for lower in result["salary_lower_ranges"]]
    salaries_upper_ranges = [upper for result in results for upper in result["salary_upper_ranges"]]
    col1, col2 = st.columns(2)
    col1.metric("Średnie zarobki min.", f'{round(mean(salaries_lower_ranges), 2)} PLN')
    col2.metric("Średnie zarobki max.", f'{round(mean(salaries_upper_ranges), 2)} PLN')

