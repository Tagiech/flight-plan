from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs

from domain.extensions.convert import HtmlConverter
from domain.flight import Flight
from domain.reserve import Reserve
from domain.work_event import WorkEvent


class WorkPlan(object):

    def __init__(self):
        options = Options()
        options.add_argument('--headless=new')
        self.service = webdriver.Chrome(options=options)
        self._convert = HtmlConverter()

    def close(self):
        self.service.close()

    def getPlan(self, login, password) -> (list[Flight], list[Reserve], list[WorkEvent]):

        self.__login(login, password)

        flights, reserves, work_events = self.__get_events()

        return flights, reserves, work_events

    def __login(self, login, password):
        try:
            self.service.get('https://edu.rossiya-airlines.com/workplan')

            loginField = self.service.find_element(By.XPATH,
                                                   '/html/body/div[3]/div/div/div/form/fieldset/div[2]/input')
            passwordField = self.service.find_element(By.XPATH,
                                                      '/html/body/div[3]/div/div/div/form/fieldset/div[3]/input')
            loginField.send_keys(login)
            passwordField.send_keys(password)

            self.service.find_element(By.XPATH,
                                      '/html/body/div[3]/div/div/div/form/fieldset/div[5]/input').click()

            WebDriverWait(self.service, 20).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[3]/div/div[1]/form[1]/div/div[4]/input')))
        except:
            raise Exception("Login failed")

    def __get_events(self) -> (list[Flight], list[Reserve], list[WorkEvent]):
        flights: list[Flight] = []
        reserves: list[Reserve] = []
        work_events: list[WorkEvent] = []

        basic_route: str = '/html/body/div[3]/div/div[4]'
        base_element = self.service.find_element(By.XPATH, basic_route)
        tables = base_element.find_elements(By.CSS_SELECTOR, 'div.panel.panel-info')

        for table in tables:
            table_header = table.find_element(By.CSS_SELECTOR, 'div.panel-heading')
            header_style = table_header.get_attribute("style")
            if "rgb(176, 214, 237)" in header_style or "rgb(202, 236, 151)" in header_style:
                element = table.find_element(By.CSS_SELECTOR, 'tbody.noPrint')
                flights.extend(self.__get_flights(element))
            elif "rgb(245, 240, 146)" in header_style:
                element = table.find_element(By.CSS_SELECTOR, 'tbody')
                reserves.extend(self.__get_reserves(element))
            elif "rgb(222, 199, 236)" in header_style:
                element = table.find_element(By.CSS_SELECTOR, 'tbody')
                work_events.extend(self.__get_work_events(element))

        return flights, reserves, work_events

    def __get_flights(self, element: WebElement) -> list[Flight]:
        try:
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            flights = self._convert.to_flight(html)
        except:
            return []
        return flights

    def __get_reserves(self, element: WebElement) -> list[Reserve]:
        try:
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            reserves = self._convert.to_reserve(html)
        except:
            return []
        return reserves

    def __get_work_events(self, element: WebElement) -> list[WorkEvent]:
        try:
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            events = self._convert.to_work_event(html)
        except:
            return []
        return events
