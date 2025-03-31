import http.server
import socketserver
import urllib.parse
import re

TXT_FILE = "data.txt"  # Verilerin bulunduğu dosya
PORT = 8000

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kelime Arama</title>
</head>
<body>
    <h2>Kelime Arama</h2>
    <form method="get" action="/search">
        <input type="text" name="q" placeholder="Aranacak kelime">
        <button type="submit">Ara</button>
    </form>
    <div id="results">{results}</div>
</body>
</html>
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.format(results="").encode("utf-8"))
        elif parsed_path.path == '/search' and 'q' in query_params:
            query = query_params['q'][0].strip()
            
            if not query:
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.format(results="<p>Aranacak kelime belirtilmedi.</p>").encode("utf-8"))
                return
            
            try:
                with open(TXT_FILE, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                matched_lines = [line.strip() for line in lines if query in line]
                
                if matched_lines:
                    result_html = "<h3>Sonuçlar:</h3>" + "".join(f"<p>{line}</p>" for line in matched_lines)
                else:
                    result_html = "<p>Sonuç bulunamadı.</p>"
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.format(results=result_html).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.format(results=f"<p>Hata: {e}</p>").encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Sunucu http://localhost:{PORT} adresinde çalışıyor...")
    httpd.serve_forever()
