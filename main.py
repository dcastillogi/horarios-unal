from src.buscador import Buscador
from src.pdf import PDF
import json

GITHUB = "https://github.com/dcastillogi"

"""
INFORMACIÓN BUSCADOR DE CURSO
Colocar cada campo de acuerdo al buscador de curso.
"""
SEDE = "1102 SEDE MEDELLÍN"
FACULTAD = "3068 FACULTAD DE MINAS"
PLAN_DE_ESTUDIOS = "3534 INGENIERÍA DE SISTEMAS E INFORMÁTICA"

def main():

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
