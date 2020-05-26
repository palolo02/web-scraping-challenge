# Paolo Vega
# SQLAlchemy Challenge
# Bootcamp
# Versión 1.0.0 May-24-2020
# Versión 1.0.1 May-24-2020
# Versión 1.0.2 May-24-2020


#################################################
# Import Modules
#################################################

from flask import Flask
from flask import render_template
from flask import redirect
import pymongo
import scrape_mars as sm

#################################################
# DB Connection
#################################################

app = Flask(__name__)

url = f'mongodb://localhost:27017/news_db'

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    print("======================================")
    conn = url
    client = pymongo.MongoClient(conn)
    # Define database and collection
    db = client.news_web
    collection = db.items
    print(collection)
    mars_data = collection.find_one()
    return render_template("index.html", data = mars_data)

@app.route("/scrape")
def scrape():
    # Add Mongo Validation
    sm.scrape_info()
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)