"""
Simple web UI for Affz Trial Engine with file upload.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import urllib.parse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from engine.engine import AssetLibrary, VariationEngine
from engine.photo_intake import scan_folder
from templates.templates import get_all_templates


PORT = int(os.environ.get("PORT", 8080))
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
        if self.path == "/api/upload":
            # Simple acknowledgment for now
            self.send_json({"status": "ok", "count": 1, "message": "Files received. Processing coming soon."})
            return

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
                self.send_json({"status": "error", "message": "Upload or scan first"}, 400)
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
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: system-ui; max-width: 800px; margin: 20px auto; padding: 16px; background: #111; color: #eee; }
    button { padding: 12px 20px; margin: 8px 0; background: #333; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }
    button:hover { background: #555; }
    input[type="file"] { margin: 10px 0; }
    pre { background: #222; padding: 15px; overflow: auto; border-radius: 6px; }
    h1 { color: #fff; }
  </style>
</head>
<body>
  <h1>Affz Trial Engine</h1>
  <p>Modeling Trial Reel generator for @affz.20</p>
  
  <h3>1. Upload Photos / Videos</h3>
  <input type="file" id="fileInput" multiple accept="image/*,video/*">
  <br>
  <button onclick="upload()">Upload Files</button>
  <div id="uploadResult"></div>

  <h3>2. Generate Variations</h3>
  <select id="template">
    <option value="transform_years">X Years Later</option>
    <option value="photobooth_max">Photoboothmaxxing</option>
    <option value="never_model">You Will Never Model</option>
    <option value="pump_check">Pump Check</option>
  </select>
  <input type="number" id="count" value="5" min="1" max="20" style="width:60px">
  <br>
  <button onclick="generate()">Generate Batch</button>
  <pre id="output">Click Generate...</pre>

  <script>
    async function upload() {
      const input = document.getElementById('fileInput');
      const files = input.files;
      if (!files.length) {
        document.getElementById('uploadResult').innerText = 'Select files first';
        return;
      }
      const formData = new FormData();
      for (let f of files) formData.append('files', f);
      const r = await fetch('/api/upload', {method:'POST', body: formData});
      const d = await r.json();
      document.getElementById('uploadResult').innerText = d.status === 'ok' ? `Uploaded ${d.count} files` : (d.message || 'Error');
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
    print(f"Starting Affz Trial Engine UI on port {PORT}")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
