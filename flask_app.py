from flask import Flask, render_template, request, jsonify
from datetime import datetime
import functions

app = Flask(__name__)

priority_list = functions.get_priority_list()
activation_list = functions.get_activation_list()

def update():
    global priority_list, activation_list
    priority_list = functions.get_priority_list()
    activation_list = functions.get_activation_list()


@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', today=today)

@app.route('/get_priorities', methods=['GET', 'POST'])
def get_priorities():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    weekday = data.get('weekday')

    # refresh
    functions.refresh(date, weekday, time)
    return jsonify(priority_list)

@app.route('/get_activations', methods=['GET'])
def get_activations():
    return jsonify(activation_list)

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify(functions.get_history())

@app.route('/save_activations', methods=['POST'])
def save_activations():
    data = request.get_json()
    selected_buttons = data.get('selected', [])

    # 저장
    functions.save_activation(selected_buttons)
    update()

    return jsonify({'status': 'success'})

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    selected_buttons = data.get('selected', [])
    date = data.get('date')
    time = data.get('time')
    weekday = data.get('weekday')

    if len(selected_buttons) > 2:
        return jsonify({'status': 'too_much'})

    # 저장
    functions.save_implementer(selected_buttons)
    functions.write_historyfile(selected_buttons, date, weekday, time)
    update()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
