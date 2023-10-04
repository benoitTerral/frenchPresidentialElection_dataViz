from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil


def initialize_driver():
    options = Options()
    prefs = {
        "download.default_directory": f"{os.getcwd()}/assets/data",
        "savefile.default_directory": f"{os.getcwd()}/assets/data",
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


def click_on_button(driver: webdriver.Chrome, xpath: str) -> None:
    """Find the elements in the HTML and click on the button"""
    elements = driver.find_elements("xpath", xpath)
    for element in elements:
        element.click()
        break
    return None


def get_webElement_in_list(driver: webdriver.Chrome, xpath: str) -> list:
    """Find the elements according to the xpath provided and attach the innerHTML to a list"""
    output = []
    elements = driver.find_elements(
        "xpath",
        xpath,
    )
    for element in elements:
        output.append(element.get_attribute("innerHTML"))
    return output


def main():
    """Starts downloading french presidential results from https://unehistoireduconflitpolitique.fr/telecharger.html"""
    folder_path = f"{os.getcwd()}/assets/data"
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Purging existing data: '{folder_path}' deleted successfully.")
        except OSError as e:
            print(
                f"Error: {e}. Unable to delete the folder '{folder_path}'. Stopping the program."
            )
            exit(1)
    driver = initialize_driver()
    driver.get("https://unehistoireduconflitpolitique.fr/telecharger.html")
    driver.maximize_window()
    click_on_button(
        driver,
        f'//div[@class="text-icon-button__Container-sc-16rlcjc-0 bFWvjM"]//div[text()="Tout refuser"]/..',
    )

    election_years = get_webElement_in_list(
        driver,
        f'//div[@class="card__Container-sc-1dystmw-0 jBDtOY"]//div[text()="Présidentielles"]/../div[starts-with(@class, "card__Badges")]//div/div',
    )

    for election_year in election_years:
        click_on_button(
            driver,
            f'//div[@class="card__Container-sc-1dystmw-0 jBDtOY"]//div[text()="Présidentielles"]/../div[starts-with(@class, "card__Badges")]//div/div[text()="{election_year}"]/..',
        )
        click_on_button(
            driver, f'//div[text()="Base de données en format csv"]/../a[@href]'
        )
        click_on_button(
            driver, f'//div[@class="modal__CloseButton-sc-le7yza-8 hAxkop"]'
        )
        time.sleep(0.5)

    driver.quit()


if __name__ == "__main__":
    main()
