from flask import Flask, jsonify, request

app = Flask(__name__)

countries = []
people = {}

@app.route('/api/<country_name>', methods=['GET', 'POST'])
def api_country(country_name):
    if request.method == 'GET':
        if not country_name in countries:
            return jsonify({"error": "Country " + country_name + " Not Found"}), 400
        return jsonify({"country": country_name})
                       
@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return jsonify({"msg": "Hello, this is a GET request.",
                        "countries_size" : str(len(countries))})
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided."}), 400
        if 'name' in data.keys():
            country_data = data['name']
            if country_data.isalpha() and len(country_data) < 20:
                countries.append(data['name'])
            else:
                return jsonify({"error": "输入的country名不符合规范"}), 400
        return jsonify({"msg": f"Hello, this is a POST request. You sent: {data}"})

@app.route('/people', methods=['GET', 'POST'])
def api_people():
    if request.method == 'GET':
        return jsonify({"msg": "Hello, this is a GET request.",
                        "people" : str(people)})
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided."}), 400
        
        import sys
        if sys.getsizeof(data) > 1000:
            # 太大的不要
            return jsonify({"error": "too big data."}), 400

        # 随机id
        import random
        id = ''.join(str(random.choice(range(10))) for _ in range(10))
        person = {
            "id" : id,
            "data" : data
        }
        people[id] = person

        return jsonify({"msg": f"add person: {person}"})
    
@app.route('/search/<people_id>', methods=['GET'])
def people_search(people_id):
    if request.method == 'GET':
        if not people_id in people.keys():
            return jsonify({"error": "No person found."}), 400
        return jsonify({"msg": f"person: {str(people[people_id])}"})

if __name__ == '__main__':
    app.run(debug=True)