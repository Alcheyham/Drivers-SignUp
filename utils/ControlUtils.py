import regex as re
import json as j

#------------------------Regex---------------------------#
holdPassedDateReg = "/^([1-9]|[12][0-9]|3[01])(\/?\.?\-?\s?)(0[1-9]|1[12])(\/?\.?\-?\s?)(19[0-9][0-9]|20[0][0-9]|20[1][0-8])$/"
plq = [
r'\b\d{2}.{0,1}[\D\W]{1}.{0,1}\d{4,5}\b',
r'\b\d{2}.{0,1}[\D\W]{2}.{0,1}\d{3,4}\b', 
r'\b\d{2}.{0,1}[\D\W]{3}.{0,1}\d{2,3}\b' ]
tckControl = "^[1-9]{1}[0-9]{9}[0,2,4,6,8]{1}$"
#------------------------Regex---------------------------#
#-------------Variables---------------#
valid_symbols = "!@#$%^&*()/_-+={}[]" 
classListOnlyOne = ["A1","F","G","A"] # There is only one data in them.
typeList = ["Eski","Yeni"] # We need it for the correct input.
# We need to compare to which is "Eski" and "Yeni".
classListOld = ["A1","B","C","D","E","F","G"] 
classListNew = ["A","B1","C1E","D","D1E","F","G"]
licenseType = ""
licenseClass= ""
getCars = ""
#-------------Variables---------------#

#-------------JSON-LOAD---------------#
with open("databases\dynamic\PersonInfo.Json", encoding='utf-8') as users:
    personData = j.load(users) 
    
with open("databases\static\Rule.json", encoding='utf-8') as rule:
    ruleData = j.load(rule) 
#-------------JSON-LOAD---------------#
    
class valueControl:
    
    @staticmethod
    def tcIdUniqControl(x): # This functin is control the duplicate data, this TCKimlik is our PK.
        for i in range(len(personData)):
            if x == personData[i]["TCKimlik"]:
                print("Kimlik Numarası kayıtlı")
                return False
        if re.match(tckControl, x):
            return True
        else:
            print("Kimlik numaranız hatalı.")
            return False
        
    @staticmethod
    def tcIdControl(x):  # This Function is for the update, if input has the personData return true.
        for i in range(len(personData)):
            if x == personData[i]["TCKimlik"]:
                return True
        print("Daha önceden kayıtlı değil")
        return False

    # First fo all we need to input the License type for license class;
    # Because only License type can definiton License class. 
    # For example: License type is "Yeni" and License Class is must be indicate (A,B1,C1E,D,D1E,F,G).
    # For example: License type is "Eski" and License Class is must be indicate (A1,B,C,D,E,F,G).
    @classmethod
    def controlAndInsertLicTypeAndClass(cls): 
        global licenseType, licenseClass
        control = True
        while control:
            licenseType = valueControl.controlLicenseType()
            if licenseType == "Eski":
                licenseClass = valueControl.controlOldLicenseClass()
                control = False
                return licenseClass
            elif licenseType == "Yeni":
                licenseClass = valueControl.controlNewLicenseClass()
                control = False
                return licenseClass

    @classmethod
    def controlLicenseType(cls):
        control = True
        while control:
            liceType = input("Ehliyet Tipi giriniz: ")
            if liceType in typeList:
                return liceType
            else:
                pass
   
    @classmethod 
    def controlOldLicenseClass(cls):
        # This function control old type license.
        control = True
        while control:
            licClass = input("Ehliyet Sınıfı giriniz: ")
            if licClass in classListOld:
                return licClass
            else:
                pass
    
    @classmethod 
    def controlNewLicenseClass(cls):
        # This function control new type license.
        control = True
        while control:
            licClass = input("Ehliyet Sınıfı giriniz: ")
            if licClass in classListNew:
                return licClass
            else:
                pass
            
    # This function find the usable car. 
    # just give it licenseType and licenseClass, it can find it at json file.
    @staticmethod
    def controlUsableCar(x,y):
        getCars = ruleData["ehliyetTipi"][x][y]
        getUsableCar = ""
        text = ""
        
        # If data has just one string, it's become an array;
        # So we have to find what licenseType and Class define one array;
        # And control them then return just one data.
        for i in getCars:
            if licenseClass in classListOnlyOne:
                return getCars
                break
            else:
                text += i + ", "
                
        # We have to save it from unnecessary space and comma.
        getUsableCar = text[0:-2]
        return getUsableCar
    
    @staticmethod
    def nameControl(x):
        # Basic name control.
        nameControlCount = 0 
        for i in range(len(x)):
            for j in range(len(valid_symbols)):
                if x[i].isdigit() or x[i] == valid_symbols[j]:
                    nameControlCount += 1 
        if nameControlCount == 0: 
            return True
        else:
            print("Girişiniz hatalı, lütfen sayı veya sembol kullanmayınız.")
            return False
     