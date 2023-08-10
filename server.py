from flask import Flask
from config import me
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
    all_cats = ["Trek", "Fuel", "Specialized", "Sale"]
    return json.dumps(all_cats)


# Start the server
app.run(debug=True)
