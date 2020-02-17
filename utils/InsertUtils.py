import utils.ControlUtils as CU 
valueControl = CU.valueControl
licenceType = ""
licenceClass = ""
getUsableCars = ""

class InsertValue:  
    
    @classmethod
    def insertUniqTCK(cls): #  insert method for TCKimlik, this is must be a PK.
        control = True
        while control: 
            tck = input("TC kimlik numarasını giriniz: ") 
            if valueControl.tcIdUniqControl(tck): # We validate data this side. 
                control = False
                return tck
            else:
                control = True      
        
    @classmethod
    def insertTCK(cls): # This block is need for the update, input must be merge with database.
        control = True
        while control: 
            tck = input("TC kimlik numarasını giriniz: ") 
            if valueControl.tcIdControl(tck): 
                control = False
                return tck
            else:
                control = True  
    
    @classmethod
    def insertUsableCars(cls):
        # This function is insert from ControlSide, because we have to control; ->
        # -> a lot things, and i dont want to do this at this file.
        # This function is get the usable cars, license Type and class define it.
        global licenceType, licenceClass, getUsableCars
        valueControl.controlAndInsertLicTypeAndClass()
        licenceType = CU.licenseType     
        licenceClass = CU.licenseClass     
        getUsableCars = valueControl.controlUsableCar(licenceType,licenceClass)    
    
    @classmethod
    def insertNS(cls): 
        # Basic name and surname control.
        control = True
        while control:
            print("İsim giriniz:  ")
            name = input().capitalize() 
            if valueControl.nameControl(name):
                return name
            else:
                print("Boş değer girmeyiniz.")
                                                     
   