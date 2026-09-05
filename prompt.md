# Prompt de desarrollo - Gestor Académico de Notas

## Rol
Actúa como desarrollador senior en Python, Streamlit y SQLite, con experiencia en aplicaciones
educativas de gestión académica.

## Objetivo
Crear una aplicación web que permita a un estudiante organizar las calificaciones de varias
asignaturas, dividir cada asignatura en tres cortes con porcentaje configurable, registrar
actividades dentro de cada corte y calcular automáticamente el avance académico (nota
acumulada, nota final y promedio general).

## Stack
Python, Streamlit, SQLite (módulo sqlite3 de la biblioteca estándar), Pandas y Plotly para
el gráfico de barras.

## Diseño visual
- Fondo: #F7F9FB
- Color principal (encabezados, botones): #1B4D3E
- Color de acento (éxito, nota aprobada): #2E8B57
- Color de alerta (nota reprobada o incompleta): #C0392B
- Tipografía: la predeterminada de Streamlit, sin personalización adicional

## Requisitos funcionales
RF01. Crear y seleccionar asignaturas.
RF02. Cada asignatura debe manejar exactamente tres cortes.
RF03. Definir el porcentaje de cada corte y validar que la suma de los tres sea 100 %.
RF04. Agregar actividades ilimitadas dentro de cada corte.
RF05. Definir el porcentaje de cada actividad dentro del corte y validar que la suma del
      corte pueda llegar a 100 %.
RF06. Registrar y actualizar la nota de cada actividad en escala de 0,0 a 5,0.
RF07. Calcular automáticamente la nota de cada corte según el peso de sus actividades.
RF08. Calcular la nota acumulada de la asignatura y mostrar la nota final cuando esté
      evaluado el 100 %.
RF09. Mostrar el porcentaje de la asignatura que ya ha sido evaluado.
RF10. Mostrar un gráfico de barras con las asignaturas y su nota acumulada/final.
RF11. Calcular el promedio general de las asignaturas registradas.
RF12. Guardar asignaturas, cortes, actividades y notas en SQLite y recuperarlos al reiniciar
      la app local.

## Requisitos no funcionales
RNF01. Interfaz clara, consistente y comprensible sin explicación extensa.
RNF02. Validar campos obligatorios, porcentajes y notas antes de guardar.
RNF03. Código organizado en funciones y, si es necesario, módulos.
RNF04. Persistencia local mediante SQLite con creación automática de tablas.
RNF05. No guardar contraseñas, tokens ni secretos dentro del código o repositorio.
RNF06. La aplicación debe ejecutarse desde requirements.txt y publicarse en Streamlit.
RNF07. El repositorio debe mostrar commits que evidencien el proceso de desarrollo.

## Datos (modelo conceptual)
- **Asignatura**: id, nombre
- **Corte**: id, asignatura_id, número (1, 2 o 3), porcentaje
- **Actividad**: id, corte_id, nombre, porcentaje, nota

Relaciones: una Asignatura tiene exactamente 3 Cortes; un Corte tiene N Actividades.

## Interfaz
- Navegación por sidebar con estas secciones: Dashboard | Asignaturas | Configuración de
  cortes | Actividades y notas
- **Dashboard**: promedio general, tarjetas resumen y gráfico de barras por asignatura
  (nota acumulada/final).
- **Asignaturas**: formulario para crear y seleccionar asignatura.
- **Configuración de cortes**: los tres cortes con porcentaje configurable, validado
  contra 100 %.
- **Actividades y notas**: agregar actividades con su peso y nota dentro del corte
  seleccionado.
- Mensajes de error y confirmación claros al guardar cualquier dato.

## Reglas de negocio y cálculo
- Nota de actividad: valor entre 0,0 y 5,0.
- Nota del corte = Σ (nota de actividad × porcentaje de actividad / 100).
- Aporte del corte = nota del corte × porcentaje del corte / 100.
- Nota acumulada = suma de los aportes de los cortes/actividades ya calificadas.
- Diferenciar siempre entre nota acumulada/parcial y nota final (solo es "final" cuando
  el 100 % de la asignatura está evaluado).
- Si faltan actividades por calificar, mostrar también el porcentaje evaluado.

## Persistencia
Base de datos SQLite (`notas.db`) con creación automática de tablas si no existen:
tabla `asignaturas`, tabla `cortes` (con clave foránea a asignatura), tabla `actividades`
(con clave foránea a corte). Operaciones requeridas: insertar, actualizar, consultar y
recuperar todo al reiniciar la app.

## Entregables
app.py, requirements.txt, README.md, .gitignore, prompt.md (este archivo).

## Aceptación
- La aplicación inicia sin errores con Streamlit.
- Permite crear asignaturas y configurar exactamente tres cortes por asignatura.
- Los porcentajes de cortes y de actividades se validan contra 100 %.
- Las notas se registran entre 0,0 y 5,0.
- Calcula correctamente nota de corte, nota acumulada y nota final.
- Muestra el porcentaje evaluado cuando la asignatura está incompleta.
- Presenta gráfico de barras por asignatura y calcula el promedio general.
- Al cerrar y reabrir la app local, todos los datos siguen disponibles (persistencia
  en SQLite).