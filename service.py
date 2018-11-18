# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:40:59 2018

@author: Parashar
"""
from flask import Flask, jsonify,abort,request
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
  host="ofcmikjy9x4lroa2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
  user="oe9mrlsukzgdk6q6",
  passwd="dlfysod5v3tovwy5",
  database='okerpdyoctxwjwf0'
)
'''
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="upadhyay16",
  database='db',
  port="3306"
)
'''

@app.route('/',methods=['GET'])
def getHome():
    return "Please open 'https://aqueou016s.herokuapp.com/ifsc' for accessing IFSC service.\nPlease go to 'https://aqueou016s.herokuapp.com/bankDetails' for accessing bankDetails services"
    
@app.route('/ifsc',methods=['POST'])
def get():
   #'' if not request.json:
     #   abort(400)
    data = request.get_json(force=True)
    ifsc = data['ifsc']
    query = "select * from okerpdyoctxwjwf0.bank_branches where ifsc='ifscCode'"
    query =query.replace('ifscCode', ifsc)
    print(query)  
    mycursor = mydb.cursor()
    mycursor.execute(query)
    r = [dict((mycursor.description[i][0], value)
              for i, value in enumerate(row)) for row in mycursor.fetchall()]
    if len(r)==0:
        return "No data found!Please use bankDetails service to get persisted bank details and then try ifsc.Database has been trimmed on server due to limited space."
    return jsonify(r)

@app.route('/ifsc',methods=['GET'])
def getIfsc():
	return 'GET is not allowed, please use POST method'

@app.route('/bankDetails',methods=['POST'])
def getBank():
   #'' if not request.json:
     #   abort(400)
    data = request.get_json(force=True)
    bank = str(data['bank'])
    city = str(data['city'])
    query = "select * from okerpdyoctxwjwf0.bank_branches where lower(bank_name) like 'bankName%' and lower(city) like 'cityName%'"
    query = query.replace('bankName', bank.lower())
    query = query.replace('cityName', city.lower())
    print(query)  
    mycursor = mydb.cursor()
    mycursor.execute(query)
    r = [dict((mycursor.description[i][0], value)
              for i, value in enumerate(row)) for row in mycursor.fetchall()]
    if len(r)==0:
        return "No data found!Database has been trimmed due to limited space on server"
    return jsonify(r)

@app.route('/bankDetails',methods=['GET'])
def getBankDetails():
	return 'GET is not allowed, please use POST method'
    
if __name__ == '__main__':
    app.run()
