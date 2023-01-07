from pymongo import MongoClient
from flask import Flask,render_template,request
from dotenv import load_dotenv 
import datetime
import os

load_dotenv()

def create_app(): 
    # app created to prevent multiple instances of db client
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.Journal

    @app.route("/", methods=["GET" , "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%b %d %Y at %H:%M")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries = [ (entry["content"],entry["date"]) for entry in app.db.entries.find({})]

        return render_template("home.html", entries=entries[::-1])
    
    return app