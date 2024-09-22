from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the model once when the app starts
model_path = r'linear_regression_best_model.pkl'  # Use raw string or double backslashes
model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    try:
        # Extracting the numeric features
        bedrooms = float(data.get('bedrooms'))
        bathrooms = float(data.get('bathrooms'))
        square_feet = float(data.get('square_feet'))
        
        # Handling the categorical feature 'Neighborhood'
        neighborhood = data.get('neighborhood')
        if neighborhood not in ['Neighborhood_Rural', 'Neighborhood_Suburb', 'Neighborhood_Urban']:
            return jsonify({'error': 'Invalid neighborhood. Choose from "Rural", "Suburb", or "Urban".'}), 400

        # One-hot encode the 'Neighborhood' feature
        neighborhood_encoded = [0, 0, 0]  # [Rural, Suburb, Urban]
        if neighborhood == 'Neighborhood_Rural':
            neighborhood_encoded = [1, 0, 0]
        elif neighborhood == 'Neighborhood_Suburb':
            neighborhood_encoded = [0, 1, 0]
        elif neighborhood == 'Neighborhood_Urban':
            neighborhood_encoded = [0, 0, 1]

    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input data. Please provide numeric values and a valid neighborhood.'}), 400

    # Combine numeric and encoded categorical features
    features = np.array([[bedrooms, bathrooms, square_feet] + neighborhood_encoded])  # 2D array

    # Debug: print the features and their shape
    print("Features for prediction:", features)
    print("Features shape:", features.shape)

    # Make prediction using the loaded model
    price_prediction = model.predict(features)

    return jsonify({'predicted_price': price_prediction[0]})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001)
    # app.run(host="0.0.0.0", port=port)


