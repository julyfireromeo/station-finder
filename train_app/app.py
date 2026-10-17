from flask import Flask, request, render_template
import logic

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_zip =  request.form.get('zipcode')

        if user_zip:
            lat = logic.zipcodetolat(user_zip)
            lon = logic.zipcodetolon(user_zip)
            town = logic.zipcodetotownish(user_zip)

            nearest_station = logic.stationfinder(lat,lon)

            return render_template('results.html', town_name=town, station_data=nearest_station)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)