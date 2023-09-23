import sys
import csv
from datetime import datetime
 #Question 1 containers

#1a Containers
weekday={'Primary':0,'Broker':0,'E-Hail':0,'Total':0}
weekend={'Primary':0,'Broker':0,'E-Hail':0,'Total':0}
total={}
Table1=[weekday,weekend,total]
    
#1b Containers
weekdayAve={'Primary':0,'Broker':0,'E-Hail':0,'Total':0}
weekendAve={'Primary':0,'Broker':0,'E-Hail':0,'Total':0}
totalAve={}
Table2=[weekdayAve,weekendAve,totalAve]
#1c Containers
weekday3={'Primary':0,'Broker':0,'E-Hail':0,'Total':0}
weekend3={'Primary':0,'Broker':0,'E-Hail':0,'Total':0}
total3={}
Table3=[weekday3,weekend3,total3]

#Question 2
histData={}


#question3 container
zipcodes={}


with open('DATA.csv', 'r') as fi:
    reader = csv.DictReader(fi)
    for row in reader:
        provider= row['ProviderType']
        status=row['Outcome']
        date=row['Tripdate']
        day=datetime.strptime(date, '%Y-%m-%d').strftime('%w')
        time=row['ADtime']
        
        #task1 container filling
        if (provider in weekday.keys()):
            if int(day)<6:
                weekdayAve[provider]+=1
                if status=='Authorized' or  status=='Completed':#number of succesful trips
                    weekday[provider]+=1
            else:
                weekendAve[provider]+=1
                if status=='Authorized' or  status=='Completed':#number of succesful trips
                    weekend[provider]+=1
        #task2 container filling
        if status=='Authorized' or  status=='Completed':
          time=row['ADtime']
          x=int(time.split(':')[0])
          if x>-1:
            if x>23:
              histData[x-24]=histData.get(x-24,0)+1
            else:
              histData[x]=histData.get(x,0)+1
        
        #task 3 container filling
        if provider=="Primary" and (status=='Authorized' or  status=='Completed'):
          hour1=datetime.strptime('6:00', "%H:%M").time()
          hour2=datetime.strptime('10:00', "%H:%M").time()
          x=int(time.split(':')[0])
          if x>-1:
            if x>23:
              x=x-24
              time=':'.join([str(x),time.split(':')[1]])
          time1=datetime.strptime(time, "%H:%M").time()
          if(time1>=hour1 and time1<=hour2):
            zip=row['PickZip']
            zipcodes[zip]=zipcodes.get(zip,0)+1
#task 1
for key in weekday:
    total[key]=weekday[key]+weekend[key]
    totalAve[key]=weekdayAve[key]+weekendAve[key]
    if key !='Total':
      weekday['Total']+=weekday[key]
      weekend['Total']+=weekend[key]
      weekdayAve['Total']+=weekdayAve[key]
      weekendAve['Total']+=weekendAve[key]
            
        
        
for key in weekdayAve:
    weekday3[key]="{:.2%}".format(weekdayAve[key]/weekdayAve['Total'])
    weekend3[key]="{:.2%}".format(weekendAve[key]/weekendAve['Total'])
    total3[key]="{:.2%}".format(totalAve[key]/totalAve['Total'])
        
    weekdayAve[key]=round(weekday[key]/5)
    weekendAve[key]=round(weekend[key]/2)
    totalAve[key]=round(total[key]/7)
print("Table1")
for i in Table1:
  print(i)
print("Table1")
for i in Table2:
  print(i)
print("Table1")
for i in Table3:
  print(i)
  


#task2
print(sorted(histData.items(), key=lambda x: x[0]))
with open('2.csv', 'w') as output:
    writer = csv.writer(output)
    writer.writerow(["Hour of Day", "Number of Trips"])
    for key, value in sorted(histData.items(), key=lambda x: x[0]):
        writer.writerow([key, value])

#task 3
with open('3.csv', 'w') as output:
    writer = csv.writer(output)
    writer.writerow(["Zip Code", "Number of Primary trips during AM rush hour"])
    count=0
    for key, value in sorted(zipcodes.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([key, value])
        count+=1
        if count==10:
            break
#for i in range(10):
  #print(sorted(zipcodes.items(), key=lambda x: x[1], reverse=True)[i])
