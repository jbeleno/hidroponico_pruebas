// Configuración
const API_BASE_URL = 'http://localhost:8000/api';
let currentEntity = 'empresas';
let currentEditId = null;

// Mapeo de entidades a sus campos
const entityFields = {
    'empresas': ['nombre', 'nit', 'activo'],
    'personas': ['nombre', 'apellido', 'documento', 'email', 'telefono', 'activo'],
    'sedes': ['empresa_id', 'nombre', 'direccion', 'latitud', 'longitud', 'responsable_id'],
    'bloques': ['sede_id', 'nombre', 'descripcion'],
    'tipos-espacio': ['nombre', 'descripcion'],
    'espacios': ['bloque_id', 'tipo_espacio_id', 'nombre', 'capacidad', 'ancho', 'largo', 'alto', 'ubicacion'],
    'tipos-estructura': ['nombre', 'descripcion'],
    'estructuras': ['espacio_id', 'tipo_estructura_id', 'codigo', 'nombre', 'capacidad', 'ancho', 'largo', 'posicion_x', 'posicion_y'],
    'usuarios': ['persona_id', 'empresa_id', 'username', 'password_hash', 'auto_registro'],
    'roles': ['nombre', 'descripcion'],
    'usuarios-roles': ['usuario_id', 'rol_id'],
    'metodos-acceso': ['usuario_id', 'tipo', 'dato_biometrico', 'activo'],
    'accesos-espacio': ['usuario_id', 'espacio_id', 'metodo_acceso'],
    'tipos-cultivo': ['nombre', 'descripcion'],
    'cultivos': ['tipo_cultivo_id', 'nombre', 'nombre_cientifico', 'descripcion'],
    'variedades-cultivo': ['cultivo_id', 'nombre', 'descripcion', 'caracteristicas'],
    'fases-produccion': ['nombre', 'duracion_estimada_dias', 'descripcion'],
    'cultivos-fases': ['variedad_cultivo_id', 'fase_produccion_id', 'orden', 'duracion_dias'],
    'nutrientes': ['nombre', 'formula_quimica', 'descripcion'],
    'fases-nutriente': ['cultivo_fase_id', 'nutriente_id', 'cantidad', 'unidad_medida', 'frecuencia']
};

// Tipos de campos
const fieldTypes = {
    'nombre': 'text',
    'apellido': 'text',
    'documento': 'text',
    'email': 'email',
    'telefono': 'text',
    'nit': 'text',
    'direccion': 'text',
    'descripcion': 'textarea',
    'caracteristicas': 'textarea',
    'formula_quimica': 'text',
    'ubicacion': 'text',
    'codigo': 'text',
    'username': 'text',
    'password_hash': 'text',
    'tipo': 'text',
    'dato_biometrico': 'text',
    'metodo_acceso': 'text',
    'unidad_medida': 'text',
    'frecuencia': 'text',
    'nombre_cientifico': 'text',
    'activo': 'checkbox',
    'auto_registro': 'checkbox',
    'empresa_id': 'number',
    'persona_id': 'number',
    'sede_id': 'number',
    'bloque_id': 'number',
    'tipo_espacio_id': 'number',
    'espacio_id': 'number',
    'tipo_estructura_id': 'number',
    'usuario_id': 'number',
    'rol_id': 'number',
    'tipo_cultivo_id': 'number',
    'cultivo_id': 'number',
    'variedad_cultivo_id': 'number',
    'fase_produccion_id': 'number',
    'cultivo_fase_id': 'number',
    'nutriente_id': 'number',
    'responsable_id': 'number',
    'latitud': 'number',
    'longitud': 'number',
    'capacidad': 'number',
    'ancho': 'number',
    'largo': 'number',
    'alto': 'number',
    'posicion_x': 'number',
    'posicion_y': 'number',
    'duracion_estimada_dias': 'number',
    'duracion_dias': 'number',
    'orden': 'number',
    'cantidad': 'number'
};

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    loadData();
});

// Configurar tabs
function setupTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentEntity = tab.dataset.entity;
            currentEditId = null;
            loadData();
        });
    });
}

// Cargar datos
async function loadData() {
    const tbody = document.getElementById('table-body');
    const thead = document.getElementById('table-head');
    tbody.innerHTML = '<tr><td colspan="100" class="loading">Cargando...</td></tr>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/${currentEntity}`);
        if (!response.ok) throw new Error('Error al cargar datos');
        
        const data = await response.json();
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="100" class="empty">No hay registros</td></tr>';
            return;
        }
        
        // Crear encabezados
        const headers = ['ID', ...entityFields[currentEntity], 'Acciones'];
        thead.innerHTML = `<tr>${headers.map(h => `<th>${formatHeader(h)}</th>`).join('')}</tr>`;
        
        // Crear filas
        tbody.innerHTML = data.map(item => {
            const cells = [
                item.id,
                ...entityFields[currentEntity].map(field => {
                    const value = item[field];
                    if (value === null || value === undefined) return '';
                    if (typeof value === 'boolean') return value ? '✓' : '✗';
                    if (field.includes('fecha')) return new Date(value).toLocaleString();
                    return String(value);
                }),
                `<button class="btn btn-edit" onclick="editItem(${item.id})">✏️ Editar</button>
                 <button class="btn btn-danger" onclick="deleteItem(${item.id})">🗑️ Eliminar</button>`
            ];
            return `<tr>${cells.map(cell => `<td>${cell}</td>`).join('')}</tr>`;
        }).join('');
        
        showMessage('Datos cargados correctamente', 'success');
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="100" class="error">Error: ${error.message}</td></tr>`;
        showMessage(`Error al cargar datos: ${error.message}`, 'error');
    }
}

// Formatear encabezado
function formatHeader(header) {
    return header
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

// Mostrar formulario de creación
function showCreateForm() {
    currentEditId = null;
    showModal('Nuevo Registro', getFormHTML());
}

// Mostrar formulario de edición
async function editItem(id) {
    currentEditId = id;
    try {
        const response = await fetch(`${API_BASE_URL}/${currentEntity}/${id}`);
        if (!response.ok) throw new Error('Error al cargar el registro');
        
        const data = await response.json();
        showModal('Editar Registro', getFormHTML(data));
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

// Obtener HTML del formulario
function getFormHTML(data = {}) {
    const fields = entityFields[currentEntity];
    const formFields = fields.map(field => {
        const type = fieldTypes[field] || 'text';
        const value = data[field] !== undefined ? data[field] : '';
        
        if (type === 'checkbox') {
            return `
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="${field}" ${value ? 'checked' : ''}>
                        ${formatHeader(field)}
                    </label>
                </div>
            `;
        } else if (type === 'textarea') {
            return `
                <div class="form-group">
                    <label>${formatHeader(field)}</label>
                    <textarea name="${field}" rows="3">${value}</textarea>
                </div>
            `;
        } else {
            return `
                <div class="form-group">
                    <label>${formatHeader(field)}</label>
                    <input type="${type}" name="${field}" value="${value}" ${type === 'number' ? 'step="any"' : ''}>
                </div>
            `;
        }
    }).join('');
    
    return `
        ${formFields}
        <div class="form-actions">
            <button type="button" class="btn btn-primary" onclick="saveItem()">Guardar</button>
            <button type="button" class="btn btn-cancel" onclick="closeModal()">Cancelar</button>
        </div>
    `;
}

// Guardar item
async function saveItem() {
    const form = document.getElementById('entity-form');
    const formData = new FormData(form);
    const data = {};
    
    // Convertir FormData a objeto
    for (const [key, value] of formData.entries()) {
        if (key === 'activo' || key === 'auto_registro') {
            data[key] = form.querySelector(`[name="${key}"]`).checked;
        } else if (fieldTypes[key] === 'number') {
            data[key] = value ? parseFloat(value) : null;
        } else {
            data[key] = value || null;
        }
    }
    
    try {
        const url = currentEditId 
            ? `${API_BASE_URL}/${currentEntity}/${currentEditId}`
            : `${API_BASE_URL}/${currentEntity}`;
        
        const method = currentEditId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al guardar');
        }
        
        closeModal();
        loadData();
        showMessage(`Registro ${currentEditId ? 'actualizado' : 'creado'} correctamente`, 'success');
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

// Eliminar item
async function deleteItem(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este registro?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/${currentEntity}/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Error al eliminar');
        
        loadData();
        showMessage('Registro eliminado correctamente', 'success');
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

// Mostrar modal
function showModal(title, content) {
    const modal = document.getElementById('modal');
    document.getElementById('modal-title').textContent = title;
    document.getElementById('entity-form').innerHTML = content;
    modal.style.display = 'block';
}

// Cerrar modal
function closeModal() {
    document.getElementById('modal').style.display = 'none';
    currentEditId = null;
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
}

// Mostrar mensaje
function showMessage(message, type) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 3000);
}

