from flask import Flask, request, abort
from config import me, db
import json
from bson import ObjectId  # this is a part of the mongoDB objectID string
from flask_cors import CORS

app = Flask("server")
CORS(app)  # WARNING: This line will disable CORS


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


@app.get("/api/products/id/<id>")
def get_product_id(id):
    if not ObjectId.is_valid(id):
        return abort(400, "Invalid ID")

    db_id = ObjectId(id)
    product = db.products.find_one({"_id": db_id})
    if not product:
        return abort(404, "ID not found")

    return json.dumps(fix_id(product))


@app.delete("/api/products/id/<id>")
def del_product_id(id):
    if not ObjectId.is_valid(id):
        return abort(400, "Invalid ID")

    db_id = ObjectId(id)
    product = db.products.delete_one({"_id": db_id})
    if not product:
        return abort(404, "ID not found")

    return json.dumps({"status": "Ok"})


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


# creeate POST and GET endpoints to support coupon codes
@app.get("/api/coupons")
def get_coupons():
    results = []
    cursor = db.coupons.find({})
    for coupon in cursor:
        results.append(fix_id(coupon))
    return json.dumps(results)


@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()

    # coupon validation/rules

    # there must be a code
    if not "code" in coupon:
        return abort(400, "Code is required")

    # there must be a discount
    if not "discount" in coupon:
        return abort(400, "Discount is required")

    # the discount cannot be bigger than 35

    db.coupons.insert_one(coupon)
    return json.dumps(fix_id(coupon))


@app.get("/api/coupons/code/<code>")
def get_coupon_code(code):
    coupon = db.coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Coupon not found")

    return json.dumps(fix_id(coupon))

# /api/coupons/id/<id>


@app.get("/api/coupons/id/<id>")
def get_coupon_id(id):
    if not ObjectId.is_valid(id):
        return abort(400, "Invalid ID")

    db_id = ObjectId(id)
    coupon = db.coupons.find_one({"_id": db_id})
    if not coupon:
        return abort(404, "ID not found")

    return json.dumps(fix_id(coupon))


@app.delete("/api/coupons/id/<id>")
def del_coupon_id(id):
    if not ObjectId.is_valid(id):
        return abort(400, "Invalid ID")

    db_id = ObjectId(id)
    product = db.coupons.delete_one({"_id": db_id})
    if not product:
        return abort(404, "ID not found")

    return json.dumps({"status": "Ok"})


# Start the server
app.run(debug=True)
