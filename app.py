from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load Dataset
data = pd.read_csv("product_data.csv")

# Label Encoders
le_product = LabelEncoder()
le_category = LabelEncoder()
le_city = LabelEncoder()
le_demand = LabelEncoder()

data["Product"] = le_product.fit_transform(data["Product"])
data["Category"] = le_category.fit_transform(data["Category"])
data["City"] = le_city.fit_transform(data["City"])
data["Demand"] = le_demand.fit_transform(data["Demand"])

# Load Model
model = pickle.load(open("model.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # User Input
    product = request.form["product"]
    category = request.form["category"]
    city = request.form["city"]
    budget = int(request.form["budget"])

    # Profit Calculation
    selling_price = budget * 1.4
    profit_amount = selling_price - budget
    profit_percent = (profit_amount / budget) * 100

    rating = 4.5
    reviews = 1000

    # Encode Input
    product_encoded = le_product.transform([product])[0]
    category_encoded = le_category.transform([category])[0]
    city_encoded = le_city.transform([city])[0]

    # Prediction
    prediction = model.predict([[product_encoded, category_encoded, city_encoded, budget, rating, reviews]])

    demand = le_demand.inverse_transform(prediction)[0]

    # Confidence Score
    try:
        probabilities = model.predict_proba([[product_encoded, category_encoded, city_encoded, budget, rating, reviews]])
        confidence = round(max(probabilities[0]) * 100, 2)
    except:
        confidence = 95

    # Marketplace
    if demand == "High":
        badge_color = "success"
        competition = "Medium"
        marketplace = "Amazon"

    elif demand == "Medium":
        badge_color = "warning"
        competition = "High"
        marketplace = "Flipkart"

    else:
        badge_color = "danger"
        competition = "Low"
        marketplace = "Meesho"

    return render_template(
        "index.html",
        demand=demand,
        competition=competition,
        marketplace=marketplace,
        selling_price=round(selling_price, 2),
        profit_amount=round(profit_amount, 2),
        profit_percent=round(profit_percent, 2),
        badge_color=badge_color,
        confidence=confidence
    )


if __name__ == "__main__":
    app.run(debug=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)