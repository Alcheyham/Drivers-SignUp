# -*- coding: utf-8 -*
from flask import Flask, jsonify, abort, request, make_response, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import json as j

app = Flask(__name__)
auth = HTTPBasicAuth()

#-------------JSON-LOAD---------------#
# We must define our database for the get all data.
with open("databases\static\Rule.json", encoding='utf-8') as rule:
    ruleData = j.load(rule)
    
with open("databases\dynamic\PersonInfo.json", encoding='utf-8') as users:
    personData = j.load(users)
#-------------JSON-LOAD---------------#
    
# Just for the lazy people.
@app.route('/')
def index():
    return redirect(url_for('ShowData'))

# This code show json data, also it is help for the my datatable.
@app.route('/Drivers_Data', methods=['GET'])
def showDrivers():
    return jsonify({'data': personData})

# This code show json data on datatable.
@app.route('/ShowData')
def ShowData():
  return render_template('showdata.html') 

# This code get License type and License class, the both can show which cars are belong which type and class.
@app.route('/api/rule/<string:licType>/<string:licClass>', methods=['GET'])
def showUsableCar(licType,licClass):
    # We can get this licType and licClass params and put the ruleData where we load json files.
    getUsableCars = ruleData["ehliyetTipi"][licType][licClass]
    if getUsableCars == None:
        return jsonify({'data': 'Not found'}),404
    print(getUsableCars)
    return jsonify({"data": getUsableCars})

# This code get specified driver data, so it's need driver id on url, if id is not found return 404

@app.route('/api/driver/<int:kimlikno>', methods=['GET'])
def showSpecifiedData(kimlikno):
    person = [person for person in personData if person['TCKimlik'] == str(kimlikno)]
    if len(person) == 0:
        return jsonify({'data': 'Not found'}),404
    return jsonify({"data": person})
 
# This code create a new driver. 
@app.route('/api/driver/signup', methods=['POST'])
def createDriver():    
    newPerson = {
        'TCKimlik': request.json['TCKimlik'],
        'ad': request.json['ad'],
        'ehliyetTipi': request.json['ehliyetTipi'],
        'ehliyetSinifi': request.json['ehliyetSinifi'],
        'kullanabildigiAraclar': request.json['kullanabildigiAraclar']
    }   
    
    personData.append(newPerson)  

    # We can update the personInfo.json with this code, i prefer the 4 indent for good looking.
    # We must update this json file, because if server is shotdown We'll gonna lose all data.
    with open('databases\dynamic\PersonInfo.Json',  "w+", encoding='utf-8') as df:
        j.dump(personData, df, indent=4 ,ensure_ascii = False)
    return jsonify({'data': newPerson}), 201

# This code delete specified student, so it's need students id on url, if id is not found return 404.
@app.route('/api/driver/delete/<int:kimlikno>', methods=['DELETE'])
def deleteDriver(kimlikno):
    person = [person for person in personData if person['TCKimlik'] == str(kimlikno)] 
    if len(person) == 0:
        return jsonify({'data': 'Not found'}), 404
    personData.remove(person[0])
    
    # If we want really delete this item, we have to delete also in json file. 
    # If we restart the server it get the old items. 
    with open('databases\dynamic\PersonInfo.Json',  "w+", encoding='utf-8') as df:
        j.dump(personData, df, indent=4 ,ensure_ascii = False)   
    return jsonify({'result': True})

# This code can update specified student, so it's need students id on url.
@app.route('/api/driver/update/<int:kimlikno>', methods=['PUT'])
def updateDriver(kimlikno):
    person = [person for person in personData if person['TCKimlik'] == str(kimlikno)] 
    if len(person) == 0: 
        return jsonify({'data': 'Surucu Yok!'}), 404
    if not request.json: 
        abort(400)

    # We have to control every side of request put, if there is problem it should be response bad request.
    if 'ehliyetTipi' in request.json and type(request.json['ehliyetTipi']) != str:
        abort(400)
    if 'ehliyetSinifi' in request.json and type(request.json['ehliyetSinifi']) != str:
        abort(400)
    if 'kullanabildigiAraclar' in request.json and type(request.json['kullanabildigiAraclar']) != str:
        abort(400)

    # Update data.
    person[0]['ehliyetTipi'] = request.json.get('ehliyetTipi', person[0]['ehliyetTipi'])
    person[0]['ehliyetSinifi'] = request.json.get('ehliyetSinifi', person[0]['ehliyetSinifi'])
    person[0]['kullanabildigiAraclar'] = request.json.get('kullanabildigiAraclar', person[0]['kullanabildigiAraclar'])
    return jsonify({'data': person})


@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'HTTP 404 Error': 'Hata'}), 404)


#I dont need that actually but it can stay there.
@auth.verify_password
def authenticate(username, password):
    if username and password:
        if username == 'admin' and password == 'qwaszx':
            return True
        else:
            return False    
        return False
 
if __name__ == '__main__':
    app.run(debug=True)