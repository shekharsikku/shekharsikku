from dotenv import load_dotenv
from os import getenv
from flask import Flask, jsonify, request, make_response, render_template, redirect
from flask_cors import CORS
from flask_pymongo import PyMongo, ObjectId

load_dotenv()

app = Flask(__name__, static_url_path="/static")
app.config["MONGO_URI"] = getenv("MONGODB_URI")
CORS(app, resources={r"/api/*": {"origins": getenv("CORS_ORIGIN")}})

mongo = PyMongo(app)
db = mongo.db.users


def api_response(message: str, code: int, data: any = None):
    if data is not None:
        return make_response(jsonify({"message": message, "data": data}), code)
    return make_response(jsonify({"message": message}), code)


@app.route("/", methods=["GET"])
def greet():
    return render_template("index.html")


@app.route("/api/v1/shekharsikku/portfolio/users", methods=["GET", "POST"])
def portfolio_contacts():
    if request.method == "POST":
        user = request.get_json()

        id = db.insert_one({
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "message": user["message"]
        }).inserted_id

        if id:
            uid = str(ObjectId(id))
            return api_response("Thank You, Your information has been successfully submitted!", 200, uid)
        return api_response("Oops! It seems there was an issue with your submission!", 400)

    elif request.method == "GET":
        users = []

        for user in db.find():
            users.append({
                "_id": str(ObjectId(user["_id"])),
                "name": user["name"],
                "email": user["email"],
                "phone": user["phone"],
                "message": user["message"],
            })
        
        if len(users) > 0:
            return api_response("Contacts fetched successfully!", 200, users)  
        return api_response("No any contact available!", 404)
    
    return api_response("Some went wrong!", 500)


@app.route('/<path:path>')
def catch_all(path):
    return redirect(getenv("DOMAIN_REDIRECT"))
