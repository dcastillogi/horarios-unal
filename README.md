# Plan de Estudio + Horario | Generador de PDF

PRÓXIMAMENTE

## Installation

Install [chromedriver](https://chromedriver.chromium.org/downloads)

Install wkhtmltopdf:

Debian/Ubuntu:

$ sudo apt-get install wkhtmltopdf
macOS:

$ brew install homebrew/cask/wkhtmltopdf

## Getting Started

## Opción 1: Utilizar el archivo `/src/plan.py`

Este archivo está diseñado para obtener la información de un acuerdo oficial de la universidad nacional relacionado con la malla curricular de una carrera, el cual se puede conseguir en la página oficial de la misma. Es importante asegurarse de que el archivo cumpla con ciertas características y sea similar al Acuerdo del plan de estudios de ingeniería de sistemas (http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=100952). Si no es parecido, el estudiante deberá hacer modificaciones al código para poder leer su propio acuerdo. Con este fin el código está bien documentado, y no dudes en forkear el repositorio para hacer los cambios pertinentes.

## Opción 2: Llenar el archivo `/src/courses.json` de forma manual o con otra alternativa programática

Para esta opción, se debe utilizar la siguiente estructura en el archivo `courses.json`:

```json
{
    "[componente]": {
        "[codigo_materia]": {
            "nombre": "...",
            "creditos": "...",
            "obligatoria": true/false,
            "prerequisitos": ["[codigo_materia]"]
        }
    }
}
```