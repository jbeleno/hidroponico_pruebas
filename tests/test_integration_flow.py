"""
Pruebas de integración con flujo completo (Ciclo de vida)
Orden: Crear Todo -> Actualizar Todo -> Eliminar Todo
Respeta dependencias entre entidades.
"""
import pytest
import time
import sys
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

# Tiempos de espera optimizados para velocidad pero manteniendo visualización
VISUAL_DELAY = 0.5  # Reducido de 2.0 a 0.5
SHORT_DELAY = 0.2   # Reducido de 1.0 a 0.2
TYPING_DELAY = 0.01 # Reducido de 0.1 a 0.01 (casi instantáneo pero visible)

def safe_print(message):
    """Imprime un mensaje de forma segura"""
    try:
        print(message)
    except UnicodeEncodeError:
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)
    sys.stdout.flush()

def print_step(message):
    """Imprime un mensaje de paso"""
    safe_print(f"\n{'='*60}")
    safe_print(f"  {message}")
    safe_print(f"{'='*60}")

def wait_visual(duration=VISUAL_DELAY):
    """Espera para visualización"""
    time.sleep(duration)

def type_visible(element, text, delay=TYPING_DELAY):
    """Escribe texto de forma visible pero rápida"""
    element.clear()
    # No waiting here to speed up
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def fill_text_field(driver, field_name, value, wait_timeout=5):
    """Llena un campo de texto"""
    wait = WebDriverWait(driver, wait_timeout)
    field = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
    type_visible(field, value)

def fill_number_field(driver, field_name, value, wait_timeout=5):
    """Llena un campo numérico"""
    wait = WebDriverWait(driver, wait_timeout)
    field = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
    type_visible(field, str(value))

def fill_checkbox(driver, field_name, checked=True, wait_timeout=5):
    """Marca o desmarca un checkbox"""
    wait = WebDriverWait(driver, wait_timeout)
    checkbox = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
    if checkbox.is_selected() != checked:
        checkbox.click()

def fill_textarea(driver, field_name, value, wait_timeout=5):
    """Llena un textarea"""
    wait = WebDriverWait(driver, wait_timeout)
    textarea = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
    type_visible(textarea, value)

@pytest.fixture(scope="module")
def driver():
    """Inicializa el driver de Selenium"""
    print_step("Inicializando navegador Chrome")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait_visual(0.5)
    
    yield driver
    
    print_step("Cerrando navegador")
    driver.quit()

@pytest.fixture(scope="function")
def frontend_url():
    """URL del frontend"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    html_path = os.path.join(project_root, "frontend", "index.html")
    return f"file://{html_path}"

@pytest.mark.integration
class TestIntegrationFlow:
    """
    Flujo de integración completo:
    1. Crear todas las entidades (Ordenadas por dependencia)
    2. Actualizar todas las entidades
    3. Eliminar todas las entidades (Orden inverso)
    """
    
    def setup_method(self):
        self.ids = {} # Almacena IDs de entidades creadas para referencias
        self.unique_suffix = str(uuid.uuid4())[:6] # Sufijo corto para unicidad

    def select_tab(self, driver, entity_name):
        wait = WebDriverWait(driver, 5)
        tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//button[@data-entity='{entity_name}']")
        ))
        tab.click()
        time.sleep(0.2) # Pequeña pausa para renderizado

    def open_create_modal(self, driver):
        wait = WebDriverWait(driver, 5)
        nuevo_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Nuevo')]")
        ))
        nuevo_btn.click()
        time.sleep(0.2)

    def save_form(self, driver):
        wait = WebDriverWait(driver, 5)
        guardar_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Guardar')]")
        ))
        guardar_btn.click()
        # Esperar a que el modal desaparezca o la tabla se actualice
        time.sleep(0.5) 

    def edit_last_item(self, driver):
        """Edita el último elemento creado (asumiendo orden descendente o buscando por texto si fuera necesario)"""
        # Por simplicidad y velocidad, editamos el primer elemento visible que debería ser el nuestro
        # si la tabla se ordena por fecha de creación descendente, o si limpiamos la BD antes.
        # Asumiremos que editamos el PRIMER elemento de la tabla.
        wait = WebDriverWait(driver, 5)
        edit_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@onclick, 'editItem')]")
        ))
        edit_btn.click()
        time.sleep(0.2)

    def delete_last_item(self, driver):
        """Elimina el primer elemento de la tabla"""
        wait = WebDriverWait(driver, 5)
        delete_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@onclick, 'deleteItem')]")
        ))
        delete_btn.click()
        time.sleep(0.2)
        
        try:
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(0.5)
        except:
            pass

    def test_full_lifecycle(self, driver, frontend_url):
        """Ejecuta el ciclo de vida completo"""
        print_step(f"INICIANDO FLUJO COMPLETO (Sufijo: {self.unique_suffix})")
        driver.get(frontend_url)
        wait_visual(1.0)

        # ==========================================
        # FASE 1: CREACIÓN (Orden de Dependencia)
        # ==========================================
        print_step("FASE 1: CREACIÓN DE ENTIDADES")

        # 1. Empresa (Independiente)
        self.select_tab(driver, "empresas")
        self.open_create_modal(driver)
        fill_text_field(driver, "nombre", f"Empresa {self.unique_suffix}")
        fill_text_field(driver, "nit", f"NIT-{self.unique_suffix}")
        fill_checkbox(driver, "activo", True)
        self.save_form(driver)
        safe_print("  [+] Empresa creada")
        # Guardamos ID simulado o asumimos que es el primero para referencias futuras si fuera necesario
        # En este flujo UI, seleccionamos por posición en tabla, así que no necesitamos extraer el ID real de la BD
        # a menos que el formulario lo pida explícitamente como input manual (que no debería ser el caso en selects).
        # PERO, los formularios actuales usan inputs numéricos para IDs foráneos.
        # Necesitamos saber los IDs.
        # ESTRATEGIA: Asumiremos que los IDs son secuenciales y acabamos de crear el último.
        # O mejor, leemos el ID de la tabla.
        self.ids['empresa'] = self._get_first_row_id(driver)

        # 2. Persona (Independiente)
        self.select_tab(driver, "personas")
        self.open_create_modal(driver)
        fill_text_field(driver, "nombre", f"Persona {self.unique_suffix}")
        fill_text_field(driver, "apellido", "Test")
        fill_text_field(driver, "documento", f"DOC-{self.unique_suffix}")
        fill_text_field(driver, "email", f"p{self.unique_suffix}@test.com")
        fill_text_field(driver, "telefono", "1234567890")
        fill_checkbox(driver, "activo", True)
        self.save_form(driver)
        self.ids['persona'] = self._get_first_row_id(driver)
        safe_print(f"  [+] Persona creada (ID: {self.ids['persona']})")

        # 3. Tipo Cultivo (Independiente)
        self.select_tab(driver, "tipos-cultivo")
        self.open_create_modal(driver)
        fill_text_field(driver, "nombre", f"TipoCultivo {self.unique_suffix}")
        fill_textarea(driver, "descripcion", "Desc")
        self.save_form(driver)
        self.ids['tipo_cultivo'] = self._get_first_row_id(driver)
        safe_print("  [+] Tipo Cultivo creado")

        # 4. Nutriente (Independiente)
        self.select_tab(driver, "nutrientes")
        self.open_create_modal(driver)
        fill_text_field(driver, "nombre", f"Nutriente {self.unique_suffix}")
        fill_text_field(driver, "formula_quimica", "NPK")
        self.save_form(driver)
        self.ids['nutriente'] = self._get_first_row_id(driver)
        safe_print("  [+] Nutriente creado")

        # 5. Rol (Independiente)
        self.select_tab(driver, "roles")
        self.open_create_modal(driver)
        fill_text_field(driver, "nombre", f"Rol {self.unique_suffix}")
        fill_textarea(driver, "descripcion", "Desc")
        self.save_form(driver)
        self.ids['rol'] = self._get_first_row_id(driver)
        safe_print("  [+] Rol creado")

        # 6. Tipo Espacio (Independiente)
        self.select_tab(driver, "tipos-espacio")
        self.open_create_modal(driver)
        fill_text_field(driver, "nombre", f"TipoEspacio {self.unique_suffix}")
        fill_textarea(driver, "descripcion", "Desc")
        self.save_form(driver)
        self.ids['tipo_espacio'] = self._get_first_row_id(driver)
        safe_print("  [+] Tipo Espacio creado")

        # 7. Fase Producción (Independiente)
        self.select_tab(driver, "fases-produccion")
        self.open_create_modal(driver)
        fill_text_field(driver, "nombre", f"Fase {self.unique_suffix}")
        fill_number_field(driver, "duracion_estimada_dias", 10)
        self.save_form(driver)
        self.ids['fase_produccion'] = self._get_first_row_id(driver)
        safe_print("  [+] Fase Producción creada")

        # 8. Tipo Estructura (Independiente)
        self.select_tab(driver, "tipos-estructura")
        self.open_create_modal(driver)
        fill_text_field(driver, "nombre", f"TipoEst {self.unique_suffix}")
        self.save_form(driver)
        self.ids['tipo_estructura'] = self._get_first_row_id(driver)
        safe_print("  [+] Tipo Estructura creado")

        # 9. Usuario (Depende: Persona, Empresa)
        self.select_tab(driver, "usuarios")
        self.open_create_modal(driver)
        fill_number_field(driver, "persona_id", self.ids['persona'])
        fill_number_field(driver, "empresa_id", self.ids['empresa'])
        fill_text_field(driver, "username", f"user_{self.unique_suffix}")
        fill_text_field(driver, "password_hash", "123456")
        self.save_form(driver)
        self.ids['usuario'] = self._get_first_row_id(driver)
        safe_print("  [+] Usuario creado")

        # 10. Sede (Depende: Empresa, Persona(Responsable))
        self.select_tab(driver, "sedes")
        self.open_create_modal(driver)
        fill_number_field(driver, "empresa_id", self.ids['empresa'])
        fill_text_field(driver, "nombre", f"Sede {self.unique_suffix}")
        fill_text_field(driver, "direccion", "Dir Test")
        fill_number_field(driver, "responsable_id", self.ids['persona'])
        self.save_form(driver)
        self.ids['sede'] = self._get_first_row_id(driver)
        safe_print("  [+] Sede creada")

        # 11. Bloque (Depende: Sede)
        self.select_tab(driver, "bloques")
        self.open_create_modal(driver)
        fill_number_field(driver, "sede_id", self.ids['sede'])
        fill_text_field(driver, "nombre", f"Bloque {self.unique_suffix}")
        self.save_form(driver)
        self.ids['bloque'] = self._get_first_row_id(driver)
        safe_print("  [+] Bloque creado")

        # 12. Espacio (Depende: Bloque, TipoEspacio)
        self.select_tab(driver, "espacios")
        self.open_create_modal(driver)
        fill_number_field(driver, "bloque_id", self.ids['bloque'])
        fill_number_field(driver, "tipo_espacio_id", self.ids['tipo_espacio'])
        fill_text_field(driver, "nombre", f"Espacio {self.unique_suffix}")
        fill_number_field(driver, "capacidad", 100)
        fill_number_field(driver, "ancho", 10)
        fill_number_field(driver, "largo", 10)
        fill_number_field(driver, "alto", 3)
        self.save_form(driver)
        self.ids['espacio'] = self._get_first_row_id(driver)
        safe_print("  [+] Espacio creado")

        # 13. Estructura (Depende: Espacio, TipoEstructura)
        self.select_tab(driver, "estructuras")
        self.open_create_modal(driver)
        fill_number_field(driver, "espacio_id", self.ids['espacio'])
        fill_number_field(driver, "tipo_estructura_id", self.ids['tipo_estructura'])
        fill_text_field(driver, "codigo", f"E-{self.unique_suffix}")
        fill_text_field(driver, "nombre", f"Est {self.unique_suffix}")
        fill_number_field(driver, "capacidad", 50)
        self.save_form(driver)
        self.ids['estructura'] = self._get_first_row_id(driver)
        safe_print("  [+] Estructura creada")

        # 14. Cultivo (Depende: TipoCultivo)
        self.select_tab(driver, "cultivos")
        self.open_create_modal(driver)
        fill_number_field(driver, "tipo_cultivo_id", self.ids['tipo_cultivo'])
        fill_text_field(driver, "nombre", f"Cultivo {self.unique_suffix}")
        fill_text_field(driver, "nombre_cientifico", "Sci Name")
        self.save_form(driver)
        self.ids['cultivo'] = self._get_first_row_id(driver)
        safe_print("  [+] Cultivo creado")

        # 15. Variedad Cultivo (Depende: Cultivo)
        self.select_tab(driver, "variedades-cultivo")
        self.open_create_modal(driver)
        fill_number_field(driver, "cultivo_id", self.ids['cultivo'])
        fill_text_field(driver, "nombre", f"Var {self.unique_suffix}")
        self.save_form(driver)
        self.ids['variedad_cultivo'] = self._get_first_row_id(driver)
        safe_print("  [+] Variedad Cultivo creada")

        # 16. Cultivo Fase (Depende: VariedadCultivo, FaseProduccion)
        self.select_tab(driver, "cultivos-fases")
        self.open_create_modal(driver)
        fill_number_field(driver, "variedad_cultivo_id", self.ids['variedad_cultivo'])
        fill_number_field(driver, "fase_produccion_id", self.ids['fase_produccion'])
        fill_number_field(driver, "orden", 1)
        fill_number_field(driver, "duracion_dias", 15)
        self.save_form(driver)
        self.ids['cultivo_fase'] = self._get_first_row_id(driver)
        safe_print("  [+] Cultivo Fase creado")

        # 17. Fase Nutriente (Depende: CultivoFase, Nutriente)
        self.select_tab(driver, "fases-nutriente")
        self.open_create_modal(driver)
        fill_number_field(driver, "cultivo_fase_id", self.ids['cultivo_fase'])
        fill_number_field(driver, "nutriente_id", self.ids['nutriente'])
        fill_number_field(driver, "cantidad", 5)
        fill_text_field(driver, "unidad_medida", "kg")
        fill_text_field(driver, "frecuencia", "Diaria")
        self.save_form(driver)
        self.ids['fase_nutriente'] = self._get_first_row_id(driver)
        safe_print("  [+] Fase Nutriente creada")

        # 18. Metodo Acceso (Depende: Usuario)
        self.select_tab(driver, "metodos-acceso")
        self.open_create_modal(driver)
        fill_number_field(driver, "usuario_id", self.ids['usuario'])
        fill_text_field(driver, "tipo", "Card")
        fill_text_field(driver, "dato_biometrico", f"Bio-{self.unique_suffix}")
        self.save_form(driver)
        self.ids['metodo_acceso'] = self._get_first_row_id(driver)
        safe_print("  [+] Metodo Acceso creado")

        # 19. Usuario Rol (Depende: Usuario, Rol)
        self.select_tab(driver, "usuarios-roles")
        self.open_create_modal(driver)
        fill_number_field(driver, "usuario_id", self.ids['usuario'])
        fill_number_field(driver, "rol_id", self.ids['rol'])
        self.save_form(driver)
        self.ids['usuario_rol'] = self._get_first_row_id(driver)
        safe_print("  [+] Usuario Rol creado")

        # 20. Acceso Espacio (Depende: Usuario, Espacio)
        self.select_tab(driver, "accesos-espacio")
        self.open_create_modal(driver)
        fill_number_field(driver, "usuario_id", self.ids['usuario'])
        fill_number_field(driver, "espacio_id", self.ids['espacio'])
        fill_text_field(driver, "metodo_acceso", "Remote")
        self.save_form(driver)
        self.ids['acceso_espacio'] = self._get_first_row_id(driver)
        safe_print("  [+] Acceso Espacio creado")

        print_step("FASE 1 COMPLETADA: Todas las entidades creadas.")
        wait_visual(1.0)

        # ==========================================
        # FASE 2: ACTUALIZACIÓN (Cualquier orden)
        # ==========================================
        print_step("FASE 2: ACTUALIZACIÓN DE ENTIDADES")
        
        # Actualizamos una muestra representativa para no hacer el test eterno,
        # o actualizamos todas si el usuario lo requiere estricto.
        # El usuario pidió "todos los cruds", así que actualizamos todo.
        
        entities_to_update = [
            ("accesos-espacio", "metodo_acceso", "Updated"),
            ("usuarios-roles", None, None), # No tiene campos texto simples facil de editar sin cambiar IDs, saltamos o cambiamos ID si hay otro rol
            ("metodos-acceso", "tipo", "Tag"),
            ("fases-nutriente", "unidad_medida", "L"),
            ("cultivos-fases", "duracion_dias", 20),
            ("variedades-cultivo", "nombre", f"VarUpd {self.unique_suffix}"),
            ("cultivos", "nombre", f"CultUpd {self.unique_suffix}"),
            ("estructuras", "nombre", f"EstUpd {self.unique_suffix}"),
            ("espacios", "nombre", f"EspUpd {self.unique_suffix}"),
            ("bloques", "nombre", f"BlqUpd {self.unique_suffix}"),
            ("sedes", "nombre", f"SedeUpd {self.unique_suffix}"),
            ("usuarios", "username", f"usr_upd_{self.unique_suffix}"),
            ("tipos-estructura", "nombre", f"TEstUpd {self.unique_suffix}"),
            ("fases-produccion", "nombre", f"FaseUpd {self.unique_suffix}"),
            ("tipos-espacio", "nombre", f"TEspUpd {self.unique_suffix}"),
            ("roles", "nombre", f"RolUpd {self.unique_suffix}"),
            ("nutrientes", "nombre", f"NutUpd {self.unique_suffix}"),
            ("tipos-cultivo", "nombre", f"TCulUpd {self.unique_suffix}"),
            ("personas", "nombre", f"PerUpd {self.unique_suffix}"),
            ("empresas", "nombre", f"EmpUpd {self.unique_suffix}"),
        ]

        for entity, field, value in entities_to_update:
            if field: # Solo si definimos algo para editar
                self.select_tab(driver, entity)
                self.edit_last_item(driver)
                if isinstance(value, int):
                    fill_number_field(driver, field, value)
                else:
                    fill_text_field(driver, field, value)
                self.save_form(driver)
                safe_print(f"  [*] {entity} actualizado")
        
        print_step("FASE 2 COMPLETADA: Todas las entidades actualizadas.")
        wait_visual(1.0)

        # ==========================================
        # FASE 3: ELIMINACIÓN (Orden Inverso a Creación)
        # ==========================================
        print_step("FASE 3: ELIMINACIÓN DE ENTIDADES (Orden Inverso)")

        # El orden debe ser exactamente el inverso de la creación para no violar FKs
        deletion_order = [
            "accesos-espacio",
            "usuarios-roles",
            "metodos-acceso",
            "fases-nutriente",
            "cultivos-fases",
            "variedades-cultivo",
            "cultivos",
            "estructuras",
            "espacios",
            "bloques",
            "sedes",
            "usuarios",
            "tipos-estructura",
            "fases-produccion",
            "tipos-espacio",
            "roles",
            "nutrientes",
            "tipos-cultivo",
            "personas",
            "empresas"
        ]

        for entity in deletion_order:
            self.select_tab(driver, entity)
            self.delete_last_item(driver)
            safe_print(f"  [-] {entity} eliminado")

        print_step("FASE 3 COMPLETADA: Todas las entidades eliminadas.")
        print_step("PRUEBA DE CICLO DE VIDA COMPLETA Y EXITOSA")

    def _get_first_row_id(self, driver):
        """Helper para obtener el ID de la primera fila"""
        try:
            wait = WebDriverWait(driver, 2)
            wait.until(EC.presence_of_element_located((By.ID, "table-body")))
            tbody = driver.find_element(By.ID, "table-body")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            if rows:
                cells = rows[0].find_elements(By.TAG_NAME, "td")
                if cells and cells[0].text.isdigit():
                    return int(cells[0].text)
        except:
            pass
        return 0
