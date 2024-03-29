from time import sleep

from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs

from domain.extensions.convert import HtmlConverter
from domain.flight import Flight
from domain.reserve import Reserve
from domain.work_event import WorkEvent
from services.telegram_logger import TelegramLogger


class WorkPlan(object):

    def __init__(self):
        options = Options()
        options.add_argument('--headless=new')
        self.__service = webdriver.Chrome(options=options)
        self.__convert = HtmlConverter()
        self.__logger = TelegramLogger()

    def close(self):
        self.__service.close()

    def getPlan(self, login, password) -> (list[Flight], list[Reserve], list[WorkEvent]):

        self.__login(login, password)

        flights, reserves, work_events = self.__get_events()

        return flights, reserves, work_events

    def __login(self, login, password):
        try:
            self.__service.get('https://edu.rossiya-airlines.com/')

            loginField = self.__service.find_element(By.XPATH,
                                                   '/html/body/div[3]/div/div/div/form/fieldset/div[2]/input')
            passwordField = self.__service.find_element(By.XPATH,
                                                      '/html/body/div[3]/div/div/div/form/fieldset/div[3]/input')
            loginField.send_keys(login)
            passwordField.send_keys(password)

            self.__service.find_element(By.XPATH,
                                      '/html/body/div[3]/div/div/div/form/fieldset/div[5]/input').click()
            self.__wait_for_page_to_load()

            self.__pass_change_password_alert()

            workplan_is_blocked = self.__check_is_workplan_is_blocked()
            if workplan_is_blocked:
                raise Exception("Workplan is blocked. To unlock you need to read the documents/pass tests")

            workplan_link = self.__service.find_element(By.XPATH, '/html/body/div[3]/div/ul/li[3]/a')
            workplan_link.click()

        except BaseException as exc:
            self.__service.save_screenshot("image.png")
            self.__logger.log_exception_with_image(exc, "image.png")
            raise

    def __get_events(self) -> (list[Flight], list[Reserve], list[WorkEvent]):
        flights: list[Flight] = []
        reserves: list[Reserve] = []
        work_events: list[WorkEvent] = []

        basic_route: str = '/html/body/div[3]/div/div[4]'
        base_element = self.__service.find_element(By.XPATH, basic_route)
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
            flights = self.__convert.to_flight(html)
        except:
            return []
        return flights

    def __get_reserves(self, element: WebElement) -> list[Reserve]:
        try:
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            reserves = self.__convert.to_reserve(html)
        except:
            return []
        return reserves

    def __get_work_events(self, element: WebElement) -> list[WorkEvent]:
        try:
            html = bs(element.get_attribute('innerHTML'), 'html.parser')
            events = self.__convert.to_work_event(html)
        except:
            return []
        return events

    def __wait_for_page_to_load(self):
        seconds = 0
        while True:
            try:
                workplan_link_element = self.__service.find_element(By.XPATH,
                                                                    '/html/body/div[3]/div/ul/li[3]/a')
                workplan_is_visible = workplan_link_element.is_displayed()
            except:
                workplan_is_visible = False
            try:
                modal_element = self.__service.find_element(By.XPATH, '/html/body/div[9]/div/div/div[1]/button')
                modal_is_visible = modal_element.is_displayed()
            except:
                modal_is_visible = False
            try:
                workplan_blocked_element = self.__service.find_element(By.CLASS_NAME,
                                                                       'head__workplan-blocked-message')
                workplan_blocked_is_visible = workplan_blocked_element.is_displayed()
            except:
                workplan_blocked_is_visible = False

            if workplan_is_visible or modal_is_visible or workplan_blocked_is_visible:
                return
            else:
                if seconds >= 30:
                    raise Exception("Login failed due to wait timeout")
                else:
                    seconds += 0.5
                    sleep(0.5)

    def __pass_change_password_alert(self):
        try:
            modal_element = self.__service.find_element(By.XPATH, '/html/body/div[9]')
            if modal_element:
                (modal_element.find_element(By.CSS_SELECTOR, 'button.bootbox-close-button.close')).click()
        except:
            pass

    def __check_is_workplan_is_blocked(self) -> bool:
        try:
            workplan_blocked_element = self.__service.find_element(By.CLASS_NAME,
                                                                   'head__workplan-blocked-message')
            return workplan_blocked_element.is_displayed()
        except:
            return False
