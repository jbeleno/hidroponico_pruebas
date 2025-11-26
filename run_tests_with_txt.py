
"""
Script: run_tests_with_txt.py
--------------------------------
Este script ejecuta todas las pruebas automatizadas del proyecto usando pytest,
genera un reporte HTML visual e interactivo y un reporte TXT detallado con toda la salida de pytest.

Ubicación de los reportes generados:
    - resultados/report_all_tests.html
    - resultados/report_all_tests.txt

Uso:
    python run_tests_with_txt.py

Requiere tener pytest y pytest-html instalados en el entorno.
"""

import subprocess
import datetime
import os

# Definir nombres de archivos y carpeta de resultados
fecha = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
carpeta_resultados = 'resultados'
os.makedirs(carpeta_resultados, exist_ok=True)

# Rutas de los reportes
html_path = os.path.join(carpeta_resultados, 'report_all_tests.html')
txt_path = os.path.join(carpeta_resultados, 'report_all_tests.txt')

# Argumentos para pytest (salida detallada y reporte HTML)
pytest_args = [
    'pytest', 'tests', f'--html={html_path}',
    '-v',            # Verbose: muestra cada test
    '-rA',           # Muestra resumen de todos los tests (xfailed, xpassed, skipped, etc)
    '--tb=long',     # Traceback largo para errores
    '--maxfail=5',   # Muestra hasta 5 fallos antes de detener (ajustable)
    '--durations=10' # Muestra los 10 tests más lentos
]

# Ejecutar pytest y guardar la salida en el archivo TXT
with open(txt_path, 'w', encoding='utf-8') as txt_file:
    result = subprocess.run(pytest_args, stdout=txt_file, stderr=subprocess.STDOUT, text=True)

print(f'Reportes generados: {html_path} y {txt_path}')
