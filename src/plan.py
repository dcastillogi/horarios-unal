import requests
from bs4 import BeautifulSoup
from collections import deque
import json


class PlanEstudios():
    """
    Generates the study plan based on the official university agreement.

    Attributes:
        plan_url: str
            URL to the official university agreement.
        html: str
            HTML content of the agreement page.
        courses: list
            List of course codes extracted from the agreement.

    Methods:
        get_page: Fetches the HTML content of the agreement page.
        get_courses: Extracts the course codes from the HTML content.
    """

    def __init__(self, plan_url: str, creds: str) -> None:
        # DO NOT MODIFY
        self.plan_url = plan_url
        self.free_creds = creds
        self.fetch_page()
        self.extract_courses()
        self.export_json()

    def fetch_page(self) -> None:
        # DO NOT MODIFY
        """
        Fetches the HTML content of the official university agreement.

        Returns:
            None
        """
        response = requests.get(self.plan_url)
        self.html = response.text

    def extract_courses(self) -> None:
        # MODIFY ME
        """
        Extracts the course codes from the HTML content.

        Returns:
            None
        """
        soup = BeautifulSoup(self.html, "html.parser")

        # Get document content
        elements = deque(soup.find('div', class_='WordSection1'))
        self.courses = {}

        # Component title variables
        section = 0
        title = ""
        candidate_title = ""

        # Group title variables
        table = 0
        subtitle = ""
        candidate_subtitle = ""

        while len(elements) > 3:
            ele = elements.popleft()
            if ele == "\n":
                continue

            """
            COMPONENT TITLE
            According to the structure of the document, career components are structured in HTML link: title <p><strong></strong><p>, followed by a
            blank space <p></p>, then the 2. table title <p><strong></strong><p> and finally 3. the table <table></table>.
            """
            if section == 0:
                # Check for title
                for cont in ele.contents:
                    if (cont.name == "strong") and len(cont.text) > 1:
                        section += 1
                        candidate_title = cont.text
                        break
            elif section == 1:
                # Check for blank space
                if len(ele.text) <= 1:
                    section += 1
                else:
                    section = 0
            elif section == 2:
                # Check for table title
                if ele.contents[0].name == "strong" and len(ele.text) > 1:
                    section += 1
                else:
                    section = 0
            elif section == 3:
                # Check for table
                if ele.name == "table":
                    candidate_title = candidate_title[3:]
                    title = candidate_title
                    self.courses[title] = {}
                elif ele.name == "div":
                    if ele.contents[0].name == "table":
                        # MODIFY ME
                        # Removes literal from title
                        candidate_title = candidate_title[3:]
                        title = candidate_title
                        self.courses[title] = {}
                section = 0

            """
            GROUP TITLE
            According to the structure of the document,  groups are table's title, which is a 0. title <p><strong></strong></p>, followed by a
            1. the table <table></table>.
            """

            if table == 0:
                # Check for subtitle
                if (ele.contents[0].name == "strong") and len(ele.text) > 1:
                    table += 1
                    candidate_subtitle = ele.text
            elif table == 1:
                # Check for table
                if ele.name == "table" or ele.name == "div":
                    subtitle = candidate_subtitle
                    self.courses[title][subtitle] = {}
                    table += 1
                elif ele.name == "div":
                    if ele.contents[0].name == "table":
                        subtitle = candidate_subtitle
                        self.courses[title][subtitle] = {}
                        table += 1
                else:
                    table = 0
            elif table == 2:
                self.courses[title][subtitle]["footnote"] = ele.text
                table = 0

            """
            COURSES TABLE
            """

            if ele.name == "table" or ele.name == "div":
                if ele.name == "div" and ele.contents[1].name != "table":
                    continue
                else:
                    table_rows = deque(ele.find_all("tr"))

                    # Delete first two rows (headers)
                    table_rows.popleft()
                    table_rows.popleft()

                    last_course = ""

                    self.courses[title][subtitle]["courses"] = {}

                    while len(table_rows) >= 1:
                        row = table_rows.popleft()
                        columns = row.find_all("td")
                        if len(columns) == 7:
                            last_course = str(columns[0].text).strip()
                            if len(str(columns[4].text).strip()) > 1:
                                req = {
                                    str(columns[4].text).strip(): str(columns[5].text).strip()
                                }
                            else:
                                req = {}

                            self.courses[title][subtitle]["courses"][last_course] = {
                                "name": str(columns[1].text).strip(),
                                "creds": str(columns[2].text).strip(),
                                "must": str(columns[3].text).strip() == "SI",
                                "reqs": req
                            }
                        elif len(columns) == 3:
                            self.courses[title][subtitle]["courses"][last_course]["reqs"][str(
                                columns[0].text).strip()] = str(columns[1].text).strip()
                        elif len(columns) == 2:
                            if last_course != "":
                                self.courses[title][subtitle]["courses"][last_course]["reqs"]["OTROS"] = True

                            

    def export_json(self) -> None:
        # DO NOT MODIFY
        """
        Save dictionary to json
        Returns:
            None
        """
        # save self.courses to /src/courses.json
        self.courses["Componente de Libre Elección"] = {
            "Agrupación: Libre Elección": {
                "courses": {},
                "footnote": "Créditos exigidos de la agrupación Libre Elección: " + self.free_creds
            }

        }
        with open("src/courses.json", "w") as file:
            json.dump(self.courses, file, indent=4, ensure_ascii=False)
