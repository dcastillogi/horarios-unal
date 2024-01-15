
from src.plan import PlanEstudios
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
MANUAL = False # Plan de estudios manual o no (a través del código en src/plan.py)
PLAN_ESTUDIOS = "http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=100952"
CREDITOS_COMPONENTE_LIBRE_ELECCION = "Treinta y dos (32)"

def main():
    # Get study plan
    if not MANUAL:
        print("======== DISCLAIMER ========")
        print("Obtener la información automáticamente de internet puede contener errores.")
        print("Este proceso borrará toda la información en src/courses.json.")
        while True:
            confirmation = input("\n¿Estás seguro de obtener la información del plan de estudio? Y/N: ")
            if confirmation == "Y":
                print("\nCargando Plan de Estudios...")
                PlanEstudios(PLAN_ESTUDIOS, CREDITOS_COMPONENTE_LIBRE_ELECCION)
                break
            elif confirmation == "N":
                quit()

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
