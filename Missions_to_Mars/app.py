from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# init flask pymongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars"
mongo  = PyMongo(app)

# root route ---------------------------------------------------------------------
@app.route("/")
def index():
    mars_data= mongo.db.Info.find_one()
    return render_template("index.html", mars=mars_data)

# scrape route -------------------------------------------------------------------
@app.route("/scrape")   # call scrape function
def scrape_all():

   # reference to Info table, drop if exists 
    Info = mongo.db.Info
    mongo.db.Info.drop()
    
    # call scrape script and insert into Mongo
    mars_data = scrape_mars.scrape_all()
    Info.insert_one(mars_data)
    return redirect("/")

# scrape route -------------------------------------------------------------------
if __name__ == "__main__":
    app.run()