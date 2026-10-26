import json
import os

with open('/Users/ginavillamizar/Documents/crewstore-catalogo/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Sort products by ID to ensure sequence 1..431
products.sort(key=lambda x: x['id'])
products_json_str = json.dumps(products, indent=2, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>crewstore.co | Catálogo Oficial 2026 • Camisetas Deportivas, Retro & Streetwear</title>
  <meta name="description" content="crewstore.co: Catálogo oficial 2026. Camisetas de fútbol, retro originals, NBA, Atlético Bucaramanga, buzos y moda urbana. Envíos y atención personalizada por WhatsApp.">
  <meta name="keywords" content="crewstore.co, camisetas deportivas, camisetas retro, camisetas futbol, NBA, moda urbana, buzos, bermudas, pantalonetas, Colombia">
  <meta property="og:title" content="crewstore.co | Catálogo Oficial 2026 • Camisetas Deportivas, Retro & Streetwear">
  <meta property="og:description" content="Catálogo digital oficial crewstore.co 2026. Camisetas de fútbol, retro originals, buzos y moda urbana. Pide fácil por WhatsApp con envío a domicilio.">
  <meta property="og:type" content="website">
  <link rel="icon" type="image/jpeg" href="logo.jpg">
  <link rel="apple-touch-icon" href="logo.jpg">
  <meta property="og:image" content="logo.jpg">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ClothingStore",
    "name": "crewstore.co",
    "description": "Catálogo Oficial Digital de crewstore.co 2026. Camisetas deportivas, retro y moda urbana.",
    "CurrenciesAccepted": "COP",
    "paymentAccepted": "Efectivo, Transferencia, Pago Contraentrega"
  }}
  </script>
  
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ -webkit-tap-highlight-color: transparent; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; scroll-behavior: smooth; }}
    body {{ background-color: #f7f7f6; color: #171717; min-height: 100vh; display: flex; flex-direction: column; overflow-x: hidden; }}
    
    .container {{ max-width: 1240px; margin: 0 auto; padding: 0 16px; width: 100%; }}
    
    /* PALETA: NEGRO (#0c0a09, #171717), BLANCO (#ffffff), DORADO (#d4af37, #facc15, #eab308) */
    
    /* 1. Barra Anuncio */
    .top-announcement {{ background: #050505; color: #facc15; font-size: 11px; padding: 8px 16px; text-transform: uppercase; letter-spacing: 1px; display: flex; justify-content: space-between; align-items: center; z-index: 40; border-bottom: 1px solid rgba(212, 175, 55, 0.25); }}
    .top-announcement span:last-child {{ color: #ffffff; }}

    /* 2. Navbar de Lujo */
    .navbar {{ position: sticky; top: 0; z-index: 35; background: rgba(12, 10, 9, 0.96); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 2px solid #d4af37; height: 68px; display: flex; align-items: center; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
    .nav-content {{ display: flex; justify-content: space-between; align-items: center; width: 100%; }}
    .brand {{ display: flex; align-items: center; gap: 12px; text-decoration: none; color: inherit; cursor: pointer; }}
    .brand-logo-img {{ width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 2px solid #d4af37; box-shadow: 0 0 12px rgba(212, 175, 55, 0.4); }}
    .brand-title {{ font-size: 19px; font-weight: 800; letter-spacing: 0.5px; line-height: 1.1; color: #ffffff; }}
    .brand-sub {{ font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #d4af37; font-weight: 700; }}
    
    .nav-actions {{ display: flex; align-items: center; gap: 8px; }}
    .btn-cart-nav {{ background: linear-gradient(135deg, #facc15 0%, #eab308 100%); color: #0c0a09; border: none; padding: 8px 18px; border-radius: 9999px; font-size: 12px; font-weight: 800; display: flex; align-items: center; gap: 8px; cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 10px rgba(212, 175, 55, 0.35); }}
    .btn-cart-nav:hover {{ transform: translateY(-1px); filter: brightness(1.08); }}
    .badge-count {{ background: #0c0a09; color: #facc15; font-weight: 800; font-size: 11px; padding: 2px 7px; border-radius: 9999px; font-family: monospace; border: 1px solid #d4af37; }}
    
    /* 3. Hero Banner Oficial */
    .hero {{ background: radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.16) 0%, #0c0a09 75%); color: #ffffff; padding: 24px 20px; border-radius: 20px; margin: 16px 0 16px 0; border: 1px solid rgba(212, 175, 55, 0.35); box-shadow: 0 12px 30px rgba(0,0,0,0.35); position: relative; overflow: hidden; }}
    .hero-tag {{ display: inline-block; background: rgba(250, 204, 21, 0.12); color: #facc15; border: 1px solid rgba(250, 204, 21, 0.35); font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; padding: 4px 12px; border-radius: 9999px; margin-bottom: 8px; }}
    .hero h2 {{ font-size: 26px; font-weight: 900; margin-bottom: 8px; line-height: 1.2; color: #ffffff; letter-spacing: 0.5px; }}
    .hero p {{ font-size: 13px; color: #d4d4d4; max-width: 650px; line-height: 1.5; margin-bottom: 14px; font-weight: 400; }}
    .hero-features {{ display: flex; flex-wrap: wrap; gap: 10px; font-size: 11px; color: #ffffff; font-weight: 600; }}
    .hero-badge {{ background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(212, 175, 55, 0.3); padding: 5px 10px; border-radius: 8px; display: inline-flex; align-items: center; gap: 6px; }}
    
    /* 4. Banner de Cestas / Combos Promocionales */
    .promo-basket {{ max-width: 100%; margin: 0 0 16px 0; background: #0c0a09; color: #ffffff; border-radius: 16px; padding: 14px 18px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; border: 1px solid rgba(212, 175, 55, 0.4); box-shadow: 0 4px 16px rgba(0,0,0,0.15); }}
    .promo-tag {{ font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #facc15; font-weight: 800; }}
    .promo-title {{ font-size: 14px; font-weight: 800; color: #ffffff; }}
    .promo-sub {{ font-size: 11px; color: #a3a3a3; }}
    .btn-promo {{ background: linear-gradient(135deg, #facc15 0%, #eab308 100%); color: #0c0a09; border: none; padding: 8px 16px; border-radius: 9999px; font-size: 11px; font-weight: 800; cursor: pointer; white-space: nowrap; }}
    
    /* 5. Barra de Navegación Pegajosa (Buscador + Píldoras de Categorías) */
    .sticky-controls {{ position: sticky; top: 68px; z-index: 30; background: #f7f7f6; padding: 12px 0 10px 0; border-bottom: 1px solid #e5e5e5; margin-bottom: 20px; }}
    
    .search-bar-wrap {{ background: #ffffff; border: 1.5px solid #d4af37; border-radius: 14px; padding: 10px 14px; display: flex; align-items: center; gap: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.05); margin-bottom: 10px; }}
    .search-icon {{ font-size: 16px; color: #d4af37; }}
    .search-input {{ width: 100%; border: none; background: transparent; font-size: 14px; font-weight: 600; outline: none; color: #0c0a09; }}
    .search-input::placeholder {{ color: #737373; font-weight: 400; }}
    .btn-clear-search {{ background: #f5f5f4; border: none; width: 22px; height: 22px; border-radius: 50%; color: #737373; font-size: 11px; font-weight: bold; cursor: pointer; display: none; align-items: center; justify-content: center; }}
    
    /* Píldoras de Secciones con scroll horizontal suave */
    .category-pills-bar {{ display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px; scrollbar-width: none; -ms-overflow-style: none; -webkit-overflow-scrolling: touch; }}
    .category-pills-bar::-webkit-scrollbar {{ display: none; }}
    
    .cat-pill {{ background: #0c0a09; color: #f5f5f4; border: 1px solid rgba(212, 175, 55, 0.35); padding: 7px 14px; border-radius: 9999px; font-size: 11px; font-weight: 700; cursor: pointer; white-space: nowrap; transition: all 0.2s; display: inline-flex; align-items: center; gap: 6px; }}
    .cat-pill:hover {{ border-color: #facc15; color: #ffffff; transform: translateY(-1px); }}
    .cat-pill.active {{ background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%); color: #0c0a09; border-color: #fde047; font-weight: 800; box-shadow: 0 3px 12px rgba(212, 175, 55, 0.4); }}
    .cat-pill .pill-count {{ background: rgba(0,0,0,0.18); font-size: 9px; padding: 2px 6px; border-radius: 9999px; font-family: monospace; }}
    .cat-pill:not(.active) .pill-count {{ background: rgba(255,255,255,0.15); color: #facc15; }}
    
    /* Indicador de Estado / Modo de Vista */
    .view-status-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding: 0 4px; }}
    .view-status-text {{ font-size: 12px; font-weight: 700; color: #171717; display: flex; align-items: center; gap: 6px; }}
    .view-status-count {{ background: #0c0a09; color: #facc15; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 9999px; font-family: monospace; border: 1px solid #d4af37; }}
    
    /* 6. Encabezados de Sección (Organización Estructurada) */
    .section-header-banner {{ background: #0c0a09; color: #ffffff; border-radius: 14px; padding: 12px 16px; margin: 24px 0 14px 0; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #d4af37; border-top: 1px solid rgba(212, 175, 55, 0.3); border-right: 1px solid rgba(212, 175, 55, 0.3); border-bottom: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 4px 14px rgba(0,0,0,0.08); }}
    .section-header-banner:first-of-type {{ margin-top: 0; }}
    .section-title-wrap {{ display: flex; align-items: center; gap: 10px; }}
    .section-icon {{ font-size: 20px; }}
    .section-title {{ font-size: 15px; font-weight: 800; color: #ffffff; }}
    .section-badge-cnt {{ background: rgba(250, 204, 21, 0.18); color: #facc15; font-size: 10px; font-weight: 800; padding: 2px 7px; border-radius: 9999px; font-family: monospace; border: 1px solid rgba(250, 204, 21, 0.4); }}
    .btn-sec-filter {{ background: rgba(255,255,255,0.08); color: #facc15; border: 1px solid rgba(212, 175, 55, 0.3); padding: 5px 10px; border-radius: 8px; font-size: 10px; font-weight: 700; cursor: pointer; transition: 0.2s; }}
    .btn-sec-filter:hover {{ background: #facc15; color: #0c0a09; }}
    
    /* 7. Cuadrícula de Productos */
    .products-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 24px; }}
    
    .card {{ background: #ffffff; border-radius: 16px; overflow: hidden; border: 1px solid #e5e5e5; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s; position: relative; }}
    .card:hover {{ transform: translateY(-3px); box-shadow: 0 10px 24px rgba(212, 175, 55, 0.16); border-color: #d4af37; }}
    
    /* Slider de Imagen */
    .card-img-wrap {{ position: relative; width: 100%; aspect-ratio: 1/1; background: #f5f5f4; overflow: hidden; }}
    .card-img {{ width: 100%; height: 100%; object-fit: cover; object-position: center; transition: opacity 0.25s ease; cursor: pointer; display: block; font-size: 0; color: transparent; }}
    .card-badge {{ position: absolute; top: 8px; left: 8px; background: #0c0a09; color: #facc15; font-family: monospace; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 9999px; border: 1px solid #d4af37; z-index: 2; pointer-events: none; }}
    
    .card-multi-badge {{ position: absolute; top: 8px; right: 8px; background: rgba(12, 10, 9, 0.88); color: #facc15; font-size: 9px; font-weight: 800; padding: 3px 7px; border-radius: 9999px; border: 1px solid rgba(212, 175, 55, 0.4); backdrop-filter: blur(4px); z-index: 2; }}
    
    .slider-toggle-bar {{ position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); background: rgba(12, 10, 9, 0.85); padding: 3px 8px; border-radius: 9999px; display: flex; align-items: center; gap: 4px; z-index: 2; backdrop-filter: blur(4px); border: 1px solid rgba(212, 175, 55, 0.3); }}
    .slider-dot-btn {{ background: none; border: none; color: #d4d4d4; font-size: 9px; font-weight: 700; cursor: pointer; padding: 2px 6px; border-radius: 6px; transition: 0.2s; }}
    .slider-dot-btn.active {{ color: #0c0a09; background: #facc15; font-weight: 800; }}
    
    .card-body {{ padding: 10px 12px; display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }}
    .card-title {{ font-size: 13px; font-weight: 700; color: #0c0a09; margin: 2px 0 6px 0; line-height: 1.25; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    
    .card-badges {{ display: flex; flex-wrap: wrap; gap: 3px; margin-bottom: 8px; }}
    .color-chip {{ font-size: 9px; background: #f5f5f4; color: #525252; padding: 2px 6px; border-radius: 6px; font-weight: 600; border: 1px solid #e5e5e5; }}
    .size-chip {{ font-size: 9px; background: #0c0a09; color: #facc15; padding: 2px 6px; border-radius: 6px; font-weight: 700; border: 1px solid rgba(212, 175, 55, 0.35); }}
    
    .card-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f5f5f4; padding-top: 8px; margin-top: auto; }}
    .card-price-label {{ font-size: 9px; text-transform: uppercase; color: #737373; font-weight: 700; display: block; }}
    .card-price {{ font-size: 15px; font-weight: 900; font-family: monospace; color: #0c0a09; }}
    .btn-order-card {{ background: #0c0a09; color: #facc15; border: 1px solid #d4af37; padding: 7px 14px; border-radius: 10px; font-size: 11px; font-weight: 800; cursor: pointer; transition: all 0.2s; }}
    .btn-order-card:hover {{ background: #facc15; color: #0c0a09; transform: translateY(-1px); }}
    
    /* 8. Barra Móvil Flotante Inferior */
    .mobile-cart-bar {{ position: fixed; bottom: 0; left: 0; right: 0; z-index: 45; background: #0c0a09; border-top: 2px solid #d4af37; padding: 10px 16px; box-shadow: 0 -6px 20px rgba(0,0,0,0.3); display: none; justify-content: space-between; align-items: center; }}
    .mobile-cart-total {{ display: flex; align-items: center; gap: 8px; }}
    .mobile-cart-label {{ font-size: 11px; color: #a3a3a3; font-weight: 600; }}
    .mobile-cart-sum {{ font-size: 17px; font-weight: 900; font-family: monospace; color: #facc15; }}
    .mobile-cart-btn {{ background: linear-gradient(135deg, #facc15 0%, #eab308 100%); color: #0c0a09; border: none; padding: 10px 20px; border-radius: 12px; font-size: 12px; font-weight: 900; cursor: pointer; }}
    
    /* 9. Modales */
    .modal-overlay {{ position: fixed; inset: 0; z-index: 60; background: rgba(0,0,0,0.75); backdrop-filter: blur(4px); display: flex; align-items: flex-end; justify-content: center; }}
    .modal-content {{ background: #ffffff; width: 100%; max-width: 520px; border-radius: 24px 24px 0 0; max-height: 88vh; overflow-y: auto; padding: 20px; box-shadow: 0 -10px 30px rgba(0,0,0,0.3); animation: slideUp 0.25s ease-out; border-top: 2px solid #d4af37; }}
    .modal-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f5f5f4; padding-bottom: 12px; margin-bottom: 16px; }}
    .modal-title {{ font-size: 16px; font-weight: 800; color: #0c0a09; }}
    .btn-close {{ width: 32px; height: 32px; border-radius: 50%; background: #f5f5f4; border: none; font-size: 14px; font-weight: bold; cursor: pointer; color: #0c0a09; }}
    
    .cat-btn {{ padding: 7px 14px; border-radius: 10px; border: 1px solid #e5e5e5; font-size: 11px; font-weight: 700; white-space: nowrap; cursor: pointer; background: #f5f5f4; color: #262626; transition: 0.2s; }}
    .cat-btn.active {{ background: #0c0a09; color: #facc15; border-color: #d4af37; }}
    
    .btn-primary {{ width: 100%; background: #0c0a09; color: #facc15; border: 1px solid #d4af37; padding: 12px; border-radius: 14px; font-size: 13px; font-weight: 800; cursor: pointer; transition: 0.2s; }}
    .btn-primary:hover {{ background: #facc15; color: #0c0a09; }}
    
    .btn-whatsapp {{ width: 100%; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: #ffffff; border: 1px solid #059669; padding: 14px; border-radius: 14px; font-size: 13px; font-weight: 900; cursor: pointer; text-transform: uppercase; letter-spacing: 0.5px; transition: 0.2s; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); }}
    .btn-whatsapp:hover {{ filter: brightness(1.08); }}
    
    /* 10. Notificación Toast */
    .toast {{ position: fixed; top: 20px; right: 20px; z-index: 100; background: #0c0a09; color: #facc15; border: 1px solid #d4af37; padding: 12px 20px; border-radius: 12px; font-size: 13px; font-weight: 800; box-shadow: 0 10px 25px rgba(0,0,0,0.3); transform: translateY(-60px); opacity: 0; transition: all 0.3s ease; }}
    .toast.show {{ transform: translateY(0); opacity: 1; }}
    
    @media (min-width: 768px) {{
      .hero {{ padding: 36px 32px; border-radius: 24px; }}
      .hero h2 {{ font-size: 36px; }}
      .hero p {{ font-size: 15px; }}
      .products-grid {{ grid-template-columns: repeat(4, 1fr); gap: 18px; }}
      .card-title {{ font-size: 14px; }}
      .card-price {{ font-size: 16px; }}
      .modal-overlay {{ align-items: center; }}
      .modal-content {{ border-radius: 24px; border: 2px solid #d4af37; }}
      .mobile-cart-bar {{ display: none !important; }}
    }}
    
    @keyframes slideUp {{ from {{ transform: translateY(100%); }} to {{ transform: translateY(0); }} }}
  </style>
</head>
<body>

  <div class="toast" id="toastMsg">✅ Prenda agregada al pedido</div>

  <!-- BARRA SUPERIOR DE ANUNCIO PARA CLIENTES -->
  <header class="top-announcement">
    <span>✨ Envíos a todo el país • Pago Contraentrega ✨</span>
    <span>Pedidos directos a WhatsApp 📲</span>
  </header>

  <!-- NAVEGACIÓN -->
  <nav class="navbar">
    <div class="container nav-content">
      <div class="brand" onclick="window.scrollTo({{ top: 0, behavior: 'smooth' }})">
        <img src="logo.jpg" alt="crewstore.co logo" class="brand-logo-img">
        <div>
          <div class="brand-title" id="brandTitle">crewstore.co</div>
          <div class="brand-sub">Catálogo Oficial 2026</div>
        </div>
      </div>

      <div class="nav-actions">
        <button class="btn-cart-nav" onclick="openCartDrawer()">
          <span>🛒 Mi Pedido</span>
          <span class="badge-count" id="cartCountBadge">0</span>
        </button>
      </div>
    </div>
  </nav>

  <!-- CONTENEDOR PRINCIPAL -->
  <main class="container" style="flex-grow: 1;">
    
    <!-- HERO BANNER -->
    <section class="hero">
      <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px; flex-wrap: wrap;">
        <img src="logo.jpg" alt="crewstore.co" style="width: 64px; height: 64px; border-radius: 50%; object-fit: cover; border: 2.5px solid #d4af37; box-shadow: 0 0 16px rgba(212, 175, 55, 0.4);">
        <div>
          <span class="hero-tag">Catálogo Oficial 2026 • crewstore.co</span>
          <h2 id="heroTitle">crewstore.co</h2>
        </div>
      </div>
      <p>Explora nuestras colecciones organizadas por secciones: Camisetas de fútbol retro y actual, colección especial Atlético Bucaramanga, buzos cortavientos, bermudas y moda deportiva. Pide fácil y seguro a través de WhatsApp.</p>
      <div class="hero-features">
        <span class="hero-badge"><strong id="heroTotalCount" style="color: #facc15;">431</strong> Prendas en Catálogo</span>
        <span class="hero-badge">🚚 Despacho a todo el país</span>
        <span class="hero-badge">📲 WhatsApp: <strong id="heroWhatsAppText" style="color: #facc15;">317 012 8692</strong></span>
      </div>
    </section>

    <!-- BANNER DE CESTAS / COMBOS PROMOCIONALES -->
    <section id="promoBasketsSection" class="promo-basket">
      <div style="display: flex; align-items: center; gap: 12px;">
        <div style="font-size: 26px;">🎁</div>
        <div>
          <div class="promo-tag" id="promoBasketTag">ESTRATEGIA DE AHORRO EN DOMICILIO</div>
          <div class="promo-title" id="promoBasketTitle">¡Arma tu Cesta de 2 o 3 Prendas y paga 1 solo domicilio!</div>
          <div class="promo-sub" id="promoBasketSub">Combina tus referencias y colores favoritos en un mismo pedido de WhatsApp.</div>
        </div>
      </div>
      <button onclick="openCartDrawer()" class="btn-promo">
        Ver mi Cesta 🛍️
      </button>
    </section>

    <!-- BARRA PEGAJOSA: BUSCADOR + SECCIONES -->
    <div class="sticky-controls">
      <!-- BUSCADOR POR NÚMERO O PALABRA CLAVE -->
      <div class="search-bar-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Buscar por número (ej: 1, 25, 120) o nombre (Bucaramanga, Madrid, Jordan...)" oninput="handleSearchInput(this.value)">
        <button class="btn-clear-search" id="btnClearSearch" onclick="clearSearch()" title="Borrar búsqueda">✕</button>
      </div>

      <!-- PÍLDORAS DE CATEGORÍAS ORGANIZADAS -->
      <div class="category-pills-bar" id="categoryPillsBar">
        <button class="cat-pill active" data-cat="all" onclick="filterBySection('all')">
          <span>✨ Todas</span>
          <span class="pill-count" id="pillCountAll">431</span>
        </button>
        <button class="cat-pill" data-cat="Fútbol & Retro" onclick="filterBySection('Fútbol & Retro')">
          <span>⚽ Fútbol & Retro</span>
          <span class="pill-count" id="pillCountFutbol">164</span>
        </button>
        <button class="cat-pill" data-cat="Atlético Bucaramanga" onclick="filterBySection('Atlético Bucaramanga')">
          <span>🐆 Bucaramanga</span>
          <span class="pill-count" id="pillCountBuc">71</span>
        </button>
        <button class="cat-pill" data-cat="Camisetas Básicas & Deportivas" onclick="filterBySection('Camisetas Básicas & Deportivas')">
          <span>⚡ Básicas & Gym</span>
          <span class="pill-count" id="pillCountBasicas">50</span>
        </button>
        <button class="cat-pill" data-cat="Bermudas & Shorts" onclick="filterBySection('Bermudas & Shorts')">
          <span>🩳 Bermudas & Shorts</span>
          <span class="pill-count" id="pillCountShorts">49</span>
        </button>
        <button class="cat-pill" data-cat="Polos Deportivas" onclick="filterBySection('Polos Deportivas')">
          <span>👕 Polos</span>
          <span class="pill-count" id="pillCountPolos">40</span>
        </button>
        <button class="cat-pill" data-cat="Buzos & Chaquetas" onclick="filterBySection('Buzos & Chaquetas')">
          <span>🧥 Buzos & Chaquetas</span>
          <span class="pill-count" id="pillCountBuzos">30</span>
        </button>
        <button class="cat-pill" data-cat="Conjuntos & Streetwear" onclick="filterBySection('Conjuntos & Streetwear')">
          <span>🔥 Conjuntos & Urbano</span>
          <span class="pill-count" id="pillCountConjuntos">27</span>
        </button>
      </div>
    </div>

    <!-- BARRA DE ESTADO / FILTRO ACTIVO -->
    <div class="view-status-bar">
      <div class="view-status-text" id="viewStatusLabel">
        <span>Organización:</span>
        <strong id="activeCategoryTitle">Todas las Secciones</strong>
      </div>
      <div class="view-status-count" id="activeCategoryCount">431 Prendas</div>
    </div>

    <!-- CONTENEDOR DE SECCIONES Y PRODUCTOS -->
    <div id="sectionsContainer"></div>

  </main>

  <!-- BARRA MÓVIL FLOTANTE DE PEDIDO -->
  <div class="mobile-cart-bar" id="mobileCartBar">
    <div class="mobile-cart-total">
      <span class="mobile-cart-label">Total (<span id="mobileCartCount">0</span>):</span>
      <span class="mobile-cart-sum" id="mobileCartTotal">$0</span>
    </div>
    <button class="mobile-cart-btn" onclick="openCartDrawer()">
      Ver Pedido 🛍️
    </button>
  </div>

  <!-- MODAL RÁPIDO: COLOR, TALLA Y CANTIDAD -->
  <div class="modal-overlay" id="modalAddToCart" style="display: none;" onclick="if(event.target===this) closeAddToCartModal()">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">Elegir Color y Talla</h3>
        <button class="btn-close" onclick="closeAddToCartModal()">✕</button>
      </div>

      <div style="display: flex; gap: 14px; margin-bottom: 16px; align-items: center;">
        <div style="position: relative; width: 90px; height: 90px; border-radius: 12px; overflow: hidden; border: 1px solid #d4af37;">
          <img id="modalProdImg" src="" style="width: 100%; height: 100%; object-fit: cover;">
          <div id="modalSliderBar" style="position: absolute; bottom: 4px; left: 0; right: 0; display: flex; justify-content: center; gap: 4px;"></div>
        </div>
        <div>
          <span style="background: #0c0a09; color: #facc15; font-family: monospace; font-size: 11px; font-weight: 800; padding: 2px 7px; border-radius: 9999px; border: 1px solid #d4af37;" id="modalProdCode">REF-001</span>
          <h4 style="font-size: 14px; font-weight: 800; color: #0c0a09; margin: 4px 0 2px 0;" id="modalProdName">Prenda</h4>
          <div style="font-size: 16px; font-weight: 900; color: #0c0a09; font-family: monospace;">
            $<span id="modalProdPrice">0</span> COP
          </div>
        </div>
      </div>

      <div style="margin-bottom: 14px;" id="modalColorsSection">
        <label style="font-size: 11px; font-weight: 800; color: #0c0a09; display: block; margin-bottom: 6px;">Color Disponible:</label>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;" id="modalColorsContainer"></div>
      </div>

      <div style="margin-bottom: 16px;" id="modalSizesSection">
        <label style="font-size: 11px; font-weight: 800; color: #0c0a09; display: block; margin-bottom: 6px;">Talla:</label>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;" id="modalSizesContainer"></div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; background: #f5f5f4; padding: 10px 14px; border-radius: 12px;">
        <span style="font-size: 12px; font-weight: 700; color: #0c0a09;">Cantidad:</span>
        <div style="display: flex; align-items: center; gap: 12px;">
          <button onclick="changeModalQty(-1)" style="width: 28px; height: 28px; border-radius: 8px; border: 1px solid #d4d4d4; background: #fff; font-weight: bold; cursor: pointer;">-</button>
          <span id="modalQtyDisplay" style="font-size: 14px; font-weight: 800; font-family: monospace;">1</span>
          <button onclick="changeModalQty(1)" style="width: 28px; height: 28px; border-radius: 8px; border: 1px solid #d4d4d4; background: #fff; font-weight: bold; cursor: pointer;">+</button>
        </div>
      </div>

      <button class="btn-primary" onclick="confirmAddToCart()">
        ✅ Agregar al Pedido
      </button>
    </div>
  </div>

  <!-- MODAL 2: CARRITO & SOLICITUD DE DATOS DE ENVÍO -->
  <div class="modal-overlay" id="modalCart" style="display: none;" onclick="if(event.target===this) closeCartDrawer()">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">🛍️ Tu Pedido</h3>
        <button class="btn-close" onclick="closeCartDrawer()">✕</button>
      </div>

      <!-- LISTA DE PRENDAS -->
      <div id="cartItemsList" style="max-height: 220px; overflow-y: auto; margin-bottom: 14px;"></div>

      <!-- TOTAL -->
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: #0c0a09; border-radius: 14px; margin-bottom: 14px; border: 1px solid #d4af37;">
        <span style="font-size: 12px; font-weight: 700; color: #ffffff;">Total a Pagar:</span>
        <span style="font-size: 18px; font-weight: 900; font-family: monospace; color: #facc15;" id="cartTotalDisplay">$0 COP</span>
      </div>

      <!-- SOLICITUD DE DATOS SOLO AL ENVIAR EL PEDIDO -->
      <div style="background: #ffffff; border: 1px solid #e5e5e5; border-radius: 14px; padding: 14px; margin-bottom: 14px;" id="checkoutFormSection">
        <h4 style="font-size: 12px; font-weight: 800; text-transform: uppercase; color: #0c0a09; margin-bottom: 4px;">
          📍 Datos para tu Entrega (Pago Contraentrega / Envío):
        </h4>
        <p style="font-size: 11px; color: #737373; margin-bottom: 10px;">
          🛵 Domicilios en Bucaramanga y Área Metropolitana y envíos a todo el país. Ingresa tu barrio y dirección para confirmar tu pedido por WhatsApp:
        </p>

        <div style="margin-bottom: 8px;">
          <input type="text" id="custName" placeholder="Nombre y Apellido *" style="width: 100%; padding: 10px 12px; border-radius: 10px; border: 1px solid #d4d4d4; font-size: 12px; outline: none;">
        </div>
        <div>
          <input type="text" id="custAddress" placeholder="Dirección de Entrega y Barrio / Ciudad *" style="width: 100%; padding: 10px 12px; border-radius: 10px; border: 1px solid #d4d4d4; font-size: 12px; outline: none;">
        </div>
      </div>

      <button class="btn-whatsapp" onclick="sendOrderToWhatsApp()">
        📲 Enviar mi Pedido al WhatsApp
      </button>
    </div>
  </div>

  <!-- PIE DE PÁGINA -->
  <footer style="background: #0c0a09; color: #a3a3a3; font-size: 11px; text-align: center; padding: 28px 16px; margin-top: auto; border-top: 2px solid #d4af37;">
    <div style="display: flex; justify-content: center; margin-bottom: 12px;">
      <img src="logo.jpg" alt="crewstore.co" style="width: 54px; height: 54px; border-radius: 50%; object-fit: cover; border: 2px solid #d4af37; box-shadow: 0 0 14px rgba(212, 175, 55, 0.4);">
    </div>
    <div style="font-weight: 900; color: #ffffff; font-size: 15px; margin-bottom: 4px;" id="footerStoreName">crewstore.co</div>
    <div>Catálogo Oficial Digital • Despacho sujeto a disponibilidad del producto, color y talla</div>
    <div style="margin-top: 6px; font-size: 10px; color: #737373;">© 2026 Todos los derechos reservados.</div>
  </footer>

  <script>
    window.DEFAULT_CATALOG_PRODUCTS = {products_json_str};
  </script>
  <script src="supabase_config.js"></script>
  <script src="products.js" onerror="console.log('Usando catálogo integrado')"></script>

  <script>
    const SECTIONS_CONFIG = [
      {{ id: 'Fútbol & Retro', name: 'Fútbol & Retro', icon: '⚽', tag: 'Camisetas Clubes & Selecciones' }},
      {{ id: 'Atlético Bucaramanga', name: 'Atlético Bucaramanga', icon: '🐆', tag: 'Edición Especial Campeón & Retro' }},
      {{ id: 'Camisetas Básicas & Deportivas', name: 'Camisetas Básicas & Gym', icon: '⚡', tag: 'Jordan, Nike, Adidas & Under Armour' }},
      {{ id: 'Bermudas & Shorts', name: 'Bermudas & Shorts', icon: '🩳', tag: 'Bermudas Rígidas & Pantalonetas Deportivas' }},
      {{ id: 'Polos Deportivas', name: 'Polos Deportivas', icon: '👕', tag: 'Camisetas Tipo Polo & Presentación' }},
      {{ id: 'Buzos & Chaquetas', name: 'Buzos & Chaquetas', icon: '🧥', tag: 'Cortavientos, Rompevientos & Hoodies' }},
      {{ id: 'Conjuntos & Streetwear', name: 'Conjuntos & Streetwear', icon: '🔥', tag: 'Conjuntos Deportivos & Moda Urbana' }}
    ];

    let state = {{
      searchQuery: '',
      activeCategory: 'all',
      products: (window.CATALOG_PRODUCTS && Array.isArray(window.CATALOG_PRODUCTS)) ? [...window.CATALOG_PRODUCTS] : [...window.DEFAULT_CATALOG_PRODUCTS],
      cart: [],
      selectedProductModal: null,
      modalQty: 1,
      modalSelectedColor: '',
      modalSelectedSize: '',
      settings: {{
        storeName: "crewstore.co",
        whatsappNumber: "573170128692"
      }},
      cloud: {{
        url: (window.SUPABASE_CONFIG && window.SUPABASE_CONFIG.url) || localStorage.getItem('crewstore_supabase_url') || '',
        anonKey: (window.SUPABASE_CONFIG && window.SUPABASE_CONFIG.anonKey) || localStorage.getItem('crewstore_supabase_anon_key') || ''
      }}
    }};

    const IMG_VER = '?v=20261025b';
    function resolveImgPath(p, id) {{
      if (!p || typeof p !== 'string' || !p.trim()) return `./products/item_${{id}}.jpg` + IMG_VER;
      const clean = p.trim();
      if (clean.startsWith('http://') || clean.startsWith('https://') || clean.startsWith('data:')) return clean;
      const base = (clean.startsWith('./') || clean.startsWith('/')) ? clean : ('./' + clean);
      return base.includes('?') ? base : (base + IMG_VER);
    }}

    function handleImgError(img, id) {{
      if (!img.dataset.retried) {{
        img.dataset.retried = '1';
        img.src = `./products/item_${{id}}.jpg`;
      }} else if (img.dataset.retried === '1') {{
        img.dataset.retried = '2';
        img.src = `products/item_${{id}}.jpg`;
      }}
    }}

    function showToast(msg) {{
      const t = document.getElementById('toastMsg');
      t.innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2200);
    }}

    function formatCOP(num) {{
      if (isNaN(num) || num === null) return '0';
      return Math.round(num).toLocaleString('es-CO');
    }}

    function formatPhone(p) {{
      if (!p) return '317 012 8692';
      const clean = p.replace(/^57/, '');
      return clean.replace(/(\\d{{3}})(\\d{{3}})(\\d{{4}})/, '$1 $2 $3');
    }}

    function getProductGallery(prod) {{
      if (!prod) return [];
      if (Array.isArray(prod.images) && prod.images.length > 0) return prod.images;
      const list = [prod.image || `./products/item_${{prod.id}}.jpg`];
      if (prod.editorialImage && !list.includes(prod.editorialImage)) {{
        list.push(prod.editorialImage);
      }}
      return list;
    }}

    function toggleCardImage(prodId, imgIndex, e) {{
      if (e) e.stopPropagation();
      const img = document.getElementById(`cardImg_${{prodId}}`);
      const prod = state.products.find(p => p.id === prodId);
      if (!img || !prod) return;
      const gallery = getProductGallery(prod);
      const targetSrc = gallery[imgIndex] || prod.image;
      img.src = resolveImgPath(targetSrc, prodId);
      const wrap = img.closest('.card-img-wrap');
      if (wrap) {{
        wrap.querySelectorAll('.slider-dot-btn').forEach((btn, idx) => {{
          btn.classList.toggle('active', idx === imgIndex);
        }});
      }}
    }}

    function handleSearchInput(val) {{
      state.searchQuery = val.trim();
      const btnClear = document.getElementById('btnClearSearch');
      if (btnClear) btnClear.style.display = state.searchQuery ? 'flex' : 'none';
      renderSectionsAndProducts();
    }}

    function clearSearch() {{
      const input = document.getElementById('searchInput');
      if (input) input.value = '';
      state.searchQuery = '';
      const btnClear = document.getElementById('btnClearSearch');
      if (btnClear) btnClear.style.display = 'none';
      renderSectionsAndProducts();
    }}

    function filterBySection(catId) {{
      state.activeCategory = catId;
      document.querySelectorAll('#categoryPillsBar .cat-pill').forEach(pill => {{
        pill.classList.toggle('active', pill.dataset.cat === catId);
      }});
      renderSectionsAndProducts();
    }}

    function updateCategoryCounts() {{
      const prods = state.products.filter(p => p.active !== false);
      const counts = {{
        all: prods.length,
        'Fútbol & Retro': 0,
        'Atlético Bucaramanga': 0,
        'Camisetas Básicas & Deportivas': 0,
        'Bermudas & Shorts': 0,
        'Polos Deportivas': 0,
        'Buzos & Chaquetas': 0,
        'Conjuntos & Streetwear': 0
      }};

      prods.forEach(p => {{
        if (counts[p.category] !== undefined) {{
          counts[p.category]++;
        }} else {{
          counts['Fútbol & Retro']++;
        }}
      }});

      const setVal = (id, val) => {{ const el = document.getElementById(id); if (el) el.innerText = val; }};
      setVal('pillCountAll', counts.all);
      setVal('pillCountFutbol', counts['Fútbol & Retro']);
      setVal('pillCountBuc', counts['Atlético Bucaramanga']);
      setVal('pillCountBasicas', counts['Camisetas Básicas & Deportivas']);
      setVal('pillCountShorts', counts['Bermudas & Shorts']);
      setVal('pillCountPolos', counts['Polos Deportivas']);
      setVal('pillCountBuzos', counts['Buzos & Chaquetas']);
      setVal('pillCountConjuntos', counts['Conjuntos & Streetwear']);
    }}

    function renderCard(item) {{
      const gallery = getProductGallery(item);
      const hasMulti = gallery.length > 1;
      const primaryImg = resolveImgPath(gallery[0] || item.image, item.id);
      
      const colorsList = item.colors && item.colors.length ? item.colors : ['Único'];
      const sizesList = item.sizes && item.sizes.length ? item.sizes : ['S', 'M', 'L', 'XL'];

      const colorBadges = colorsList.map(c => `<span class="color-chip">${{c}}</span>`).join('');
      const sizeBadges = sizesList.map(s => `<span class="size-chip">${{s}}</span>`).join('');
      const multiBadge = hasMulti ? `<span class="card-multi-badge">📸 ${{gallery.length}} fotos</span>` : '';

      const galleryDots = hasMulti ? `
        <div class="slider-toggle-bar">
          ${{gallery.map((_, gIdx) => `
            <button class="slider-dot-btn ${{gIdx === 0 ? 'active' : ''}}" onclick="toggleCardImage(${{item.id}}, ${{gIdx}}, event)">${{gIdx + 1}}</button>
          `).join('')}}
        </div>
      ` : '';

      return `
        <div class="card">
          <div class="card-img-wrap" onclick="openAddToCartModal(${{item.id}})">
            <img id="cardImg_${{item.id}}" src="${{primaryImg}}" class="card-img" alt="" loading="lazy" decoding="async" onerror="handleImgError(this, ${{item.id}})">
            <span class="card-badge">${{item.code}}</span>
            ${{multiBadge}}
            ${{galleryDots}}
          </div>
          <div class="card-body">
            <div>
              <h3 class="card-title" title="${{item.name}}">${{item.name}}</h3>
              <div class="card-badges">${{colorBadges}} ${{sizeBadges}}</div>
            </div>
            <div class="card-footer">
              <div>
                <span class="card-price-label">Precio</span>
                <span class="card-price">$${{formatCOP(item.salePrice)}}</span>
              </div>
              <button class="btn-order-card" onclick="openAddToCartModal(${{item.id}})">Pedir</button>
            </div>
          </div>
        </div>
      `;
    }}

    function renderSectionsAndProducts() {{
      const container = document.getElementById('sectionsContainer');
      if (!container) return;

      let list = state.products.filter(p => p.active !== false);

      // Si hay término de búsqueda activo (por número o por texto)
      if (state.searchQuery) {{
        const raw = state.searchQuery.toLowerCase();
        const numOnly = raw.replace(/\\D/g, '');

        list = list.filter(p => {{
          const codeLower = (p.code || '').toLowerCase();
          const nameLower = (p.name || '').toLowerCase();
          const catLower = (p.category || '').toLowerCase();
          const idStr = String(p.id);

          if (numOnly) {{
            const numInt = parseInt(numOnly, 10);
            if (p.id === numInt || idStr.includes(numOnly) || codeLower.includes(numOnly)) return true;
          }}
          return codeLower.includes(raw) || nameLower.includes(raw) || catLower.includes(raw);
        }});

        document.getElementById('activeCategoryTitle').innerText = `Búsqueda: "${{state.searchQuery}}"`;
        document.getElementById('activeCategoryCount').innerText = `${{list.length}} Encontradas`;

        if (list.length === 0) {{
          container.innerHTML = `
            <div style="text-align: center; padding: 48px 16px; background: #ffffff; border-radius: 20px; border: 1px solid #e5e5e5; margin-bottom: 30px;">
              <div style="font-size: 36px; margin-bottom: 8px;">🔍</div>
              <h3 style="font-size: 16px; font-weight: 800; color: #0c0a09;">No encontramos resultados para "${{state.searchQuery}}"</h3>
              <p style="font-size: 12px; color: #737373; margin: 6px 0 16px 0;">Intenta buscar por número (ej: 1, 25, 120) o por equipo como "Bucaramanga", "Madrid", "River", "Buzo".</p>
              <button onclick="clearSearch()" class="btn-primary" style="max-width: 200px; margin: 0 auto; padding: 8px 14px; font-size: 12px;">Limpiar Búsqueda</button>
            </div>
          `;
          return;
        }}

        container.innerHTML = `
          <div class="products-grid">
            ${{list.map(renderCard).join('')}}
          </div>
        `;
        return;
      }}

      // MODO 1: Una categoría específica seleccionada
      if (state.activeCategory !== 'all') {{
        const secCfg = SECTIONS_CONFIG.find(s => s.id === state.activeCategory) || {{ id: state.activeCategory, name: state.activeCategory, icon: '🏷️', tag: 'Colección' }};
        const catItems = list.filter(p => (p.category || '') === state.activeCategory);

        document.getElementById('activeCategoryTitle').innerText = secCfg.name;
        document.getElementById('activeCategoryCount').innerText = `${{catItems.length}} Prendas`;

        container.innerHTML = `
          <div class="section-header-banner" style="margin-top: 0;">
            <div class="section-title-wrap">
              <span class="section-icon">${{secCfg.icon}}</span>
              <div>
                <h3 class="section-title">${{secCfg.name}}</h3>
                <span style="font-size: 10px; color: #d4af37;">${{secCfg.tag}}</span>
              </div>
            </div>
            <button class="btn-sec-filter" onclick="filterBySection('all')">Ver Todas Las Secciones</button>
          </div>
          <div class="products-grid">
            ${{catItems.map(renderCard).join('')}}
          </div>
        `;
        return;
      }}

      // MODO 2: Vista General Organizada por Secciones Claras
      document.getElementById('activeCategoryTitle').innerText = 'Todas las Secciones';
      document.getElementById('activeCategoryCount').innerText = `${{list.length}} Prendas`;

      let htmlBlocks = '';
      SECTIONS_CONFIG.forEach(sec => {{
        const secItems = list.filter(p => (p.category || '') === sec.id);
        if (secItems.length === 0) return;

        htmlBlocks += `
          <section id="section-${{sec.id.replace(/\\s+/g, '-')}}" style="margin-bottom: 28px;">
            <div class="section-header-banner">
              <div class="section-title-wrap">
                <span class="section-icon">${{sec.icon}}</span>
                <div>
                  <h3 class="section-title">${{sec.name}}</h3>
                  <span style="font-size: 10px; color: #d4af37;">${{sec.tag}}</span>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <span class="section-badge-cnt">${{secItems.length}} prendas</span>
                <button class="btn-sec-filter" onclick="filterBySection('${{sec.id}}')">Ver sólo esta →</button>
              </div>
            </div>
            <div class="products-grid">
              ${{secItems.map(renderCard).join('')}}
            </div>
          </section>
        `;
      }});

      container.innerHTML = htmlBlocks;
    }}

    function ensureSequentialNumbering(list) {{
      if (!Array.isArray(list)) return [];
      return list.map((p, idx) => {{
        const seq = idx + 1;
        const newCode = `REF-${{String(seq).padStart(3, '0')}}`;
        let newName = p.name || `Prenda CrewStore ${{String(seq).padStart(3, '0')}}`;
        if (/\\s+\\d{{1,3}}$/.test(newName.trim())) {{
          newName = newName.trim().replace(/\\s+\\d{{1,3}}$/, ` ${{String(seq).padStart(3, '0')}}`);
        }}
        return {{ ...p, id: seq, code: newCode, name: newName }};
      }});
    }}

    function trackProductAnalytics(prodId, eventType) {{
      try {{
        const stats = JSON.parse(localStorage.getItem('crewstore_v2_analytics_stats') || '{{}}');
        if (!stats[prodId]) stats[prodId] = {{ views: 0, carts: 0, orders: 0 }};
        stats[prodId][eventType] = (stats[prodId][eventType] || 0) + 1;
        localStorage.setItem('crewstore_v2_analytics_stats', JSON.stringify(stats));
      }} catch (e) {{}}
    }}

    function openAddToCartModal(prodId) {{
      const prod = state.products.find(p => p.id === prodId);
      if (!prod) return;
      trackProductAnalytics(prod.code || prodId, 'views');
      state.selectedProductModal = prod;
      state.modalQty = 1;

      const colors = prod.colors && prod.colors.length ? prod.colors : ['Blanco', 'Negro'];
      const sizes = prod.sizes && prod.sizes.length ? prod.sizes : ['Única'];

      state.modalSelectedColor = colors[0];
      state.modalSelectedSize = sizes[0];

      document.getElementById('modalProdCode').innerText = prod.code;
      document.getElementById('modalProdName').innerText = prod.name;
      document.getElementById('modalProdPrice').innerText = formatCOP(prod.salePrice);
      document.getElementById('modalQtyDisplay').innerText = state.modalQty;

      const gallery = getProductGallery(prod);
      const img = document.getElementById('modalProdImg');
      img.src = resolveImgPath(gallery[0] || prod.image, prod.id);
      img.onerror = () => handleImgError(img, prod.id);

      const sliderBar = document.getElementById('modalSliderBar');
      if (gallery.length > 1) {{
        sliderBar.innerHTML = gallery.map((_, gIdx) => `
          <button class="slider-dot-btn ${{gIdx === 0 ? 'active' : ''}}" onclick="setModalImg(${{gIdx}}, this)">${{gIdx + 1}}</button>
        `).join('');
      }} else {{
        sliderBar.innerHTML = '';
      }}

      const colorsContainer = document.getElementById('modalColorsContainer');
      colorsContainer.innerHTML = colors.map((c, idx) => `
        <button class="cat-btn ${{idx === 0 ? 'active' : ''}}" onclick="selectModalColor('${{c}}', this)">${{c}}</button>
      `).join('');

      const sizesContainer = document.getElementById('modalSizesContainer');
      sizesContainer.innerHTML = sizes.map((s, idx) => `
        <button class="cat-btn ${{idx === 0 ? 'active' : ''}}" onclick="selectModalSize('${{s}}', this)">${{s}}</button>
      `).join('');

      document.getElementById('modalAddToCart').style.display = 'flex';
    }}

    function setModalImg(imgIdx, btnEl) {{
      const p = state.selectedProductModal;
      if (!p) return;
      const gallery = getProductGallery(p);
      const img = document.getElementById('modalProdImg');
      img.src = resolveImgPath(gallery[imgIdx] || p.image, p.id);
      document.querySelectorAll('#modalSliderBar .slider-dot-btn').forEach((b, i) => {{
        b.classList.toggle('active', i === imgIdx);
      }});
    }}

    function selectModalColor(col, btn) {{
      state.modalSelectedColor = col;
      document.querySelectorAll('#modalColorsContainer .cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }}

    function selectModalSize(sz, btn) {{
      state.modalSelectedSize = sz;
      document.querySelectorAll('#modalSizesContainer .cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }}

    function changeModalQty(delta) {{
      state.modalQty = Math.max(1, state.modalQty + delta);
      document.getElementById('modalQtyDisplay').innerText = state.modalQty;
    }}

    function closeAddToCartModal() {{
      document.getElementById('modalAddToCart').style.display = 'none';
    }}

    function confirmAddToCart() {{
      if (!state.selectedProductModal) return;
      trackProductAnalytics(state.selectedProductModal.code || state.selectedProductModal.id, 'carts');
      state.cart.push({{
        ...state.selectedProductModal,
        selectedColor: state.modalSelectedColor,
        selectedSize: state.modalSelectedSize,
        quantity: state.modalQty
      }});
      closeAddToCartModal();
      updateCartBadge();
      showToast(`✅ ${{state.selectedProductModal.name}} agregada al carrito`);
    }}

    function updateCartBadge() {{
      const count = state.cart.reduce((sum, i) => sum + i.quantity, 0);
      const total = state.cart.reduce((sum, i) => sum + (i.salePrice * i.quantity), 0);
      
      const b = document.getElementById('cartCountBadge');
      if (b) b.innerText = count;

      const mobBar = document.getElementById('mobileCartBar');
      if (mobBar) {{
        if (count > 0) {{
          mobBar.style.display = 'flex';
          document.getElementById('mobileCartCount').innerText = count;
          document.getElementById('mobileCartTotal').innerText = '$' + formatCOP(total);
        }} else {{
          mobBar.style.display = 'none';
        }}
      }}
    }}

    function openCartDrawer() {{
      const list = document.getElementById('cartItemsList');
      if (!list) return;

      if (state.cart.length === 0) {{
        list.innerHTML = `<div style="text-align: center; padding: 24px; color: #737373; font-size: 13px;">Tu pedido está vacío. Elige una prenda del catálogo para comenzar.</div>`;
        document.getElementById('checkoutFormSection').style.display = 'none';
      }} else {{
        document.getElementById('checkoutFormSection').style.display = 'block';
        list.innerHTML = state.cart.map((item, idx) => `
          <div style="display: flex; gap: 10px; align-items: center; padding: 10px 0; border-bottom: 1px solid #f5f5f4;">
            <img src="${{item.image}}" style="width: 46px; height: 46px; object-fit: cover; border-radius: 8px; border: 1px solid #e5e5e5;">
            <div style="flex-grow: 1;">
              <div style="font-size: 12px; font-weight: 800; color: #0c0a09;">${{item.name}} (${{item.code}})</div>
              <div style="font-size: 11px; color: #737373;">Color: <strong>${{item.selectedColor}}</strong> • Talla: <strong>${{item.selectedSize}}</strong>${{item.quantity > 1 ? ` • Cant: <strong>${{item.quantity}}</strong>` : ''}}</div>
              <div style="font-size: 13px; font-weight: 900; font-family: monospace; color: #0c0a09; margin-top: 2px;">
                $${{formatCOP(item.salePrice * item.quantity)}} COP
              </div>
            </div>
            <button onclick="removeCartItem(${{idx}})" style="background: none; border: none; color: #ef4444; font-size: 15px; font-weight: bold; cursor: pointer; padding: 4px;">✕</button>
          </div>
        `).join('');
      }}

      const total = state.cart.reduce((sum, i) => sum + (i.salePrice * i.quantity), 0);
      document.getElementById('cartTotalDisplay').innerText = '$' + formatCOP(total) + ' COP';
      document.getElementById('modalCart').style.display = 'flex';
    }}

    function removeCartItem(idx) {{
      state.cart.splice(idx, 1);
      updateCartBadge();
      openCartDrawer();
    }}

    function closeCartDrawer() {{
      document.getElementById('modalCart').style.display = 'none';
    }}

    function sendOrderToWhatsApp() {{
      if (state.cart.length === 0) {{
        alert('Tu pedido está vacío. Agrega prendas antes de continuar.');
        return;
      }}

      const name = document.getElementById('custName').value.trim();
      const address = document.getElementById('custAddress').value.trim();

      if (!name) {{ alert('Por favor ingresa tu Nombre y Apellido.'); return; }}
      if (!address) {{ alert('Por favor ingresa tu Dirección de Entrega (con Barrio o Ciudad).'); return; }}

      const total = state.cart.reduce((sum, i) => sum + (i.salePrice * i.quantity), 0);
      const code = 'PED-' + Math.floor(1000 + Math.random() * 9000);

      const eSparkles = '\\u2728';
      const eFire = '\\uD83D\\uDD25';
      const eShirt = '\\uD83D\\uDC55';
      const ePin = '\\uD83D\\uDCCD';
      const eBag = '\\uD83D\\uDECD';
      const eMoney = '\\uD83D\\uDCB0';

      let text = `${{eSparkles}} *¡Hola crewstore.co!* ${{eFire}}\\n`;
      text += `Me gustaría realizar el siguiente pedido (${{code}}):\\n\\n`;
      text += `${{eBag}} *PRENDAS SELECCIONADAS:*\\n`;

      state.cart.forEach((i, idx) => {{
        const itemTotal = i.salePrice * i.quantity;
        text += `\\n${{idx + 1}}. ${{eShirt}} *${{i.name}}* (${{i.code}})\\n`;
        text += `   • Color: ${{i.selectedColor}} | Talla: ${{i.selectedSize}}${{i.quantity > 1 ? ` | Cant: ${{i.quantity}}` : ''}}\\n`;
        text += `   • Valor: *$${{formatCOP(itemTotal)}} COP*\\n`;
      }});

      text += `\\n${{eMoney}} *TOTAL PRENDAS:* *$${{formatCOP(total)}} COP*\\n\\n`;
      text += `${{ePin}} *DATOS DE ENTREGA:*\\n`;
      text += `   • *Nombre:* ${{name}}\\n`;
      text += `   • *Dirección / Barrio:* ${{address}}\\n\\n`;
      text += `Quedo atento(a) para coordinar disponibilidad y despacho. ¡Muchas gracias! ${{eSparkles}}`;

      if (state.cloud.url && state.cloud.anonKey) {{
        fetch(state.cloud.url + '/rest/v1/orders', {{
          method: 'POST',
          headers: {{
            'apikey': state.cloud.anonKey,
            'Authorization': 'Bearer ' + state.cloud.anonKey,
            'Content-Type': 'application/json'
          }},
          body: JSON.stringify({{
            order_code: 'CREW-' + code,
            customer_name: name,
            customer_address: address,
            customer_phone: '',
            items: state.cart,
            total: total
          }})
        }}).catch(() => {{}});
      }}

      const cleanPhone = state.settings.whatsappNumber.replace(/\\D/g, '');
      const waUrl = `https://api.whatsapp.com/send?phone=${{cleanPhone}}&text=${{encodeURIComponent(text)}}`;
      window.open(waUrl, '_blank');
    }}

    async function loadProductsFromSupabase() {{
      if (!state.cloud.url || !state.cloud.anonKey) return false;
      try {{
        fetch(state.cloud.url + '/rest/v1/store_settings?id=eq.crewstore&select=*', {{
          headers: {{ 'apikey': state.cloud.anonKey, 'Authorization': 'Bearer ' + state.cloud.anonKey }}
        }}).then(r => r.ok ? r.json() : []).then(sRows => {{
          if (Array.isArray(sRows) && sRows.length > 0) {{
            if (sRows[0].store_name) state.settings.storeName = sRows[0].store_name;
            if (sRows[0].whatsapp_number) state.settings.whatsappNumber = sRows[0].whatsapp_number;
            document.getElementById('heroWhatsAppText').innerText = formatPhone(state.settings.whatsappNumber);
            document.getElementById('brandTitle').innerText = state.settings.storeName;
            document.getElementById('footerStoreName').innerText = state.settings.storeName;
          }}
        }}).catch(() => {{}});

        const res = await fetch(state.cloud.url + '/rest/v1/products?id=gt.10000&select=*&order=id.asc', {{
          headers: {{ 'apikey': state.cloud.anonKey, 'Authorization': 'Bearer ' + state.cloud.anonKey }}
        }});
        if (res.ok) {{
          const rows = await res.json();
          if (rows && rows.length > 0) {{
            state.products = ensureSequentialNumbering(rows.map(r => {{
              const localId = Number(r.id) > 10000 ? Number(r.id) - 10000 : Number(r.id);
              const primaryImg = (r.image && r.image.trim()) ? r.image : `./products/item_${{localId}}.jpg`;
              let imgs = [primaryImg];
              if (r.raw_image) {{
                try {{
                  const parsedImgs = JSON.parse(r.raw_image);
                  if (Array.isArray(parsedImgs) && parsedImgs.length > 0) imgs = parsedImgs;
                }} catch (e) {{}}
              }}
              return {{
                id: localId,
                code: String(r.code || '').replace(/^CREW-/, ''),
                name: r.name,
                category: r.category,
                salePrice: Number(r.sale_price),
                colors: Array.isArray(r.colors) ? r.colors : ['Blanco', 'Negro'],
                sizes: Array.isArray(r.sizes) ? r.sizes : ['Única'],
                image: primaryImg,
                images: imgs,
                editorialImage: (r.editorial_image && r.editorial_image.trim()) ? r.editorial_image : (r.editorialImage || null),
                active: r.active
              }};
            }}));
            localStorage.setItem('crewstore_v9_products_cache', JSON.stringify(state.products));
            return true;
          }}
        }}
      }} catch (e) {{
        console.warn('Cargando respaldo local:', e);
      }}
      return false;
    }}

    async function initApp() {{
      localStorage.removeItem('crewstore_products_cache');
      localStorage.removeItem('crewstore_settings_cache');
      if (window.location.protocol === 'file:') {{
        localStorage.removeItem('crewstore_v9_products_cache');
        localStorage.removeItem('crewstore_v2_settings_cache');
      }} else {{
        const cachedSettings = localStorage.getItem('crewstore_v2_settings_cache');
        if (cachedSettings) {{
          try {{ state.settings = {{ ...state.settings, ...JSON.parse(cachedSettings) }}; }} catch(e){{}}
        }}
        const cachedProds = localStorage.getItem('crewstore_v9_products_cache');
        if (cachedProds) {{
          try {{
            const parsed = JSON.parse(cachedProds);
            if (parsed && parsed.length > 0) state.products = ensureSequentialNumbering(parsed);
          }} catch(e){{}}
        }}
      }}
      state.products = ensureSequentialNumbering(state.products);

      updateCategoryCounts();
      renderSectionsAndProducts();
      updateCartBadge();

      document.getElementById('heroTotalCount').innerText = state.products.length;
      document.getElementById('heroWhatsAppText').innerText = formatPhone(state.settings.whatsappNumber);
      document.getElementById('brandTitle').innerText = state.settings.storeName;
      document.getElementById('footerStoreName').innerText = state.settings.storeName;

      try {{
        const [resProds, resSettings] = await Promise.all([
          fetch('http://localhost:8081/api/products?t=' + Date.now()),
          fetch('http://localhost:8081/api/settings?t=' + Date.now())
        ]);
        if (resSettings.ok) {{
          const srvSettings = await resSettings.json();
          if (srvSettings && srvSettings.storeName) {{
            state.settings = {{ ...state.settings, ...srvSettings }};
            document.getElementById('heroWhatsAppText').innerText = formatPhone(state.settings.whatsappNumber);
            document.getElementById('brandTitle').innerText = state.settings.storeName;
            document.getElementById('footerStoreName').innerText = state.settings.storeName;
          }}
        }}
        if (resProds.ok) {{
          const srvProds = await resProds.json();
          if (Array.isArray(srvProds) && srvProds.length > 0) {{
            state.products = ensureSequentialNumbering(srvProds);
            updateCategoryCounts();
            renderSectionsAndProducts();
            document.getElementById('heroTotalCount').innerText = state.products.length;
          }}
        }}
      }} catch (e) {{}}

      const loaded = await loadProductsFromSupabase();
      if (loaded) {{
        updateCategoryCounts();
        renderSectionsAndProducts();
        document.getElementById('heroTotalCount').innerText = state.products.length;
      }}
    }}

    // Acceso oculto al panel: 5 toques rápidos en el footer
    (function () {{
      let taps = 0, timer = null;
      const el = document.getElementById('footerStoreName');
      if (!el) return;
      el.style.userSelect = 'none';
      el.style.webkitUserSelect = 'none';
      el.addEventListener('click', () => {{
        taps++;
        clearTimeout(timer);
        timer = setTimeout(() => {{ taps = 0; }}, 2500);
        if (taps >= 5) {{ taps = 0; window.location.href = 'bv-panel-7k2q.html'; }}
      }});
    }})();

    initApp();

    async function refreshRealtimeCatalog() {{
      if (document.hidden || state.selectedProductModal) return;
      const loaded = await loadProductsFromSupabase();
      if (loaded) {{
        updateCategoryCounts();
        renderSectionsAndProducts();
        document.getElementById('heroTotalCount').innerText = state.products.length;
      }}
    }}
    document.addEventListener('visibilitychange', () => {{
      if (!document.hidden) refreshRealtimeCatalog();
    }});
    setInterval(refreshRealtimeCatalog, 20000);
  </script>
</body>
</html>
'''

with open('/Users/ginavillamizar/Documents/crewstore-catalogo/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated new index.html successfully with Negro, Blanco y Dorado and Sections Organization!")
