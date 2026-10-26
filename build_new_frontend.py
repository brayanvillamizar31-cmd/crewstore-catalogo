import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    orig = f.read()

start_marker = "window.DEFAULT_CATALOG_PRODUCTS = ["
end_marker = "];\n  </script>\n  <script src=\"supabase_config.js\"></script>"

idx1 = orig.find(start_marker)
idx2 = orig.find(end_marker)

if idx1 == -1 or idx2 == -1:
    print("Error: Split markers not found in index.html")
    sys.exit(1)

catalog_script_part = orig[idx1:idx2 + 2]

head_and_html_part = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>crewstore.co | Luxury Streetwear & Blokecore • Catálogo Oficial 2026</title>
  <meta name="description" content="crewstore.co: Drop Oficial 2026. Streetwear de lujo, camisetas de fútbol retro originals, Atlético Bucaramanga, buzos y piezas exclusivas. Envíos contraentrega a toda Colombia por WhatsApp.">
  <meta name="keywords" content="crewstore.co, streetwear, blokecore, camisetas retro, camisetas futbol, oversize, bucaramanga, buzos, moda urbana, colombia">
  <meta property="og:title" content="crewstore.co | Luxury Streetwear & Blokecore • Catálogo Oficial 2026">
  <meta property="og:description" content="Explora el catálogo oficial de crewstore.co 2026. Moda urbana de lujo, piezas exclusivas y fútbol retro. Pide directo a WhatsApp.">
  <meta property="og:type" content="website">
  <link rel="icon" type="image/jpeg" href="logo.jpg">
  <link rel="apple-touch-icon" href="logo.jpg">
  <meta property="og:image" content="logo.jpg">

  <!-- Google Fonts: Plus Jakarta Sans & Space Grotesk -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "ClothingStore",
    "name": "crewstore.co",
    "description": "Catálogo Oficial Digital de crewstore.co 2026. Luxury Streetwear, fútbol retro y moda urbana.",
    "currenciesAccepted": "COP",
    "paymentAccepted": "Efectivo, Transferencia, Pago Contraentrega"
  }
  </script>
  
  <style>
    :root {
      --bg-base: #09090b;
      --bg-surface: #121216;
      --bg-elevated: #18181f;
      --bg-card: #131318;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-gold: rgba(212, 175, 55, 0.35);
      --border-gold-bright: #d4af37;
      --gold-primary: #d4af37;
      --gold-light: #facc15;
      --gold-accent: #f59e0b;
      --gold-glow: rgba(212, 175, 55, 0.28);
      --text-primary: #ffffff;
      --text-secondary: #a1a1aa;
      --text-muted: #71717a;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html {
      -webkit-tap-highlight-color: transparent;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      scroll-behavior: smooth;
      background-color: var(--bg-base);
    }
    body {
      background-color: var(--bg-base);
      color: var(--text-primary);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      line-height: 1.45;
      position: relative;
    }

    /* Ambient Gold Glow & Street Grid Background */
    body::before {
      content: "";
      position: fixed;
      top: 0; left: 0; right: 0; height: 500px;
      background: radial-gradient(ellipse 70% 350px at 50% -100px, rgba(212, 175, 55, 0.15), transparent 75%);
      pointer-events: none;
      z-index: 0;
    }

    .container {
      max-width: 1260px;
      margin: 0 auto;
      padding: 0 16px;
      width: 100%;
      position: relative;
      z-index: 1;
    }

    /* 1. Micro-Ticker Superior */
    .top-announcement {
      background: #040405;
      color: var(--gold-light);
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 8px 16px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 40;
      border-bottom: 1px solid rgba(212, 175, 55, 0.25);
    }
    .top-announcement .ticker-pulse {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #ffffff;
    }
    .top-announcement .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #22c55e;
      box-shadow: 0 0 8px #22c55e;
      animation: pulseGlow 1.8s infinite;
    }
    @keyframes pulseGlow {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* 2. Navbar de Lujo Streetwear */
    .navbar {
      position: sticky;
      top: 0;
      z-index: 35;
      background: rgba(9, 9, 11, 0.88);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-gold);
      height: 72px;
      display: flex;
      align-items: center;
      box-shadow: 0 4px 30px rgba(0,0,0,0.6);
      transition: all 0.3s;
    }
    .nav-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: inherit;
      cursor: pointer;
    }
    .brand-logo-wrap {
      position: relative;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      padding: 2px;
      background: linear-gradient(135deg, #d4af37, #453712, #d4af37);
      box-shadow: 0 0 16px rgba(212, 175, 55, 0.35);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .brand:hover .brand-logo-wrap {
      transform: scale(1.06) rotate(3deg);
    }
    .brand-logo-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
      display: block;
    }
    .brand-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 19px;
      font-weight: 800;
      letter-spacing: 1px;
      line-height: 1.1;
      color: #ffffff;
      text-transform: uppercase;
    }
    .brand-sub {
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--gold-primary);
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
    }
    
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .btn-cart-nav {
      background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
      color: #09090b;
      border: 1px solid #fef08a;
      padding: 9px 18px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);
    }
    .btn-cart-nav:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 26px rgba(212, 175, 55, 0.55);
      filter: brightness(1.08);
    }
    .badge-count {
      background: #09090b;
      color: #facc15;
      font-weight: 800;
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 9999px;
      font-family: 'JetBrains Mono', monospace;
      border: 1px solid #d4af37;
    }

    /* 3. Hero Lookbook & 3D Album Showcase (Inspirado en imágenes del usuario) */
    .hero-editorial {
      position: relative;
      background: linear-gradient(135deg, rgba(18, 18, 22, 0.95) 0%, rgba(9, 9, 11, 0.98) 100%);
      border: 1px solid var(--border-gold);
      border-radius: 24px;
      padding: 28px 20px;
      margin: 18px 0 20px 0;
      box-shadow: 0 16px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.06);
      overflow: hidden;
    }
    /* Ghost Background Typography */
    .hero-editorial::before {
      content: "CREW";
      position: absolute;
      right: -20px;
      bottom: -30px;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 160px;
      font-weight: 900;
      letter-spacing: -6px;
      color: rgba(255, 255, 255, 0.025);
      pointer-events: none;
      line-height: 1;
      z-index: 0;
    }
    .hero-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 24px;
      position: relative;
      z-index: 1;
      align-items: center;
    }
    @media (min-width: 900px) {
      .hero-grid {
        grid-template-columns: 1.15fr 0.85fr;
        gap: 36px;
        padding: 10px 14px;
      }
    }
    .hero-content {
      display: flex;
      flex-direction: column;
    }
    .hero-tag-wrap {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(212, 175, 55, 0.1);
      border: 1px solid rgba(212, 175, 55, 0.4);
      padding: 5px 14px;
      border-radius: 9999px;
      width: fit-content;
      margin-bottom: 14px;
    }
    .hero-tag-text {
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      color: var(--gold-light);
      letter-spacing: 1.5px;
      text-transform: uppercase;
    }
    .hero-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 32px;
      font-weight: 900;
      line-height: 1.08;
      letter-spacing: -0.5px;
      color: #ffffff;
      margin-bottom: 10px;
      text-transform: uppercase;
    }
    .hero-title .gold-accent {
      background: linear-gradient(135deg, #ffffff 30%, #facc15 80%, #d4af37 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-desc {
      font-size: 13.5px;
      color: var(--text-secondary);
      line-height: 1.6;
      margin-bottom: 20px;
      max-width: 580px;
    }
    .hero-badges-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 20px;
    }
    .hero-spec-badge {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 6px 12px;
      border-radius: 10px;
      font-size: 11px;
      font-weight: 600;
      color: #ffffff;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: 'Space Grotesk', sans-serif;
    }
    .hero-spec-badge strong {
      color: var(--gold-light);
    }
    .hero-cta-group {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
    }
    .btn-hero-primary {
      background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
      color: #09090b;
      border: 1px solid #fef08a;
      padding: 12px 24px;
      border-radius: 14px;
      font-size: 13px;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.25s;
      box-shadow: 0 4px 18px rgba(212, 175, 55, 0.35);
    }
    .btn-hero-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(212, 175, 55, 0.5);
    }
    .btn-hero-secondary {
      background: rgba(255, 255, 255, 0.06);
      color: #ffffff;
      border: 1px solid var(--border-gold);
      padding: 12px 20px;
      border-radius: 14px;
      font-size: 13px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
      cursor: pointer;
      transition: all 0.25s;
    }
    .btn-hero-secondary:hover {
      background: rgba(212, 175, 55, 0.15);
      border-color: var(--gold-light);
      color: var(--gold-light);
    }

    /* 3D Floating Streetwear Album Deck (Spotify / The Weeknd aesthetic from image) */
    .hero-deck-wrap {
      display: flex;
      justify-content: center;
      align-items: center;
      perspective: 1200px;
      position: relative;
    }
    .hero-deck-card {
      position: relative;
      width: 100%;
      max-width: 380px;
      background: #111115;
      border: 1.5px solid var(--border-gold-bright);
      border-radius: 20px;
      padding: 12px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(212, 175, 55, 0.2);
      transform: rotateY(-6deg) rotateX(4deg);
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s;
    }
    .hero-deck-card:hover {
      transform: rotateY(0deg) rotateX(0deg) translateY(-4px);
      box-shadow: 0 25px 60px rgba(0,0,0,0.9), 0 0 40px rgba(212, 175, 55, 0.35);
    }
    .deck-img-wrap {
      position: relative;
      width: 100%;
      aspect-ratio: 4/5;
      border-radius: 14px;
      overflow: hidden;
      background: #000000;
    }
    .deck-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      filter: contrast(1.05);
      transition: transform 0.5s ease;
    }
    .hero-deck-card:hover .deck-img {
      transform: scale(1.03);
    }
    .deck-tag-floating {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(9, 9, 11, 0.85);
      border: 1px solid var(--gold-primary);
      color: var(--gold-light);
      font-family: 'Space Grotesk', monospace;
      font-size: 10px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 9999px;
      backdrop-filter: blur(8px);
    }
    .deck-tag-coords {
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(9, 9, 11, 0.85);
      border: 1px solid rgba(255,255,255,0.15);
      color: #d4d4d8;
      font-family: 'JetBrains Mono', monospace;
      font-size: 9px;
      padding: 4px 8px;
      border-radius: 6px;
      backdrop-filter: blur(8px);
    }
    /* Player Deck Bar at Bottom */
    .deck-player-bar {
      margin-top: 12px;
      background: rgba(24, 24, 28, 0.95);
      border: 1px solid rgba(212, 175, 55, 0.25);
      border-radius: 12px;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .player-track-info {
      display: flex;
      align-items: center;
      gap: 10px;
      overflow: hidden;
    }
    .player-play-icon {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--gold-light);
      color: #09090b;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 900;
      flex-shrink: 0;
      box-shadow: 0 0 12px rgba(250, 204, 21, 0.5);
    }
    .player-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 12px;
      font-weight: 800;
      color: #ffffff;
      white-space: nowrap;
    }
    .player-sub {
      font-size: 10px;
      color: var(--gold-primary);
      white-space: nowrap;
    }
    .player-equalizer {
      display: flex;
      align-items: flex-end;
      gap: 3px;
      height: 18px;
      padding-right: 4px;
    }
    .eq-bar {
      width: 3px;
      background: var(--gold-light);
      border-radius: 9999px;
      animation: eqBounce 1.2s ease-in-out infinite alternate;
    }
    .eq-bar:nth-child(1) { height: 6px; animation-delay: 0.1s; }
    .eq-bar:nth-child(2) { height: 14px; animation-delay: 0.3s; }
    .eq-bar:nth-child(3) { height: 10px; animation-delay: 0.2s; }
    .eq-bar:nth-child(4) { height: 16px; animation-delay: 0.4s; }
    .eq-bar:nth-child(5) { height: 8px; animation-delay: 0.15s; }
    @keyframes eqBounce {
      0% { height: 4px; }
      100% { height: 18px; }
    }

    /* 4. Banner de Combos Streetwear */
    .promo-basket {
      background: linear-gradient(135deg, rgba(24, 24, 30, 0.95) 0%, rgba(14, 14, 18, 0.95) 100%);
      border: 1px solid var(--border-gold);
      border-radius: 18px;
      padding: 16px 20px;
      margin: 0 0 20px 0;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .promo-tag {
      font-family: 'Space Grotesk', monospace;
      font-size: 10px;
      font-weight: 800;
      color: var(--gold-light);
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 2px;
    }
    .promo-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 15px;
      font-weight: 800;
      color: #ffffff;
    }
    .promo-sub {
      font-size: 12px;
      color: var(--text-secondary);
    }
    .btn-promo {
      background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
      color: #09090b;
      border: 1px solid #fef08a;
      padding: 10px 20px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: 0.5px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .btn-promo:hover {
      filter: brightness(1.1);
      transform: translateY(-1px);
    }

    /* 5. Sticky Controls: Buscador + Píldoras de Secciones */
    .sticky-controls {
      position: sticky;
      top: 72px;
      z-index: 30;
      background: rgba(9, 9, 11, 0.94);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      padding: 14px 0 12px 0;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 22px;
    }
    
    .search-bar-wrap {
      background: #141419;
      border: 1.5px solid var(--border-gold);
      border-radius: 16px;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.4);
      margin-bottom: 12px;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .search-bar-wrap:focus-within {
      border-color: var(--gold-light);
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }
    .search-icon {
      font-size: 16px;
      color: var(--gold-light);
    }
    .search-input {
      width: 100%;
      border: none;
      background: transparent;
      font-size: 14px;
      font-weight: 600;
      outline: none;
      color: #ffffff;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .search-input::placeholder {
      color: var(--text-muted);
      font-weight: 400;
    }
    .btn-clear-search {
      background: rgba(255, 255, 255, 0.1);
      border: none;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      color: #ffffff;
      font-size: 11px;
      font-weight: bold;
      cursor: pointer;
      display: none;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }
    .btn-clear-search:hover {
      background: var(--gold-light);
      color: #09090b;
    }

    /* Píldoras de Categorías con scroll suave */
    .category-pills-bar {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 4px;
      scrollbar-width: none;
      -ms-overflow-style: none;
      -webkit-overflow-scrolling: touch;
    }
    .category-pills-bar::-webkit-scrollbar { display: none; }

    .cat-pill {
      background: #14141a;
      color: #d4d4d8;
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 8px 16px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    .cat-pill:hover {
      border-color: var(--gold-primary);
      color: #ffffff;
      transform: translateY(-1px);
    }
    .cat-pill.active {
      background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
      color: #09090b;
      border-color: #fef08a;
      font-weight: 800;
      box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
    }
    .cat-pill .pill-count {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      padding: 2px 7px;
      border-radius: 9999px;
    }
    .cat-pill.active .pill-count {
      background: #09090b;
      color: #facc15;
    }
    .cat-pill:not(.active) .pill-count {
      background: rgba(255, 255, 255, 0.08);
      color: var(--gold-primary);
      border: 1px solid rgba(212, 175, 55, 0.3);
    }

    /* Estado de Organización */
    .view-status-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      padding: 0 4px;
    }
    .view-status-text {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-secondary);
      display: flex;
      align-items: center;
      gap: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .view-status-text strong {
      color: #ffffff;
    }
    .view-status-count {
      background: #14141a;
      color: var(--gold-light);
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 9999px;
      border: 1px solid var(--border-gold);
    }

    /* 6. Encabezados de Sección Lookbook Editorial */
    .section-header-banner {
      background: linear-gradient(90deg, #131318 0%, #0d0d10 100%);
      border: 1px solid var(--border-gold);
      border-left: 4px solid var(--gold-primary);
      border-radius: 16px;
      padding: 14px 18px;
      margin: 32px 0 16px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .section-header-banner:first-of-type { margin-top: 0; }
    .section-title-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .section-num-tag {
      background: rgba(212, 175, 55, 0.12);
      border: 1px solid var(--border-gold);
      color: var(--gold-light);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 800;
      padding: 4px 8px;
      border-radius: 8px;
    }
    .section-icon {
      font-size: 20px;
    }
    .section-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 16px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
    .section-subtag {
      font-size: 11px;
      color: var(--gold-primary);
      font-weight: 600;
      letter-spacing: 0.5px;
    }
    .section-badge-cnt {
      background: rgba(250, 204, 21, 0.12);
      color: var(--gold-light);
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 9999px;
      border: 1px solid rgba(250, 204, 21, 0.35);
      white-space: nowrap;
    }
    .btn-sec-filter {
      background: rgba(255, 255, 255, 0.05);
      color: #ffffff;
      border: 1px solid var(--border-gold);
      padding: 6px 12px;
      border-radius: 10px;
      font-size: 11px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }
    .btn-sec-filter:hover {
      background: var(--gold-light);
      color: #09090b;
      border-color: var(--gold-light);
    }

    /* 7. Cuadrícula de Productos Streetwear de Lujo */
    .products-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-bottom: 28px;
    }
    @media (min-width: 640px) {
      .products-grid { grid-template-columns: repeat(2, 1fr); gap: 14px; }
    }
    @media (min-width: 768px) {
      .products-grid { grid-template-columns: repeat(3, 1fr); gap: 16px; }
    }
    @media (min-width: 1024px) {
      .products-grid { grid-template-columns: repeat(4, 1fr); gap: 18px; }
    }

    .card {
      background: var(--bg-card);
      border-radius: 18px;
      overflow: hidden;
      border: 1px solid var(--border-subtle);
      box-shadow: 0 4px 18px rgba(0,0,0,0.4);
      display: flex;
      flex-direction: column;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }
    .card:hover {
      transform: translateY(-4px);
      border-color: var(--border-gold-bright);
      box-shadow: 0 14px 35px rgba(0,0,0,0.6), 0 0 25px rgba(212, 175, 55, 0.22);
    }

    /* Slider & Visual de Imagen */
    .card-img-wrap {
      position: relative;
      width: 100%;
      aspect-ratio: 1/1;
      background: #09090c;
      overflow: hidden;
      cursor: pointer;
    }
    .card-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      transition: transform 0.4s ease, opacity 0.2s ease;
      display: block;
    }
    .card:hover .card-img {
      transform: scale(1.04);
    }
    .card-badge {
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(9, 9, 11, 0.88);
      color: var(--gold-light);
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 9999px;
      border: 1px solid var(--gold-primary);
      z-index: 2;
      pointer-events: none;
      backdrop-filter: blur(6px);
    }
    .card-multi-badge {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(9, 9, 11, 0.88);
      color: #ffffff;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 9px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 9999px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(6px);
      z-index: 2;
    }
    .slider-toggle-bar {
      position: absolute;
      bottom: 8px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(9, 9, 11, 0.88);
      padding: 3px 8px;
      border-radius: 9999px;
      display: flex;
      align-items: center;
      gap: 4px;
      z-index: 2;
      backdrop-filter: blur(6px);
      border: 1px solid var(--border-gold);
    }
    .slider-dot-btn {
      background: none;
      border: none;
      color: #a1a1aa;
      font-family: 'JetBrains Mono', monospace;
      font-size: 9px;
      font-weight: 700;
      cursor: pointer;
      padding: 2px 6px;
      border-radius: 6px;
      transition: 0.2s;
    }
    .slider-dot-btn.active {
      color: #09090b;
      background: var(--gold-light);
      font-weight: 800;
    }

    .card-body {
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      flex-grow: 1;
      background: var(--bg-card);
    }
    .card-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 13.5px;
      font-weight: 700;
      color: #ffffff;
      margin: 2px 0 8px 0;
      line-height: 1.3;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .card-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-bottom: 10px;
    }
    .color-chip {
      font-size: 9.5px;
      background: rgba(255, 255, 255, 0.05);
      color: #d4d4d8;
      padding: 2px 7px;
      border-radius: 6px;
      font-weight: 600;
      border: 1px solid rgba(255, 255, 255, 0.08);
      font-family: 'Space Grotesk', sans-serif;
    }
    .size-chip {
      font-size: 9.5px;
      background: #09090c;
      color: var(--gold-light);
      padding: 2px 7px;
      border-radius: 6px;
      font-weight: 700;
      border: 1px solid var(--border-gold);
      font-family: 'JetBrains Mono', monospace;
    }
    
    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 10px;
      margin-top: auto;
    }
    .card-price-label {
      font-size: 9px;
      text-transform: uppercase;
      color: var(--text-muted);
      font-weight: 700;
      letter-spacing: 0.5px;
      display: block;
      font-family: 'Space Grotesk', sans-serif;
    }
    .card-price {
      font-family: 'JetBrains Mono', monospace;
      font-size: 15px;
      font-weight: 800;
      color: var(--gold-light);
    }
    .btn-order-card {
      background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
      color: #09090b;
      border: 1px solid #fef08a;
      padding: 7px 14px;
      border-radius: 10px;
      font-size: 11px;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: 0.5px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);
    }
    .btn-order-card:hover {
      filter: brightness(1.12);
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(212, 175, 55, 0.45);
    }

    /* 8. Barra Móvil Flotante Inferior */
    .mobile-cart-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 45;
      background: rgba(9, 9, 11, 0.95);
      backdrop-filter: blur(14px);
      border-top: 1.5px solid var(--border-gold-bright);
      padding: 12px 16px;
      box-shadow: 0 -8px 30px rgba(0,0,0,0.6);
      display: none;
      justify-content: space-between;
      align-items: center;
    }
    .mobile-cart-total {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .mobile-cart-label {
      font-size: 11px;
      color: var(--text-secondary);
      font-weight: 600;
      font-family: 'Space Grotesk', sans-serif;
      text-transform: uppercase;
    }
    .mobile-cart-sum {
      font-family: 'JetBrains Mono', monospace;
      font-size: 18px;
      font-weight: 900;
      color: var(--gold-light);
    }
    .mobile-cart-btn {
      background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
      color: #09090b;
      border: 1px solid #fef08a;
      padding: 10px 20px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: 0.5px;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(212, 175, 55, 0.35);
    }

    /* 9. Modales de Lujo (Quick Add & Carrito Drawer) */
    .modal-overlay {
      position: fixed;
      inset: 0;
      z-index: 60;
      background: rgba(0,0,0,0.82);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      display: flex;
      align-items: flex-end;
      justify-content: center;
    }
    .modal-content {
      background: #121217;
      color: #ffffff;
      width: 100%;
      max-width: 520px;
      border-radius: 24px 24px 0 0;
      max-height: 90vh;
      overflow-y: auto;
      padding: 22px;
      box-shadow: 0 -12px 40px rgba(0,0,0,0.7);
      animation: slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      border-top: 2px solid var(--border-gold-bright);
      border-left: 1px solid var(--border-gold);
      border-right: 1px solid var(--border-gold);
    }
    @media (min-width: 768px) {
      .modal-overlay { align-items: center; }
      .modal-content {
        border-radius: 24px;
        border: 2px solid var(--border-gold-bright);
        box-shadow: 0 20px 60px rgba(0,0,0,0.8), 0 0 30px rgba(212, 175, 55, 0.2);
      }
    }
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 14px;
      margin-bottom: 16px;
    }
    .modal-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 17px;
      font-weight: 800;
      color: #ffffff;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .btn-close {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.1);
      font-size: 14px;
      font-weight: bold;
      cursor: pointer;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }
    .btn-close:hover {
      background: var(--gold-light);
      color: #09090b;
    }

    .cat-btn {
      padding: 8px 16px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      font-size: 12px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
      white-space: nowrap;
      cursor: pointer;
      background: #181820;
      color: #ffffff;
      transition: 0.2s;
    }
    .cat-btn:hover {
      border-color: var(--gold-primary);
    }
    .cat-btn.active {
      background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
      color: #09090b;
      border-color: #fef08a;
      font-weight: 800;
      box-shadow: 0 2px 10px rgba(212, 175, 55, 0.35);
    }

    .btn-primary {
      width: 100%;
      background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
      color: #09090b;
      border: 1px solid #fef08a;
      padding: 13px;
      border-radius: 14px;
      font-size: 13.5px;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      cursor: pointer;
      transition: 0.2s;
      box-shadow: 0 4px 18px rgba(212, 175, 55, 0.35);
    }
    .btn-primary:hover {
      filter: brightness(1.1);
      transform: translateY(-1px);
    }

    .btn-whatsapp {
      width: 100%;
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      color: #ffffff;
      border: 1px solid #34d399;
      padding: 15px;
      border-radius: 14px;
      font-size: 14px;
      font-weight: 900;
      font-family: 'Space Grotesk', sans-serif;
      cursor: pointer;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      transition: 0.2s;
      box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }
    .btn-whatsapp:hover {
      filter: brightness(1.08);
      transform: translateY(-1px);
    }

    /* 10. Notificación Toast */
    .toast {
      position: fixed;
      top: 24px;
      right: 24px;
      z-index: 100;
      background: #09090b;
      color: var(--gold-light);
      border: 1.5px solid var(--border-gold-bright);
      padding: 12px 22px;
      border-radius: 14px;
      font-size: 13px;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      box-shadow: 0 12px 30px rgba(0,0,0,0.6), 0 0 20px rgba(212, 175, 55, 0.3);
      transform: translateY(-60px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .toast.show {
      transform: translateY(0);
      opacity: 1;
    }

    @keyframes slideUp {
      from { transform: translateY(100%); }
      to { transform: translateY(0); }
    }
  </style>
</head>
<body>

  <div class="toast" id="toastMsg">✅ Prenda agregada al pedido</div>

  <!-- BARRA SUPERIOR DE ANUNCIO PARA CLIENTES -->
  <header class="top-announcement">
    <span class="ticker-pulse">
      <span class="pulse-dot"></span>
      CREWSTORE // DROP ARCHIVE 2026
    </span>
    <span>✨ ENVÍOS A TODA COLOMBIA • PAGO CONTRAENTREGA ✨</span>
    <span>PEDIDOS A WHATSAPP 📲</span>
  </header>

  <!-- NAVEGACIÓN DE LUJO -->
  <nav class="navbar">
    <div class="container nav-content">
      <div class="brand" onclick="window.scrollTo({ top: 0, behavior: 'smooth' })">
        <div class="brand-logo-wrap">
          <img src="logo.jpg" alt="crewstore.co logo" class="brand-logo-img">
        </div>
        <div>
          <div class="brand-title" id="brandTitle">crewstore.co</div>
          <div class="brand-sub">Luxury Streetwear Archive</div>
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
    
    <!-- HERO EDITORIAL & 3D ALBUM SHOWCASE -->
    <section class="hero-editorial">
      <div class="hero-grid">
        <!-- Columna Izquierda: Información Editorial -->
        <div class="hero-content">
          <div class="hero-tag-wrap">
            <span style="font-size: 12px;">🔥</span>
            <span class="hero-tag-text">DROP OFICIAL 2026 // LIMITED EDITION</span>
          </div>

          <h1 class="hero-title">
            CREWSTORE<br>
            <span class="gold-accent">LUXURY STREETWEAR</span>
          </h1>

          <p class="hero-desc">
            Moda urbana de corte internacional, camisetas de fútbol retro & actual, básicos oversized y siluetas exclusivas. Elige tu referencia, personaliza tu talla y coordina tu pedido directo con pago contraentrega en Bucaramanga y envíos a todo el país.
          </p>

          <div class="hero-badges-row">
            <span class="hero-spec-badge">
              <span>👕</span> <strong id="heroTotalCount">431</strong> Prendas en Catálogo
            </span>
            <span class="hero-spec-badge">
              <span>⚡</span> Calidad 1.1 Importada
            </span>
            <span class="hero-spec-badge">
              <span>🚚</span> Contraentrega Colombia
            </span>
            <span class="hero-spec-badge">
              <span>📲</span> <strong id="heroWhatsAppText">317 012 8692</strong>
            </span>
          </div>

          <div class="hero-cta-group">
            <button class="btn-hero-primary" onclick="document.getElementById('sectionsContainer').scrollIntoView({ behavior: 'smooth' })">
              Explorar Drops ⚡
            </button>
            <button class="btn-hero-secondary" onclick="openCartDrawer()">
              Ver Mi Pedido 🛍️
            </button>
          </div>
        </div>

        <!-- Columna Derecha: 3D Floating Album Lookbook (Inspirado en Spotify / The Weeknd imagen) -->
        <div class="hero-deck-wrap">
          <div class="hero-deck-card">
            <div class="deck-img-wrap">
              <img src="assets/editorial/crew_backprint.jpg" alt="Crewstore Streetwear Lookbook" class="deck-img" onerror="this.src='logo.jpg'">
              <span class="deck-tag-floating">// CREW ARCHIVE 01</span>
              <span class="deck-tag-coords">04°38'N 74°05'W</span>
            </div>
            <div class="deck-player-bar">
              <div class="player-track-info">
                <div class="player-play-icon">▶</div>
                <div>
                  <div class="player-title">CREW SOUNDTRACK // 2026</div>
                  <div class="player-sub">By Any Means Necessary • Drop 01</div>
                </div>
              </div>
              <div class="player-equalizer" title="Crew Radio Audio Vibe">
                <div class="eq-bar"></div>
                <div class="eq-bar"></div>
                <div class="eq-bar"></div>
                <div class="eq-bar"></div>
                <div class="eq-bar"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- BANNER DE COMBOS PROMOCIONALES -->
    <section id="promoBasketsSection" class="promo-basket">
      <div style="display: flex; align-items: center; gap: 14px;">
        <div style="font-size: 28px; background: rgba(212, 175, 55, 0.12); padding: 8px 12px; border-radius: 12px; border: 1px solid var(--border-gold);">🎁</div>
        <div>
          <div class="promo-tag" id="promoBasketTag">OFERTA EXCLUSIVA // COMBOS URBANOS</div>
          <div class="promo-title" id="promoBasketTitle">¡Arma tu Combo de 2 o 3 Prendas y aprovecha precios especiales!</div>
          <div class="promo-sub" id="promoBasketSub">Combina tus referencias, colores y tallas favoritas en un solo pedido coordinado por WhatsApp.</div>
        </div>
      </div>
      <button onclick="openCartDrawer()" class="btn-promo">
        Ver mi Pedido 🛍️
      </button>
    </section>

    <!-- BARRA PEGAJOSA: BUSCADOR + SECCIONES -->
    <div class="sticky-controls">
      <!-- BUSCADOR POR NÚMERO O PALABRA CLAVE -->
      <div class="search-bar-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Buscar por número (ej: 1, 25, 120) o club / estilo (Bucaramanga, Madrid, Jordan, Buzo)..." oninput="handleSearchInput(this.value)">
        <button class="btn-clear-search" id="btnClearSearch" onclick="clearSearch()" title="Borrar búsqueda">✕</button>
      </div>

      <!-- PÍLDORAS DE CATEGORÍAS ORGANIZADAS -->
      <div class="category-pills-bar" id="categoryPillsBar">
        <button class="cat-pill active" data-cat="all" onclick="filterBySection('all')">
          <span>✨ Todos los Drops</span>
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
          <span>🧥 Buzos & Hoodies</span>
          <span class="pill-count" id="pillCountBuzos">30</span>
        </button>
        <button class="cat-pill" data-cat="Conjuntos & Streetwear" onclick="filterBySection('Conjuntos & Streetwear')">
          <span>🔥 Conjuntos Streetwear</span>
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
        <div style="position: relative; width: 90px; height: 90px; border-radius: 14px; overflow: hidden; border: 1.5px solid var(--border-gold); background: #000;">
          <img id="modalProdImg" src="" style="width: 100%; height: 100%; object-fit: cover;">
          <div id="modalSliderBar" style="position: absolute; bottom: 4px; left: 0; right: 0; display: flex; justify-content: center; gap: 4px;"></div>
        </div>
        <div>
          <span style="background: #09090c; color: var(--gold-light); font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 9999px; border: 1px solid var(--gold-primary);" id="modalProdCode">REF-001</span>
          <h4 style="font-size: 15px; font-weight: 800; font-family: 'Space Grotesk', sans-serif; color: #ffffff; margin: 6px 0 3px 0;" id="modalProdName">Prenda</h4>
          <div style="font-size: 17px; font-weight: 900; color: var(--gold-light); font-family: 'JetBrains Mono', monospace;">
            $<span id="modalProdPrice">0</span> COP
          </div>
        </div>
      </div>

      <div style="margin-bottom: 16px;" id="modalColorsSection">
        <label style="font-size: 11px; font-weight: 800; font-family: 'Space Grotesk', sans-serif; text-transform: uppercase; color: var(--gold-light); display: block; margin-bottom: 8px;">Color Disponible:</label>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;" id="modalColorsContainer"></div>
      </div>

      <div style="margin-bottom: 18px;" id="modalSizesSection">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <label style="font-size: 11px; font-weight: 800; font-family: 'Space Grotesk', sans-serif; text-transform: uppercase; color: var(--gold-light);">Talla Disponible:</label>
          <span style="font-size: 11px; color: var(--text-secondary);">Elige una o escribe la tuya</span>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px;" id="modalSizesContainer"></div>
        <div style="position: relative;">
          <input type="text" id="customSizeInput" placeholder="✍️ ¿Buscas otra talla? Escríbela aquí (ej. 32, XXL, 16)..." oninput="handleCustomSizeInput(this.value)" style="width: 100%; padding: 10px 14px; border-radius: 12px; border: 1.5px solid rgba(255, 255, 255, 0.15); font-size: 13px; outline: none; background: #16161d; font-weight: 700; color: #ffffff; box-sizing: border-box; transition: border-color 0.2s; font-family: 'Space Grotesk', sans-serif;">
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; background: #181820; padding: 12px 16px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.08);">
        <span style="font-size: 13px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; color: #ffffff;">Cantidad:</span>
        <div style="display: flex; align-items: center; gap: 14px;">
          <button onclick="changeModalQty(-1)" style="width: 30px; height: 30px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); background: #22222a; color: #fff; font-weight: bold; cursor: pointer;">-</button>
          <span id="modalQtyDisplay" style="font-size: 15px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: var(--gold-light);">1</span>
          <button onclick="changeModalQty(1)" style="width: 30px; height: 30px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); background: #22222a; color: #fff; font-weight: bold; cursor: pointer;">+</button>
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
        <h3 class="modal-title">🛍️ Tu Pedido Streetwear</h3>
        <button class="btn-close" onclick="closeCartDrawer()">✕</button>
      </div>

      <!-- LISTA DE PRENDAS -->
      <div id="cartItemsList" style="max-height: 240px; overflow-y: auto; margin-bottom: 16px;"></div>

      <!-- TOTAL -->
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; background: #09090c; border-radius: 14px; margin-bottom: 16px; border: 1.5px solid var(--border-gold-bright);">
        <span style="font-size: 13px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; color: #ffffff; text-transform: uppercase;">Total a Pagar:</span>
        <span style="font-size: 20px; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: var(--gold-light);" id="cartTotalDisplay">$0 COP</span>
      </div>

      <!-- SOLICITUD DE DATOS SOLO AL ENVIAR EL PEDIDO -->
      <div style="background: #181820; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 16px; margin-bottom: 16px;" id="checkoutFormSection">
        <h4 style="font-size: 12px; font-weight: 800; font-family: 'Space Grotesk', sans-serif; text-transform: uppercase; color: var(--gold-light); margin-bottom: 6px; letter-spacing: 0.5px;">
          📍 Datos de Entrega (Pago Contraentrega / Envíos):
        </h4>
        <p style="font-size: 11.5px; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.4;">
          🛵 Envíos en Bucaramanga y a todo el país (el valor del domicilio lo cancelas contraentrega al recibir directamente al repartidor). Ingresa tus datos para coordinar:
        </p>

        <div style="margin-bottom: 10px;">
          <input type="text" id="custName" placeholder="Nombre y Apellido *" style="width: 100%; padding: 11px 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); font-size: 13px; outline: none; background: #121217; color: #ffffff; font-family: 'Space Grotesk', sans-serif;">
        </div>
        <div>
          <input type="text" id="custAddress" placeholder="Dirección de Entrega y Barrio / Ciudad *" style="width: 100%; padding: 11px 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); font-size: 13px; outline: none; background: #121217; color: #ffffff; font-family: 'Space Grotesk', sans-serif;">
        </div>
      </div>

      <button class="btn-whatsapp" onclick="sendOrderToWhatsApp()">
        <span>📲</span>
        <span>Enviar Pedido al WhatsApp</span>
      </button>
    </div>
  </div>

  <!-- PIE DE PÁGINA LUXURY -->
  <footer style="background: #050507; color: var(--text-secondary); font-size: 12px; text-align: center; padding: 36px 16px; margin-top: auto; border-top: 1.5px solid var(--border-gold-bright);">
    <div style="display: flex; justify-content: center; margin-bottom: 14px;">
      <div style="width: 58px; height: 58px; border-radius: 50%; padding: 2px; background: linear-gradient(135deg, #d4af37, #453712, #d4af37); box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);">
        <img src="logo.jpg" alt="crewstore.co" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover; display: block;">
      </div>
    </div>
    <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 900; color: #ffffff; font-size: 18px; margin-bottom: 6px; letter-spacing: 1px;" id="footerStoreName">CREWSTORE.CO</div>
    <div style="max-width: 500px; margin: 0 auto; color: #a1a1aa; font-size: 11.5px; line-height: 1.5;">Luxury Streetwear & Blokecore • Catálogo Oficial 2026 • Despacho sujeto a disponibilidad de referencias y tallas</div>
    <div style="margin-top: 10px; font-size: 10.5px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">© 2026 CREWSTORE. Todos los derechos reservados. Bucaramanga, Colombia.</div>
  </footer>

  <script>
    """

js_part = orig[idx2 + 2:]

# Let's customize renderCard and renderSectionsAndProducts in js_part for the new section headers and styling
old_render_section = """        htmlBlocks += `
          <section id="section-${sec.id.replace(/\\s+/g, '-')}" style="margin-bottom: 28px;">
            <div class="section-header-banner">
              <div class="section-title-wrap">
                <span class="section-icon">${sec.icon}</span>
                <div>
                  <h3 class="section-title">${sec.name}</h3>
                  <span style="font-size: 10px; color: #d4af37;">${sec.tag}</span>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <span class="section-badge-cnt">${secItems.length} prendas</span>
                <button class="btn-sec-filter" onclick="filterBySection('${sec.id}')">Ver sólo esta →</button>
              </div>
            </div>
            <div class="products-grid">
              ${secItems.map(renderCard).join('')}
            </div>
          </section>
        `;"""

new_render_section = """        const secIdx = String(SECTIONS_CONFIG.indexOf(sec) + 1).padStart(2, '0');
        htmlBlocks += `
          <section id="section-${sec.id.replace(/\\s+/g, '-')}" style="margin-bottom: 34px;">
            <div class="section-header-banner">
              <div class="section-title-wrap">
                <span class="section-num-tag">// DROP ${secIdx}</span>
                <span class="section-icon">${sec.icon}</span>
                <div>
                  <h3 class="section-title">${sec.name}</h3>
                  <div class="section-subtag">${sec.tag}</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span class="section-badge-cnt">${secItems.length} prendas</span>
                <button class="btn-sec-filter" onclick="filterBySection('${sec.id}')">Ver sólo este drop →</button>
              </div>
            </div>
            <div class="products-grid">
              ${secItems.map(renderCard).join('')}
            </div>
          </section>
        `;"""

if old_render_section in js_part:
    js_part = js_part.replace(old_render_section, new_render_section)
    print("Replaced section block template in JS successfully!")
else:
    print("Warning: old_render_section not exact match, checking alternative...")

# Also update single category view header in JS
old_cat_view = """          <div class="section-header-banner" style="margin-top: 0;">
            <div class="section-title-wrap">
              <span class="section-icon">${secCfg.icon}</span>
              <div>
                <h3 class="section-title">${secCfg.name}</h3>
                <span style="font-size: 10px; color: #d4af37;">${secCfg.tag}</span>
              </div>
            </div>
            <button class="btn-sec-filter" onclick="filterBySection('all')">Ver Todas Las Secciones</button>
          </div>"""

new_cat_view = """          <div class="section-header-banner" style="margin-top: 0;">
            <div class="section-title-wrap">
              <span class="section-num-tag">// COLECCIÓN ACTIVA</span>
              <span class="section-icon">${secCfg.icon}</span>
              <div>
                <h3 class="section-title">${secCfg.name}</h3>
                <div class="section-subtag">${secCfg.tag}</div>
              </div>
            </div>
            <button class="btn-sec-filter" onclick="filterBySection('all')">← Ver Todos los Drops</button>
          </div>"""

if old_cat_view in js_part:
    js_part = js_part.replace(old_cat_view, new_cat_view)
    print("Replaced single category header in JS successfully!")

# Also let's update cart item display in JS to have dark theme
old_cart_item = """          <div style="display: flex; gap: 10px; align-items: center; padding: 10px 0; border-bottom: 1px solid #f5f5f4;">
            <img src="${item.image}" style="width: 46px; height: 46px; object-fit: cover; border-radius: 8px; border: 1px solid #e5e5e5;">
            <div style="flex-grow: 1;">
              <div style="font-size: 12px; font-weight: 800; color: #0c0a09;">${item.name} (${item.code})</div>
              <div style="font-size: 11px; color: #737373;">Color: <strong>${item.selectedColor}</strong> • Talla: <strong>${item.selectedSize}</strong>${item.quantity > 1 ? ` • Cant: <strong>${item.quantity}</strong>` : ''}</div>
              <div style="font-size: 13px; font-weight: 900; font-family: monospace; color: #0c0a09; margin-top: 2px;">
                $${formatCOP(item.salePrice * item.quantity)} COP
              </div>
            </div>
            <button onclick="removeCartItem(${idx})" style="background: none; border: none; color: #ef4444; font-size: 15px; font-weight: bold; cursor: pointer; padding: 4px;">✕</button>
          </div>"""

new_cart_item = """          <div style="display: flex; gap: 12px; align-items: center; padding: 12px; border-radius: 12px; background: #16161c; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 8px;">
            <img src="${item.image}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 10px; border: 1px solid var(--border-gold);">
            <div style="flex-grow: 1;">
              <div style="font-size: 13px; font-weight: 800; font-family: 'Space Grotesk', sans-serif; color: #ffffff;">${item.name} (${item.code})</div>
              <div style="font-size: 11px; color: var(--text-secondary); margin: 2px 0;">Color: <strong style="color: #fff;">${item.selectedColor}</strong> • Talla: <strong style="color: var(--gold-light);">${item.selectedSize}</strong>${item.quantity > 1 ? ` • Cant: <strong style="color: #fff;">${item.quantity}</strong>` : ''}</div>
              <div style="font-size: 14px; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: var(--gold-light);">
                $${formatCOP(item.salePrice * item.quantity)} COP
              </div>
            </div>
            <button onclick="removeCartItem(${idx})" style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); color: #f87171; width: 28px; height: 28px; border-radius: 8px; font-size: 13px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
          </div>"""

if old_cart_item in js_part:
    js_part = js_part.replace(old_cart_item, new_cart_item)
    print("Replaced cart item display in JS successfully!")

new_full_content = head_and_html_part + catalog_script_part + js_part

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(new_full_content)

print(f"index.html successfully updated! New size: {len(new_full_content)} bytes")
