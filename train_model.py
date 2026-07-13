import pandas as pd

from sklearn.tree import DecisionTreeClassifier

from sklearn.preprocessing import LabelEncoder

import pickle

# Load CSV file
data = pd.read_csv("product_data.csv")

# Convert text to numbers
le_product = LabelEncoder()
le_category = LabelEncoder()
le_city = LabelEncoder()
le_demand = LabelEncoder()

data["Product"] = le_product.fit_transform(data["Product"])
data["Category"] = le_category.fit_transform(data["Category"])
data["City"] = le_city.fit_transform(data["City"])
data["Demand"] = le_demand.fit_transform(data["Demand"])

# Features
X = data[["Product", "Category", "City", "Price", "Rating", "Reviews"]]

# Target
y = data["Demand"]

# Train Model
model = DecisionTreeClassifier()

model.fit(X, y)

# Save Model
pickle.dump(model, open("model.pkl", "wb"))

print("Model Trained Successfully!")