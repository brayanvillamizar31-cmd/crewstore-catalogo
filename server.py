import http.server
import socketserver
import os
import re
import json
import time
import threading
import subprocess
import urllib.parse
import urllib.request

PORT = 8081
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = BASE_DIR
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.json")
PRODUCTS_JS_FILE = os.path.join(BASE_DIR, "products.js")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
PURCHASES_FILE = os.path.join(BASE_DIR, "purchases.json")
INDEX_HTML_FILE = os.path.join(BASE_DIR, "index.html")
ADMIN_HTML_FILE = os.path.join(BASE_DIR, "bv-panel-7k2q.html")

SUPABASE_URL = "https://nksouvdezctybcwolvfa.supabase.co/rest/v1/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rc291dmRlemN0eWJjd29sdmZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE1NTczMzEsImV4cCI6MjEwNzEzMzMzMX0._FLrAKNq1av0knWG4tkcPxErKm3DnXLefTlaYkN0xlY"

DEFAULT_SETTINGS = {
    "storeName": "crewstore.co",
    "whatsappNumber": "573170128692",
    "globalMargin": 45,
    "currency": "COP",
    "adminPin": "1234",
    "roundThousands": True
}

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_SETTINGS, f, ensure_ascii=False, indent=2)

_sync_lock = threading.Lock()


def push_products_to_supabase(products_data):
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": "Bearer " + SUPABASE_KEY,
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        for i in range(0, len(products_data), 50):
            chunk = []
            for p in products_data[i:i + 50]:
                pid = int(p["id"])
                imgs = p.get("images") if isinstance(p.get("images"), list) and p.get("images") else [p.get("image")]
                chunk.append({
                    "id": 10000 + pid,
                    "code": "CREW-" + str(p.get("code", "")).replace("CREW-", ""),
                    "name": p.get("name", ""),
                    "category": p.get("category") or "Camisetas & Polos",
                    "supplier_price": p.get("supplierPrice", 45000),
                    "margin_percent": p.get("marginPercent", 45),
                    "sale_price": p.get("salePrice", 65000),
                    "colors": p.get("colors") or ["Blanco", "Negro"],
                    "sizes": p.get("sizes") or ["Única"],
                    "image": p.get("image") or f"./products/item_{pid}.jpg",
                    "editorial_image": p.get("editorialImage"),
                    "raw_image": json.dumps(imgs, ensure_ascii=False),
                    "active": p.get("active", True) is not False
                })
            req = urllib.request.Request(
                SUPABASE_URL + "products?on_conflict=id",
                data=json.dumps(chunk).encode("utf-8"),
                method="POST",
                headers=headers
            )
            with urllib.request.urlopen(req, timeout=15):
                pass
    except Exception as e:
        print(f"Aviso sync Supabase products: {e}", flush=True)


def push_settings_to_supabase(settings_data):
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": "Bearer " + SUPABASE_KEY,
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        payload = [{
            "id": "crewstore",
            "store_name": settings_data.get("storeName", "crewstore.co"),
            "whatsapp_number": settings_data.get("whatsappNumber", "573170128692"),
            "global_margin": settings_data.get("globalMargin", 45),
            "admin_pin": settings_data.get("adminPin", "1234"),
            "round_thousands": True
        }]
        req = urllib.request.Request(
            SUPABASE_URL + "store_settings?on_conflict=id",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception as e:
        print(f"Aviso sync Supabase settings: {e}", flush=True)


def sync_products_into_html(products_data):
    default_block = "window.DEFAULT_CATALOG_PRODUCTS = " + json.dumps(products_data, ensure_ascii=False, indent=2) + ";"
    pattern = re.compile(r"window\.DEFAULT_CATALOG_PRODUCTS\s*=\s*\[.*?\];", re.DOTALL)
    for html_path in (INDEX_HTML_FILE, ADMIN_HTML_FILE):
        if os.path.exists(html_path):
            try:
                with open(html_path, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content, count = pattern.subn(lambda _: default_block, content, count=1)
                if html_path == INDEX_HTML_FILE:
                    new_content = re.sub(
                        r'(<strong id="heroTotalCount">)\d+(</strong>)',
                        rf"\g<1>{len(products_data)}\g<2>",
                        new_content
                    )
                if count > 0 and new_content != content:
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
            except Exception as e:
                print(f"Error actualizando HTML {html_path}: {e}", flush=True)


def sync_settings_into_html(settings_data):
    store_name = settings_data.get("storeName", "crewstore.co")
    whatsapp = settings_data.get("whatsappNumber", "573170128692")
    settings_block = (
        "settings: {\n"
        f"        storeName: {json.dumps(store_name, ensure_ascii=False)},\n"
        f"        whatsappNumber: {json.dumps(whatsapp, ensure_ascii=False)}\n"
        "      }"
    )
    pattern = re.compile(r"settings:\s*\{\s*storeName:\s*['\"].*?['\"],\s*whatsappNumber:\s*['\"].*?['\"]\s*\}", re.DOTALL)
    for html_path in (INDEX_HTML_FILE, ADMIN_HTML_FILE):
        if os.path.exists(html_path):
            try:
                with open(html_path, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content, count = pattern.subn(lambda _: settings_block, content, count=1)
                if count > 0 and new_content != content:
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
            except Exception as e:
                print(f"Error actualizando settings en {html_path}: {e}", flush=True)


def git_auto_sync_loop():
    """Detecta cambios en el código o catálogo cada 5s y los sube en tiempo real a GitHub."""
    while True:
        time.sleep(5)
        if not os.path.exists(os.path.join(BASE_DIR, ".git")):
            continue
        with _sync_lock:
            try:
                st = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=BASE_DIR,
                    capture_output=True,
                    text=True
                )
                if st.returncode == 0 and st.stdout.strip():
                    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=False)
                    msg = f"Auto-sync en tiempo real: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                    c = subprocess.run(["git", "commit", "-m", msg], cwd=BASE_DIR, capture_output=True, text=True)
                    if c.returncode == 0:
                        p = subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
                        if p.returncode == 0:
                            print(f"✅ GitHub actualizado en tiempo real ({msg})", flush=True)
            except Exception as e:
                print(f"Aviso git auto-sync: {e}", flush=True)


class BoutiqueHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/products":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if os.path.exists(PRODUCTS_FILE):
                with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(b"[]")
            return

                elif path == "/api/purchases":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if os.path.exists(PURCHASES_FILE):
                with open(PURCHASES_FILE, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(b"[]")
            return

        elif path == "/api/settings":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(json.dumps(DEFAULT_SETTINGS).encode("utf-8"))
            return

        elif path == "/" or path == "/index.html":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        if path == "/api/products":
            try:
                data = json.loads(body.decode("utf-8"))
                if isinstance(data, list) and len(data) > 0:
                    with _sync_lock:
                        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        js_content = "window.CATALOG_PRODUCTS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
                        with open(PRODUCTS_JS_FILE, "w", encoding="utf-8") as f:
                            f.write(js_content)
                        sync_products_into_html(data)
                    threading.Thread(target=push_products_to_supabase, args=(data,), daemon=True).start()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "count": len(data)}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

                elif path == "/api/purchases":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if os.path.exists(PURCHASES_FILE):
                with open(PURCHASES_FILE, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(b"[]")
            return

        elif path == "/api/settings":
            try:
                data = json.loads(body.decode("utf-8"))
                if isinstance(data, dict):
                    merged = {**DEFAULT_SETTINGS, **data}
                    with _sync_lock:
                        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                            json.dump(merged, f, ensure_ascii=False, indent=2)
                        sync_settings_into_html(merged)
                    threading.Thread(target=push_settings_to_supabase, args=(merged,), daemon=True).start()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run():
    threading.Thread(target=git_auto_sync_loop, daemon=True).start()
    socketserver.TCPServer.allow_reuse_address = True
    for port in [8081, 8080, 8082, 3000, 5000]:
        try:
            with socketserver.TCPServer(("", port), BoutiqueHandler) as httpd:
                print(f"Servidor iniciado exitosamente en http://localhost:{port} (Auto-sync GitHub + Supabase activo)", flush=True)
                httpd.serve_forever()
                break
        except OSError:
            print(f"Puerto {port} ocupado, intentando siguiente...", flush=True)


if __name__ == "__main__":
    run()
