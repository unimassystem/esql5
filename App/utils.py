'''
Created on Apr 19, 2017

@author: qs
'''

from flask import make_response,jsonify



def http_response_nor(message,code=200):
    return make_response(jsonify(message),code)

def http_response_error(message,code=404):
    return make_response(jsonify({"error":{"message":message,"code":code}}),code)


def http_response_succes(message):
    return make_response(jsonify(message))

