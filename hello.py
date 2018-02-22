from flask import Flask
import os
from flask import make_response
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

    #r = make_response({
    #    "speech": "speech",
    #    "displayText": "displayText",
    #    "source": "mySource"
    #})
    #r = make_response({})
    #r.headers['Content-Type'] = 'application/json'
    #return r

    return app.response_class(json.dumps({
        "speech": "speech12312312312",
        "displayText": "displayText",
        "source": "mySource",
        "data": {},
        "contextOut": [],
        "source": "mysource"
    } , indent=4), content_type='application/json')
 
if __name__ == "__main__":
    #app.run()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
