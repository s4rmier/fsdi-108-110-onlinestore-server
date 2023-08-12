import pymongo
import certifi

me = {
    "name": "Romnick",
    "last_name": "Sarmiento",
    "age": 34,
    "hobbies": ["Gaming", "Movies"],
    "address": {
        "street": "Lago Ventana",
        "city": "Chula Vista",
        "zip": 91914,
    }
}


# database config
con_str = "mongodb+srv://romnick:sdgkufsdi@cluster0.hl6bxb3.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database("urbanbikesco")
