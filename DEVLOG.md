# Registro de Desarrollo: Mejora de la Experiencia de Búsqueda de Cursos en la Universidad Nacional

----------------------------------------

PENDIENTE

- Soporte de convenciones en términos de Sede para otras sedes diferentes a la Sede Medellín
- Gestionar correctamente los cursos virtuales
- Organizar grupos en orden ascendente, no tan desorganizado cómo esta en el buscador de cursos.
- Mejorar la documentación del código
- Implementar un generador de Prompts para que Chat GPT cree un horario a partir de las materias que el usuario le diga.

----------------------------------------

## Antecedentes

El propósito inicial de este proyecto es abordar las deficiencias de usabilidad y los tiempos de carga del [buscador de cursos de la Universidad Nacional](https://sia.unal.edu.co/Catalogo/facespublico/public/servicioPublico.jsf?taskflowId=task-flow-AC_CatalogoAsignaturas). Se busca proporcionar una solución que concentre toda la información en una sola vista, de forma accesible y sin complicaciones, con el objetivo de reducir tiempos de carga y minimizar la cantidad de clics necesarios para que los usuarios accedan a la información.

Entre las opciones consideradas se encuentran:

### Organizador de Horario

Esta opción se basa en una aplicación o página web que genere alternativas de horarios posibles. Aunque existen opciones como "Kairos" que cumplen adecuadamente con este requisito, aún requieren que los estudiantes accedan al buscador de cursos y a su plan de estudios correspondiente. Finalmente, algunos estudiantes (como yo) prefieren crear su horario manualmente y solo requieren la información sobre su plan de estudios y los grupos disponibles.

### Página Web Alternativa al Buscador de Cursos

Con esta opción, es posible mejorar los tiempos de carga y la interfaz. Para lograrlo, el código debería generar su propia base de datos de cursos mediante web scraping al inicio del semestre. Posteriormente, presentaría dicha información de manera atractiva y clara. También requeriría integrar los planes de estudio de cada carrera para que los usuarios tengan acceso a ellos. Sin embargo, esta solución implicaría un despliegue en la nube, no incentivaría la participación de los estudiantes y es probable que no muestre toda la información en una sola vista, lo que requeriría que los usuarios realicen varios clics y solicitudes a la página (a largo plazo llevaría nuevamente a problemas de carga).

### PDF con Plan de Estudios y Horarios

Esta es la opción elegida, ya que solo requiere tiempo de programación inicial y el tiempo de ejecución del programa cuando se deba actualizar el horario (probablemente cada 6 meses). Además, permite adaptarse a otras carreras, alentando a otros estudiantes a dedicar tiempo para la creación de un PDF para sus respectivas carreras.

Finalmente, esta alternativa no necesita despliegue en la nube, además con un diseño compacto en el PDF se podrían lograr los objetivos propuestos de velocidad y accesibilidad de toda la información en una sola vista. Finalmente, una vez el PDF generado, se puede compartir por los grupos de carrera, etc, y no se debe volver a generar hasta el otro semestre. Para estudiantes que tienen dificultades de acceso a internet, tiene una gran ventaja con respecto a los otros dos.

## Propuesta Inicial

Dado que el buscador de cursos carece de una API, y utiliza una tecnología relativamente anticuada que dificulta la obtención sencilla de información, es probable que sea necesario utilizar [Selenium](https://selenium-python.readthedocs.io/index.html) para realizar web scraping y obtener la información necesaria del buscador de cursos.

Para lograr esto, antes cada estudiante deberá proporcionar los cursos de su carrera, y será responsabilidad de este encontrar el plan de estudios y realizar las modificaciones pertinentes en caso de ser necesario (por ejemplo, [Ingeniería de Sistemas](http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=100952)).

Una vez se cuenten con los datos mencionados, se ejecutará el programa para obtener el horario de cada materia, así como información sobre el orden de las materias, los prerrequisitos, y otros detalles relevantes. Con esta información disponible, el siguiente paso será generar un PDF, lo cual es factible a partir de un archivo HTML.

## Desarrollo

### Plan de Estudios

Para obtener el plan de estudios, es necesario realizar una solicitud al enlace correspondiente para obtener el HTML de la página. Luego, utilizando [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), se puede organizar el HTML para ser iterable en python. Dado que toda la página está construida con etiquetas `<p>` y `<table>`, va a ser necesario en encontrar patrones entre ellas.

Primero, los títulos de los componentes, los cuales están dentro de las etiquetas `<p><strong?></strong></p>`, siempre luego de estas etíquetas habrá otra `<p>` con un espacio en blanco, luego de está seguirá otro título `<p><strong?></strong></p>`, y inmediatamente despúes una `<table></table>`. Mientras se recorré el código html de la página, a la vez se va verificando este patrón y almacenando la información en un diccionario. Posteriormente, se almacena el diccionario en un archivo JSON.

En cuanto al tiempo de ejecución, este proceso depende principalmente del tiempo de carga de la página web. Al utilizar diccionarios y establecer la jerarquía simultáneamente se almacena de la información, se evita el uso de funciones de búsqueda adicionales o realizar múltiples recorridos sobre los datos. Esto contribuye a una ejecución más eficiente y optimizada del programa.

Es importante mencionar que esta sección no es replicable para otras carreras, ya que cada una puede tener una estructura HTML diferente. En este caso, cada estudiante debe llenar el archivo `courses.json` manualmente o crear un proceso automatizado, similar al usado en este repositorio. Una opción para aquellos estudiantes, y que se puede implementar fácilmente con el código actual, sería obtener la malla a partir de la información del buscador de cursos, ya que allí se encuentran los prerrequisitos de cada materia, entre otra información.

### Buscador de Cursos

Con el plan de estudios a la mano, se programo un bot que ingresa al buscador de cursos, y obtiene todas las materias ofertadas para ingeniería de sistemas. Con la lista de materias lista para consultarle el horario, se obtiene el diccionario del paso anterior y se busca una a uno el código de la materia en todos los cursos ya cargados del buscador de cursos, se ingresa a la página y se obtiene el horario, profesor, etc.

Está sección considero que no necesita modificación, ya que el buscador de cursos funciona de forma muy estándar en cualquier carrera e incluso sede. Solo hay que cambiar las variables del archivo main.py. En términos de optimización, buscar el código de la materia en la página se realiza usando una función de busqueda de selenium. Este proceso podría optimizarse, considerando que el diccionario es un mapa hash, se podría recorrer la tabla con todos los cursos del buscador de cursos y luego buscarlo en el diccionario. Esto probablemente ahorraría el proceso de búsqueda realizaado por Selenium que no debe ser igual de optimó que en un hash map.

Sin embargo, considerando que el buscador puede tener materias extrañas, que en realidad son otro tipo de cursos ofertados para estudiantes con necesidades específicas, y en vista de que el código actual funciona cómo lo esperado, no se hicieron ningunos cambios.

Finalmente, se repite el proceso anterior, pero para las materias libre elección, estás sin base a un plan de estudio, pues son abiertas a todos.

### Generador de PDF

Con toda la información en mano, el siguiente paso era abordar el diseño del PDF. La densidad y relevancia de los datos presentes dificultaron la búsqueda de un diseño óptimo. Opté por utilizar Figma para esbozar el diseño y luego implementé HTML y CSS para generar el PDF. Sin embargo, este proceso resultó bastante complejo debido a las limitaciones de compatibilidad de wkhtmltopdf con ciertas propiedades de CSS. En consecuencia, me vi en la necesidad de recurrir en gran medida al uso de tablas para organizar el contenido, extrañando particularmente la flexibilidad que proporciona "display: flex".

## Conclusiones

PRÓXIMAMENTE.