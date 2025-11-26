# Instrucciones para visualizar el reporte de pruebas

## Reporte HTML

Después de ejecutar las pruebas, se genera un archivo HTML con el resumen y detalle de todos los tests en:

```
resultados/report_all_tests.html
```

### ¿Cómo visualizarlo correctamente?

1. Abre el archivo `report_all_tests.html` desde la carpeta `resultados`.
2. Asegúrate de que la URL en tu navegador termine así:

```
/report_all_tests.html?sort=result
```

Esto garantiza que los resultados se muestren ordenados por estado (fallidos, exitosos, etc). Si abres el HTML y no ves el parámetro `?sort=result`, recarga o copia la URL agregando `?sort=result` al final.

> Ejemplo de URL local:
>
> `file:///C:/Users/Juan%20Forero/Desktop/hidroponico_pruebas/resultados/report_all_tests.html?sort=result`

### ¿Qué información muestra?
- Estado de cada prueba (Passed, Failed, Skipped, etc)
- Logs y salidas de cada test
- Filtros y orden dinámico
- Resumen de ejecución y tiempos

---

Si tienes dudas sobre cómo interpretar el reporte, consulta con el equipo de pruebas o revisa la documentación de [pytest-html](https://pypi.org/project/pytest-html/).
