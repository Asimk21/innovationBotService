import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/')
def index():
    return {'hello': 'world'}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
@app.route('/getdetails', methods=['POST'])
def create_user():
    # This is the JSON body the user sent in their POST request.
    user_as_json = app.current_request.json_body
    query = user_as_json['query']
    # We'll echo the json body back to the user in a 'user' key.
    displayText="Are you sure you want to know about"+query
    logger.info('Request Came..Yay!!!! %s'%(user_as_json))
    return {'speech': 'This is a sample response from your webhook!', "displayText": displayText}
    #return {'hello': 'world'}
# See the README documentation for more examples.
#

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

app.run(debug=True, port=port, host='0.0.0.0')
