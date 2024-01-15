
from src.buscador import Buscador
from src.pdf import PDF
import json


GITHUB = "https://github.com/danielcgiraldo"

"""
INFORMACIÓN BUSCADOR DE CURSO
Colocar cada campo de acuerdo al buscador de curso.
"""
SEDE = "1102 SEDE MEDELLÍN"
FACULTAD = "3068 FACULTAD DE MINAS"
PLAN_DE_ESTUDIOS = "3534 INGENIERÍA DE SISTEMAS E INFORMÁTICA"

"""
INFORMACIÓN PLAN DE ESTUDIOS
Plan de estudios del programa curricular de pregrado.
"""
CREDITOS_COMPONENTE_LIBRE_ELECCION = "Treinta y dos (32)"

def main():

    # Get courses
    print("\nCargando Horarios...")
    with open("src/courses.json", "r") as file:
        courses = json.load(file)
    scraper = Buscador(courses, options={ "campus": SEDE, "faculty": FACULTAD, "plan": PLAN_DE_ESTUDIOS })

    with open("src/courses.json", "w") as file:
            json.dump(scraper.courses, file, indent=4, ensure_ascii=False)

    print("\nGenerando PDF...")
    pdf = PDF(scraper.courses, GITHUB, PLAN_DE_ESTUDIOS, SEDE)

    with open("src/courses.json", "r") as file:
        courses = json.load(file)

    pdf = PDF(courses, GITHUB, PLAN_DE_ESTUDIOS, SEDE)
    

if __name__ == '__main__':
    main()
    print("FINALIZADO")
