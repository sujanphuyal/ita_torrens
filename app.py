from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import pandas as pd

# Load the trained model
model = tf.keras.models.load_model("nids_model.keras")

# Initialize Flask app
app = Flask(__name__)

# Define attack categories
attack_categories = {
    0: "Normal",
    1: "DoS Attack",
    2: "Probe Attack",
    3: "Privilege Escalation",
    4: "Remote Access Attack"
}

@app.route("/")
def home():
    return "Intrusion Detection System (IDS) API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data
        data = request.get_json()

        # Convert data to numpy array
        features = np.array(data["features"]).reshape(1, -1, 1)  # Reshape for model

        # Make a prediction
        prediction = model.predict(features)
        predicted_class = np.argmax(prediction)  # Get highest probability class

        # Return the result
        response = {
            "predicted_class": int(predicted_class),
            "attack_type": attack_categories[predicted_class],
            "confidence": float(np.max(prediction))
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
