from flask import Flask, render_template, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

API_KEY = 'b5ca0859e1e9d779e741ab93ff817b38'  # Your aviationstack API key

@app.route('/', methods=['GET', 'POST'])
def index():
    flight_info = None
    search_time = None

    if request.method == 'POST':
        flight_number = request.form['flight']
        url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_iata={flight_number}"
        response = requests.get(url)
        data = response.json()
        search_time = datetime.now().strftime("%d %B %Y, %I:%M %p")

        if 'data' in data and len(data['data']) > 0:
            flight = data['data'][0]

            flight_info = {
                'airline': flight['airline']['name'],
                'flight_number': flight['flight']['iata'],
                'status': flight['flight_status'],
                'departure': flight['departure']['airport'],
                'arrival': flight['arrival']['airport'],
                'scheduled_departure': flight['departure']['scheduled'],
                'scheduled_arrival': flight['arrival']['scheduled'],
                'terminal': flight['departure'].get('terminal', 'N/A'),
                'delay': flight['departure'].get('delay', 0)
            }
        else:
            flight_info = {'error': 'Flight not found'}

    return render_template('flight.html', flight=flight_info, time=search_time)

# ✅ Render-compatible run block outside the function
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Use Render's provided port
    app.run(debug=True, host="0.0.0.0", port=port)
