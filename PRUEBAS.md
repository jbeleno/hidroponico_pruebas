# Documentación de Pruebas - Sistema Hidropónico

Este documento describe todas las pruebas implementadas y ejecutadas en el proyecto del Sistema Hidropónico.

## 📋 Índice

1. [Pruebas de Base de Datos](#pruebas-de-base-de-datos)
2. [Pruebas Unitarias](#pruebas-unitarias)
   - [Modelos](#pruebas-de-modelos)
   - [Schemas](#pruebas-de-schemas)
   - [API](#pruebas-de-api)
3. [Pruebas de Integración](#pruebas-de-integración)
4. [Resumen de Cobertura](#resumen-de-cobertura)

---

## Pruebas de Base de Datos

**Archivo**: `test_database.py`

### Descripción
Script de prueba para verificar la estructura y funcionamiento de la base de datos PostgreSQL.

### Pruebas Implementadas

#### 1. **test_conexion()**
- **Objetivo**: Verificar la conexión a la base de datos PostgreSQL
- **Validaciones**:
  - Conexión exitosa a la base de datos
  - Obtención de la versión de PostgreSQL
- **Resultado esperado**: Conexión exitosa con mensaje de confirmación

#### 2. **test_tablas()**
- **Objetivo**: Verificar que todas las tablas esperadas existan en la base de datos
- **Validaciones**:
  - Comparación entre tablas esperadas (del JSON.json) y tablas existentes
  - Identificación de tablas faltantes
  - Identificación de tablas adicionales
- **Resultado esperado**: Todas las tablas del modelo están presentes

#### 3. **test_foreign_keys()**
- **Objetivo**: Verificar que las claves foráneas estén correctamente creadas
- **Validaciones**:
  - Consulta de todas las foreign keys en la base de datos
  - Conteo de relaciones establecidas
- **Resultado esperado**: Foreign keys correctamente configuradas

#### 4. **test_indices()**
- **Objetivo**: Verificar que los índices personalizados estén creados
- **Validaciones**:
  - Búsqueda de índices con prefijo `idx_`
  - Conteo de índices encontrados
- **Resultado esperado**: Índices creados correctamente

#### 5. **test_insertar_datos_prueba()**
- **Objetivo**: Insertar datos de prueba básicos en la base de datos
- **Validaciones**:
  - Inserción de una empresa de prueba
  - Manejo de conflictos (ON CONFLICT DO NOTHING)
  - Retorno del ID generado
- **Resultado esperado**: Datos de prueba insertados correctamente

### Ejecución
```bash
docker-compose exec python python test_database.py
```

---

## Pruebas Unitarias

### Pruebas de Modelos

**Archivo**: `tests/test_unit_models.py`

#### Descripción
Pruebas unitarias para los modelos de SQLAlchemy que representan las entidades del sistema.

#### Modelos Probados

1. **TestEmpresaModel**
   - Creación de empresa con todos los campos
   - Valor por defecto del campo `activo`

2. **TestPersonaModel**
   - Creación de persona con todos los campos
   - Valor por defecto del campo `activo`

3. **TestSedeModel**
   - Creación de sede con coordenadas geográficas
   - Relación con empresa y responsable

4. **TestBloqueModel**
   - Creación de bloque con descripción
   - Relación con sede

5. **TestTipoEspacioModel**
   - Creación de tipo de espacio

6. **TestEspacioModel**
   - Creación de espacio con dimensiones (ancho, largo, alto)
   - Capacidad y ubicación

7. **TestUsuarioModel**
   - Creación de usuario con hash de contraseña
   - Valor por defecto de `auto_registro`

8. **TestRolModel**
   - Creación de rol con descripción

9. **TestTipoCultivoModel**
   - Creación de tipo de cultivo

10. **TestCultivoModel**
    - Creación de cultivo con nombre científico
    - Relación con tipo de cultivo

11. **TestNutrienteModel**
    - Creación de nutriente con fórmula química

12. **TestFaseProduccionModel**
    - Creación de fase de producción con duración estimada

13. **TestVariedadCultivoModel**
    - Creación de variedad de cultivo con características

#### Ejecución
```bash
pytest tests/test_unit_models.py -v
```

---

### Pruebas de Schemas

**Archivo**: `tests/test_unit_schemas.py`

#### Descripción
Pruebas unitarias para los esquemas de Pydantic que validan los datos de entrada y salida de la API.

#### Schemas Probados

1. **TestEmpresaSchemas**
   - Creación válida de empresa
   - Valor por defecto de `activo` (True)
   - Validación de campo requerido `nombre`
   - Actualización parcial con `EmpresaUpdate`

2. **TestPersonaSchemas**
   - Creación válida de persona
   - Validación de campos requeridos (`nombre`, `apellido`)

3. **TestSedeSchemas**
   - Creación válida de sede con coordenadas
   - Validación de campos requeridos (`empresa_id`, `nombre`)

4. **TestTipoCultivoSchemas**
   - Creación válida de tipo de cultivo
   - Validación de campo requerido `nombre`

5. **TestNutrienteSchemas**
   - Creación válida de nutriente con fórmula química
   - Validación de campo requerido `nombre`

6. **TestCultivoSchemas**
   - Creación válida de cultivo
   - Validación de campos requeridos (`tipo_cultivo_id`, `nombre`)

7. **TestUsuarioSchemas**
   - Creación válida de usuario
   - Validación de campos requeridos completos

8. **TestRolSchemas**
   - Creación válida de rol
   - Validación de campo requerido `nombre`

#### Ejecución
```bash
pytest tests/test_unit_schemas.py -v
```

---

### Pruebas de API

**Archivo**: `tests/test_unit_api.py`

#### Descripción
Pruebas unitarias para los endpoints de la API REST usando FastAPI TestClient.

#### Endpoints Probados

1. **TestEmpresaAPI**
   - `GET /api/empresas` - Listar empresas (vacía)
   - `POST /api/empresas` - Crear empresa
   - `GET /api/empresas/{id}` - Obtener empresa por ID
   - `GET /api/empresas/99999` - Error 404 para empresa inexistente
   - `PUT /api/empresas/{id}` - Actualizar empresa
   - `DELETE /api/empresas/{id}` - Eliminar empresa

2. **TestPersonaAPI**
   - `POST /api/personas` - Crear persona
   - `GET /api/personas` - Listar personas

3. **TestTipoCultivoAPI**
   - `POST /api/tipos-cultivo` - Crear tipo de cultivo
   - `GET /api/tipos-cultivo/{id}` - Obtener tipo de cultivo por ID

4. **TestNutrienteAPI**
   - `POST /api/nutrientes` - Crear nutriente
   - `GET /api/nutrientes` - Listar nutrientes

5. **TestRootEndpoint**
   - `GET /` - Endpoint raíz con información de la API

6. **TestAPIValidation**
   - Validación de campos requeridos faltantes (422)
   - Actualización de entidad inexistente (404)
   - Eliminación de entidad inexistente (404)

#### Códigos de Estado Probados
- `200 OK` - Operaciones exitosas
- `404 NOT_FOUND` - Recurso no encontrado
- `422 UNPROCESSABLE_ENTITY` - Validación fallida

#### Ejecución
```bash
pytest tests/test_unit_api.py -v
```

---

## Pruebas de Integración

**Archivo**: `tests/test_integration_flow.py`

### Descripción
Pruebas end-to-end (E2E) del frontend usando Selenium WebDriver con un enfoque de **flujo completo de ciclo de vida**. Estas pruebas simulan la interacción de un usuario real con la interfaz web, ejecutando todas las operaciones CRUD en un orden que respeta las dependencias entre entidades.

### Características
- **Navegador**: Chrome (configurado con ChromeDriverManager)
- **Modo**: Visible (no headless) para visualización durante las pruebas
- **Delays optimizados**: Tiempos reducidos para ejecución más rápida pero aún visible
- **Gestión de dependencias**: Crea, actualiza y elimina entidades respetando las relaciones de clave foránea
- **Flujo único**: Una sola prueba que ejecuta todo el ciclo de vida

### Flujo de Prueba: `test_full_lifecycle`

La prueba ejecuta un ciclo completo en **3 fases**:

#### **Fase 1: Creación (Orden de Dependencias)**
Crea todas las entidades en el orden correcto para satisfacer las dependencias:

**Entidades Independientes:**
1. Empresa
2. Persona
3. Tipo Cultivo
4. Nutriente
5. Rol
6. Tipo Espacio
7. Fase Producción
8. Tipo Estructura

**Entidades Dependientes:**
9. Usuario (depende de Persona, Empresa)
10. Sede (depende de Empresa, Persona)
11. Bloque (depende de Sede)
12. Espacio (depende de Bloque, Tipo Espacio)
13. Estructura (depende de Espacio, Tipo Estructura)
14. Cultivo (depende de Tipo Cultivo)
15. Variedad Cultivo (depende de Cultivo)
16. Cultivo Fase (depende de Variedad Cultivo, Fase Producción)
17. Fase Nutriente (depende de Cultivo Fase, Nutriente)
18. Método Acceso (depende de Usuario)
19. Usuario Rol (depende de Usuario, Rol)
20. Acceso Espacio (depende de Usuario, Espacio)

#### **Fase 2: Actualización**
Actualiza todas las entidades creadas para verificar la funcionalidad de edición.

#### **Fase 3: Eliminación (Orden Inverso)**
Elimina todas las entidades en **orden inverso** a la creación para evitar violaciones de clave foránea:
1. Acceso Espacio
2. Usuario Rol
3. Método Acceso
4. Fase Nutriente
5. Cultivo Fase
6. Variedad Cultivo
7. Cultivo
8. Estructura
9. Espacio
10. Bloque
11. Sede
12. Usuario
13. Tipo Estructura
14. Fase Producción
15. Tipo Espacio
16. Rol
17. Nutriente
18. Tipo Cultivo
19. Persona
20. Empresa

### Funciones Auxiliares

- `select_tab()`: Selecciona un tab específico en la interfaz
- `open_create_modal()`: Abre el modal de creación
- `save_form()`: Guarda el formulario
- `edit_last_item()`: Edita el último elemento creado
- `delete_last_item()`: Elimina el último elemento creado
- `fill_text_field()`: Llena campos de texto de forma rápida pero visible
- `fill_number_field()`: Llena campos numéricos
- `fill_checkbox()`: Marca/desmarca checkboxes
- `fill_textarea()`: Llena textareas
- `_get_first_row_id()`: Obtiene el ID de la primera fila de la tabla

### Ejecución
```bash
# Requiere Chrome instalado
pytest tests/test_integration_flow.py -v

# Sin warnings para salida más limpia
pytest tests/test_integration_flow.py -v --disable-warnings
```

---

## Resumen de Cobertura

### Pruebas de Base de Datos
- ✅ Conexión a base de datos
- ✅ Estructura de tablas
- ✅ Foreign keys
- ✅ Índices
- ✅ Inserción de datos

### Pruebas Unitarias
- ✅ **Modelos**: 13 modelos probados (100% de modelos principales)
- ✅ **Schemas**: 8 esquemas probados con validaciones
- ✅ **API**: 6 grupos de endpoints probados con casos exitosos y de error

### Pruebas de Integración
- ✅ **Flujo Completo de Ciclo de Vida**: 1 prueba integral que cubre 20 entidades
- ✅ **Gestión de Dependencias**: Creación, actualización y eliminación en orden correcto
- ✅ **Interfaz de Usuario**: Navegación, formularios, modales, tablas
- ✅ **Validación End-to-End**: Flujo completo desde frontend hasta base de datos

### Estadísticas
- **Total de pruebas unitarias**: ~51 pruebas
- **Total de pruebas de integración**: 1 prueba de flujo completo (cubre 20 entidades)
- **Entidades probadas**: 20 entidades del sistema
- **Cobertura de endpoints**: Todos los endpoints principales de la API

---

## Ejecución de Pruebas

### Ejecutar todas las pruebas
```bash
pytest tests/ -v
```

### Solo pruebas unitarias
```bash
pytest tests/ -m unit -v
```

### Solo pruebas de integración
```bash
pytest tests/ -m integration -v
```

### Con cobertura de código
```bash
pytest tests/ --cov=backend --cov-report=html --cov-report=term
```

### Usando el script de Windows
```bash
run_tests.bat
```

---

## Requisitos para Ejecutar Pruebas

### Pruebas Unitarias
- Python 3.x
- pytest
- Dependencias de `requirements.txt`
- Base de datos PostgreSQL corriendo (Docker)

### Pruebas de Integración
- Todo lo anterior +
- Chrome/Chromium instalado
- ChromeDriver (se descarga automáticamente con webdriver-manager)
- Backend corriendo en `http://localhost:8000`
- Frontend accesible en `frontend/index.html`

---

## Notas Importantes

1. **Base de Datos**: Las pruebas unitarias usan la misma base de datos que el sistema en desarrollo. Se recomienda usar una base de datos de prueba separada para producción.

2. **Datos Únicos**: Las pruebas generan IDs únicos usando UUID para evitar conflictos entre ejecuciones.

3. **Pruebas de Integración**: La prueba de flujo completo está optimizada para ejecución rápida pero visible. Los tiempos de espera son reducidos (0.5s entre acciones principales, 0.01s entre caracteres) para acelerar la ejecución sin perder visibilidad.

4. **Fixtures**: Se utilizan fixtures de pytest para compartir configuración entre pruebas (cliente de API, sesión de BD, datos de ejemplo).

5. **Marcadores**: Las pruebas están marcadas con `@pytest.mark.unit` o `@pytest.mark.integration` para facilitar la ejecución selectiva.

---



---

**Última actualización**: Documento generado automáticamente basado en el código de pruebas existente.

