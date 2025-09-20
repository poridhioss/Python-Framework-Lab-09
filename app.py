# app.py

import time
from api import API
from middleware import Middleware

app = API()

# Function-based handlers (existing)
@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}!"

# Class-based handler (new!)
@app.route("/books")
class BooksResource:
    def get(self, req, resp):
        resp.text = "List all books"
    
    def post(self, req, resp):
        resp.text = "Create a new book"

@app.route("/users/{id:d}")
class UserResource:
    def get(self, req, resp, id):
        resp.text = f"Get user {id}"
    
    def put(self, req, resp, id):
        resp.text = f"Update user {id}"
    
    def delete(self, req, resp, id):
        resp.text = f"Delete user {id}"

def sample_handler(req, resp):
    resp.text = "Django-style route registration"

app.add_route("/sample", sample_handler)

@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", context={
        "name": "PoridhiFrame", 
        "title": "Best Framework"
    }).encode()

def custom_exception_handler(request, response, exception_cls):
    response.text = f"Error occurred: {str(exception_cls)}"

app.add_exception_handler(custom_exception_handler)

@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")

# Custom logging middleware
class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, resp):
        print("Processing response", req.url)

app.add_middleware(SimpleCustomMiddleware)

class RequestTimingMiddleware(Middleware):
    def process_request(self, req):
        import time
        req.start_time = time.time()
    
    def process_response(self, req, resp):
        if hasattr(req, 'start_time'):
            duration = time.time() - req.start_time
            resp.headers['X-Response-Time'] = f"{duration:.4f}s"

app.add_middleware(RequestTimingMiddleware)

@app.route("/api/products", allowed_methods=["GET", "POST"])
def products_api(request, response):
    if request.method == "GET":
        response.text = "List products"
    elif request.method == "POST":
        response.text = "Create product"

@app.route("/api/orders", allowed_methods=["GET"])
def orders_api(request, response):
    response.text = "List orders"

# Django-style route with method control
def admin_handler(req, resp):
    resp.text = "Admin panel - PATCH only"

app.add_route("/api/admin", admin_handler, allowed_methods=["PATCH"])