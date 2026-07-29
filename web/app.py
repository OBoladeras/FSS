from backend import times
from flask import Flask, render_template, jsonify

app = Flask(__name__)
loader = times()


@app.route('/', methods=['GET'])
def index():
    data = {
        "combustion&electric": {
            "name": "Combustion & Electric",
            "times": {
                "endurance": [],
                "acceleration": [],
                "autocross": [],
                "skidpad": []
            }
        },
        "driverless": {
            "name": "Driverless",
            "times": {
                "trackdrive": [],
                "acceleration": [],
                "autocross": [],
                "skidpad": [],
            }
        },
        "classic-cup": {
            "name": "Classic Cup",
            "times": {
                "endurance": [],
                "acceleration": [],
                "autocross": [],
            }
        },
    }

    return render_template('index.html', data=data)


@app.route('/api/results/<cat>/<sub>')
def api_results(cat: str, sub: str):
    try:
        return jsonify({'rows': loader.get_data_from(cat, sub)})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=8082)
