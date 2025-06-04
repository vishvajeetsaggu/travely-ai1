from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
@app.route('/api/calculate', methods=['POST'])
def calculate_trip():
    data = request.get_json()
    city = data.get('city')
    budget = data.get('budget')
    
    if not city or not budget:
        abort(400, description="Missing city or budget")
    
    # Get destination data (matching your frontend's DESTINATION_AVERAGES)
    destination_data = {
        "Paris": {
            "flight": 600,
            "hotelPerNight": 150,
            "airbnbPerNight": 100,
            "minDays": 1,
            "maxDays": 14
        },
        "Tokyo": {
            "flight": 900,
            "hotelPerNight": 120,
            "airbnbPerNight": 80,
            "minDays": 1,
            "maxDays": 10
        },
        "New York": {
            "flight": 400,
            "hotelPerNight": 200,
            "airbnbPerNight": 120,
            "minDays": 1,
            "maxDays": 10
        }
    }.get(city)
    
    if not destination_data:
        abort(400, description="Invalid city")
    
    # Simple calculation logic
    flight_cost = destination_data['flight']
    daily_cost = destination_data['hotelPerNight']  # Using hotel as default
    suggested_days = min(7, int((budget - flight_cost) / daily_cost))
    min_budget = flight_cost + daily_cost  # Minimum 1 day
    
    return jsonify({
        "city": city,
        "flightCost": flight_cost,
        "dailyLodgingCost": daily_cost,
        "suggestedDays": suggested_days,
        "minBudgetRequired": min_budget
    })