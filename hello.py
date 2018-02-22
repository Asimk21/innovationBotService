from flask import Flask

import json
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/getdetails', methods=['POST'])
def get_details():
    return app.response_class(json.dumps({"Print": "Something"}), content_type='application/json')
 
if __name__ == "__main__":
    app.run()
