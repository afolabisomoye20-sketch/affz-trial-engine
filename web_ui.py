"""
Simple local web UI for Affz Trial Engine.
Run with: python web_ui.py
Then open http://localhost:8080
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import urllib.parse
from pathlib import Path
import sys

# Fix imports for Render
sys.path.insert(0, str(Path(__file__).parent))

from engine.engine import AssetLibrary, VariationEngine
from engine.photo_intake import scan_folder
from templates.templates import get_all_templates


PORT = 8080
library = AssetLibrary()
engine = None


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_html().encode())
        elif self.path == "/api/templates":
            self.send_json([{"id": t.id, "name": t.name, "tier": t.tier.value} for t in get_all_templates()])
        elif self.path == "/api/library":
            self.send_json({"count": len(library.assets), "assets": list(library.assets.keys())[:20]})
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode() if length else "{}"
        data = json.loads(body) if body else {}

        if self.path == "/api/scan":
            folder = data.get("folder", "data/sample_photos")
            try:
                assets = scan_folder(folder, library)
                library.save()
                global engine
                engine = VariationEngine(library)
                self.send_json({"status": "ok", "count": len(assets)})
            except Exception as e:
                self.send_json({"status": "error", "message": str(e)}, 500)

        elif self.path == "/api/generate":
            if not engine:
                self.send_json({"status": "error", "message": "Scan library first"}, 400)
                return
            template_id = data.get("template", "transform_years")
            count = int(data.get("count", 5))
            try:
                variations = engine.generate_batch(template_id, count=count)
                result = [v.to_dict() for v in variations]
                self.send_json({"status": "ok", "variations": result})
            except Exception as e:
                self.send_json({"status": "error", "message": str(e)}, 500)
        else:
            self.send_error(404)

    def send_json(self, obj, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj, indent=2).encode())

    def get_html(self) -> str:
        return """
<!DOCTYPE html>
<html>
<head>
  <title>Affz Trial Engine</title>
  <style>
    body { font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 20px; background: #111; color: #eee; }
    button { padding: 10px 20px; margin: 8px; background: #333; color: white; border: none; cursor: pointer; }
    button:hover { background: #555; }
    pre { background: #222; padding: 15px; overflow: auto; }
    h1 { color: #fff; }
  </style>
</head>
<body>
  <h1>Affz Trial Engine</h1>
  <p>Modeling Trial Reel generator for @affz.20</p>
  
  <h3>1. Scan Photo Folder</h3>
  <button onclick="scan()">Scan data/sample_photos</button>
  <div id="scanResult"></div>

  <h3>2. Generate Variations</h3>
  <select id="template">
    <option value="transform_years">X Years Later</option>
    <option value="photobooth_max">Photoboothmaxxing</option>
    <option value="never_model">You Will Never Model</option>
    <option value="pump_check">Pump Check</option>
  </select>
  <input type="number" id="count" value="5" min="1" max="20" style="width:60px">
  <button onclick="generate()">Generate Batch</button>
  <pre id="output">Click Generate...</pre>

  <script>
    async function scan() {
      const r = await fetch('/api/scan', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({folder:'data/sample_photos'})});
      const d = await r.json();
      document.getElementById('scanResult').innerText = d.status === 'ok' ? `Scanned ${d.count} assets` : d.message;
    }
    async function generate() {
      const template = document.getElementById('template').value;
      const count = document.getElementById('count').value;
      const r = await fetch('/api/generate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({template, count})});
      const d = await r.json();
      document.getElementById('output').textContent = JSON.stringify(d, null, 2);
    }
  </script>
</body>
</html>
"""


def main():
    print(f"Starting Affz Trial Engine UI on http://localhost:{PORT}")
    print("Open in browser. Press Ctrl+C to stop.")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
