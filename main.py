
from src.buscador import Buscador
from src.pdf import PDF
import json


GITHUB = "https://github.com/danielcgiraldo"

"""
INFORMACIÓN BUSCADOR DE CURSO
Colocar cada campo de acuerdo al buscador de curso.
"""
SEDE = "1102 SEDE MEDELLÍN"
FACULTAD = "3065 FACULTAD DE CIENCIAS"
PLAN_DE_ESTUDIOS = "3505 INGENIERÍA BIOLÓGICA"
"""
3068 FACULTAD DE MINAS
    3534 INGENIERÍA DE SISTEMAS E INFORMÁTICA

3065 FACULTAD DE CIENCIAS
    3505 INGENIERÍA BIOLÓGICA
    3647 CIENCIAS DE LA COMPUTACIÓN
"""

def main():

    # Get courses
    print("\nCargando Horarios...")
    scraper = Buscador(options={ "campus": SEDE, "faculty": FACULTAD, "plan": PLAN_DE_ESTUDIOS })

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
