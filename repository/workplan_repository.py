from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs

from domain.extensions import convert
from domain.flight import Flight
from domain.reserve import Reserve
from domain.work_event import WorkEvent


class WorkPlan(object):

    def __init__(self):
        options = Options()
        options.add_argument('--headless=new')
        self.service = webdriver.Chrome(options=options)

    def getPlan(self, login, password) -> (list[Flight], list[Reserve], list[WorkEvent]):

        self.__login(login, password)

        flights = self.__get_flights()
        flights.extend(self.__get_early_flights())
        reserves = self.__get_reserves()
        events = self.__get_work_events()

        return flights, reserves, events

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

    def __get_flights(self) -> list[Flight]:
        try:
            element = self.service.find_element(By.XPATH,
                                                '/html/body/div[3]/div/div[4]/div[2]/div[2]/table/tbody[2]')
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            flights = convert.to_flight(html)
        except:
            return []
        return flights

    def __get_early_flights(self) -> list[Flight]:
        try:
            element = self.service.find_element(By.XPATH,
                                                '/html/body/div[3]/div/div[4]/div[3]/div[2]/table/tbody[1]')
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            flights = convert.to_flight(html)
        except:
            return []
        return flights

    def __get_reserves(self) -> list[Reserve]:
        try:
            element = self.service.find_element(By.XPATH,
                                                '/html/body/div[3]/div/div[4]/div[4]/div[2]/table/tbody')
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            reserves = convert.to_reserve(html)
        except:
            return []
        return reserves

    def __get_work_events(self) -> list[WorkEvent]:
        try:
            element = self.service.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div[5]/div[2]/table/tbody')
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            events = convert.to_work_event(html)
        except:
            return []
        return events
