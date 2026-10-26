#!/usr/bin/env python3
"""
Validador de Despliegue e Integridad para Tienda Catálogo.
Utilizado por el Agente de CI/CD para asegurar que el sitio esté 100% sano antes de subir a GitHub y Vercel.
"""
import os
import sys
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def check_file_exists(filename, min_size=10):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        return False, f"Falta el archivo requerido: {filename}"
    size = os.path.getsize(filepath)
    if size < min_size:
        return False, f"El archivo {filename} parece estar vacío ({size} bytes)"
    return True, f"OK ({size} bytes)"

def validate_products():
    json_path = os.path.join(BASE_DIR, "products.json")
    if not os.path.exists(json_path):
        return False, "No se encontró products.json"

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, f"Error de sintaxis en products.json: {e}"

    if not isinstance(data, list):
        return False, "products.json debe ser una lista de productos"

    missing_images = []
    for item in data:
        img = item.get("image")
        if img:
            # quitar prefijos si los hay
            clean_img = img.lstrip("/")
            full_img_path = os.path.join(BASE_DIR, clean_img)
            if not os.path.exists(full_img_path):
                missing_images.append((item.get("id", "sin-id"), img))

    summary = f"Total productos: {len(data)}"
    if missing_images:
        details = ", ".join([f"ID {i}: {path}" for i, path in missing_images[:5]])
        if len(missing_images) > 5:
            details += f" (y {len(missing_images) - 5} más)"
        return False, f"Hay {len(missing_images)} imágenes no encontradas: {details}"

    return True, summary

def validate_all():
    print("==================================================")
    print(" 🚀 AGENTE CI/CD: VALIDACIÓN PREVIA AL DESPLIEGUE")
    print("==================================================")
    
    passed = True
    
    # 1. Archivos principales
    for f in ["index.html", "bv-panel-7k2q.html", "products.json", "products.js", "vercel.json"]:
        ok, msg = check_file_exists(f)
        status = "✅" if ok else "❌"
        print(f"{status} {f}: {msg}")
        if not ok:
            passed = False

    # 2. Integridad de productos e imágenes
    ok, msg = validate_products()
    status = "✅" if ok else "❌"
    print(f"{status} Catálogo de Productos: {msg}")
    if not ok:
        passed = False

    print("--------------------------------------------------")
    if passed:
        print("🎉 ¡TODAS LAS VALIDACIONES PASARON EXITOSAMENTE!")
        print("El proyecto está listo para ser desplegado a producción.")
        return 0
    else:
        print("⚠️ SE ENCONTRARON ERRORES. Corrige antes de desplegar.")
        return 1

if __name__ == "__main__":
    sys.exit(validate_all())
