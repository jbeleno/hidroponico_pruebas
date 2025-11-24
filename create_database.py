import json
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Cargar configuración desde variables de entorno o valores por defecto
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'hidroponico'),
    'user': os.getenv('DB_USER', 'www-admin'),
    'password': os.getenv('DB_PASSWORD', 'hello!')
}

def mapear_tipo_dato(data_type, length):
    """Mapea tipos de datos del JSON a tipos de PostgreSQL"""
    tipo_map = {
        'int': 'INTEGER',
        'string': f'VARCHAR({length})' if length > 0 else 'TEXT',
        'boolean': 'BOOLEAN',
        'float': 'REAL',
        'timestamp': 'TIMESTAMP'
    }
    return tipo_map.get(data_type, 'TEXT')

def crear_tabla(conn, clase):
    """Crea una tabla basada en la definición de clase del JSON"""
    cursor = conn.cursor()
    
    # Construir columnas
    columnas = []
    foreign_keys = []
    
    for attr in clase['attributes']:
        nombre = attr['name']
        tipo = mapear_tipo_dato(attr['data_type'], attr['length'])
        
        # Construir definición de columna
        col_def = f'"{nombre}" {tipo}'
        
        # Agregar PRIMARY KEY
        if attr.get('primary_key') == 'True':
            col_def += ' PRIMARY KEY'
        
        # Agregar AUTOINCREMENT (SERIAL en PostgreSQL)
        if attr.get('autoincrement') == 'True':
            if attr['data_type'] == 'int':
                col_def = f'"{nombre}" SERIAL PRIMARY KEY'
        
        # Agregar NOT NULL para campos importantes
        if nombre in ['nombre', 'empresa_id', 'sede_id', 'bloque_id', 
                      'espacio_id', 'persona_id', 'usuario_id', 'username', 
                      'password_hash', 'tipo_cultivo_id', 'cultivo_id']:
            if 'PRIMARY KEY' not in col_def:
                col_def += ' NOT NULL'
        
        # Agregar UNIQUE para campos únicos
        if nombre in ['nit', 'documento', 'email', 'username', 'codigo']:
            if 'PRIMARY KEY' not in col_def:
                col_def += ' UNIQUE'
        
        # Agregar DEFAULT para campos booleanos
        if attr['data_type'] == 'boolean' and nombre in ['activo', 'auto_registro']:
            default_value = 'true' if nombre == 'activo' else 'false'
            col_def += f' DEFAULT {default_value}'
        
        # Agregar DEFAULT para timestamps
        if attr['data_type'] == 'timestamp' and nombre in ['fecha_creacion', 'fecha_acceso']:
            col_def += ' DEFAULT CURRENT_TIMESTAMP'
        
        columnas.append(col_def)
        
        # Preparar foreign keys
        if attr.get('foreign_key') == 'True':
            foreign_keys.append(nombre)
    
    # Construir query CREATE TABLE
    query = f'CREATE TABLE IF NOT EXISTS "{clase["class"]}" (\n'
    query += ',\n'.join(columnas)
    
    # Agregar foreign keys desde la sección references
    if 'references' in clase:
        for ref in clase['references']:
            campo_origen = ref['campo_origen']
            tabla_destino = ref['tabla_destino']
            campo_destino = ref['campo_destino']
            query += f',\nCONSTRAINT fk_{clase["class"]}_{campo_origen} '
            query += f'FOREIGN KEY ("{campo_origen}") '
            query += f'REFERENCES "{tabla_destino}" ("{campo_destino}") '
            query += 'ON DELETE CASCADE'
    
    query += '\n);'
    
    try:
        cursor.execute(query)
        conn.commit()
        print(f'✓ Tabla "{clase["class"]}" creada exitosamente')
    except psycopg2.Error as e:
        conn.rollback()
        print(f'✗ Error creando tabla "{clase["class"]}": {e}')
    finally:
        cursor.close()

def crear_indices(conn):
    """Crea índices para mejorar el rendimiento"""
    cursor = conn.cursor()
    
    indices = [
        'CREATE INDEX IF NOT EXISTS idx_sede_empresa_id ON "sede"("empresa_id");',
        'CREATE INDEX IF NOT EXISTS idx_sede_responsable_id ON "sede"("responsable_id");',
        'CREATE INDEX IF NOT EXISTS idx_bloque_sede_id ON "bloque"("sede_id");',
        'CREATE INDEX IF NOT EXISTS idx_espacio_bloque_id ON "espacio"("bloque_id");',
        'CREATE INDEX IF NOT EXISTS idx_espacio_tipo_espacio_id ON "espacio"("tipo_espacio_id");',
        'CREATE INDEX IF NOT EXISTS idx_estructura_espacio_id ON "estructura"("espacio_id");',
        'CREATE INDEX IF NOT EXISTS idx_usuario_persona_id ON "usuario"("persona_id");',
        'CREATE INDEX IF NOT EXISTS idx_usuario_empresa_id ON "usuario"("empresa_id");',
        'CREATE INDEX IF NOT EXISTS idx_acceso_espacio_usuario_id ON "acceso_espacio"("usuario_id");',
        'CREATE INDEX IF NOT EXISTS idx_acceso_espacio_espacio_id ON "acceso_espacio"("espacio_id");',
    ]
    
    for idx_query in indices:
        try:
            cursor.execute(idx_query)
            conn.commit()
            print(f'✓ Índice creado: {idx_query.split("ON")[1].split("(")[0].strip()}')
        except psycopg2.Error as e:
            print(f'✗ Error creando índice: {e}')
    
    cursor.close()

def main():
    """Función principal"""
    print("=" * 60)
    print("Creando base de datos desde JSON.json")
    print("=" * 60)
    
    # Cargar JSON
    try:
        with open('JSON.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("✗ Error: No se encontró el archivo JSON.json")
        return
    except json.JSONDecodeError as e:
        print(f"✗ Error: JSON inválido - {e}")
        return
    
    # Conectar a PostgreSQL
    try:
        print(f"\nConectando a PostgreSQL...")
        print(f"Host: {DB_CONFIG['host']}")
        print(f"Database: {DB_CONFIG['database']}")
        
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print("✓ Conexión exitosa\n")
    except psycopg2.Error as e:
        print(f"✗ Error conectando a PostgreSQL: {e}")
        return
    
    # Crear tablas en orden (respetando dependencias)
    print("Creando tablas...\n")
    
    # Orden de creación basado en dependencias
    orden_creacion = [
        'empresa', 'persona', 'tipo_espacio', 'tipo_estructura',
        'tipo_cultivo', 'fase_produccion', 'nutriente', 'rol',
        'sede', 'bloque', 'espacio', 'estructura',
        'usuario', 'usuario_rol', 'metodo_acceso', 'acceso_espacio',
        'cultivo', 'variedad_cultivo', 'cultivo_fase', 'fase_nutriente'
    ]
    
    # Crear diccionario de clases por nombre
    clases_dict = {clase['class']: clase for clase in data['classes']}
    
    # Crear tablas en orden
    for nombre_clase in orden_creacion:
        if nombre_clase in clases_dict:
            crear_tabla(conn, clases_dict[nombre_clase])
    
    # Crear índices
    print("\nCreando índices...\n")
    crear_indices(conn)
    
    # Verificar tablas creadas
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tablas = cursor.fetchall()
    cursor.close()
    
    print("\n" + "=" * 60)
    print(f"✓ Base de datos creada exitosamente!")
    print(f"✓ Total de tablas creadas: {len(tablas)}")
    print("\nTablas creadas:")
    for tabla in tablas:
        print(f"  - {tabla[0]}")
    print("=" * 60)
    
    conn.close()

if __name__ == '__main__':
    main()

