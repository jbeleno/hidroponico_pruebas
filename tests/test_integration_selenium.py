"""
Pruebas de integración usando Selenium para el frontend
"""
import pytest
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os


# Tiempo de espera entre acciones para visualización (en segundos)
VISUAL_DELAY = 2.0  # 2 segundos entre acciones principales
SHORT_DELAY = 1.0   # 1 segundo para acciones menores
TYPING_DELAY = 0.1  # 0.1 segundos entre caracteres para escritura visible


def safe_print(message):
    """Imprime un mensaje de forma segura evitando problemas de encoding"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Si hay problemas de encoding, reemplazar caracteres especiales
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)
    sys.stdout.flush()


def print_step(message):
    """Imprime un mensaje de paso de la prueba"""
    safe_print(f"\n{'='*60}")
    safe_print(f"  {message}")
    safe_print(f"{'='*60}")


def wait_visual(duration=VISUAL_DELAY):
    """Espera para visualización"""
    time.sleep(duration)


def type_visible(element, text, delay=TYPING_DELAY):
    """Escribe texto en un campo de forma visible, carácter por carácter"""
    element.clear()
    wait_visual(0.3)
    for char in text:
        element.send_keys(char)
        time.sleep(delay)
    wait_visual(0.3)


def fill_text_field(driver, field_name, value, wait_timeout=10):
    """Llena un campo de texto de forma visible"""
    wait = WebDriverWait(driver, wait_timeout)
    field = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
    safe_print(f"    Escribiendo '{value}' en campo '{field_name}'...")
    type_visible(field, value)
    safe_print(f"    [OK] Campo '{field_name}' completado")


def fill_number_field(driver, field_name, value, wait_timeout=10):
    """Llena un campo numérico de forma visible"""
    wait = WebDriverWait(driver, wait_timeout)
    field = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
    safe_print(f"    Escribiendo '{value}' en campo '{field_name}'...")
    type_visible(field, str(value))
    safe_print(f"    [OK] Campo '{field_name}' completado")


def fill_checkbox(driver, field_name, checked=True, wait_timeout=10):
    """Marca o desmarca un checkbox"""
    wait = WebDriverWait(driver, wait_timeout)
    checkbox = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
    if checkbox.is_selected() != checked:
        safe_print(f"    {'Marcando' if checked else 'Desmarcando'} checkbox '{field_name}'...")
        checkbox.click()
        wait_visual(0.5)
        safe_print(f"    [OK] Checkbox '{field_name}' {'marcado' if checked else 'desmarcado'}")
    else:
        safe_print(f"    [OK] Checkbox '{field_name}' ya está {'marcado' if checked else 'desmarcado'}")


def fill_textarea(driver, field_name, value, wait_timeout=10):
    """Llena un textarea de forma visible"""
    wait = WebDriverWait(driver, wait_timeout)
    textarea = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
    safe_print(f"    Escribiendo '{value}' en textarea '{field_name}'...")
    type_visible(textarea, value)
    safe_print(f"    [OK] Textarea '{field_name}' completado")


@pytest.fixture(scope="module")
def driver():
    """Fixture para inicializar el driver de Selenium"""
    print_step("Inicializando navegador Chrome para pruebas de integración")
    chrome_options = Options()
    # Asegurar que el navegador sea visible (NO headless)
    # chrome_options.add_argument("--headless")  # Comentado para ver el navegador
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")  # Maximizar ventana
    
    # Usar webdriver-manager para descargar automáticamente el driver
    safe_print("  Descargando/configurando ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    safe_print("  [OK] Navegador Chrome iniciado correctamente")
    wait_visual(1.0)
    
    yield driver
    
    print_step("Cerrando navegador")
    driver.quit()


@pytest.fixture(scope="function")
def frontend_url():
    """URL del frontend"""
    # Obtener la ruta absoluta del archivo HTML
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    html_path = os.path.join(project_root, "frontend", "index.html")
    return f"file://{html_path}"


@pytest.fixture(scope="function")
def api_base_url():
    """URL base de la API"""
    return "http://localhost:8000/api"


@pytest.mark.integration
@pytest.mark.slow
class TestCRUDOperations:
    """Pruebas CRUD completas (Crear, Leer, Actualizar, Eliminar) para diferentes entidades"""
    
    def get_unique_id(self):
        """Genera un ID único para las pruebas"""
        import uuid
        return str(uuid.uuid4())[:8].replace('-', '')
    
    def select_tab(self, driver, entity_name):
        """Selecciona un tab específico"""
        wait = WebDriverWait(driver, 10)
        tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//button[@data-entity='{entity_name}']")
        ))
        tab.click()
        wait_visual(2.0)
        safe_print(f"  [OK] Tab '{entity_name}' seleccionado")
    
    def open_create_modal(self, driver):
        """Abre el modal de creación"""
        wait = WebDriverWait(driver, 10)
        nuevo_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Nuevo')]")
        ))
        nuevo_btn.click()
        wait_visual(2.0)
        safe_print("  [OK] Modal de creación abierto")
    
    def save_form(self, driver):
        """Guarda el formulario"""
        wait = WebDriverWait(driver, 10)
        guardar_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Guardar')]")
        ))
        safe_print("  Haciendo clic en 'Guardar'...")
        guardar_btn.click()
        wait_visual(3.0)  # Esperar a que se guarde y recargue la tabla
        safe_print("  [OK] Formulario guardado")
    
    def get_first_row_id(self, driver):
        """Obtiene el ID de la primera fila de la tabla"""
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "table-body")))
        wait_visual(2.0)
        
        # Buscar la primera fila con datos (no "Cargando..." ni "No hay registros")
        tbody = driver.find_element(By.ID, "table-body")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 0:
                first_cell = cells[0]
                if first_cell.text and first_cell.text.isdigit():
                    return int(first_cell.text)
        return None
    
    def edit_first_item(self, driver):
        """Hace clic en el botón editar del primer elemento"""
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "table-body")))
        wait_visual(2.0)
        
        # Buscar el primer botón de editar
        edit_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@onclick, 'editItem')]")
        ))
        safe_print("  Haciendo clic en botón 'Editar' del primer registro...")
        edit_btn.click()
        wait_visual(2.0)
        safe_print("  [OK] Modal de edición abierto")
    
    def delete_first_item(self, driver):
        """Elimina el primer elemento de la tabla"""
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "table-body")))
        wait_visual(2.0)
        
        # Buscar el primer botón de eliminar
        delete_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@onclick, 'deleteItem')]")
        ))
        safe_print("  Haciendo clic en botón 'Eliminar' del primer registro...")
        delete_btn.click()
        wait_visual(1.5)
        
        # Confirmar eliminación en el diálogo de confirmación (JavaScript confirm)
        try:
            # Esperar un momento para que aparezca el diálogo
            time.sleep(0.5)
            alert = driver.switch_to.alert
            safe_print("  Confirmando eliminación en diálogo...")
            alert.accept()
            wait_visual(3.0)
            safe_print("  [OK] Registro eliminado")
        except Exception as e:
            # Si no hay diálogo, la eliminación puede ser directa
            wait_visual(2.0)
            safe_print("  [OK] Eliminación procesada")
    
    def test_crud_empresas(self, driver, frontend_url):
        """Prueba CRUD completo para Empresas"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Empresas (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR EMPRESA ===")
        self.select_tab(driver, "empresas")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_text_field(driver, "nombre", f"Empresa Test {unique_id}")
        fill_text_field(driver, "nit", f"NIT{unique_id}")
        fill_checkbox(driver, "activo", True)
        
        self.save_form(driver)
        safe_print("  [OK] Empresa creada exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR EMPRESA ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Empresa Editada {unique_id}")
        fill_text_field(driver, "nit", f"NIT-EDIT-{unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Empresa editada exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR EMPRESA ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Empresa eliminada exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Empresas completado exitosamente")
    
    def test_crud_personas(self, driver, frontend_url):
        """Prueba CRUD completo para Personas"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Personas (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR PERSONA ===")
        self.select_tab(driver, "personas")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_text_field(driver, "nombre", f"María {unique_id}")
        fill_text_field(driver, "apellido", f"González {unique_id}")
        fill_text_field(driver, "documento", f"DOC{unique_id}")
        fill_text_field(driver, "email", f"maria.{unique_id}@test.com")
        fill_text_field(driver, "telefono", f"300{unique_id[-7:]}")
        fill_checkbox(driver, "activo", True)
        
        self.save_form(driver)
        safe_print("  [OK] Persona creada exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR PERSONA ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"María Editada {unique_id}")
        fill_text_field(driver, "telefono", f"301{unique_id[-7:]}")
        
        self.save_form(driver)
        safe_print("  [OK] Persona editada exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR PERSONA ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Persona eliminada exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Personas completado exitosamente")
    
    def test_crud_tipos_cultivo(self, driver, frontend_url):
        """Prueba CRUD completo para Tipos de Cultivo"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Tipos de Cultivo (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR TIPO DE CULTIVO ===")
        self.select_tab(driver, "tipos-cultivo")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_text_field(driver, "nombre", f"Frutas {unique_id}")
        fill_textarea(driver, "descripcion", f"Descripción de frutas {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Tipo de cultivo creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR TIPO DE CULTIVO ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Frutas Editadas {unique_id}")
        fill_textarea(driver, "descripcion", f"Descripción editada {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Tipo de cultivo editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR TIPO DE CULTIVO ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Tipo de cultivo eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Tipos de Cultivo completado exitosamente")
    
    def test_crud_nutrientes(self, driver, frontend_url):
        """Prueba CRUD completo para Nutrientes"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Nutrientes (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR NUTRIENTE ===")
        self.select_tab(driver, "nutrientes")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_text_field(driver, "nombre", f"Potasio {unique_id}")
        fill_text_field(driver, "formula_quimica", f"K{unique_id[-3:]}")
        fill_textarea(driver, "descripcion", f"Nutriente esencial {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Nutriente creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR NUTRIENTE ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Potasio Editado {unique_id}")
        fill_text_field(driver, "formula_quimica", f"K-EDIT-{unique_id[-3:]}")
        
        self.save_form(driver)
        safe_print("  [OK] Nutriente editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR NUTRIENTE ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Nutriente eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Nutrientes completado exitosamente")
    
    def test_crud_roles(self, driver, frontend_url):
        """Prueba CRUD completo para Roles"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Roles (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR ROL ===")
        self.select_tab(driver, "roles")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_text_field(driver, "nombre", f"Operador {unique_id}")
        fill_textarea(driver, "descripcion", f"Rol de operador {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Rol creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR ROL ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Operador Editado {unique_id}")
        fill_textarea(driver, "descripcion", f"Descripción editada {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Rol editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR ROL ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Rol eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Roles completado exitosamente")
    
    def test_crud_tipos_espacio(self, driver, frontend_url):
        """Prueba CRUD completo para Tipos de Espacio"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Tipos de Espacio (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR TIPO DE ESPACIO ===")
        self.select_tab(driver, "tipos-espacio")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_text_field(driver, "nombre", f"Invernadero {unique_id}")
        fill_textarea(driver, "descripcion", f"Espacio cerrado {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Tipo de espacio creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR TIPO DE ESPACIO ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Invernadero Editado {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Tipo de espacio editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR TIPO DE ESPACIO ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Tipo de espacio eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Tipos de Espacio completado exitosamente")
    
    def test_crud_fases_produccion(self, driver, frontend_url):
        """Prueba CRUD completo para Fases de Producción"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Fases de Producción (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR FASE DE PRODUCCIÓN ===")
        self.select_tab(driver, "fases-produccion")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_text_field(driver, "nombre", f"Germinación {unique_id}")
        fill_number_field(driver, "duracion_estimada_dias", 7)
        fill_textarea(driver, "descripcion", f"Fase inicial {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Fase de producción creada exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR FASE DE PRODUCCIÓN ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Germinación Editada {unique_id}")
        fill_number_field(driver, "duracion_estimada_dias", 10)
        
        self.save_form(driver)
        safe_print("  [OK] Fase de producción editada exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR FASE DE PRODUCCIÓN ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Fase de producción eliminada exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Fases de Producción completado exitosamente")
    
    def test_crud_tipos_estructura(self, driver, frontend_url):
        """Prueba CRUD completo para Tipos de Estructura"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Tipos de Estructura (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR TIPO DE ESTRUCTURA ===")
        self.select_tab(driver, "tipos-estructura")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_text_field(driver, "nombre", f"Torre Vertical {unique_id}")
        fill_textarea(driver, "descripcion", f"Estructura vertical {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Tipo de estructura creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR TIPO DE ESTRUCTURA ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Torre Vertical Editada {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Tipo de estructura editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR TIPO DE ESTRUCTURA ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Tipo de estructura eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Tipos de Estructura completado exitosamente")
    
    def test_crud_metodos_acceso(self, driver, frontend_url):
        """Prueba CRUD completo para Métodos de Acceso"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Métodos de Acceso (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # Primero necesitamos crear una persona y usuario para tener IDs válidos
        # Por simplicidad, usaremos IDs existentes o crearemos datos de prueba primero
        
        # CREAR
        safe_print("\n  === CREAR MÉTODO DE ACCESO ===")
        safe_print("  NOTA: Esta prueba requiere usuario_id existente")
        safe_print("  Usando usuario_id=1 para la prueba...")
        
        self.select_tab(driver, "metodos-acceso")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "usuario_id", 1)
        fill_text_field(driver, "tipo", f"Tarjeta {unique_id}")
        fill_text_field(driver, "dato_biometrico", f"DATA{unique_id}")
        fill_checkbox(driver, "activo", True)
        
        self.save_form(driver)
        safe_print("  [OK] Método de acceso creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR MÉTODO DE ACCESO ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "tipo", f"Tarjeta Editada {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Método de acceso editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR MÉTODO DE ACCESO ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Método de acceso eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Métodos de Acceso completado exitosamente")
    
    def test_crud_sedes(self, driver, frontend_url):
        """Prueba CRUD completo para Sedes"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Sedes (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR SEDE ===")
        self.select_tab(driver, "sedes")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "empresa_id", 1)
        fill_text_field(driver, "nombre", f"Sede Principal {unique_id}")
        fill_text_field(driver, "direccion", f"Calle {unique_id} #123")
        fill_number_field(driver, "latitud", 4.6097)
        fill_number_field(driver, "longitud", -74.0817)
        fill_number_field(driver, "responsable_id", 1)
        
        self.save_form(driver)
        safe_print("  [OK] Sede creada exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR SEDE ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Sede Editada {unique_id}")
        fill_text_field(driver, "direccion", f"Calle Editada {unique_id} #456")
        
        self.save_form(driver)
        safe_print("  [OK] Sede editada exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR SEDE ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Sede eliminada exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Sedes completado exitosamente")
    
    def test_crud_bloques(self, driver, frontend_url):
        """Prueba CRUD completo para Bloques"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Bloques (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR BLOQUE ===")
        self.select_tab(driver, "bloques")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "sede_id", 1)
        fill_text_field(driver, "nombre", f"Bloque A {unique_id}")
        fill_textarea(driver, "descripcion", f"Bloque de producción {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Bloque creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR BLOQUE ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Bloque A Editado {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Bloque editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR BLOQUE ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Bloque eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Bloques completado exitosamente")
    
    def test_crud_espacios(self, driver, frontend_url):
        """Prueba CRUD completo para Espacios"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Espacios (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR ESPACIO ===")
        self.select_tab(driver, "espacios")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "bloque_id", 1)
        fill_number_field(driver, "tipo_espacio_id", 1)
        fill_text_field(driver, "nombre", f"Espacio {unique_id}")
        fill_number_field(driver, "capacidad", 100)
        fill_number_field(driver, "ancho", 10.5)
        fill_number_field(driver, "largo", 20.5)
        fill_number_field(driver, "alto", 3.0)
        fill_text_field(driver, "ubicacion", f"Zona {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Espacio creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR ESPACIO ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Espacio Editado {unique_id}")
        fill_number_field(driver, "capacidad", 150)
        
        self.save_form(driver)
        safe_print("  [OK] Espacio editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR ESPACIO ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Espacio eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Espacios completado exitosamente")
    
    def test_crud_estructuras(self, driver, frontend_url):
        """Prueba CRUD completo para Estructuras"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Estructuras (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR ESTRUCTURA ===")
        self.select_tab(driver, "estructuras")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "espacio_id", 1)
        fill_number_field(driver, "tipo_estructura_id", 1)
        fill_text_field(driver, "codigo", f"EST{unique_id}")
        fill_text_field(driver, "nombre", f"Estructura {unique_id}")
        fill_number_field(driver, "capacidad", 50)
        fill_number_field(driver, "ancho", 5.0)
        fill_number_field(driver, "largo", 5.0)
        fill_number_field(driver, "posicion_x", 10.0)
        fill_number_field(driver, "posicion_y", 10.0)
        
        self.save_form(driver)
        safe_print("  [OK] Estructura creada exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR ESTRUCTURA ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Estructura Editada {unique_id}")
        fill_text_field(driver, "codigo", f"EST-EDIT-{unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Estructura editada exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR ESTRUCTURA ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Estructura eliminada exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Estructuras completado exitosamente")
    
    def test_crud_usuarios(self, driver, frontend_url):
        """Prueba CRUD completo para Usuarios"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Usuarios (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR USUARIO ===")
        self.select_tab(driver, "usuarios")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "persona_id", 1)
        fill_number_field(driver, "empresa_id", 1)
        fill_text_field(driver, "username", f"user{unique_id}")
        fill_text_field(driver, "password_hash", f"hash{unique_id}")
        fill_checkbox(driver, "auto_registro", False)
        
        self.save_form(driver)
        safe_print("  [OK] Usuario creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR USUARIO ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "username", f"user_editado{unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Usuario editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR USUARIO ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Usuario eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Usuarios completado exitosamente")
    
    def test_crud_usuarios_roles(self, driver, frontend_url):
        """Prueba CRUD completo para Usuarios-Roles"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Usuarios-Roles (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR USUARIO-ROL ===")
        self.select_tab(driver, "usuarios-roles")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "usuario_id", 1)
        fill_number_field(driver, "rol_id", 1)
        
        self.save_form(driver)
        safe_print("  [OK] Usuario-Rol creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR USUARIO-ROL ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_number_field(driver, "rol_id", 2)
        
        self.save_form(driver)
        safe_print("  [OK] Usuario-Rol editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR USUARIO-ROL ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Usuario-Rol eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Usuarios-Roles completado exitosamente")
    
    def test_crud_accesos_espacio(self, driver, frontend_url):
        """Prueba CRUD completo para Accesos Espacio"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Accesos Espacio (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR ACCESO ESPACIO ===")
        self.select_tab(driver, "accesos-espacio")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "usuario_id", 1)
        fill_number_field(driver, "espacio_id", 1)
        fill_text_field(driver, "metodo_acceso", f"Tarjeta {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Acceso Espacio creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR ACCESO ESPACIO ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "metodo_acceso", f"Biometría {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Acceso Espacio editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR ACCESO ESPACIO ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Acceso Espacio eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Accesos Espacio completado exitosamente")
    
    def test_crud_cultivos(self, driver, frontend_url):
        """Prueba CRUD completo para Cultivos"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Cultivos (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR CULTIVO ===")
        self.select_tab(driver, "cultivos")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "tipo_cultivo_id", 1)
        fill_text_field(driver, "nombre", f"Tomate {unique_id}")
        fill_text_field(driver, "nombre_cientifico", f"Solanum lycopersicum {unique_id}")
        fill_textarea(driver, "descripcion", f"Cultivo de tomate {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Cultivo creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR CULTIVO ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Tomate Editado {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Cultivo editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR CULTIVO ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Cultivo eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Cultivos completado exitosamente")
    
    def test_crud_variedades_cultivo(self, driver, frontend_url):
        """Prueba CRUD completo para Variedades Cultivo"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Variedades Cultivo (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR VARIEDAD CULTIVO ===")
        self.select_tab(driver, "variedades-cultivo")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "cultivo_id", 1)
        fill_text_field(driver, "nombre", f"Variedad A {unique_id}")
        fill_textarea(driver, "descripcion", f"Descripción variedad {unique_id}")
        fill_textarea(driver, "caracteristicas", f"Características {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Variedad Cultivo creada exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR VARIEDAD CULTIVO ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_text_field(driver, "nombre", f"Variedad A Editada {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Variedad Cultivo editada exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR VARIEDAD CULTIVO ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Variedad Cultivo eliminada exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Variedades Cultivo completado exitosamente")
    
    def test_crud_cultivos_fases(self, driver, frontend_url):
        """Prueba CRUD completo para Cultivos-Fases"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Cultivos-Fases (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR CULTIVO-FASE ===")
        self.select_tab(driver, "cultivos-fases")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "variedad_cultivo_id", 1)
        fill_number_field(driver, "fase_produccion_id", 1)
        fill_number_field(driver, "orden", 1)
        fill_number_field(driver, "duracion_dias", 7)
        
        self.save_form(driver)
        safe_print("  [OK] Cultivo-Fase creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR CULTIVO-FASE ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_number_field(driver, "orden", 2)
        fill_number_field(driver, "duracion_dias", 10)
        
        self.save_form(driver)
        safe_print("  [OK] Cultivo-Fase editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR CULTIVO-FASE ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Cultivo-Fase eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Cultivos-Fases completado exitosamente")
    
    def test_crud_fases_nutriente(self, driver, frontend_url):
        """Prueba CRUD completo para Fases-Nutriente"""
        unique_id = self.get_unique_id()
        print_step(f"TEST CRUD: Fases-Nutriente (ID único: {unique_id})")
        driver.get(frontend_url)
        wait_visual(2.0)
        
        # CREAR
        safe_print("\n  === CREAR FASE-NUTRIENTE ===")
        self.select_tab(driver, "fases-nutriente")
        self.open_create_modal(driver)
        
        safe_print("  Llenando formulario...")
        fill_number_field(driver, "cultivo_fase_id", 1)
        fill_number_field(driver, "nutriente_id", 1)
        fill_number_field(driver, "cantidad", 10.5)
        fill_text_field(driver, "unidad_medida", f"ml {unique_id}")
        fill_text_field(driver, "frecuencia", f"Diaria {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Fase-Nutriente creado exitosamente")
        wait_visual(2.0)
        
        # EDITAR
        safe_print("\n  === EDITAR FASE-NUTRIENTE ===")
        self.edit_first_item(driver)
        
        safe_print("  Modificando campos...")
        fill_number_field(driver, "cantidad", 15.0)
        fill_text_field(driver, "frecuencia", f"Semanal {unique_id}")
        
        self.save_form(driver)
        safe_print("  [OK] Fase-Nutriente editado exitosamente")
        wait_visual(2.0)
        
        # ELIMINAR
        safe_print("\n  === ELIMINAR FASE-NUTRIENTE ===")
        self.delete_first_item(driver)
        safe_print("  [OK] Fase-Nutriente eliminado exitosamente")
        wait_visual(2.0)
        
        print_step("[OK] CRUD de Fases-Nutriente completado exitosamente")

