from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
import time

# Configure Selenium to use Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing for security

# Path to your ChromeDriver (download it from https://sites.google.com/chromium.org/driver/)
chrome_driver_path = "/Users/chris24michel/Downloads/chromedriver-mac-x64-3/chromedriver"

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the parcel detail page
url = "https://portal.assessor.lacounty.gov/parceldetail/4267030003"

try:
    # Open the URL in the browser
    driver.get(url)

    # Wait for the page to load (adjust the sleep time if needed)
    time.sleep(5)  # Increase this if the content takes longer to load

    # Check for alerts (e.g., "No APN Found") and dismiss them
    try:
        alert = driver.switch_to.alert
        print(f"Alert detected: {alert.text}")
        alert.dismiss()  # Dismiss the alert
    except:
        # No alert present
        pass

   

    # Locate and click the "Parcel Change" section to expand it
    try:
        parcel_change_section = driver.find_element(By.XPATH, "//li[@heading='Parcel Change']/a[contains(text(), 'Parcel Change')]")
        parcel_change_section.click()  # Click to expand the section
        print("Clicked on the Parcel Change section.")
        time.sleep(3)  # Wait for the section to load
    except NoSuchElementException:
        print("Parcel Change section not found on the page.")
        driver.quit()
        exit()
    try:
        alert = driver.switch_to.alert
        print(f"Alert detected: {alert.text}")
        alert.dismiss()  # Dismiss the alert
    except:
        # No alert present
        pass
    # Extract the HTML content after expanding the section
    page_source = driver.page_source

    # Parse the HTML content using BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    with open('test.html', 'w') as outfile:
        outfile.write(soup.prettify())
    # Find the <td> element with the specified attributes
    old_ain_td = soup.find('td', {'ng-class': "{'text-red text-bold': parcelchangeRow.OldAIN==ain}", 'class': 'text-red text-bold'})

    if old_ain_td:
        # Extract the text content of the <a> tag inside the <td>
        old_ain = old_ain_td.find('a', {'class': 'ng-binding'}).text.strip()

        # Print the old AIN
        print(f"Old AIN: {old_ain}")
    else:
        print("Old AIN not found on the page.")
     # Find the <td> element for the new AIN
    new_ain_td = soup.find('td', {'ng-class': "{'text-red text-bold': parcelchangeRow.NewAIN==ain}"})
    if new_ain_td:
        # Extract the text content of the <a> tag inside the <td>
        new_ain = new_ain_td.find('a', {'class': 'ng-binding'}).text.strip()
        print(f"New AIN: {new_ain}")
    else:
        print("New AIN not found on the page.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    driver.quit()