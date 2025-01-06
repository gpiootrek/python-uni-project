import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sites.nofluffjobs.scraper import scrape as nfj_scrape
from sites.pracujpl.scraper import scrape as pracujpl_scrape
from job_analysis import *


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
        
    st.title("Job offers analysis")
    setup_inputs()
    st.button(
        "Analize",
        type="primary",
        on_click=on_analyze_click,
        disabled=st.session_state.get("disabled_analysis", True) or st.session_state.get("loading", True)
    )


def setup_inputs() -> None:
    global categories_selection, exp_selection, skills_selection
    
    categories_selection = st.segmented_control(
        "Category",
        categories_options,
        selection_mode="single",
        on_change=set_state,
        key="categories",
        disabled=st.session_state.get("loading", True)
    )
    exp_selection = st.pills(
        "Experience",
        exp_options,
        selection_mode="single",
        key="exp",
        on_change=set_state,
        disabled=st.session_state.get("loading", True)
    )
    skills_selection = st.selectbox(
        'Skills',
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
    
    # Use ResultAnalyzer for skill frequency and overall analysis
    result_analyzer = ResultAnalyzer(results)
    analysis_results = result_analyzer.analyze()
    
    # Display results using Streamlit
    display_results(analysis_results)


def set_state() -> None:
    if st.session_state.categories and st.session_state.exp:
        st.session_state.disabled_analysis = (len(st.session_state.categories) < 1 and len(st.session_state.exp) < 1)
    else:
        st.session_state.disabled_analysis = True


def display_results(analysis_results) -> None:
    # Display total offers
    st.write(f"### Total Offers: {analysis_results['total_offers']}")

    # Display salary statistics
    Visualization.display_salary_statistics(analysis_results["salary_statistics"])

    # Skill frequency table
    Visualization.display_skill_frequency_table(analysis_results)

    # Visualize primary skill frequency
    Visualization.plot_skill_frequency(
        analysis_results["skill_frequency"]["primary"],
        title="Top 5 Most Frequently Required Primary Skills"
    )

    # Visualize secondary skill frequency
    Visualization.plot_skill_frequency(
        analysis_results["skill_frequency"]["secondary"],
        title="Top 5 Most Frequently Required Secondary Skills"
    )