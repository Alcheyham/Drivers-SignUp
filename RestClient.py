import json as j
import urllib.request
import requests
import pprint
import utils.ControlUtils as CU
import utils.InsertUtils as IU
getControl = CU.valueControl()
getInsert = IU.InsertValue()


with open("databases\dynamic\PersonInfo.Json", "r") as users:
    global personData
    personData = j.load(users) 
    
with open("databases\static\Rule.json", "r") as rule:
    global ruleData
    ruleData = j.load(rule) 

control = True
while control:
    choose = input("Bütün kayıtlar için 1 \n"
                   "Seçilmiş şoför bilgileri için 2 \n"   
                   "Ehliyetin tipine ve Sınıfına göre kullanılan araçları listelemek için 3 \n"   
                   "Şoför eklemek için  4 \n"   
                   "Şofor silmek için  5 \n" 
                   "Şoföre ait ehliyet tip ve sınıf güncellemesi için  6 \n"                
                   )
    try:
        if int(choose) == 1:
            # Get data from url and print them.
            resp = requests.get('http://localhost:5000/Drivers_Data')
            for i in (resp.json()["data"]):
                print(i["TCKimlik"], "|" ,i["ad"],"|" , i["ehliyetTipi"],"|" , i["ehliyetSinifi"],"|" , i["kullanabildigiAraclar"] )

        if int(choose) == 2:
            try:
            # We input to TCKimlik what we want and get this data.
                uri = 'http://localhost:5000/api/driver'
                i = input("TC Kimlik numarası giriniz: ")
                res = urllib.request.urlopen(uri + '/' + i)    
                res_body = res.read()
                data = j.loads(res_body.decode("utf-8"))
                for j in range(len(data["data"])):
                    print(data["data"][j])                    
            except urllib.error.URLError as err:
                print('HATA: {}'.format(err.reason))
                
        if int(choose) == 3:
            try:
                # Sometimes we forget the rules, so we have to find what is old what is new;
                # So we can quick query about usable car.
                # This code need just 2 parameters, they are license Type and License Class.
                uri = 'http://localhost:5000/api/rule'
                getInsert.insertUsableCars()
                licType = IU.licenceType
                licClass = IU.licenceClass
                res = urllib.request.urlopen(uri + '/' + licType + '/' + licClass)    
                res_body = res.read()
                data = j.loads(res_body.decode("utf-8"))
                print(data["data"])    
            except urllib.error.URLError as err:
                print('HATA: {}'.format(err.reason))
        if int(choose) == 4:
            try: 
                # We can insert the new drivers.
                tck = getInsert.insertUniqTCK()    
                name = getInsert.insertNS()  
                getInsert.insertUsableCars()
                licType = IU.licenceType
                licClass = IU.licenceClass
                getUsableCar = IU.getUsableCars               
                data ={
                    "TCKimlik": tck,  
                    "ad": name,
                    "ehliyetTipi": licType,
                    "ehliyetSinifi": licClass,
                    "kullanabildigiAraclar": getUsableCar
                }
                resp = requests.post('http://localhost:5000/api/driver/signup', json= data)         
            except urllib.error.URLError as err:
                print('HATA: {}'.format(err.reason))

        if int(choose) == 5:
            try:
                # Delete the drivers.
                delete = input("Silmek istediğiniz kimlik numarasını giriniz:")
                resp = requests.delete('http://localhost:5000/api/driver/delete/'+ delete)   
            except urllib.error.URLError as err:
                print('HATA: {}'.format(err.reason))

        if int(choose) == 6:
            try:
                # Some drivers can ger the new license Class or update old to new;
                # So they need the change their information, this block is for them.
                tck = getInsert.insertTCK()    
                getInsert.insertUsableCars()
                licType = IU.licenceType
                licClass = IU.licenceClass
                getUsableCar = IU.getUsableCars               
                data ={
                    "ehliyetTipi": licType,
                    "ehliyetSinifi": licClass,
                    "kullanabildigiAraclar": getUsableCar
                }
                resp = requests.put('http://localhost:5000/api/driver/update/'+tck, json=data)
                print(resp)
                if (resp.status_code == 200):
                    print('işlem başarılı!')
                    getText = resp.text   
                    updatedData = j.loads(getText)
                    print(updatedData["data"][0])
            except:
                pass
    except:
        pass
