import csv
import time
import paho.mqtt.client as paho
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report
import math


fdf=pd.DataFrame(columns=["no_changes","dmax","dmin","davg","ddmax","ddmin","ddavg","no_ones","no_one_changes"])
Tdf=pd.DataFrame(columns=["no_changes","dmax","dmin","davg","ddmax","ddmin","ddavg","no_ones","no_one_changes"])
TestDF = pd.DataFrame(columns=['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
       'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20',
       'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30',
       'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'M0',
       'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11',
       'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'M19', 'M20', 'M21',
       'M22', 'M23', 'M24', 'M25', 'M26', 'M27', 'M28', 'M29', 'M30', 'M31',
       'M32', 'M33', 'M34', 'M35', 'M36', 'M37', 'M38', 'M39'])

broker="192.168.4.1"
port=1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Data/modules")

def on_publish(client,userdata,result):
    print("data published \n")
    pass

def Predict(data):
    listt = data[1:].split(" ")
    listt = [int(i) for i in listt] 
    print(listt)
    print(len(listt))
    TestDF = pd.DataFrame(np.array([listt]),columns =['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
       'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20',
       'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30',
       'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'M0',
       'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11',
       'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'M19', 'M20', 'M21',
       'M22', 'M23', 'M24', 'M25', 'M26', 'M27', 'M28', 'M29', 'M30', 'M31',
       'M32', 'M33', 'M34', 'M35', 'M36', 'M37', 'M38', 'M39']) 
    
    
    for index,row in TestDF.iterrows():
        testrow = row
        slope=0
        nochanges=0
        dmax=0;
        dmin=0;
        davg=0;
        ddmax=0;
        ddmin=0;
        ddavg=0;
        
        print(row)
        print(4)
        
        for i in range(0,39):
            diff = row["A"+str(i)] - row["A"+str(i+1)]
            #print("diff = "+str(diff)+" and slope = "+str(slope))
            if diff<0 and (slope>=0):
                slope = -1
                nochanges+=1
            elif diff>0 and (slope<=0):
                slope=1
                nochanges+=1
            else:
                #print("value not incremented")
                pass
        #print(str(index)+"    "+str(nochanges)+"    "+str(output[index]))
        #time.sleep(1000);
        print(5)
        print(nochanges)
        
        drow=row.diff()[1:-40].abs()
        dmax=drow.max()
        dmin=drow.min()
        davg=drow.mean()
        
        ddrow=row.diff().diff()[1:-41].abs()
        ddmax=ddrow.max()
        ddmin=ddrow.min()
        ddavg=ddrow.mean()
        
        print(114)
        
        no_ones=0
        no_one_changes=0
        for i in range(40,80):
            if (row["M"+str(i-40)] == 1):
                no_ones+=1
        mdrow = row.diff()[40:].abs()
        for i in range(0,40):
            if (mdrow[i] == 1):
                no_one_changes+=1
        print(125)
        break
    print(127)
    dataE = [(nochanges) ,dmax,dmin,davg,ddmax,ddmin,ddavg,no_ones,no_one_changes]
    Tdf = pd.DataFrame([dataE], columns=["no_changes","dmax","dmin","davg","ddmax","ddmin","ddavg","no_ones","no_one_changes"])
    #Tdf=Tdf.append({'no_changes': str(nochanges) , 'dmax':dmax, 'dmin':dmin, 'davg':davg, 'ddmax':ddmax, 'ddmin':ddmin, 'ddavg':ddavg, 'no_ones':no_ones, 'no_one_changes':no_one_changes}, ignore_index=True)
    print(128)
    print("publishing...")
    print(str(clf.predict(Tdf.tail(1))))
    client1.publish("Data/output",str(clf.predict(Tdf.tail(1)))[1])

def on_message(client, userdata, msg):
    print("Recieved Data:"+msg.payload.decode()+":")
    data = msg.payload.decode()
    print("predict for "+str(data))
    Predict(data)
    


df1 = pd.read_csv("D:\\Downloads\\Train1.csv")
df2 = pd.read_csv("D:\\Downloads\\Train2.csv")
df3 = pd.read_csv("D:\\Downloads\\Train3.csv")
df4 = pd.read_csv("D:\\Downloads\\Train4.csv")

dfg = pd.concat([df1,df2],axis = 0).reset_index(drop=True)
dfb = pd.concat([df2,df3],axis = 0).reset_index(drop=True)

y = [0]*400+[0]*200+[1]*200


df = pd.concat([dfg,dfb],axis = 0).reset_index(drop=True)


clf = SVC(kernel='linear') 

fdf=fdf.iloc[0:0]
for index,row in df.iterrows():
    testrow = row
    slope=0
    nochanges=0
    dmax=0;
    dmin=0;
    davg=0;
    ddmax=0;
    ddmin=0;
    ddavg=0;
    
    for i in range(0,38):
        diff = row["A"+str(i)] - row["A"+str(i+1)]
        #print("diff = "+str(diff)+" and slope = "+str(slope))
        if diff<0 and (slope>=0):
            slope = -1
            nochanges+=1
        elif diff>0 and (slope<=0):
            slope=1
            nochanges+=1
        else:
            #print("value not incremented")
            pass
    #print(str(index)+"    "+str(nochanges)+"    "+str(output[index]))
    #time.sleep(1000);
    
    drow=row.diff()[1:-40].abs()
    dmax=drow.max()
    dmin=drow.min()
    davg=drow.mean()
    
    ddrow=row.diff().diff()[1:-41].abs()
    ddmax=ddrow.max()
    ddmin=ddrow.min()
    ddavg=ddrow.mean()
    
    no_ones=0
    no_one_changes=0
    for i in range(40,80):
        if (row["M"+str(i-40)] == 1):
            no_ones+=1
    mdrow = row.diff()[40:].abs()
    for i in range(0,40):
        if (mdrow[i] == 1):
            no_one_changes+=1
            
    fdf=fdf.append({'no_changes': (nochanges) , 'dmax':dmax, 'dmin':dmin, 'davg':davg, 'ddmax':ddmax, 'ddmin':ddmin, 'ddavg':ddavg, 'no_ones':no_ones, 'no_one_changes':no_one_changes}, ignore_index=True)


X_train, X_test, y_train, y_test = train_test_split(fdf, y, test_size=0.2)
clf.fit(X_train, y_train) 

y_pred = clf.predict(X_test)

results = confusion_matrix(y_test, y_pred) 
print('Confusion Matrix :')
print(results) 
print('Accuracy Score :',accuracy_score(y_test, y_pred)) 
print('Report : ')
print(classification_report(y_test, y_pred))


client1= paho.Client("control1")
client1.on_publish = on_publish
client1.on_connect = on_connect
client1.on_message = on_message
client1.connect(broker,port)


client1.loop_forever()


