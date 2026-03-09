import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get("PORT", 3000))

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for Telegram WebApp
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        super().end_headers()

def handler(event, context):
    """Vercel serverless handler for static files"""
    from static.index import app as static_app
    return static_app(event, context)

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"🌐 Server running on http://localhost:{PORT}")
    server.serve_forever()
