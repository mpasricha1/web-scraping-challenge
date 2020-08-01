from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrap_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017/marsdata_app"
mongo = PyMongo(app,uri=conn)

@app.route("/")
@app.route("/index")
def index():
	marsData = mongo.db.collection.find_one()
	# print(marsData["title"])
	return render_template('index.html', marsData=marsData)

@app.route("/scrape")
def scrape():
	marsData = scrap_mars.scrapeMars()

	mongo.db.collection.update({}, marsData, upsert=True)

	return redirect("/")

if __name__ == "__main__":
	app.run(debug=True)