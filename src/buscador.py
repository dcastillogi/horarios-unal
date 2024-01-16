from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import re
import time


class Buscador():
    """


    """

    def __init__(self, options) -> None:
        self.courses = {}
        self.campus = options["campus"]
        self.faculty = options["faculty"]
        self.plan = options["plan"]
        self.run_bot()

    def wait_loading(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//body[contains(@style, 'cursor: auto')]"))
        )

    def run_bot(self):
        self.driver = driver = webdriver.Chrome()
        # Navigate to the target website
        self.driver.get(
            "https://sia.unal.edu.co/Catalogo/facespublico/public/servicioPublico.jsf?taskflowId=task-flow-AC_CatalogoAsignaturas")
        try:
            self.get_all_courses()
            self.get_free_courses()
        finally:
            # Close the browser window after execution
            self.driver.quit()

    def get_all_courses(self):
        # Wait a second because starting too fast
        time.sleep(2)

        # Nivel de estudio
        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc1"))
        select.select_by_visible_text("Pregrado")

        self.wait_loading()

        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc9"))
        select.select_by_visible_text(self.campus)

        self.wait_loading()

        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc2"))
        select.select_by_visible_text(self.faculty)

        self.wait_loading()

        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc3"))
        select.select_by_visible_text(self.plan)

        self.wait_loading()

        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc4"))
        select.select_by_visible_text("TODAS MENOS LIBRE ELECCIÓN")

        self.wait_loading()

        for i in range(1, 8):
            self.driver.find_element(By.NAME, f"pt1:r1:0:sbc{i}").click()

        self.driver.find_element(
            By.CSS_SELECTOR, "a.af_button_link").click()

        self.wait_loading()

        for i in range(len(self.driver.find_elements(By.CSS_SELECTOR, "tr.af_table_data-row"))):
            ele = self.driver.find_elements(By.CSS_SELECTOR, "tr.af_table_data-row")[i]
            cols = ele.find_elements(By.TAG_NAME, "td")
            course_id = cols[0].text
            course_tipo = cols[3].text
            if (course_tipo not in self.courses):
                self.courses[course_tipo] = {}
            self.courses[course_tipo][course_id] = {}
            self.courses[course_tipo][course_id]["name"] = cols[1].text
            self.courses[course_tipo][course_id]["creds"] = cols[2].text
            self.courses[course_tipo][course_id]["must"] = False
            self.courses[course_tipo][course_id]["reqs"] = {}
            self.courses[course_tipo][course_id]["desc"] = cols[4].text
            cols[0].find_element(By.TAG_NAME, "a").click()

            self.wait_loading()
            # Get all schedules and groups
            self.courses[course_tipo][course_id]["schedule"] = {}
            for sch in self.driver.find_elements(
                    By.XPATH, "//span[normalize-space(@class)='borde salto af_panelGroupLayout']"):
                info = sch.find_elements(
                    By.CSS_SELECTOR, "div")
                if len(info) != 12:
                    continue
                self.courses[course_tipo][course_id]["schedule"][self.get_group_num(sch.find_element(By.TAG_NAME, "table").text)] = {
                    "pro": info[6].text,
                    "time": info[8].text,
                }
            self.driver.find_element(
                By.CLASS_NAME, "af_button").click()
            self.wait_loading()

        self.wait_loading()

    def get_free_courses(self):

        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc4"))
        select.select_by_visible_text("LIBRE ELECCIÓN")

        self.wait_loading()

        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc5"))
        select.select_by_visible_text("Por facultad y plan")

        self.wait_loading()

        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc10"))
        select.select_by_visible_text(self.campus)

        self.wait_loading()

        select = Select(self.driver.find_element(By.NAME, "pt1:r1:0:soc6"))
        for option in select.options:
            if ' '.join(self.campus.split()[1:]) in option.text:
                select.select_by_visible_text(option.text)
                break

        self.wait_loading()

        self.driver.find_element(
            By.CSS_SELECTOR, "a.af_button_link").click()

        self.wait_loading()

        for i in range(len(self.driver.find_elements(By.CSS_SELECTOR, "tr.af_table_data-row"))):
            ele = self.driver.find_elements(By.CSS_SELECTOR, "tr.af_table_data-row")[i]
            cols = ele.find_elements(By.TAG_NAME, "td")
            course_id = cols[0].text
            course_tipo = cols[3].text
            if (course_tipo not in self.courses):
                self.courses[course_tipo] = {}
            self.courses[course_tipo][course_id] = {}
            self.courses[course_tipo][course_id]["name"] = cols[1].text
            self.courses[course_tipo][course_id]["creds"] = cols[2].text
            self.courses[course_tipo][course_id]["must"] = False
            self.courses[course_tipo][course_id]["reqs"] = {}
            self.courses[course_tipo][course_id]["desc"] = cols[4].text
            cols[0].find_element(By.TAG_NAME, "a").click()

            self.wait_loading()
            # Get all schedules and groups
            self.courses[course_tipo][course_id]["schedule"] = {}
            for sch in self.driver.find_elements(
                    By.XPATH, "//span[normalize-space(@class)='borde salto af_panelGroupLayout']"):
                info = sch.find_elements(
                    By.CSS_SELECTOR, "div")
                if len(info) != 12:
                    continue
                self.courses[course_tipo][course_id]["schedule"][self.get_group_num(sch.find_element(By.TAG_NAME, "table").text)] = {
                    "pro": info[6].text,
                    "time": info[8].text,
                }
            self.driver.find_element(
                By.CLASS_NAME, "af_button").click()
            self.wait_loading()

    def get_group_num(self, title):
        regex_pattern = r"\(([^)]+)\)"

        match = re.search(regex_pattern, title)
        if match:
            return match.group(1)
        else:
            return title
