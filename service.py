# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:40:59 2018
"""
from flask import Flask, jsonify,abort,request
import mysql.connector

app = Flask(__name__)

#mysql.connector is used to connect to MySQL database
mydb = mysql.connector.connect(
  host="ofcmikjy9x4lroa2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
  user="oe9mrlsukzgdk6q6",
  passwd="dlfysod5v3tovwy5",
  database='okerpdyoctxwjwf0'
)

@app.route('/',methods=['GET'])
def getHome():
    return "Please open 'https://aqueou016s.herokuapp.com/ifsc' for accessing IFSC service.\nPlease go to 'https://aqueou016s.herokuapp.com/bankDetails' for accessing bankDetails services"
 
#endpoint to get data from database when ifsc code is entered	
@app.route('/ifsc',methods=['POST'])
def get():
   #'' if not request.json:
     #   abort(400)
    #getting request in json format
    data = request.get_json(force=True)
    ifsc = data['ifsc']

    #MySQL query to get data from database
    query = "select * from okerpdyoctxwjwf0.bank_branches where ifsc='ifscCode'"
    query =query.replace('ifscCode', ifsc)
    print(query)  
    mycursor = mydb.cursor()
	
    #executing the query
    mycursor.execute(query)
    r = [dict((mycursor.description[i][0], value)
              for i, value in enumerate(row)) for row in mycursor.fetchall()]

    #returning data in json format if present. If data is not present, then error message is displayed
    if len(r)==0:
        return "No data found!Please use bankDetails service to get persisted bank details and then try ifsc.Database has been trimmed on server due to limited space."
    return jsonify(r)

#displaying error message so that when endpoint is hit in browser, it knows that GET is not supported
@app.route('/ifsc',methods=['GET'])
def getIfsc():
	return 'GET is not allowed, please use POST method'

@app.route('/bankDetails',methods=['POST'])
def getBank():
   #'' if not request.json:
     #   abort(400)
    #getting request in json format
    data = request.get_json(force=True)
    bank = str(data['bank'])
    city = str(data['city'])
	
    #MySQL query to get data from database
    query = "select * from okerpdyoctxwjwf0.bank_branches where lower(bank_name) like 'bankName%' and lower(city) like 'cityName%'"
    query = query.replace('bankName', bank.lower())
    query = query.replace('cityName', city.lower())
    print(query)  

    #executing the query
    mycursor = mydb.cursor()
    mycursor.execute(query)
    r = [dict((mycursor.description[i][0], value)
              for i, value in enumerate(row)) for row in mycursor.fetchall()]

     #returning data in json format if present. If data is not present, then error message is displayed
    if len(r)==0:
        return "No data found!Database has been trimmed due to limited space on server"
    return jsonify(r)

#displaying error message so that when endpoint is hit in browser, it knows that GET is not supported
@app.route('/bankDetails',methods=['GET'])
def getBankDetails():
	return 'GET is not allowed, please use POST method'
    
if __name__ == '__main__':
    app.run()
