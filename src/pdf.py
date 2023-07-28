import os
from datetime import datetime
import re
import pdfkit


class PDF:
    def __init__(self, courses, author, program, campus) -> None:
        self.courses = courses
        self.campus = campus
        self.author = author
        self.program = program
        self.html = read_html_file("src/html/pdf.html")
        self.content = {}
        self.gen_head_info()
        self.gen_courses()
        self.gen_pdf()

    def gen_head_info(self):
        self.content["program"] = (' '.join(self.program.split(
        )[1:]) + ", " + ' '.join(self.campus.split()[1:])).title()
        self.content["author"] = self.author.split("/")[-1]
        self.content["author_link"] = self.author
        self.content["date"] = datetime.now().strftime("%B %d, %Y")
        if self.campus == "1102 SEDE MEDELLÍN":
            self.content["conventions1"] = '''<table class="convention-campus">
                        <tr>
                            <th>LUN.</th>
                            <th>MAR.</th>
                            <th>MIE.</th>
                            <th>JUE.</th>
                            <th>VIE.</th>
                            <th>SÁB.</th>
                            <th>DOM.</th>
                        </tr>
                        <tr>
                            <td style="background-color: black; color: white;">
                                <span>8:00</span>
                                <span>10:00</span>
                            </td>
                            <td></td>
                            <td style="background-color: #d9d9d9;"><span>14:00</span>
                                <span>16:00</span>
                            </td>
                            <td></td>
                            <td><span>12:00</span>
                                <span>14:00</span>
                            </td>
                            <td></td>
                            <td></td>
                        </tr>
                    </table>
                    <table class="convention-campus-info">
                        <tbody>
                            <tr>
                                <td style="background-color: black;"></td>
                                <td>Campus Volador y Río</td>
                                <td></td>
                                <td style="background-color: #d9d9d9;"></td>
                                <td>Campus Robledo</td>
                                <td></td>
                                <td style="border: 2px solid #e5e5e5;"></td>
                                <td>Indeterminado</td>
                            </tr>
                        </tbody>
                    </table>'''
            self.content["conventions2"] = '''<table class="convention-code">
                        <tbody>
                            <tr>
                                <td>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <th>CÓDIGO</th>
                                            </tr>
                                            <tr>
                                                <td class="mid-gray"></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                                <td>Asignatura Obligatoria</td>
                                <td></td>
                                <td>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <th>CÓDIGO</th>
                                            </tr>
                                            <tr>
                                                <td></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                                <td>Asignatura Opcional</td>
                            </tr>
                        </tbody>
                    </table>'''
        else:
            self.content["conventions2"] = ""
            self.content["conventions1"] = '''<table class="convention-code">
                        <tbody>
                            <tr>
                                <td>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <th>CÓDIGO</th>
                                            </tr>
                                            <tr>
                                                <td class="mid-gray"></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                                <td>Asignatura Obligatoria</td>
                                <td></td>
                                <td>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <th>CÓDIGO</th>
                                            </tr>
                                            <tr>
                                                <td></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                                <td>Asignatura Opcional</td>
                            </tr>
                        </tbody>
                    </table>'''

    def gen_courses(self):
        self.content["components"] = ""
        for component in self.courses:
            self.content["components"] += '<section class="component">'
            self.content["components"] += f'<div class="title border"><h2>{component}</h2></div>'
            for group in self.courses[component]:
                self.content["components"] += f'<div class="group border"><h3>{group}</h3></div>'
                if len(self.courses[component][group]["courses"]) > 0:
                    self.content["components"] += '''
                <table class="title">
            <tbody>
                <tr>
                    <td></td>
                    <td></td>
                    <th class="border light-gray">REQUISITOS</th>
                </tr>
                <tr class="title">
                    <th class="border">CÓDIGO</th>
                    <th class="border">DESCRIPCIÓN DE LA ASIGNATURA</th>
                    <th class="border light-gray">
                        <table>
                            <tbody>
                                <tr class="reqs">
                                    <td>
                                        CÓDIGO
                                    </td>
                                    <td>
                                        NOMBRE DE LA ASIGNATURA
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </th>
                </tr>'''
                else:
                    self.content["components"] += f'<div class="message border">Consultar Programa Curricular Oficial</div>'
                for course in self.courses[component][group]["courses"]:
                    if self.courses[component][group]["courses"][course]["must"]:
                        must_class = "mid-gray"
                    else:
                        must_class = ""
                    # Get all requirements for course
                    reqs = ""
                    for req_id, req_name in self.courses[component][group]["courses"][course]["reqs"].items():
                        if req_id != "OTROS":

                            reqs += f'''
                        <tr class="reqs">
                                    <td>{req_id}</td>
                                    <td>{req_name.title()}</td>
                                </tr>'''

                    if "OTROS" in self.courses[component][group]["courses"][course]["reqs"].keys():
                        reqs += f'''
                        <tr class="reqs">
                                    <td></td>
                                    <td>Requisito Especial (Consultar Malla Oficial)</td>
                                </tr>'''
                    # Get all groups for course and organize calendar
                    course_schedule = ""
                    groups_keys = self.courses[component][group]["courses"][course]["schedule"].keys(
                    )
                    last_class = ""

                    for i, g in enumerate(groups_keys):
                        if i + 1 == len(groups_keys):
                            last_class = "border"
                        course_schedule += f'''
                        <tr class="course-schedule {last_class}">
                    <td class={must_class}>
                    </td>
                    <td>
                        <table>
                            <tbody>
                        '''
                        # Course info
                        super_indices = '¹²³⁴⁵⁶⁷'
                        bloqs = extract_bloque_text(
                            self.courses[component][group]["courses"][course]["schedule"][g]["time"])
                        bloqs_text = "Bloques: "

                        for index, bloq in enumerate(bloqs):
                            bloqs_text += bloq + super_indices[index]
                            if len(bloqs) > index + 1:
                                bloqs_text += ", "

                        if len(bloqs) == 0:
                            bloqs_text = ""

                        course_schedule += f'''
                        <tr>
                                    <th>Grupo ({g})</th>
                                    <td>{self.courses[component][group]["courses"][course]["schedule"][g]["pro"]}</td>
                                    <td>{bloqs_text}</td>
                                </tr>
                        '''

                        # course calendar
                        course_schedule += '''</tbody>
                        </table>
                    </td>
                    <td>
                        <table>
                            <tbody>
                                <tr>'''

                        if len(re.findall(r"\b(\d{2}/\d{2}/\d{4})\b\s*-\s*\b(\d{2}/\d{2}/\d{4})\b", self.courses[component][group]["courses"][course]["schedule"][g]["time"])) > 1:
                            # Si un curso, cambia de horarios a lo largo del semestre, (múltiples pares de fechas en el string)
                            course_schedule += '''<td>Múltiples Horarios</td>'''
                        else:

                            patron = r"\n([A-ZÁÉÍÓÚÜÑ]+) de (\d{2}:\d{2}) a (\d{2}:\d{2})."
                            days = {
                                "LUNES": ["", ""],
                                "MARTES": ["", ""],
                                "MIÉRCOLES": ["", ""],
                                "JUEVES": ["", ""],
                                "VIERNES": ["", ""],
                                "SÁBADO": ["", ""],
                                "DOMINGO": ["", ""]
                            }
                            resultado = re.findall(
                                patron, self.courses[component][group]["courses"][course]["schedule"][g]["time"])

                            for a, r in enumerate(resultado):
                                days[r[0]][1] += f"<span>{r[1]}</span><span>{r[2]}</span>"
                                if len(bloqs) == len(resultado):
                                    days[r[0]][1] += f"<label>{a + 1}</label>"
                                    if bloqs[a][0] == "M":
                                        days[r[0]][0] = "mid-gray"
                                    else:
                                        days[r[0]][0] = "black"

                            course_schedule += f'''
                                        <td class="{days["LUNES"][0]}">{days["LUNES"][1]}</td>
                                        <td class="{days["MARTES"][0]}">{days["MARTES"][1]}</td>
                                        <td class="{days["MIÉRCOLES"][0]}">{days["MIÉRCOLES"][1]}</td>
                                        <td class="{days["JUEVES"][0]}">{days["JUEVES"][1]}</td>
                                        <td class="{days["VIERNES"][0]}">{days["VIERNES"][1]}</td>
                                        <td class="{days["SÁBADO"][0]}">{days["SÁBADO"][1]}</td>
                                        <td class="{days["DOMINGO"][0]}">{days["DOMINGO"][1]}</td>
                            '''

                        course_schedule += '''
                        </tr>
                        </tbody>
                        </table>
                    </td>
                </tr>'''

                    no_schedule_class = ""
                    if len(groups_keys) == 0:
                        no_schedule_class = "border"

                    if not "desc" in self.courses[component][group]["courses"][course]:
                        self.courses[component][group]["courses"][course]["desc"] = ""

                    self.content["components"] += f'''
                    <tr class="course-info">
                    <td class="{must_class + " " + no_schedule_class}">
                        {course}
                    </td>
                    <td class="{no_schedule_class}">
                        <table>
                            <tbody>
                                <tr>
                                    <td><h4>{self.courses[component][group]["courses"][course]["name"].title()}</h4></td>
                                    <td>Créditos: {self.courses[component][group]["courses"][course]["creds"]}</td>
                                </tr>
                            </tbody>
                        </table>
                        <p>{self.courses[component][group]["courses"][course]["desc"]}</p>
                    </td>
                    <td class="mid-gray {no_schedule_class}">
                        <table class="reqs">
                            <tbody>
                                {reqs}
                            </tbody>
                        </table>
                    </td>
                </tr>
                    '''
                    if len(groups_keys) > 0:
                        self.content["components"] += f'''<tr class="course-schedule">
                    <td class="{must_class}">

                    </td>
                    <td class="sch">
                        <div>
                            <p>GRUPOS</p>
                        </div>

                    </td>
                    <td>
                        <table>
                            <tbody>
                                <tr>
                                    <th>LUN.</th>
                                    <th>MAR.</th>
                                    <th>MIE.</th>
                                    <th>JUE.</th>
                                    <th>VIE.</th>
                                    <th>SÁB.</th>
                                    <th>DOM.</th>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                {course_schedule}'''

                if len(self.courses[component][group]["courses"]) > 0:
                    self.content["components"] += '</tbody></table>'
                self.content["components"] += f'<div class="message border">{self.courses[component][group]["footnote"]}</div>'
            self.content["components"] += '</section>'

    def gen_pdf(self):
        for variable, value in self.content.items():
            self.html = self.html.replace("{{" + variable + "}}", value)
        if not os.path.exists(f"pdf/{self.campus}/{self.program}"):
            os.makedirs(f"pdf/{self.campus}/{self.program}")
        pdfkit.from_string(
            self.html, f"pdf/{self.campus}/{self.program}/{self.program} {datetime.now().strftime('%d-%m-%Y')}.pdf", css="src/html/style.css", options={"enable-local-file-access": ""})


def read_html_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def extract_bloque_text(input_text):
    # Use a regular expression to find all occurrences of "BLOQUE" followed by one or more letters/digits
    bloque_matches = re.findall(r'BLOQUE\s+(\w+)', input_text)
    return bloque_matches
