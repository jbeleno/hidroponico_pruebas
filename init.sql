-- Script de inicialización opcional para PostgreSQL
-- Este archivo se ejecuta automáticamente al crear el contenedor

-- Crear extensión para UUID si es necesario (opcional)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Base de datos hidroponico inicializada correctamente';
END $$;

