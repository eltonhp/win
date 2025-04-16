from flask import Flask, jsonify, request
from service.award_service import AwardService
from repository.database_initializer import DatabaseInitializer
import os

app = Flask(__name__)

@app.route('/award-intervals', methods=['POST'])
def award_intervals():
    result = AwardService().get_award_intervals()
    return jsonify(result)

if __name__ == '__main__':
    os.makedirs(os.path.join("src", "banco"), exist_ok=True)
    DatabaseInitializer().initialize()
    app.run(debug=False, port=8081, host='0.0.0.0')
