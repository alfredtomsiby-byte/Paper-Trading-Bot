from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import sys


def get_spike_with_selenium():
    """Use Selenium to get rendered JavaScript content"""
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    
    try:
        driver.get("https://www.pizzint.watch/")
        
        # Wait for page to load
        time.sleep(5)
        
        # Get all text
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Look for the spike
        lines = page_text.split('\n')
        for i, line in enumerate(lines):
            if 'domino' in line.lower() or 'spike' in line.lower():
                print(f"Found: {line}")
                numbers = re.findall(r'(\d{1,3})%', line)
                if numbers:
                    spike = int(numbers[0])
                    print(f"Spike: {spike}%")
                    return spike
        
        # Also check specific elements by class (inspect the page to find these)
        try:
            spike_element = driver.find_element(By.CLASS_NAME, "spike-value")
            print(f"Found by class: {spike_element.text}")
        except:
            pass
        
        return 0
        
    finally:
        driver.quit()

# Run it
while True:
    spike = get_spike_with_selenium()

    if spike > 200:
        print("Time to Invest in DEFENSE SHARES, the Pizza Index Spike is over 200%")   
        
        #INSERT BUY CODE
        import strategy_one
        strategy_one.run_strategy()
        #THIS BUY CODE seems to work but is ugly, like idk why

        days_of_sleep = 7
        print(f"Pausing Trades for {days_of_sleep} days")
        time.sleep(days_of_sleep * 24 * 60 *60)
    else:
        print("Pizza Index NOT HIGH Enough, checking in 15 minutes")
        time.sleep(15*60)


