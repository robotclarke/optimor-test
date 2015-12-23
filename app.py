from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


TARIFF_URL = (
    'http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk'
)
COUNTRIES = [
    'Canada', 'Germany', 'Iceland', 'Pakistan', 'Singapore', 'South Africa'
]


def main():
    browser = webdriver.Firefox()
    wait = WebDriverWait(browser, 10)
    print_all_tariffs(COUNTRIES, browser, wait)


def print_all_tariffs(country_names, browser, wait):
    browser.get(TARIFF_URL)

    country_field = wait.until(EC.presence_of_element_located(
        (By.ID, 'countryName')
    ))

    for country_name in country_names:
        _print_country_landline_tariff(country_name, country_field, wait)


def _print_country_landline_tariff(country_name, country_field, wait):
    country_field.send_keys(country_name, Keys.RETURN)

    # The page has two tables with ID #standardRatesTable so we
    # have to guarantee the right one by starting at the div above
    tariff_plan = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR,
         '#paymonthlyTariffPlan #standardRatesTable '
         'tr:first-child td:last-child')
    ))

    print(u'{}: {}'.format(
        country_name, tariff_plan.get_attribute('innerHTML')
    ))

    country_field.clear()


if __name__ == '__main__':
    main()
