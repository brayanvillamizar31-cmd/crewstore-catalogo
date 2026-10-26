-- ==============================================================================
-- SISTEMA EN LA NUBE (SUPABASE): CATÁLOGO DE ROPA & TIENDA ONLINE
-- COPIA Y PEGA ESTE SCRIPT COMPLETO EN EL 'SQL EDITOR' DE TU PROYECTO SUPABASE Y PULSA 'RUN'
-- ==============================================================================

-- 1. TABLA DE PRODUCTOS (PRENDAS DEL CATÁLOGO)
CREATE TABLE IF NOT EXISTS public.products (
    id BIGINT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'Prendas Femeninas',
    supplier_price NUMERIC NOT NULL DEFAULT 20000,
    margin_percent NUMERIC NOT NULL DEFAULT 40,
    sale_price NUMERIC NOT NULL DEFAULT 28000,
    colors JSONB NOT NULL DEFAULT '["Blanco", "Negro"]'::jsonb,
    sizes JSONB NOT NULL DEFAULT '["Única"]'::jsonb,
    image TEXT NOT NULL,
    editorial_image TEXT,
    raw_image TEXT,
    active BOOLEAN NOT NULL DEFAULT true,
    description TEXT DEFAULT 'Prenda de alta calidad con diseño moderno.',
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- Asegurar columna editorial_image si la tabla ya existía
ALTER TABLE public.products ADD COLUMN IF NOT EXISTS editorial_image TEXT;

-- 2. TABLA DE CONFIGURACIÓN DE LA TIENDA
CREATE TABLE IF NOT EXISTS public.store_settings (
    id TEXT PRIMARY KEY DEFAULT 'main',
    store_name TEXT NOT NULL DEFAULT 'PERLA BOUTIQUE',
    whatsapp_number TEXT NOT NULL DEFAULT '573173104097',
    global_margin NUMERIC NOT NULL DEFAULT 40,
    admin_pin TEXT NOT NULL DEFAULT '1234',
    round_thousands BOOLEAN NOT NULL DEFAULT true,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 3. TABLA DE PEDIDOS REGISTRADOS
CREATE TABLE IF NOT EXISTS public.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_code TEXT NOT NULL UNIQUE,
    customer_name TEXT NOT NULL,
    customer_address TEXT NOT NULL,
    customer_phone TEXT,
    items JSONB NOT NULL,
    total NUMERIC NOT NULL,
    status TEXT NOT NULL DEFAULT 'pendiente',
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 4. POLÍTICAS DE ACCESO Y SEGURIDAD BLINDADA (Row Level Security - RLS)
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.store_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

-- Limpiar políticas anteriores
DROP POLICY IF EXISTS "Permitir lectura publica de productos" ON public.products;
DROP POLICY IF EXISTS "Permitir insercion y actualizacion de productos" ON public.products;
DROP POLICY IF EXISTS "Permitir modificacion solo a administradores autenticados" ON public.products;
DROP POLICY IF EXISTS "Permitir lectura publica de ajustes" ON public.store_settings;
DROP POLICY IF EXISTS "Permitir actualizacion de ajustes" ON public.store_settings;
DROP POLICY IF EXISTS "Permitir modificacion de ajustes solo a administradores" ON public.store_settings;
DROP POLICY IF EXISTS "Permitir creacion y lectura de pedidos" ON public.orders;
DROP POLICY IF EXISTS "Permitir crear pedidos a clientes" ON public.orders;
DROP POLICY IF EXISTS "Permitir lectura de pedidos solo a administradores" ON public.orders;
DROP POLICY IF EXISTS "Permitir gestion de pedidos solo a administradores" ON public.orders;

-- A) PRODUCTOS (PRENDAS):
-- 1. Clientes pueden ver las prendas 24/7 (Lectura pública)
CREATE POLICY "Permitir lectura publica de productos" ON public.products
    FOR SELECT TO anon, authenticated USING (true);

-- 2. Solo el Administrador con sesión iniciada puede crear, editar o eliminar prendas
CREATE POLICY "Permitir modificacion solo a administradores autenticados" ON public.products
    FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- B) AJUSTES DE TIENDA:
-- 1. Clientes pueden leer nombre y whatsapp de la tienda
CREATE POLICY "Permitir lectura publica de ajustes" ON public.store_settings
    FOR SELECT TO anon, authenticated USING (true);

-- 2. Solo el Administrador puede modificar los ajustes
CREATE POLICY "Permitir modificacion de ajustes solo a administradores" ON public.store_settings
    FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- C) PEDIDOS:
-- 1. Clientes pueden registrar pedidos desde el carrito
CREATE POLICY "Permitir crear pedidos a clientes" ON public.orders
    FOR INSERT TO anon, authenticated WITH CHECK (true);

-- 2. Solo el Administrador puede consultar o gestionar los pedidos de los clientes
CREATE POLICY "Permitir lectura de pedidos solo a administradores" ON public.orders
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "Permitir gestion de pedidos solo a administradores" ON public.orders
    FOR UPDATE TO authenticated USING (true);

-- Insertar configuración inicial por defecto
INSERT INTO public.store_settings (id, store_name, whatsapp_number, global_margin, admin_pin)
VALUES ('main', 'PERLA BOUTIQUE', '573173104097', 40, '1234')
ON CONFLICT (id) DO UPDATE SET store_name = 'PERLA BOUTIQUE';
