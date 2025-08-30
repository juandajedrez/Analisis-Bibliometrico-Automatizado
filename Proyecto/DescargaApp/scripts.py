from playwright.sync_api import sync_playwright, Page, expect
import pandas as pd
import os
import sys
import requests

# Add project root to system path to access shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from .resources.credentials import username, password  # Import login credentials

# Define login and search URLs
login_url = "https://login.intelproxy.com/v2/conector/google/solicitar?cuenta=7Ah6RNpGWF22jjyq&url=ezp.2aHR0cHM6Ly9pZWVleHBsb3JlLmllZWUub3JnL3NlYXJjaC9zZWFyY2hyZXN1bHQuanNwP2FjdGlvbj1zZWFyY2gmbmV3c2VhcmNoPXRydWU-"
ieee_base_url = "https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?action=search&newsearch=true"

# Function to log in using Google credentials
def login(page: Page, username: str, password: str):
    page.goto(login_url)
    page.fill('input[type="email"]', username)
    page.click("#identifierNext")
    page.wait_for_selector('input[type="password"]')
    page.fill('input[type="password"]', password)
    page.click("#passwordNext")

# Generate IEEE search URL
def create_ieee_search_url(page_number: int, query: str):
    query_encoded = query.replace(" ", "%20")
    return f"https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText={query_encoded}&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&rowsPerPage=100&pageNumber={page_number}"

# Generate Sage search URL
def create_sage_search_url(page_number: int, query: str):
    query_encoded = query.replace(" ", "%20")
    return f"https://journals-sagepub-com.crai.referencistas.com/action/doSearch?field1=AllField&text1={query_encoded}&publication=&Ppub=&access=&pageSize=100&startPage={page_number}"

# Generate ScienceDirect search URL
def create_sciencedirect_search_url(query: str):
    query_encoded = query.replace(" ", "%20")
    return f"https://www-sciencedirect-com.crai.referencistas.com/search?qs={query_encoded}&show=100"

# Extract BibTeX citations from IEEE
def extract_ieee_information(page: Page, query: str):
    while not page.url.startswith(ieee_base_url):
        page.wait_for_timeout(1000)
    expect(page).to_have_url(ieee_base_url)

    page.goto(create_ieee_search_url(1, query))
    page.click('#xplMainContent > div.ng-SearchResults.row.g-0 > div.col > xpl-results-list > div.results-actions.hide-mobile > label > input')
    page.wait_for_timeout(10000)

    page.click('#xplMainContent > div.ng-Dashboard > div.col-12.action-bar.hide-mobile > ul > li.Menu-item.inline-flexed.export-filter.no-line-break.pe-3.myproject-export > xpl-export-search-results > button')
    page.wait_for_timeout(2300)

    page.click('body > ngb-modal-window > div > div > div.d-flex.align-items-center.border-bottom > ul > li:nth-child(2)')
    page.wait_for_timeout(4000)

    page.wait_for_selector('label[for="download-bibtex"] > input', timeout=60000)
    page.click('label[for="download-bibtex"] > input')

    page.wait_for_selector('button.stats-SearchResults_Citation_Download.xpl-btn-primary', timeout=60000)
    page.click('button.stats-SearchResults_Citation_Download.xpl-btn-primary')
    page.wait_for_timeout(15000)

# Extract BibTeX citations from Sage
def extract_sage_information(page: Page, query: str):
    search_url = create_sage_search_url(1, query)
    page.goto(search_url)

    while not page.url.startswith(search_url):
        page.wait_for_timeout(1000)
    expect(page).to_have_url(search_url)

    page.click('#onetrust-accept-btn-handler')
    page.click('#action-bar-select-all')
    page.click('#pb-page-content > div > div > main > div.content.search-page > div > div > div > div.search-result.doSearch > div.search-result--grid > div.search-result--grid__block.search-result--grid__block__2 > div > div.article-actionbar__btns')
    page.wait_for_timeout(2000)
    page.select_option('#citation-format', 'bibtex')
    page.wait_for_timeout(7000)
    page.click('#exportCitation > div > div > div.form-buttons > a')
    page.wait_for_timeout(15000)

# Extract BibTeX citations from ScienceDirect
def extract_sciencedirect_information(page: Page, query: str):
    search_url = create_sciencedirect_search_url(query)
    page.goto(search_url)

    while not page.url.startswith(search_url):
        page.wait_for_timeout(1000)
    expect(page).to_have_url(search_url)

    page.click('#srp-toolbar > div.grid.row.u-show-from-sm > span > span.result-header-controls-container > span:nth-child(1) > div')
    page.click('#srp-toolbar > div.grid.row.u-show-from-sm > span > span.result-header-controls-container > span.header-links-container > div.ExportAllLink.result-header-action__control.u-margin-s-left > button > span')

    page.wait_for_selector('button[data-aa-button="srp-export-multi-bibtex"]', timeout=60000)
    page.click('button[data-aa-button="srp-export-multi-bibtex"]')
    page.wait_for_timeout(15000)

# Clear all files from the specified folder
def clear_folder(folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chdir(folder)
    files = os.listdir()
    for file in files:
        os.remove(file)
        print(f"File '{file}' deleted")
    print(f"All files in folder '{folder}' have been deleted")

# Send status updates to Django backend
def update_status(message: str):
    requests.get("http://127.0.0.1:8000/api/actualizar_estado/", params={"estado": message})

# Main test function that runs the full extraction workflow
def test(page: Page, query: str):
    update_status("Starting login...")
    login(page, username, password)

    update_status("Extracting information from IEEE...")
    extract_ieee_information(page, query)

    update_status("Extracting information from Sage...")
    extract_sage_information(page, query)

    update_status("Extracting information from ScienceDirect...")
    extract_sciencedirect_information(page, query)

    update_status("Process completed.")

# Entry point for Playwright automation
with sync_playwright() as p:
    query = input("Enter the search term:\n")
    clear_folder('archivos_csv')
    browser = p.chromium.launch(headless=True, downloads_path='archivos_csv')  # Run in headless mode
    page = browser.new_page()
    test(page, query)
    browser.close()