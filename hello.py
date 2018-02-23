import numpy as np
#import cPickle as pickle
#import gym
import tensorflow as tf
from tensorflow.python import debug as tf_debug
import os
import io
import collections
import re, string
from gensim.models import Word2Vec
import sys


from flask import Flask
import os
from flask import make_response
import json
from flask import request


app = Flask(__name__)
log_dir = './support'
i = "off"
inputs = ""
word_model = ""
words_embedding = ""
outputs = ""
states = ""
inputs_length = ""

def data_preprocessor(request_str):
    request_str = request_str.strip()
    request_str = request_str.lower()
    request_str = request_str.split(" ")
    return request_str





@app.route("/")
def hello():
    return "Hello World!"

@app.route('/getdetails', methods=['POST'])
def get_details():
    req = request.get_json(silent=True, force=True)
    global i
    global inputs
    global word_model
    global words_embedding
    global outputs
    global states
    global inputs_length
    print("Request:")
    print(json.dumps(req, indent=4))

    
    #targets = tf.placeholder(tf.float32,shape=[None,None,100],name="Targets")
    print ("i=" + str(i))
    
    if i=="off":
        inputs = tf.placeholder(tf.float32,shape=[None,100],name="Inputs")
        inputs_length = tf.placeholder(tf.int32,shape=[None],name="inputs_length")

        with tf.name_scope('DynamicLSTMNetwork'):
             fw_rnn_cell = tf.nn.rnn_cell.LSTMCell(100)
             # generate prediction
             outputs, states = tf.nn.dynamic_rnn(fw_rnn_cell,tf.expand_dims(inputs,0),sequence_length=inputs_length,dtype=tf.float32)
             
        word_model = Word2Vec.load(log_dir+'/model.bin')
        words_embedding = list(word_model.wv.vocab)
        i="on"


    with tf.Session() as sess:
      
        print (inputs)
        saver = tf.train.Saver()
        saver.restore(sess,log_dir+'/answerer.ckpt')
        #query = json.loads(req)

        #print(req)
        #print(req["data"])
        #print(req["data"]["text"])
       
        #sentence = data_preprocessor(req["data"]["text"]) 
        sentence = data_preprocessor(req["data"]["text"]) 
        
        print(sentence)        
        #convert words to their corressponding embeddings
        
        line_with_word_embeddings = [word_model.wv[word] for word in sentence]
        response = ""
        for i in range(0,30):

            result = sess.run(outputs,feed_dict={inputs:line_with_word_embeddings,inputs_length:[len(sentence)]})
            answer =  word_model.wv.similar_by_vector(result[0][2])[0][0]
            line_with_word_embeddings.append(word_model.wv[answer])
            line_with_word_embeddings = line_with_word_embeddings[1:]
            response = response +" "+ answer

        # saver = ""
        # outputs = ""
        # states = ""
    return app.response_class(json.dumps({
        "speech": "speech12312312312",
        "displayText": "displayText",
        "source": "mySource",
        "data": {"slack": 
                   {
                    "text": response
                   }
                },
        "contextOut": [],
        "source": "mysource"
    } , indent=4), content_type='application/json')
 
if __name__ == "__main__":
    #app.run()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
