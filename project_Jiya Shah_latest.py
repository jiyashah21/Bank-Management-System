#BANK MANAGEMENT SYSTEM
import pymysql as sql
conn=sql.connect(host='localhost',user='root',passwd='', db='project')
cur=conn.cursor()
def check_conn():
    f=sql.connect(host='localhost',user='root',passwd='')
    if f:
        print("connected to SQL")
    else:
        print("error connecting to SQL")
        
def mainmenu():
    while True:
        print("\t\t\t HFDC BANK")
        print()
        print("\t1. Existing user")
        print("\t2. New User? Create an account.")
        print("\t3. Exit")
        ch=int(input("Enter your choice:"))
        if ch==1:
            print("---------------------------------------------------------------------------")
            login()
        elif ch==2:
            print("---------------------------------------------------------------------------")
            newacc()
        elif ch==3:
            break
def newacc():
    global cur
    global conn
    print("Enter the account holder details:")
    name=input("NAME:")
    age=input("AGE:")
    if age.isnumeric():
        age=int(age)
    else:
        while age.isnumeric()==False:
          print("Enter a valid input value")
          age=input("AGE:")
        age=int(age)          
            
    address=input("ADDRESS:")
    phone=input("PHONE NUMBER:")
    while len(phone)!=10 or phone.isnumeric()==False:
            print("Invalid input. Your phone number must contain 10 digits only.")
            print("Try again")
            phone=input("PHONE NUMBER:")    
    phone=int(phone)       
    gender=input('GENDER(M/F/OTHER):')
    gender=gender.lower()
    while gender not in ['m','f','other']:
        print("Enter a valid input")
        gender=input('GENDER(M/F/OTHER):')
        gender=gender.lower()
    nationality=input('NATIONALITY:')
    nationality=nationality.lower()
    print("TYPE OF ACCOUNT")
    print('\t1.SAVINGS (s)')
    print('\t2.PPF (p)')
    print('\t3.NRI (n)')
    print('\t4.JOINT (j)')
    typeofacc=input("\tEnter your choice (s/p/n/j):")
    
    while typeofacc not in 'spnj':
        print("Enter a valid input")
        print("TYPE OF ACCOUNT")
        print('\t1.SAVINGS (s)')
        print('\t2.PPF (p)')
        print('\t3.NRI (n)')
        print('\t4.JOINT (j)')
        typeofacc=input("\tEnter your choice (s/p/n/j):")        
        
    if typeofacc=="j":
        print("Enter details of the joint holder:")
        jname=input("NAME:")
        jage=input("AGE:")
        if jage.isnumeric():
            jage=int(jage)
        else:
            while jage.isnumeric()==False:
              print("Enter a valid input value")
              jage=input("AGE:")
        jage=int(jage)  
        jaddress=input("ADDRESS:")
        jphone=input("PHONE NUMBER:")
        while len(jphone)!=10 or jphone.isnumeric()==False:
            print("Invalid input. Your phone number must contain 10 digits only.")
            print("Try again")
            jphone=input("PHONE NUMBER:")
        jphone=int(jphone)       
        jgender=input('GENDER(M/F/OTHER):')
        jgender=jgender.lower()
        while jgender not in ['m','f','other']:
            print("Enter a valid input")
            jgender=input('GENDER(M/F/OTHER):')
            jgender=jgender.lower()
        jnationality=input('NATIONALITY:')
        jnationality=jnationality.lower()

    if age<18:
        print ("The account holder is a minor.")
        print("Details of guardian required")
        gname= input("Enter guardian's name:")
        gage=input("Enter guardian's age:")
        if gage.isnumeric():
            gage=int(gage)
        else:
            while gage.isnumeric()==False:
              print("Enter a valid input value")
              gage=input("Enter guardian's age:")
        gage=int(gage)  
        gaddress= input("Enter guardian's address:")
        gphone=input("Enter guardian's phone number:")
        while len(gphone)!=10 or gphone.isnumeric()==False:
            print("Invalid input. Your phone number must contain 10 digits only.")
            print("Try again")
            gphone=input("Enter guardian's phone number:")
        gphone=int(gphone)       
        ggender=input("Guardian's gender(M/F/OTHER):")
        ggender=ggender.lower()
        while ggender not in ['m','f','other']:
            print("Enter a valid input")
            ggender=input("Guardian's gender(M/F/OTHER):")
            ggender=ggender.lower()
        gnationality=input("Enter guardian's nationality:")
        gnationality=gnationality.lower()
        grelationwithmain= input("How is the guardian related to the account holder?")
        print("ACCOUNT CREATED SUCCESSFULLY!!")
    else:
        print("ACCOUNT CREATED SUCCESSFULLY!!")
    
    
    cur.execute('create table if not exists accdetails(ACCNO bigint primary key, NAME varchar(20), AGE int, ADDRESS varchar(80), PHONENUM bigint, GENDER varchar(5), NATIONALITY varchar(20), TYPEOFACC varchar(1))')
    
    accno=''
    import random as r
    for i in range(10):
        q=r.randint(0,9)
        accno+=str(q)
    cur.execute('select ACCNO from accdetails')
    listofaccno=cur.fetchall()
    while accno in listofaccno and accno[0]=='0':
        for i in range(10):
            q=r.randint(0,9)
            accno+=str(q)
    accno=int(accno)
    print("Your account number is:",accno)
    newentry="insert into accdetails values(%s,'%s',%s,'%s',%s,'%s','%s','%s')"%(accno,name,age,address,phone,gender,nationality,typeofacc)
    cur.execute(newentry)
    if typeofacc=='j':
        cur.execute('create table if not exists jointholder(ACCNO bigint primary key, NAME varchar(20), AGE int, ADDRESS varchar(80), PHONENUM bigint, GENDER varchar(5), NATIONALITY varchar(20))')
        newentry="insert into jointholder values(%s,'%s',%s,'%s',%s,'%s','%s')"%(accno,jname,jage,jaddress,jphone,jgender,jnationality)
        cur.execute(newentry)

    if age<18:
        cur.execute('create table if not exists guardian(ACCNO bigint primary key, NAME varchar(20), AGE int, ADDRESS varchar(80), PHONENUM bigint, GENDER varchar(5), NATIONALITY varchar(20), RELATION varchar(20))')
        newentry="insert into guardian values(%s,'%s',%s,'%s',%s,'%s','%s','%s')"%(accno,gname,gage,gaddress,gphone,ggender,gnationality,grelationwithmain)
        cur.execute(newentry)
    bal=0
    cur.execute('create table if not exists balance(ACCNO bigint primary key, BALANCE float default 0.00)')
    newentry="insert into balance values(%s,%s)"%(accno,bal)
    cur.execute(newentry)

    #taking login details from customer:
    print()
    print("FOR FIRST TIME USERS: IF YOU HAVE OPENED AN ACCOUNT IN THIS BANK FOR THE FIRST TIME, THEN YOU WON'T HAVE AN EXISTING USERNAME, SO PLEASE ENETR \"NO\" IN THE FIELD BELOW AND CREATE YOUR USERNAME")
    a=input("Do you have an existing username in this bank?(Yes/No)")
    a=a.lower()
    if a not in ['yes','no']:
        while a not in ['yes','no']:
            print("Enter a valid input")
            a=input("Do you have an existing username in this bank?(Yes/No)")
            a=a.lower()
    if a=='yes':
        a1=input("Do you wish to add the above account to the same username?(Yes/No)")
        if a1.lower() not in ['yes','no']:
            while a1.lower() not in ['yes','no']:
                print("Enter a valid input")
                a1=input("Do you wish to add the above account to the same username?(Yes/No)")
        if a1.lower()=='yes':
            uname=input("Enter your username:")
            cur.execute("select UNAME,PASSWD from logindetails")
            x=cur.fetchall()
            d={}
            for i in range(len(x)):
                u=x[i][0]
                p=x[i][1]
                d[u]=p
            if uname in d.keys():
                pass
            else:
                while uname not in d.keys():
                    print("This username does not exist")
                    print("Try again")
                    uname=input("Enter your username:")
            pw=input("Enter your password:")
            if d[uname]==pw:
                newentry="insert into logindetails values(%s, '%s','%s')"%(accno,uname,pw)
                cur.execute(newentry)
                print("Login details verified and account added to the same username!!")    
            else:
                while pw!=d[uname]:
                    print("Incorrect password")
                    print("Try again")
                    pw=input("Enter your password:")
        elif a1.lower()=='no':
            uname=input("Create your username:")
            pw=input("Enter password (must contain atleast 8 characters and atmost 30 characters - combination of numbers as well as characters):")
            while len(pw)<8:
                print("The password should contain atleast 8 characters!!!")
                pw=input("Enter password (must contain atleast 8 characters - combination of numbers as well as characters):")
            print("LOGIN CREATED SUCCESSFULLY!!")
            bal=0
            cur.execute('create table if not exists logindetails(ACCNO bigint primary key, UNAME varchar(20), PASSWD varchar(30))')
            newentry="insert into logindetails values(%s, '%s','%s')"%(accno,uname,pw)
            cur.execute(newentry)
            
    elif a=='no':
        cur.execute('create table if not exists logindetails(ACCNO bigint primary key, UNAME varchar(20), PASSWD varchar(30))')
        uname=input("Create your username:")
        cur.execute("select UNAME,PASSWD from logindetails")
        x=cur.fetchall()
        d={}
        for i in range(len(x)):
            u=x[i][0]
            p=x[i][1]
            d[u]=p
        while uname in d.keys():
            print("This username already exits. Please create a new username")
        pw=input("Enter password (must contain atleast 8 characters and atmost 30 characters - combination of numbers as well as characters):")
        while len(pw)<8:
            print("The password should contain atleast 8 characters!!!")
            pw=input("Enter password (must contain atleast 8 characters - combination of numbers as well as characters):")
        print("LOGIN CREATED SUCCESSFULLY!!")
        newentry="insert into logindetails values(%s, '%s','%s')"%(accno,uname,pw)
        cur.execute(newentry)    
    conn.commit()

def login():
    print()
    global cur
    global conn
    cur.execute("select UNAME,PASSWD from logindetails")
    x=cur.fetchall()
    d={}
    for i in range(len(x)):
        u=x[i][0]
        p=x[i][1]
        d[u]=p
    print("\t\t\t LOGIN PAGE")
    uname=input("Enter your username:")
    if uname in d.keys():
        pw=input("Enter your password:")
        
    else:
        t=1
        while uname not in d.keys() and t!=3:
            print("This username does not exist")
            print("Try again")
            uname=input("Enter your username:")
            t+=1
        if uname in d.keys():
            pw=input("Enter your password:")
        else:
            print("You have exceeded the maximum number of tries to enter correct username!!!")
            print("Redirecting to mainmenu...")
            print()
            mainmenu()

    if d[uname]==pw:
        print("Logged in successfully!!")
        submenu(uname)
    else:
        t=1
        while d[uname]!=pw and t!=3:
            print("Incorrect password")
            print("Try again")
            pw=input("Enter your password:")
            t+=1
        if d[uname]==pw:
            print("Logged in successfully!!")
            submenu(uname)
        else:
            print("You have exceeded the maximum number of tries to enter correct password!!!")
            print("Redirecting to login page...")
            print()
            login()
    
    
def submenu(uname):
  
    while True:
        print()
        print("\t\t\t YOUR ACCOUNT")
        print("\t1. Withdraw money")
        print("\t2. Deposit money")
        print("\t3. Check Balance")
        print("\t4. Transfer to another account in this bank")
        print("\t5. Check details of accounts linked to your username")
        print("\t6. Apply for loan/FD")
        print("\t7. Update details")
        print("\t8. Check interest rates")
        print("\t9. Close account")
        print("\t10. Back to main menu")
        c=int(input("Enter your choice:"))
        if c==1:
            withdraw(uname)
        elif c==2:
            deposit(uname)
        elif c==3:
            checkbal(uname)
        elif c==4:
            neft(uname)
        elif c==5:
            checkdetails(uname)
        elif c==6:
            options(uname)
        elif c==7:
            updatedetails(uname)
        elif c==8:
            checkinterest()
        elif c==9:
            closeacc(uname)
            break
            mainemnu()
        elif c==10:
            break
            mainmenu()
        

def withdraw(uname):
    print()    
    global cur
    global conn
    
    s="select l.ACCNO,BALANCE from balance b,logindetails l where b.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    print("You have the following accounts linked to your username:")
    d={}
    for i in range(len(x)):
        acc=x[i][0]
        bal=x[i][1]
        d[acc]=bal
        print(i+1,'. ', acc)
    acc=int(input("Enter the account number from the above list you want to withdraw money from:"))
    if acc in d.keys():
        balance=d[acc]
        wamt=int(input("Enter amount to be withdrawn:"))
        if d[acc]>=wamt:
            balance=balance-wamt
            print("Amount withdrawn successfully!!")
            print("Balance after transaction: Rs.",balance)
            s="Update balance set BALANCE=%s where ACCNO=%s"%(balance,acc)
            cur.execute(s)
            conn.commit()
            submenu(uname)
        else:
            print("Please check your balance and try again.")
            submenu(uname)
    else:
        print("This account number does not exist")
        print("Try again")
        withdraw(uname)
    
    conn.commit()
    
def deposit(uname):
    print()
    global cur
    global conn
    s="select l.ACCNO,BALANCE from balance b,logindetails l where b.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    print("You have the following accounts linked to your username:")
    d={}
    for i in range(len(x)):
        acc=x[i][0]
        bal=x[i][1]
        d[acc]=bal
        print(i+1,'. ', acc)
    acc=int(input("Enter the account number from the above list you want to deposit money to:"))
    if acc in d.keys():
        balance=d[acc]
        damt=int(input("Enter amount to be deposited:"))
        balance=balance+damt
        print("Amount deposited successfully!!")
        print("Balance after transaction: Rs.",balance)
        s="Update balance set BALANCE=%s where ACCNO=%s"%(balance,acc)
        cur.execute(s)
        conn.commit()
        submenu(uname)
        
    else:
        print("This account number does not exist")
        print("Try again")
        deposit(uname)
    
    conn.commit()
    
def checkdetails(uname):
    print()
    global conn
    global cur
    s="select a.ACCNO,NAME,AGE,ADDRESS,PHONENUM,GENDER,NATIONALITY,TYPEOFACC from accdetails a,logindetails l where a.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    print("You have the following accounts linked to your username:")
    d={}
    for i in range(len(x)):
        acc=x[i][0]
        details=[]
        for j in range(1,len(x[i])):
            details.append(x[i][j])
        d[acc]=details
        print(i+1,'. ', acc)
    acc=int(input("Enter the account number from the above list you wish to check details for:"))
    if acc in d.keys():
        print("The details for account number ", acc," are as follows:")
        print("\tNAME OF ACCOUNT HOLDER:",d[acc][0])
        print("\tAGE OF ACCOUNT HOLDER:",d[acc][1])
        print("\tADDRESS OF ACCOUNT HOLDER:",d[acc][2])
        print("\tPHONE NUMBER OF ACCOUNT HOLDER:",d[acc][3])
        print("\tGENDER OF ACCOUNT HOLDER:",d[acc][4])
        print("\tNATIONALITY OF ACCOUNT HOLDER:",d[acc][5])
        if d[acc][6]=='s':
            d[acc][6]='SAVINGS'
        elif d[acc][6]=='p':
            d[acc][6]='PPF'
        elif d[acc][6]=='n':
            d[acc][6]='NRI'
        elif d[acc][6]=='j':
            d[acc][6]='JOINT'
        print("\tTYPE OF ACCOUNT:",d[acc][6])

        if d[acc][6]=='JOINT':
            print()
            print("\tThis is a joint account")
            print("\tThe joint holder details are as follows:")
            s="select j.ACCNO,NAME,AGE,ADDRESS,PHONENUM,GENDER,NATIONALITY from jointholder j,logindetails l where j.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
            cur.execute(s)
            x=cur.fetchall()
            for i in x:
               print("\tNAME OF JOINT HOLDER:",i[1])
               print("\tAGE OF JOINT HOLDER:",i[2])
               print("\tADDRESS OF JOINT HOLDER:",i[3])
               print("\tPHONE NUMBER OF JOINT HOLDER:",i[4])
               print("\tGENDER OF JOINT HOLDER:",i[5])
               print("\tNATIONALITY OF JOINT HOLDER:",i[6])
        if d[acc][1]<18:
            print()
            print("\tThe primary holder of this account is a minor.")
            print("\tThe guardian details are as follows:")
            s="select g.ACCNO,NAME,AGE,ADDRESS,PHONENUM,GENDER,NATIONALITY,RELATION from guardian g,logindetails l where g.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
            cur.execute(s)
            x=cur.fetchall()
            for i in x:
               print("\tNAME OF GUARDIAN:",i[1])
               print("\tAGE OF GUARDIAN:",i[2])
               print("\tADDRESS OF GUARDIAN:",i[3])
               print("\tPHONE NUMBER OF GUARDIAN:",i[4])
               print("\tGENDER OF GUARDIAN:",i[5])
               print("\tNATIONALITY OF GUARDIAN:",i[6])
               print("\tRELATION OF GUARDIAN WITH PRIMARY ACCOUNT HOLDER:",i[7])
    else:
        print("This account number does not exist")
        print("Try again")
        checkdetails(uname)
    
    cont=input("Do you wish to view details for any other account?(yes/no):")
    cont=cont.lower()
    if cont not in ['yes','no']:
        while cont not in ['yes','no']:
            print("Enter a valid input")
            cont=input("Do you wish to view details for any other account?(yes/no):")
            cont=cont.lower()
    elif cont=="yes":
        checkdetails(uname)
    elif cont=="no":
        submenu(uname)


    
        
def checkbal(uname):
    print()
    global conn
    global cur
    s="select l.ACCNO,BALANCE from balance b,logindetails l where b.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    print("You have the following accounts linked to your username:")
    d={}
    for i in range(len(x)):
        acc=x[i][0]
        bal=x[i][1]
        d[acc]=bal
        print(i+1,'. ', acc)
        
    acc=int(input("Enter the account number from the above list you wish to check balance for:"))
    if acc in d.keys():
        print("Account balance: Rs.",d[acc])
    else:
        print("This account number does not exist")
        print("Try again")
        checkbal(uname)
    cont=input("Do you wish to check balance for any other account?(yes/no):")
    cont=cont.lower()
    if cont not in ['yes','no']:
        while cont not in ['yes','no']:
            print("Enter a valid input")
            cont=input("Do you wish to view details for any other account?(Yes/No)")
            cont=cont.lower()
    elif cont=="yes":
        checkbal(uname)
    elif cont=="no":
        submenu(uname)

def neft(uname):
    print()
    global conn
    global cur
    s="select l.ACCNO,BALANCE from balance b,logindetails l where b.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    s="select ACCNO,BALANCE from balance"
    cur.execute(s)
    allacc=cur.fetchall()
    d1={}
    for i in range(len(allacc)):
        acc=allacc[i][0]
        bal=allacc[i][1]
        d1[acc]=bal
    print(d1)
    print("You have the following accounts linked to your username:")
    d={}
    for i in range(len(x)):
        acc=x[i][0]
        bal=x[i][1]
        d[acc]=bal
        print(i+1,'. ', acc)
        
    acc=int(input("Enter the account number from the above list you wish to transfer funds from:"))
    if acc in d.keys():
        print("Account balance: Rs.",d[acc])
        credit=int(input("Enter the 10-digit account number of the receiver you wish to transfer funds to:"))
        if credit in d1:
            transfer=int(input("Enter amount you want to transfer: Rs."))
            if transfer>d[acc]:
                print("Transaction failed:(")
                print("Please check your balance and try again.")
                submenu(uname)
            else:
                d1[credit]+=transfer
                d1[acc]=d1[acc]-transfer
                d[acc]=d[acc]-transfer
                print(d)
                print(d1)
                s="update balance set BALANCE=%s where ACCNO=%s"%(d1[credit],credit)
                cur.execute(s)
                s="update balance set BALANCE=%s where ACCNO=%s"%(d1[acc],acc)
                cur.execute(s)
                conn.commit()
                print("Transaction successful")
                print("Rs.",transfer," has been debited from your account no.", acc ,"and transferred to account no.", credit)
        else:
            print("This account number does not exist")
            print("Try again")
            neft(uname)
                       
    else:
        print("This account number does not exist")
        print("Try again")
        neft(uname)
    conn.commit()
def checkdetailsforupd(uname,acc):
    print()
    global conn
    global cur
    s="select a.ACCNO,NAME,AGE,ADDRESS,PHONENUM,GENDER,NATIONALITY,TYPEOFACC from accdetails a,logindetails l where a.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    print("You have the following accounts linked to your username:")
    d={}
    for i in range(len(x)):
        accno=x[i][0]
        details=[]
        for j in range(1,len(x[i])):
            details.append(x[i][j])
        d[accno]=details
    if acc in d.keys():
        print("The details for account number ", acc," are as follows:")
        print("\tNAME OF ACCOUNT HOLDER:",d[acc][0])
        print("\tAGE OF ACCOUNT HOLDER:",d[acc][1])
        print("\tADDRESS OF ACCOUNT HOLDER:",d[acc][2])
        print("\tPHONE NUMBER OF ACCOUNT HOLDER:",d[acc][3])
        print("\tGENDER OF ACCOUNT HOLDER:",d[acc][4])
        print("\tNATIONALITY OF ACCOUNT HOLDER:",d[acc][5])
        if d[acc][6]=='s':
            d[acc][6]='SAVINGS'
        elif d[acc][6]=='p':
            d[acc][6]='PPF'
        elif d[acc][6]=='n':
            d[acc][6]='NRI'
        elif d[acc][6]=='j':
            d[acc][6]='JOINT'
        print("\tTYPE OF ACCOUNT:",d[acc][6])

        if d[acc][6]=='JOINT':
            print()
            print("\tThis is a joint account")
            print("\tThe joint holder details are as follows:")
            s="select j.ACCNO,NAME,AGE,ADDRESS,PHONENUM,GENDER,NATIONALITY from jointholder j,logindetails l where j.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
            cur.execute(s)
            x=cur.fetchall()
            for i in x:
               print("\tNAME OF JOINT HOLDER:",i[0])
               print("\tAGE OF JOINT HOLDER:",i[1])
               print("\tADDRESS OF JOINT HOLDER:",i[2])
               print("\tPHONE NUMBER OF JOINT HOLDER:",i[3])
               print("\tGENDER OF JOINT HOLDER:",i[4])
               print("\tNATIONALITY OF JOINT HOLDER:",i[5])
        if d[acc][1]<18:
            print()
            print("\tThe primary holder of this account is a minor.")
            print("\tThe guardian details are as follows:")
            s="select g.ACCNO,NAME,AGE,ADDRESS,PHONENUM,GENDER,NATIONALITY,RELATION from guardian g,logindetails l where g.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
            cur.execute(s)
            x=cur.fetchall()
            for i in x:
               print("\tNAME OF GUARDIAN:",i[1])
               print("\tAGE OF GUARDIAN:",i[2])
               print("\tADDRESS OF GUARDIAN:",i[3])
               print("\tPHONE NUMBER OF GUARDIAN:",i[4])
               print("\tGENDER OF GUARDIAN:",i[5])
               print("\tNATIONALITY OF GUARDIAN:",i[6])
               print("\tRELATION OF GUARDIAN WITH PRIMARY ACCOUNT HOLDER:",i[7])
    else:
        print("This account number does not exist")
        print("Try again")
        updatedetails(uname)
    
    
    
def updatedetails(uname):
    print()
    global conn
    global cur
    s="select a.ACCNO,NAME,AGE,ADDRESS,PHONENUM,GENDER,NATIONALITY,TYPEOFACC from accdetails a,logindetails l where a.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    print("You have the following accounts linked to your username:")
    d={}
    for i in range(len(x)):
        acc=x[i][0]
        details=[]
        for j in range(1,len(x[i])):
            details.append(x[i][j])
        d[acc]=details
        print(i+1,'. ', acc)
    acc=int(input("Enter the account number from the above list you wish to update details for:"))
    if acc in d.keys():
        e=input("Do you wish to view the existing account details before updating?(yes/no):")
        e=e.lower()
        if e not in ['yes','no']:
            while e not in ['yes','no']:
                print("Enter a valid input")
                e=input("Do you wish to view the existing account details before updating?(yes/no):")
                e=e.lower()
        elif e=="yes":
            checkdetailsforupd(uname,acc)
        elif e=="no":
            pass
        updmenu(d,'accdetails',acc)
        
    conn.commit()
    
def updmenu(d,table,acc):
    print("The following fields are updatable for this account:")
    print("\tF.no. Field")
    print("\t1. NAME")
    print("\t2. AGE")
    print("\t3. ADDRESS")
    print("\t4. PHONE NUMBER")
    print("\t5. GENDER")
    print("\t6. NATIONALITY")
    if d[acc][1]<18:
        print("\t7. GUARDIAN DETAILS")
    if d[acc][6]=='j':
        print("\t8. JOINT HOLDER DETAILS")
    c=int(input("Enter the field number of the field you want to update:"))
    if c==1:
        updname=input("Enter the new value you wish to set for this field:")
        s="update "+ table+ " set NAME='%s' where ACCNO=%s"%(updname,acc)
        cur.execute(s)
        print("Value updated successfully!!!")
        
    elif c==2:
        newage=input("Enter the new value you wish to set for this field:")
        if newage.isnumeric():
            newage=int(newage)
        else:
            while newage.isnumeric()==False:
                print("Enter a valid input value")
                newage=input("Enter the new value you wish to set for this field:")
            newage=int(newage)
        s="update "+table+" set AGE=%s where ACCNO=%s"%(newage,acc)
        cur.execute(s)
        print("Value updated successfully!!!")
            
    elif c==3:
        updaddr=input("Enter the new value you wish to set for this field:")
        s="update "+table+" set ADDRESS='%s' where ACCNO=%s"%(updaddr,acc)
        cur.execute(s)
        print("Value updated successfully!!!")
            
    elif c==4:
        nphone=input("Enter the new value you wish to set for this field:")
        while len(nphone)!=10 or nphone.isnumeric()==False:
            print("Invalid input. Your phone number must contain 10 digits only.")
            print("Try again")
            nphone=input("Enter the new value you wish to set for this field:")
        nphone=int(nphone)
        s="update "+table+" set PHONENUM=%s where ACCNO=%s"%(nphone,acc)
        cur.execute(s)
        print("Value updated successfully!!!")
            
    elif c==5:
        ngender=input("Enter the new value you wish to set for this field(M/F/OTHER):")
        ngender=ngender.lower()
        while ngender not in ['m','f','other']:
            print("Enter a valid input")
            ngender=input('Enter the new value you wish to set for this field(M/F/OTHER):')
            ngender=ngender.lower()
        s="update "+table+ " set GENDER='%s' where ACCNO=%s"%(ngender,acc)
        cur.execute(s)
        print("Value updated successfully!!!")
            
    elif c==6:
        updnationality=input("Enter the new value you wish to set for this field:")
        s="update "+table+" set NATIONALITY='%s' where ACCNO=%s"%(updnationality.lower(),acc)
        cur.execute(s)
        print("Value updated successfully!!!")
        
    conn.commit()
    
    if d[acc][1]<18 and c==7:
        updmenu(d,'guardian',acc)
    if d[acc][6]=='j' and c==8:
        updmenu(d,'jointholder',acc)
        
    conn.commit() 
    cont=input("Do you wish to update details for any other fields?(yes/no):")
    cont=cont.lower()
    if cont not in ['yes','no']:
        while cont not in ['yes','no']:
            print("Enter a valid input")
            cont=input("Do you wish to continue updating details for any other fields?(Yes/No)")
            cont=cont.lower()
    elif cont=="yes":
        updmenu(d,table,acc)
    elif cont=="no":
        print()
        pass

def options(uname):
    print()
    global conn
    global cur
    '''s="select ACCNO from accdetails details where UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()'''
    print("Apply for:")
    print("\t1. LOAN")
    print("\t2. FIXED DEPOSIT")
    a=int(input("Enter your choice:"))
    if a==1:
        loan(uname)
    elif a==2:
        fd(uname)

def loan(uname):
    print("Enter the following details about the loan applicant:")
    lname=input("NAME:")
    lage=input("AGE:")
    if lage.isnumeric():
        lage=int(lage)
    else:
        while lage.isnumeric()==False:
          print("Enter a valid input value")
          lage=input("AGE:")
        lage=int(lage)          
            
    laddress=input("ADDRESS:")
    lphone=input("PHONE NUMBER:")
    while len(lphone)!=10 or lphone.isnumeric()==False:
            print("Invalid input. Your phone number must contain 10 digits only.")
            print("Try again")
            lphone=input("PHONE NUMBER:")    
    lphone=int(lphone)       
    lgender=input('GENDER(M/F/OTHER):')
    lgender=lgender.lower()
    while lgender not in ['m','f','other']:
        print("Enter a valid input")
        lgender=input('GENDER(M/F/OTHER):')
        lgender=lgender.lower()
    lnationality=input('NATIONALITY:')
    lnationality=lnationality.lower()
    lstatus=input("MARITAL STATUS(married/single):")
    lstatus=lstatus.lower()
    while lstatus not in ['married','single']:
        print("Enter a valid input")
        lstatus=input("MARITAL STATUS(married/single):")
        lstatus=lstatus.lower()
    lqual=input("QUALIFICATION:")
    lqual=lqual.lower()
    loccu=input("OCCUPATION:")
    lincome=float(input("MONTHLY INCOME: Rs."))
    loanamount=int(input("LOAN AMOUNT: Rs."))
    loanterm=int(input("LOAN REPAYMENT TENURE(in years):"))
    loanpurpose=input("PURPOSE OF TAKING LOAN:")
    if loanterm<=5:
        rate=8.5
    elif loanterm>5 and loanterm<=10:
        rate=10
    elif loanterm>10 and loanterm<=15:
        rate=11.5
    elif loanterm>15:
        rate=13
    print("Interest rate applicable on your loan tenure is :",rate,"%")
   
    print("The loan is to be repaid through monthly installments")
    interest=loanamount*rate*loanterm*0.01
    amounttobepaid=loanamount+interest
    print("Total amount to be repaid to the bank(including interest): Rs.",amounttobepaid)
    if amounttobepaid/12 > lincome:
        print("SORRY!! YOU ARE NOT ELIGIBLE TO TAKE LOAN ON THE BASIS OF YOUR INCOME :(")
    else:
        print("Monthly installment to be paid: Rs.",amounttobepaid/12)
        #ask account number
        s="select ACCNO from logindetails where UNAME='%s'"%(uname,)
        cur.execute(s)
        x=cur.fetchall()
        
        y=[]
        for i in x:
            i=list(i)
            y+=i
        
        print("You have the following accounts linked to your username:")
        c=0
        for i in y:
            print(c+1,'. ', i)
        accno=int(input("Enter the account number from the above list you wish to link to the loan:"))
        amtrepaid=0
        amtleft=amounttobepaid
        if accno in y:
            cur.execute('create table if not exists loandetails(ACCNO bigint, NAME varchar(20), AGE int, ADDRESS varchar(80), PHONENUM bigint, GENDER varchar(5), NATIONALITY varchar(20), MARITALSTATUS varchar(10),QUALIFICATION varchar(25), OCCUPATION varchar(20), MONTHLYINCOME float, LOANAMT float, LOANTENURE float, PURPOSE varchar(50), INTERESTRATE float, EMI float)')
            newentry="insert into loandetails values(%s,'%s',%s,'%s',%s,'%s','%s','%s','%s','%s',%s,%s,%s,'%s',%s,%s)"%(accno,lname,lage,laddress,lphone,lgender,lnationality,lstatus,lqual,loccu,lincome,loanamount,loanterm,loanpurpose,rate,amounttobepaid/12)
            cur.execute(newentry)
            print("LOAN GRANTED SUCCESSFULLY!!!")
        else:
            while accno not in y:
                print("Invalid input!!!")
                accno=int(input("Enter the account number from the above list you wish to link to the loan:"))
            cur.execute('create table if not exists loandetails(ACCNO bigint, NAME varchar(20), AGE int, ADDRESS varchar(80), PHONENUM bigint, GENDER varchar(5), NATIONALITY varchar(20), MARITALSTATUS varchar(10),QUALIFICATION varchar(25), OCCUPATION varchar(20), MONTHLYINCOME float, LOANAMT float, LOANTENURE float, PURPOSE varchar(50), INTERESTRATE float, EMI float, AMTREPAID float, AMTLEFT float, DATEOFISSUE timestamp)')
            newentry="insert into loandetails values(%s,'%s',%s,'%s',%s,'%s','%s','%s','%s','%s',%s,%s,%s,'%s',%s,%s)"%(accno,lname,lage,laddress,lphone,lgender,lnationality,lstatus,lqual,loccu,lincome,loanamount,loanterm,loanpurpose,rate,amounttobepaid/12,amtrepaid,amtleft)
            cur.execute(newentry)
            print("LOAN GRANTED SUCCESSFULLY!!!")
            
                
    conn.commit()

def fd(uname):
    print("Enter the following details about the FD applicant:")
    fdname=input("NAME:")
    fdage=input("AGE:")
    if fdage.isnumeric():
        fdage=int(fdage)
    else:
        while fdage.isnumeric()==False:
          print("Enter a valid input value")
          fdage=input("AGE:")
        fdage=int(fdage)          
            
    fdaddress=input("ADDRESS:")
    fdphone=input("PHONE NUMBER:")
    while len(fdphone)!=10 or fdphone.isnumeric()==False:
            print("Invalid input. Your phone number must contain 10 digits only.")
            print("Try again")
            fdphone=input("PHONE NUMBER:")    
    fdphone=int(fdphone)       
    fdgender=input('GENDER(M/F/OTHER):')
    fdgender=fdgender.lower()
    while fdgender not in ['m','f','other']:
        print("Enter a valid input")
        fdgender=input('GENDER(M/F/OTHER):')
        fdgender=fdgender.lower()
    fdnationality=input('NATIONALITY:')
    fdnationality=fdnationality.lower()
    fdamount=int(input("AMOUNT TO BE FIXED DEPOSITED: Rs."))
    fdterm=int(input("FIXED DEPOSIT TENURE(in years):"))
    
    if fdterm<=1:
        rate=6
    elif fdterm>1 and fdterm<=2:
        rate=7
    elif fdterm>2 and fdterm<=3:
        rate=7.5
    elif fdterm>3:
        rate=8
    print("Interest rate applicable on your FD tenure is :",rate,"%")
    fdmaturityamt=fdamount*((1+(rate*0.01))**fdterm)
    print("Total amount bank will pay you when FD matures(including interest, compounded annually): Rs.",fdmaturityamt)
    #ask account number
    s="select ACCNO from logindetails where UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    
    y=[]
    for i in x:
        i=list(i)
        y+=i
    print("You have the following accounts linked to your username:")
    c=0
    for i in y:
        print(c+1,'. ', i)
    accno=int(input("Enter the account number from the above list you wish to link to the fd:"))
    if accno in y:
        cur.execute('create table if not exists fddetails(ACCNO bigint, NAME varchar(20), AGE int, ADDRESS varchar(80), PHONENUM bigint, GENDER varchar(5), NATIONALITY varchar(20), FDAMT float, FDTENURE float, INTERESTRATE float, MATURITYAMT float)')
        newentry="insert into fddetails values(%s,'%s',%s,'%s',%s,'%s','%s',%s,%s,%s,%s)"%(accno,fdname,fdage,fdaddress,fdphone,fdgender,fdnationality,fdamount, fdterm, rate,fdmaturityamt)
        cur.execute(newentry)
        print("FD CREATED SUCCESSFULLY!!!")
    else:
        while accno not in y:
            print("Invalid input!!!")
            accno=int(input("Enter the account number from the above list you wish to link to the fd:"))
        cur.execute('create table if not exists fddetails(ACCNO bigint, NAME varchar(20), AGE int, ADDRESS varchar(80), PHONENUM bigint, GENDER varchar(5), NATIONALITY varchar(20), FDAMT float, FDTENURE float, INTERESTRATE float, MATURITYAMT float, DATEOFISSUE timestamp)')
        newentry="insert into fddetails values(%s,'%s',%s,'%s',%s,'%s','%s',%s,%s,%s,%s)"%(accno,fdname,fdage,fdaddress,fdphone,fdgender,fdnationality,fdamount, fdterm, rate,fdmaturityamt)
        cur.execute(newentry)
        print("FD CREATED SUCCESSFULLY!!!")
            
                
    conn.commit()    
    
    

def closeacc(uname):
    print()
    global conn
    global cur
    s="select ACCNO from logindetails where UNAME='%s'"%(uname,)
    cur.execute(s)
    x=cur.fetchall()
    s="select ACCNO from jointholder j natural join logindetails l where j.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    y=cur.fetchall()
    s="select ACCNO from guardian g natural join logindetails l where g.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    z=cur.fetchall()
    s="select ACCNO from balance b natural join logindetails l where b.ACCNO=l.ACCNO and UNAME='%s'"%(uname,)
    cur.execute(s)
    bal=cur.fetchall()
    newx=[]
    for i in x:
        i=list(i)
        newx+=i
    newy=[]
    for i in y:
        i=list(i)
        newy+=i
    newz=[]
    for i in z:
        i=list(i)
        newz+=i
    print("You have the following accounts linked to your username:")
    for i in range(len(newx)):
        print(i+1,'. ', newx[i])
    acc=int(input("Enter the account number from the above list you wish to close:"))
    if acc in newx:
        s="select l.ACCNO,BALANCE from balance b,logindetails l where b.ACCNO=l.ACCNO and UNAME='%s' and b.ACCNO=%s"%(uname,acc)
        cur.execute(s)
        balance=cur.fetchall()
        d={}
        for i in range(len(balance)):
            accno=balance[i][0]
            b=balance[i][1]
            d[accno]=b
        print("This account has Rs.", d[acc])
        if d[acc]!=0:
            print("How would you like to take out the amount?")
            print("1. CASH")
            print("2. TRANSFER TO SOME OTHER ACCOUNT")
            enter=int(input("Enter your choice:"))
            if enter not in [1,2]:
                print("INVALID INPUT!!!")
                while enter not in [1,2]:
                    enter=input("Enter your choice:")
            if enter==1:
                print("Please visit your nearest branch to collect your balance amount")
                pass
            elif enter==2:
                print("Redirecting you to online transfer page...")
                neft(uname)
                    
                    
        s="delete from accdetails where ACCNO=%s"%(acc,)
        cur.execute(s)
        s="delete from logindetails where ACCNO=%s"%(acc,)
        cur.execute(s)
        s="delete from balance where ACCNO=%s"%(acc,)
        if acc in newy:
            s="delete from jointholder where ACCNO=%s"%(acc,)
            cur.execute(s)
        if acc in newz:
            s="delete from guardian where ACCNO=%s"%(acc,)
            cur.execute(s)
        conn.commit()
        print("ACCOUNT NO. ",acc," CLOSED SUCCESSFULLY")
        print("THANK YOU FOR CHOOSING WORLD BANK!!")
    else:
        while acc not in newx:
            print("INVALID INPUT!!!")
            acc=int(input("Enter the account number from the above list you wish to close:"))
        s="delete from accdetails where ACCNO=%s"%(acc,)
        cur.execute(s)
        s="delete from logindetails where ACCNO=%s"%(acc,)
        cur.execute(s)
        if acc in newy:
            s="delete from jointholder where ACCNO=%s"%(acc,)
            cur.execute(s)
        if acc in newz:
            s="delete from guardian where ACCNO=%s"%(acc,)
            cur.execute(s)
        print("ACCOUNT NO. ",acc," CLOSED SUCCESSFULLY")
        print("THANK YOU FOR CHOOSING WORLD BANK!!")
    
    conn.commit()
    


def checkinterest():
    print()
    from tabulate import tabulate as table
    fdrates=[['0 to 1','6%'],['1 to 2','7%'],['2 to 3','7.5%'],['3 and above','8%']]
    fdheading=['Tenure(in yrs)','Interest rates(p.a.)']
    print("\tFIXED DEPOSIT INTEREST RATES:")
    print(table(fdrates,headers=fdheading,tablefmt='pretty'))
    print()
    loanrates=[['0 to 5','8.5%'],['5 to 10','10%'],['10 to 15','11.5%'],['15 and above','13%']]
    loanheading=['Loan Tenure(in yrs)','Interest rates(p.a.)']
    print("\tLOAN INTEREST RATES:")
    print(table(loanrates,headers=loanheading,tablefmt='pretty'))
    
    

        
check_conn()        
mainmenu()
        
    
