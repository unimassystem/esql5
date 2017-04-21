'''
Created on Apr 19, 2017

@author: qs
'''

from flask import make_response,jsonify


def response_error(message,code=400):
    return make_response(jsonify({"error":{"message":message,"code":code}}),404)


def response_succes(message):
    return make_response(jsonify(message))

