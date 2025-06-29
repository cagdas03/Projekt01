import http.server
import socketserver
import os
import cgi
import json

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'products.json')
IMAGE_DIR = os.path.join(STATIC_DIR, 'images')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def render_template(self, template_name, context=None):
        context = context or {}
        with open(os.path.join(TEMPLATES_DIR, template_name), 'r', encoding='utf-8') as f:
            html = f.read()
        for key, value in context.items():
            html = html.replace('{{' + key + '}}', value)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def load_products(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_products(self, products):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False)

    def do_GET(self):
        if self.path == '/':
            products = self.load_products()
            items = []
            for p in products:
                item = (
                    '<div class="product">'
                    f'<img src="/static/{p.get("image", "")}" alt="{p.get("title", "")}">' 
                    f'<h2>{p.get("title", "")}</h2>'
                    f'<p>{p.get("description", "")}</p>'
                    '</div>'
                )
                items.append(item)
            context = {'product_items': '\n'.join(items)}
            self.render_template('index.html', context)
        elif self.path == '/admin':
            self.render_template('admin.html')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/admin':
            content_type = self.headers.get('content-type')
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE': content_type},
            )
            title = form.getvalue('title', '')
            description = form.getvalue('description', '')
            fileitem = form['image'] if 'image' in form else None
            image_path = ''
            if fileitem is not None and fileitem.filename:
                filename = os.path.basename(fileitem.filename)
                os.makedirs(IMAGE_DIR, exist_ok=True)
                filepath = os.path.join(IMAGE_DIR, filename)
                with open(filepath, 'wb') as f:
                    f.write(fileitem.file.read())
                image_path = f'images/{filename}'
            products = self.load_products()
            products.append({'title': title, 'description': description, 'image': image_path})
            self.save_products(products)
            self.send_response(303)
            self.send_header('Location', '/admin')
            self.end_headers()
        else:
            self.send_error(404)

if __name__ == '__main__':
    os.makedirs(IMAGE_DIR, exist_ok=True)
    PORT = 8000
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f'Server running on port {PORT}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
