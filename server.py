from flask import Flask, request, abort
from config import me, db
import json

app = Flask("server")


@app.get("/")
def home():
    return "Hello World"


@app.get("/test")
def test():
    return "This is a test page"

# get /about to show your name


@app.get("/about")
def about():
    return "Romnick Sarmiento"

### API ###

# get /api/about/developer
# return full name: name last_name


@app.get("/api/about/developer")
def about_dev():
    return json.dumps(me["name"] + " " + me["last_name"])


@app.get("/api/about")
def about_data():
    return json.dumps(me)


@app.get("/api/categories")
def categories():
    all_cats = []
    cursor = db.products.find({})
    for product in cursor:
        make = product["make"]
        if make not in all_cats:
            all_cats.append(make)

    return json.dumps(all_cats)


def fix_id(record):
    record["_id"] = str(record["_id"])
    return record


@app.get("/api/products")
def get_products():
    products = []
    cursor = db.products.find({})
    for product in cursor:
        products.append(fix_id(product))

    return json.dumps(products)


@app.post("/api/products")
def save_product():
    product = request.get_json()

    db.products.insert_one(product)

    return json.dumps(fix_id(product))


@app.get("/api/products/make/<make>")
def get_by_category(make):
    products = []
    cursor = db.products.find({"make": make})
    for product in cursor:
        products.append(fix_id(product))

    return json.dumps(products)

# get /api/reports/total
# the total value of the catalog (sum of all prices)


@app.get("/api/reports/total")
def get_total():
    catalog_total = 0
    cursor = db.products.find({})
    for product in cursor:
        catalog_total += product["price"]

    print(catalog_total)

    return json.dumps(f"The catalog total is: ${catalog_total}")


# Start the server
app.run(debug=True)
