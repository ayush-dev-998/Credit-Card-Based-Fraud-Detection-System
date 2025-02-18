from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

# Load the model
model = joblib.load('credit_card_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Map transaction type to numeric value
    type_mapping = {
        "TRANSFER": 1,
        "CASH_OUT": 0,
        "CASH_IN": 2,
        "PAYMENT": 3,
        "DEBIT": 4
    }
    type_value = type_mapping[data['type']]
    
    # Prepare data for prediction
    input_data = [
        data['step'], type_value, data['amount'], data['oldbalanceOrg'],
        data['newbalanceOrig'], data['oldbalanceDest'], data['newbalanceDest'], 
        data['isFlaggedFraud']
    ]
    
    # Make prediction
    y_pred = model.predict([input_data])
    result = 'Fraud Transaction' if y_pred[0] == 1 else 'Normal Transaction'
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
