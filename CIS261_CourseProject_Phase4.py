import datetime, os

totalValsDict = {}
emp_File = os.path.join("C:\\","Users","Administrator.PLABDC01","Desktop","employees.txt")
user_File = os.path.join("C:\\","Users","Administrator.PLABDC01","Desktop","users.txt")

def addUser (filepath):
    print("###### Create users, passwords, and roles #####")
    f = open(filepath, 'a')
    newUser = True
    while newUser == True :
        user_ID = input("Enter user name or 'End' to quit: ")
        if user_ID.lower() != "end":
            userID = user_ID
            password = input("Enter password: ")
            auth = False
            while auth == False :
                authType = input("Enter Role (Admin or User): ")
                if authType.lower() == "admin": 
                    authCode = authType
                    auth = True
                elif authType.lower() == "user":
                    authCode = authType
                    auth = True
            userInfo = userID+"|"+password+"|"+authCode
            f.write(userInfo + "\n")          
        else:
            newUser = False
    f.close()     
    userList = dispUser(filepath)
    return userList

def dispUser (filepath):
    userList = []
    f = open(filepath, 'r')
    for x in f:
        userList.append(x.strip("\n"))
    for i in userList :
        userDetails = i.split("|")
        user_ID, password, authCode = userDetails[0], userDetails[1], userDetails[2]
        print("User Name: "+user_ID+" Password: "+password+" Role: "+authCode)
    return userList
    
def getDates() :
    fromDate, toDate = "", ""
    fromDate = input("Enter start date (YYYY-MM-DD): ")
    tokens = fromDate.split("-")
    if len(tokens[0]) != 4 or len(tokens[1]) != 2 or len(tokens[2]) != 2:
        fromDate = ""
    else:
        year = int(tokens[0])
        month = int(tokens[1])
        day = int(tokens[2])
        toDate = input("Enter end date (mm/dd/yyyy): ")
        tokens2 = toDate.split("-")
        if len(tokens2[0]) != 4 or len(tokens[1]) != 2 or len(tokens[2]) != 2:
            toDate = ""
        else:
            year2 = int(tokens2[0])
            month2 = int(tokens2[1])
            day2 = int(tokens2[2])
            a = datetime.date(year, month, day)
            b = datetime.date(year2, month2, day2)
            if a > b:
                fromDate = "invalid"
    return fromDate, toDate

def getName () :
    empName = input("Enter Employee name: ")
    return empName

def getHours () :
    hours = input("Enter amount of hours worked: ")
    return hours

def getHourRate () :
    hRate = input("Enter hourly rate: ")
    return hRate

def getTaxRate () :
    tRate = input("Enter tax rate: ")
    return tRate

def calcPayInfo(hours, hRate, tRate) :
    a = float(hours)
    b = float(hRate)
    c = float(tRate)

    grossPay = a * b
    incomeTax =  float(grossPay) * c
    netPay = float(grossPay) - incomeTax
    return grossPay, incomeTax, netPay

def getDate () :
    selectDate = input("Enter start date for report (MM/DD/YYYY) or ALL for all data in file: ")
    if selectDate.lower() == "all":
        selectDate = "all"
    else:
        tokens = selectDate.split("/")
        year = str(tokens[2])
        month = str(tokens[0])
        day = str(tokens[1])
        selectDate =year+"-"+month+"-"+day

    return selectDate

def dispEmp(name, hours, hRate, tRate, tHours, tGrossPay, tNetPay, tIncomeTax) :
    grossPay, incomeTax, netPay = calcPayInfo(hours, hRate, tRate)
    tax = float(tRate)
    print("********************************************************")
    print("Name:  ", name)
    print("Hours Worked:  ", "{:.2f}".format(float(hours)))
    print("Hourly Rate:  ", "{:.2f}".format(float(hRate)))
    print("Gross Pay:  ", "{:.2f}".format(float(grossPay)))
    print("Tax Rate:  ", '{0}%'.format((tax * 100),"%"))
    print("Income Tax:  ", "{:.2f}".format(float(incomeTax)))
    print("Net Pay:  ", "{:.2f}".format(float(netPay)))
    print("********************************************************\n")

    tHours, tGrossPay, tNetPay, tIncomeTax = updateTotals(hours, grossPay, incomeTax, netPay, tHours, tGrossPay, tNetPay, tIncomeTax)
    return tHours, tGrossPay, tNetPay, tIncomeTax, grossPay, incomeTax, netPay

def updateTotals(hours, grossPay, incomeTax, netPay, tHours, tGrossPay, tNetPay, tIncomeTax) :
    tHours += float(hours)
    tGrossPay += float(grossPay)
    tNetPay += float(netPay)
    tIncomeTax += float(incomeTax)
    return tHours, tGrossPay, tNetPay, tIncomeTax

def dispTotals(totalEmps, totalHours, totalGrossPay, totalIncomeTax, totalNetPay) :
        print("\nTotal Number of Employees: ", totalEmps)
        print("Total Hours Worked: ", "{:.2f}".format(totalHours))
        print("Total Gross Pay: ", "{:.2f}".format(totalGrossPay))
        print("Total Income Tax: ", "{:.2f}".format(totalIncomeTax))
        print("Total Net Pay: ", "{:.2f}".format(totalNetPay))

def login(list):
    print("\n##### Data Entry #####")
    userName = input("Enter User Name: ")
    password = input("Enter Password: ")
    found = False
    for x in list:
        cred = x.split("|")
        if userName == cred[0] and password == cred[1]:
            authCode = cred[2]
            found = True
    if found == False:
        print("User does not exist")
        
    return authCode

user_List = addUser(user_File)
authFlag = login(user_List)
keepGoing = True
totalEmps, totalHours, totalGrossPay, totalNetPay, totalIncomeTax= 0, 0, 0, 0, 0

if authFlag.lower() == "admin" :
    while keepGoing == True :
        empName = getName()
        if empName.lower() == "end" :
            keepGoing = False
            selectDate = getDate()
            empList = []
            
            f = open(emp_File, 'r')
            for x in f:
                empList.append(x.strip("\n"))
            if selectDate.lower() == "all" :
                i = 0    
                for i in empList:
                    empDetails = i.split("|")                                
                    totalHours, totalGrossPay, totalNetPay, totalIncomeTax, grossPay, incomeTax, netPay = dispEmp(empDetails[2], empDetails[3], empDetails[4], empDetails[5], totalHours, totalGrossPay, totalNetPay, totalIncomeTax)                
                    totalValsDict = {'hours':totalHours,'GrossPay':totalGrossPay,'NetPay':totalNetPay,'IncomeTax':totalIncomeTax}
                totalEmps = len(empList)
            
                dispTotals(totalEmps,totalValsDict['hours'],totalValsDict['GrossPay'],totalValsDict['NetPay'],totalValsDict['IncomeTax'])            
            else :
                dateEmp = []
                for x in empList:
                    entry = x.split("|")
                    if selectDate == entry[0]:
                        dateEmp.append(x)
                i = 0    
                for i in dateEmp:
                    empDetails = i.split("|")
                              
                    totalHours, totalGrossPay, totalNetPay, totalIncomeTax, grossPay, incomeTax, netPay = dispEmp(empDetails[2], empDetails[3], empDetails[4], empDetails[5], totalHours, totalGrossPay, totalNetPay, totalIncomeTax)                
                    totalValsDict = {'hours':totalHours,'GrossPay':totalGrossPay,'NetPay':totalNetPay,'IncomeTax':totalIncomeTax}
                totalEmps = len(dateEmp)            
                dispTotals(totalEmps,totalValsDict['hours'],totalValsDict['GrossPay'],totalValsDict['NetPay'],totalValsDict['IncomeTax'])        
        else :
            dateLoop = "y"
            err1 = "Invalid date format. Try again."
            err2 = "To date must be after from date. Try again."
            while dateLoop == "y" :
                fromDate, toDate = getDates()
                if fromDate == "" or toDate == "":
                    print(err1 + "\n")
                elif fromDate == "invalid":
                    print(err2 + "\n")
                else:
                    dateLoop = "n"

            hours = getHours()
            hRate = getHourRate()
            tRate = getTaxRate()
        
            empDetails = fromDate+"|"+toDate+"|"+empName+"|"+hours+"|"+hRate+"|"+tRate

            f = open(emp_File, 'a')
            f.write(empDetails + "\n")
            f.close()
elif authFlag.lower() == "user":
    selectDate = getDate()
    empList = []
            
    f = open(emp_File, 'r')
    for x in f:
        empList.append(x.strip("\n"))
    if selectDate.lower() == "all" :
        i = 0    
        for i in empList:
            empDetails = i.split("|")                               
            totalHours, totalGrossPay, totalNetPay, totalIncomeTax, grossPay, incomeTax, netPay = dispEmp(empDetails[2], empDetails[3], empDetails[4], empDetails[5], totalHours, totalGrossPay, totalNetPay, totalIncomeTax)               
            totalValsDict = {'hours':totalHours,'GrossPay':totalGrossPay,'NetPay':totalNetPay,'IncomeTax':totalIncomeTax}
        totalEmps = len(empList)            
        dispTotals(totalEmps,totalValsDict['hours'],totalValsDict['GrossPay'],totalValsDict['NetPay'],totalValsDict['IncomeTax'])
            
    else :
        dateEmp = []
        for x in empList:
            entry = x.split("|")
            if selectDate == entry[0]:
                dateEmp.append(x)
            i = 0    
            for i in dateEmp:
                empDetails = i.split("|")                              
                totalHours, totalGrossPay, totalNetPay, totalIncomeTax, grossPay, incomeTax, netPay = dispEmp(empDetails[2], empDetails[3], empDetails[4], empDetails[5], totalHours, totalGrossPay, totalNetPay, totalIncomeTax)                
                totalValsDict = {'hours':totalHours,'GrossPay':totalGrossPay,'NetPay':totalNetPay,'IncomeTax':totalIncomeTax}
            totalEmps = len(dateEmp)          
            dispTotals(totalEmps,totalValsDict['hours'],totalValsDict['GrossPay'],totalValsDict['NetPay'],totalValsDict['IncomeTax'])
