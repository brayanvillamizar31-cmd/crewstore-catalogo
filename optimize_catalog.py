#!/usr/bin/env python3
"""
Agente de Optimización & UI/UX - Tienda Boutique
Optimización Inteligente de Calidad Visual:
- Respaldo de seguridad automático de originales en products_backup/
- Preserva la calidad visual al 100% (calidad 85% y resolución retina hasta 1400px)
- Solo toca imágenes pesadas (> 250KB)
- Agrega lazy loading en index.html
"""
import os
import sys
import shutil
import subprocess
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_DIR = os.path.join(BASE_DIR, "products")
BACKUP_DIR = os.path.join(BASE_DIR, "products_backup")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")

def get_directory_size(path):
    total = 0
    if not os.path.exists(path):
        return 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def backup_images():
    if not os.path.exists(BACKUP_DIR):
        print("💾 Creando copia de seguridad en products_backup/ por seguridad...")
        shutil.copytree(PRODUCTS_DIR, BACKUP_DIR)
        print("✅ Respaldo completo creado con éxito.")
    else:
        print("ℹ️ Ya existe una copia de seguridad en products_backup/.")

def restore_images():
    if not os.path.exists(BACKUP_DIR):
        print("❌ No se encontró la carpeta de respaldo products_backup/.")
        return
    print("🔄 Restaurando imágenes originales desde products_backup/...")
    shutil.rmtree(PRODUCTS_DIR)
    shutil.copytree(BACKUP_DIR, PRODUCTS_DIR)
    print("✅ Imágenes originales 100% restauradas.")

def fix_lazy():
    print("==================================================")
    print(" 🚀 ACTIVANDO LAZY LOADING EN INDEX.HTML")
    print("==================================================")
    if not os.path.exists(INDEX_HTML):
        print("❌ No se encontró index.html")
        return

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    target = 'class="card-img" alt="" onerror="handleImgError(this, ${item.id})">'
    replacement = 'class="card-img" alt="" loading="lazy" decoding="async" onerror="handleImgError(this, ${item.id})">'

    if 'loading="lazy"' in content:
        print("ℹ️ Lazy loading ya está activado en index.html.")
        return

    if target in content:
        new_content = content.replace(target, replacement)
        with open(INDEX_HTML, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ Lazy loading y decoding asíncrono activados en las tarjetas.")
    else:
        print("⚠️ No se encontró la etiqueta exacta para reemplazar de forma automática.")

def smart_compress(quality=85, max_dimension=1400, size_threshold_kb=250):
    print("==================================================")
    print(" ⚡ OPTIMIZACIÓN INTELIGENTE (SIN PÉRDIDA VISUAL)")
    print("==================================================")

    backup_images()

    initial_size = get_directory_size(PRODUCTS_DIR)
    images = [f for f in os.listdir(PRODUCTS_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]

    print(f"Examinando {len(images)} imágenes...")
    print(f"Reglas: Mantener resolución Retina (máx {max_dimension}px), Calidad alta ({quality}%), solo fotos > {size_threshold_kb}KB.\n")

    optimized_count = 0
    bytes_threshold = size_threshold_kb * 1024

    for img in images:
        img_path = os.path.join(PRODUCTS_DIR, img)
        before_sz = os.path.getsize(img_path)

        if before_sz < bytes_threshold:
            continue  # Dejar intacta porque ya es ligera

        # Redimensionar solo si supera 1400px (retina)
        subprocess.run(
            ["sips", "--resampleHeightWidthMax", str(max_dimension), img_path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Optimizar metadatos y aplicar calidad 85% (indistinguible para el ojo humano)
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(quality), img_path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        after_sz = os.path.getsize(img_path)
        if after_sz < before_sz:
            saved_img = before_sz - after_sz
            print(f"  • {img}: {format_size(before_sz)} -> {format_size(after_sz)} (Ahorro: -{format_size(saved_img)})")
            optimized_count += 1

    final_size = get_directory_size(PRODUCTS_DIR)
    total_saved = initial_size - final_size
    percent = (total_saved / initial_size) * 100 if initial_size > 0 else 0

    print("--------------------------------------------------")
    print(f"🎉 ¡OPTIMIZACIÓN FINALIZADA!")
    print(f"📸 Fotos optimizadas: {optimized_count} (el resto ya era ligero y se dejó 100% original)")
    print(f"📊 Peso total antes:  {format_size(initial_size)}")
    print(f"📉 Peso total ahora:  {format_size(final_size)}")
    print(f"✨ Ahorro de datos:   {format_size(total_saved)} (-{percent:.1f}%)")
    print(f"🛡️ Respaldo seguro:   guardado en {BACKUP_DIR}")

def audit():
    print("==================================================")
    print(" 🎨 AGENTE DE RENDIMIENTO & UI/UX: AUDITORÍA")
    print("==================================================")
    total_size = get_directory_size(PRODUCTS_DIR)
    images = [f for f in os.listdir(PRODUCTS_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    print(f"📸 Total de imágenes: {len(images)}")
    print(f"⚖️ Peso total: {format_size(total_size)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--compress", action="store_true")
    parser.add_argument("--restore", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.restore:
        restore_images()
    elif args.all:
        fix_lazy()
        print("\n")
        smart_compress()
    elif args.compress:
        smart_compress()
    else:
        audit()
