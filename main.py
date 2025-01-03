from flask import Flask, render_template, url_for, redirect, request, make_response

class Product:
    def __init__(self, name, price, category, description="мне лень", img="img1.jpg"):
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.img = img


    def __str__(self) -> str:
        return f"Product - {self.name}\nPrice - {self.price}"

class Client:
    def __init__(self, login, password, cart=None) -> None:
        self.login = login
        self.password = password
        self.cart = cart if cart is not None else []

    def add_to_cart(self, product):
        self.cart.append(product)

log = "ghj"
pas = "pass"

hot_dogs = [Product("Hot dog", 60, "spicy", "descdewggerw", "img1.jpg"),
            Product("VERY Hot dog", 120, "hot", "fheruwiopfheuiwop", "img2.jpg"),
            Product("dog", 9, "small", "dfhbuiewfdheuwi", "img3.jpg"),
            Product("ot hot dog", 900, "vegan", "fjewiofjiewofjeiwo", "img4.jpg")]

clients = []
a = 3
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home(status=None):
    status = request.args.get("status")
    return render_template("index.html", status=status)

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/sign_up_verification", methods=["POST"])
def sign_up_verification():
    for client in clients:
        if client.login == request.form.get("login"):
            return redirect(url_for("sign_up", status="Login already exists")) 

    clients.append(Client(request.form.get("login"), request.form.get("password")))

    res = make_response(redirect(url_for("home")))
    res.set_cookie("Login", request.form.get("login"))
    res.set_cookie("Password", request.form.get("password"))

    return res

@app.route("/log_in")
def log_in():
    login_cookie = request.cookies.get("Login")
    password_cookie = request.cookies.get("Password")
    print(f"Cookies - Login -> {login_cookie}\nPassword -> {password_cookie}")

    if login_cookie and password_cookie:
        for client in clients:
            print(f"client -> Login: {client.login}\nPassword -> {client.password}")
            if client.login == login_cookie and client.password == password_cookie:
                print("Login successful!")
                return redirect(url_for("home", status="Authorized"))

    
    
    return render_template("log_in.html")



@app.route("/products/")
@app.route("/products/<category>")
def products(category=""):
    client_login = request.args.get('client_login')

    login_cookie = request.cookies.get("Login")
    password_cookie = request.cookies.get("Password")

    # if client_login == None:
    #     return render_template("error.html") 
    for client in clients:
        if client.login == login_cookie and client.password == password_cookie:
            print(f"Client login -> {client.login}\nclient password -> {client.password}")

            return render_template(
                "products.html", 
                items=[item for item in hot_dogs] if category == "" else [item for item in hot_dogs if category.lower() == item.category],
                client_logged_in=True
            )
        else:
            return render_template("error.html")
    return render_template(
                "products.html", 
                items=[item for item in hot_dogs] if category == "" else [item for item in hot_dogs if category.lower() == item.category],
                client_logged_in=False
            )
    
    
@app.route("/log_out")
def log_out():

    response = make_response(redirect(url_for("home")))

    if 'Login' in request.cookies:
        response.set_cookie('Login', '', expires=0)# max_age = 60*60*24, secure=True, httponly=True,

    if 'Password' in request.cookies:
        response.set_cookie('Password', '', expires=0)


    return response
    


@app.route('/delete', methods=['POST'])
def delete():
    product_name = request.form.get('product_name')
    for hotdog in hot_dogs:
        if hotdog.name == product_name:
            hot_dogs.remove(hotdog)
            break
    return redirect(url_for('products'))


@app.route('/manage')
def manage_products():
    return render_template('manage.html')


@app.route('/addpr', methods=['POST'])
def addpr():
    hot_dogs.append(Product(request.form['product_name'], request.form['product_price'], request.form['product_category'], request.form['product_description'], request.form['product_img']))
    return redirect(url_for('products'))



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search/<item>")
def search(item):
    return render_template("search.html", item = [product for product in hot_dogs if product.name == item][0])



@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product_name")

    login_cookie = request.cookies.get("Login")
    password_cookie = request.cookies.get("Password")
    
    if not login_cookie or not password_cookie:
        print("Dont logged in")
        return redirect(url_for("log_in"))

    
    for client in clients:
        if client.login == login_cookie and client.password == password_cookie:
            for product in hot_dogs:
                if product.name == product_name:
                    client.add_to_cart(product)
                    print(f"{product_name} добавлен в корзину {client.login}")
                    return redirect(url_for("products"))
    
    return redirect(url_for("products"))


@app.route("/cart")
def view_cart():
    login_cookie = request.cookies.get("Login")
    password_cookie = request.cookies.get("Password")

    for client in clients:
        if client.login == login_cookie and client.password == password_cookie:
            return render_template("cart.html", items=client.cart)

    return redirect(url_for("log_in"))


# @app.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     client_login = request.form['client_login']
#     ##########################
#     client = [client for client in client_list if client.login == client_login][0]
#     ###########################

#     if client is None:
#         return redirect(url_for('log_in'))
    
#     for hotdog in hot_dogs:
#         if hotdog.name == request.form['name']:
#             client.cart.append(hotdog)
#             break
    
#     return redirect(url_for('cart', client_login=client_login))


# @app.route('/remove_from_cart', methods=['POST'])
# def remove_from_cart():
#     name = request.form['name']
#     for item in cart_list:
#         if item.name == name:
#             cart_list.remove(item)
#     return redirect(url_for('cart'))

# @app.route('/cart')
# def cart():
#     client_login = request.args.get('client_login')
#     client = [client for client in client_list if client.login == client_login][0]

#     if client:
#         return render_template("cart.html", items=client.cart)
    
#     return redirect(url_for('log_in'))



# # @app.route("/switch/<frmo>/<to>")
# # def switch(frmo, to):
# #     # [dog for dog in hot_dogs if dog.price >= int(frmo) and dog.price <= int(to) ]
# #     return render_template("switch.html", items=hot_dogs, frmo=int(frmo), to=int(to))

# @app.route("/switch/<frmo>/<to>")
# def switch(frmo, to):
#     return render_template("products.html", items=[dog for dog in hot_dogs if int(frmo) < dog.price < int(to) ])


app.run(debug=True)

