# BEGIN CODE HERE

from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT

import numpy as np
from numpy.linalg import norm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])

@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get("name")
    print(name)
    list_of_products = []
    doc = mongo.db.products.find({"$text": {"$search": f"\"{name}\""}}).sort("price", -1)
    for x in doc:
        print(x)
        list_of_products.append(x)
    json_list = json.dumps(list_of_products, default=str)
    return json_list

    # END CODE HERE

@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE

    # update if product exists
    new_product = request.json
    exists = mongo.db.products.find_one({"name": new_product["name"]})
    if exists is not None:
        mongo.db.products.update_one({"name": new_product["name"]}, {"$set": {"price": new_product["price"], "size": new_product["size"] ,
                                                                        "production_year": new_product["production_year"], "color": new_product["color"]}})
        return "OK"
    else:
        # insert in Mondo DB - body parameter
        print(new_product)
        mongo.db.products.insert_one(new_product)
        return "OK"
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    new_product = request.json

    num_list1 = []
    for key, value in new_product.items():
        if isinstance(value, (int, float)):
            num_list1.append(value)

    num_arr1 = np.array(num_list1)
    print(num_arr1)
    products = mongo.db.products.find()
    list_of_products = []
    for product in products:
        num_list2 = []
        for key, value in product.items():
            if isinstance(value, (int, float)):
                num_list2.append(value)
        num_arr2 = np.array(num_list2)
        print(num_arr2)
        cosine_similarity = np.dot(num_arr1, num_arr2)/(norm(num_arr1)*norm(num_arr2))
        if cosine_similarity > 0.7:
            list_of_products.append(product)
    json_list = json.dumps(list_of_products, default=str)
    return json_list
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE

    try:
        url = "https://qa.auth.gr/el/x/studyguide/600000438/current"
        options = Options()
        # does not apper as window
        options.headless = True
        # setting a chrome browser
        driver = webdriver.Chrome(options=options)
        # goes to the specified url
        driver.get(url)

        semester = request.args.get('semester')
        print(semester)

        # takes all subjects of the given semester
        element = driver.find_element(By.ID, "exam"+semester)
        elements = element.find_elements(By.TAG_NAME, "a")

        res = []
        for element in elements:
            # takes the text from the paragraph tags
            res.append(element.text)
            print(element.text)

        # Flask response with status code = 200,
        # Note that 200 is the default status code, so it's not necessary to specify that code.
        return jsonify(res), 200
    except Exception as e:
        return "BAD REQUEST", 400

    # END CODE HERE