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

**Archivo**: `tests/test_integration_selenium.py`

### Descripción
Pruebas end-to-end (E2E) del frontend usando Selenium WebDriver. Estas pruebas simulan la interacción de un usuario real con la interfaz web.

### Características
- **Navegador**: Chrome (configurado con ChromeDriverManager)
- **Modo**: Visible (no headless) para visualización durante las pruebas
- **Delays visuales**: Incluye pausas para visualización de las acciones
- **Escritura visible**: Escribe carácter por carácter para simular usuario real

### Pruebas CRUD Implementadas

Se han implementado pruebas CRUD completas (Crear, Leer, Actualizar, Eliminar) para las siguientes entidades:

1. **Empresas** (`test_crud_empresas`)
   - Crear empresa con nombre, NIT y estado activo
   - Editar empresa modificando nombre y NIT
   - Eliminar empresa

2. **Personas** (`test_crud_personas`)
   - Crear persona con datos completos
   - Editar persona modificando nombre y teléfono
   - Eliminar persona

3. **Tipos de Cultivo** (`test_crud_tipos_cultivo`)
   - Crear tipo de cultivo con nombre y descripción
   - Editar tipo de cultivo
   - Eliminar tipo de cultivo

4. **Nutrientes** (`test_crud_nutrientes`)
   - Crear nutriente con nombre, fórmula química y descripción
   - Editar nutriente
   - Eliminar nutriente

5. **Roles** (`test_crud_roles`)
   - Crear rol con nombre y descripción
   - Editar rol
   - Eliminar rol

6. **Tipos de Espacio** (`test_crud_tipos_espacio`)
   - Crear tipo de espacio
   - Editar tipo de espacio
   - Eliminar tipo de espacio

7. **Fases de Producción** (`test_crud_fases_produccion`)
   - Crear fase con nombre, duración estimada y descripción
   - Editar fase modificando duración
   - Eliminar fase

8. **Tipos de Estructura** (`test_crud_tipos_estructura`)
   - Crear tipo de estructura
   - Editar tipo de estructura
   - Eliminar tipo de estructura

9. **Métodos de Acceso** (`test_crud_metodos_acceso`)
   - Crear método de acceso con usuario_id, tipo y dato biométrico
   - Editar método de acceso
   - Eliminar método de acceso

10. **Sedes** (`test_crud_sedes`)
    - Crear sede con empresa_id, nombre, dirección y coordenadas
    - Editar sede
    - Eliminar sede

11. **Bloques** (`test_crud_bloques`)
    - Crear bloque con sede_id, nombre y descripción
    - Editar bloque
    - Eliminar bloque

12. **Espacios** (`test_crud_espacios`)
    - Crear espacio con dimensiones y capacidad
    - Editar espacio modificando capacidad
    - Eliminar espacio

13. **Estructuras** (`test_crud_estructuras`)
    - Crear estructura con código, nombre, capacidad y posiciones
    - Editar estructura
    - Eliminar estructura

14. **Usuarios** (`test_crud_usuarios`)
    - Crear usuario con persona_id, empresa_id, username y password_hash
    - Editar usuario
    - Eliminar usuario

15. **Usuarios-Roles** (`test_crud_usuarios_roles`)
    - Crear relación usuario-rol
    - Editar relación cambiando rol_id
    - Eliminar relación

16. **Accesos Espacio** (`test_crud_accesos_espacio`)
    - Crear acceso a espacio con usuario_id, espacio_id y método
    - Editar acceso
    - Eliminar acceso

17. **Cultivos** (`test_crud_cultivos`)
    - Crear cultivo con tipo_cultivo_id, nombre científico y descripción
    - Editar cultivo
    - Eliminar cultivo

18. **Variedades Cultivo** (`test_crud_variedades_cultivo`)
    - Crear variedad con cultivo_id, nombre, descripción y características
    - Editar variedad
    - Eliminar variedad

19. **Cultivos-Fases** (`test_crud_cultivos_fases`)
    - Crear relación cultivo-fase con orden y duración
    - Editar relación modificando orden y duración
    - Eliminar relación

20. **Fases-Nutriente** (`test_crud_fases_nutriente`)
    - Crear relación fase-nutriente con cantidad, unidad y frecuencia
    - Editar relación modificando cantidad y frecuencia
    - Eliminar relación

### Funciones Auxiliares

- `select_tab()`: Selecciona un tab específico en la interfaz
- `open_create_modal()`: Abre el modal de creación
- `save_form()`: Guarda el formulario
- `edit_first_item()`: Edita el primer elemento de la tabla
- `delete_first_item()`: Elimina el primer elemento de la tabla
- `fill_text_field()`: Llena campos de texto de forma visible
- `fill_number_field()`: Llena campos numéricos
- `fill_checkbox()`: Marca/desmarca checkboxes
- `fill_textarea()`: Llena textareas

### Ejecución
```bash
# Requiere Chrome instalado
pytest tests/test_integration_selenium.py -v -m integration
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
- ✅ **CRUD Completo**: 20 entidades con operaciones CRUD completas
- ✅ **Interfaz de Usuario**: Navegación, formularios, modales, tablas
- ✅ **Validación End-to-End**: Flujo completo desde frontend hasta base de datos

### Estadísticas
- **Total de pruebas unitarias**: ~50+ pruebas
- **Total de pruebas de integración**: 20 pruebas CRUD completas
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

3. **Pruebas de Integración**: Las pruebas de Selenium son más lentas y requieren que el navegador esté visible. Se pueden ejecutar en modo headless comentando la línea correspondiente.

4. **Fixtures**: Se utilizan fixtures de pytest para compartir configuración entre pruebas (cliente de API, sesión de BD, datos de ejemplo).

5. **Marcadores**: Las pruebas están marcadas con `@pytest.mark.unit` o `@pytest.mark.integration` para facilitar la ejecución selectiva.

---

## Mejoras Futuras

- [ ] Agregar pruebas de rendimiento
- [ ] Implementar pruebas de carga
- [ ] Agregar pruebas de seguridad
- [ ] Implementar pruebas de accesibilidad
- [ ] Agregar pruebas de compatibilidad entre navegadores
- [ ] Implementar CI/CD con ejecución automática de pruebas

---

**Última actualización**: Documento generado automáticamente basado en el código de pruebas existente.

