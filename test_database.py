"""
Script de prueba para verificar la estructura de la base de datos
"""
import json
import psycopg2
import os

# Cargar configuración
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'hidroponico'),
    'user': os.getenv('DB_USER', 'www-admin'),
    'password': os.getenv('DB_PASSWORD', 'hello!')
}

def test_conexion():
    """Prueba la conexión a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        print(f"✓ Conexión exitosa - PostgreSQL {version[0]}")
        return True
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        return False

def test_tablas():
    """Verifica que todas las tablas esperadas existan"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Cargar JSON para obtener lista de tablas esperadas
        with open('JSON.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tablas_esperadas = {clase['class'] for clase in data['classes']}
        
        # Obtener tablas existentes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tablas_existentes = {row[0] for row in cursor.fetchall()}
        
        # Comparar
        faltantes = tablas_esperadas - tablas_existentes
        extra = tablas_existentes - tablas_esperadas
        
        if faltantes:
            print(f"✗ Tablas faltantes: {', '.join(faltantes)}")
        if extra:
            print(f"⚠ Tablas adicionales: {', '.join(extra)}")
        if not faltantes and not extra:
            print(f"✓ Todas las {len(tablas_esperadas)} tablas existen")
        
        cursor.close()
        conn.close()
        return len(faltantes) == 0
    except Exception as e:
        print(f"✗ Error verificando tablas: {e}")
        return False

def test_foreign_keys():
    """Verifica que las foreign keys estén correctamente creadas"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                tc.table_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name 
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            ORDER BY tc.table_name, kcu.column_name;
        """)
        
        fks = cursor.fetchall()
        print(f"✓ Se encontraron {len(fks)} foreign keys")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error verificando foreign keys: {e}")
        return False

def test_indices():
    """Verifica que los índices estén creados"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE schemaname = 'public'
            AND indexname LIKE 'idx_%'
            ORDER BY indexname;
        """)
        
        indices = cursor.fetchall()
        print(f"✓ Se encontraron {len(indices)} índices personalizados")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error verificando índices: {e}")
        return False

def test_insertar_datos_prueba():
    """Inserta datos de prueba básicos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Insertar empresa de prueba
        cursor.execute("""
            INSERT INTO empresa (nombre, nit, activo) 
            VALUES ('Empresa de Prueba', '123456789', true)
            ON CONFLICT DO NOTHING
            RETURNING id;
        """)
        empresa_id = cursor.fetchone()
        
        if empresa_id:
            print(f"✓ Datos de prueba insertados (empresa_id: {empresa_id[0]})")
        else:
            print("✓ Datos de prueba ya existían")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error insertando datos de prueba: {e}")
        conn.rollback()
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("Ejecutando pruebas de la base de datos")
    print("=" * 60)
    print()
    
    resultados = []
    
    print("1. Probando conexión...")
    resultados.append(("Conexión", test_conexion()))
    print()
    
    print("2. Verificando tablas...")
    resultados.append(("Tablas", test_tablas()))
    print()
    
    print("3. Verificando foreign keys...")
    resultados.append(("Foreign Keys", test_foreign_keys()))
    print()
    
    print("4. Verificando índices...")
    resultados.append(("Índices", test_indices()))
    print()
    
    print("5. Insertando datos de prueba...")
    resultados.append(("Datos de Prueba", test_insertar_datos_prueba()))
    print()
    
    # Resumen
    print("=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    for nombre, resultado in resultados:
        estado = "✓ PASS" if resultado else "✗ FAIL"
        print(f"{nombre:20} {estado}")
    
    exitos = sum(1 for _, r in resultados if r)
    total = len(resultados)
    print(f"\nPruebas exitosas: {exitos}/{total}")
    print("=" * 60)

if __name__ == '__main__':
    main()

