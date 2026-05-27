from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from database import get_connection
import time

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def scrape_website(url):
    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        driver.quit()

def extract_events(html, club_id):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove noise
    for tag in soup(['script', 'style', 'nav', 'footer']):
        tag.decompose()
    
    text = soup.get_text(separator=' ', strip=True)
    print(f"Page text preview: {text[:500]}")
    return text

def process_club_url(url, club_id):
    print(f"Scraping {url}...")
    html = scrape_website(url)
    
    if not html:
        print("Could not scrape website")
        return
    
    text = extract_events(html, club_id)
    print("Done — raw text extracted successfully")
    return text