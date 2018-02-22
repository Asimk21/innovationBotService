from flask import Flask
import os

import json
from flask import request
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/getdetails', methods=['POST'])
def get_details():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    return app.response_class(json.dumps(req, indent=4), content_type='application/json')
 
if __name__ == "__main__":
    #app.run()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
