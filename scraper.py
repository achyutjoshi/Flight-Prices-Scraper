

# From command line execute following command
# python makemytrip.py 

import urllib2
import json
import sys 
import re
#import datetime
from datetime import date, time, datetime
#from datetime import datetime, date, time
#import mapping as city
import pickle
from dateutil.rrule import rrule, DAILY



BASE_URL="http://flights.makemytrip.com/makemytrip/"

class MakeMyTrip(object):
    
    def __init__(self):
        self.url_browse = ""
        self.flights_data = ""
        self.stoppage = ""
        self.arrival_time = ""
        self.trip_json = []
        
    def browse(self, url="", roundtrip=False):
        print url
        try:
            self.url_browse = urllib2.urlopen(url).read()
        except urllib2.HTTPError:  
            print 'There was an ERROR'
        fil = open("out.txt","w")
        fil.write(self.url_browse)
        fil.close()
        i = 0
        fil = open("out.txt","r")
        if roundtrip:
            json_list = json.loads(fil.read())
            #print json_list#['filterData']
            print "-"*50
            json_list = json.loads(json_list['fd'])
            return json_list
        for line in fil.readlines():
            i = i+1
            if "flightsData" in line:
                self.flights_data = line
                break
        temp_flights_data = self.flights_data.replace("var flightsData = ","").strip()
        temp_flights_data = temp_flights_data[:-1]
        fil = open("out.txt","w")
        fil.write(temp_flights_data)
        fil.close()
        try :
            json_list = json.loads(temp_flights_data)
        except ValueError : 
            json_list = 1
        return json_list
    
    def create_json_oneway(self, dump_list):
        for i in range(len(dump_list)):
            temp = '{ "airline" : "' + dump_list[i]['le'][0]['an'] + '"'
            temp = temp + ', "price" : "' + str(dump_list[i]['af']) + '"'
            temp = temp + ', "total_time" : "' + str(dump_list[i]['td']) + '"'
            temp = temp + ', "depart_date" : "' + str(dump_list[i]['le'][0]['fd']) + '"'
            temp = temp + ', "depart_time" : "' + str(dump_list[i]['le'][0]['fdt']) + '"'
            temp_dump_list = dump_list[i]['le']
            for x in range(len(temp_dump_list)):
                if x == (len(temp_dump_list)-1):
                    temp = temp + ', "arrival_date" : "' + str(temp_dump_list[x]['fa']) + '"'
                    temp = temp + ', "arrival_time" : "' + str(temp_dump_list[x]['fat']) + '"}'
            self.trip_json.append(temp)
        return json.dumps(self.trip_json)
        
    def create_json_roundtrip(self, dump_list):
        #Todo : Complete this function to return the custom JSON as response 
        for i in range(len(dump_list)):
            return json.loads(['fd'])
        
    def journey_oneway(self, origin, destination, depart_date, adult=1, children=0, infant=0):
        adult = str(adult) if adult >= 1 else "1"
        children = str(children) if children >= 1 else str(children)
        infant = str(infant) if infant >= 1 else str(infant)
        new_url = BASE_URL + "search/O/O/E/" + adult +"/" + children + "/" + infant + "/S/V0/" + origin + "_" + destination + "_" + depart_date
        return self.browse(new_url)
    
    def journey_roundtrip(self, origin, destination, depart_date, return_date, adult=1, children=0, infant=0):
        new_url = BASE_URL + 'splitRTDataService.json?classType=E&deptDate=' + depart_date + '&fltMap=&fromCity='+ origin + '&noOfAdlts=' + str(adult) + \
        '&noOfChd=' + str(children) + '&noOfInfnt=' + str(infant) + '&returnDate=' + return_date + '&toCity=' + destination + '&tripType=R&tripTypeDup=R'
        return self.browse(new_url, True)
        
    #Todo: Get rid of this method
    def read_line(self):
        flights_data=""
        i = 0
        fil = open("out.txt","r")
        for line in fil.readlines():
            i = i+1
            if "flightsData" in line:
                flights_data = line
        #print "Total lines",i
        self.format_flights_data(flights_data)
        #self.getFlightTable(flights_data)
        
    #Todo: Get rid of this method
    def format_flights_data(self, flights_data):
        new_flights_data = flights_data.replace("var flightsData = ","").strip()
        new_flights_data = new_flights_data[:-1]
        fil = open("out.txt","w")
        fil.write(new_flights_data)
        fil.close()
        d = new_flights_data
        li = json.loads(d)
        self.create_json_oneway(li)
        #print type(new_flights_data)
            
    def get_extra_detail(self, flights_data):
        #date_size=len(flights_data)
        halt = flights_data[0]['f']
        layover = ""
        for x in range(len(flights_data)):
            halt = halt + u"   \u2708   " + flights_data[x]['t'] + " ( " + flights_data[x]['du'] + " )"
            if x > 0:
                layover = layover + flights_data[x]['f'] + "  ( " + flights_data[x]['lo'] + " )  "
            if x == (len(flights_data)-1):
                self.arrival_time = flights_data[x]['fa'] + " " +flights_data[x]['fat']
        print halt
        return layover
        #return halt
        
    def print_json(self, l):
        
        tmp_size = len(l)
        for i in range(tmp_size):   
            print ""
            print u"\033[1m" + l[i]['le'][0]['an'] , u"\033[0m      \u20B9 \033[92m", l[i]['af'], "\033[0m  in  ", l[i]['td']
            layover=self.get_extra_detail(l[i]['le']) 
            #ToDo
            print l[i]['le'][0]['fd'],  l[i]['le'][0]['fdt'], \
             u"  --->>  ", self.arrival_time
            print "\tStoppage : ", layover
            #print "Arrival : ", l[i]['le'][0]['fa'], l[i]['le'][0]['fat']
            print u"\u2982"*50

 
 #To write the required files into json format

    def file_json(self,l,destination, origin , flight_date):
        if l == 1 :
            taken_date = str(datetime.today().date())
            f1.write("Origin" + "," + "Destination" + "," + "Dept_Date" + "," + "Dept_Time" + "," + "Arr_Time" + "," + "Total_Fare" + "," + "Base_Fare" + "," + "Fuel_Fare" + "," + "Airways" + "," + "Available" + "," + "Duration" + "," + "Class_Type" + "," + "Flight Number" + "," + "Flight Code" + "," + "FlightID" + "," + "Hopping" + "," +"Taken" +"\n")
            f1.write(origin + "," + destination + "," + flight_date + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + ","+ "NA" + "," + "NA" + "," + "NA" + "," + "NA" + ","+ taken_date +"\n")
        else :
            tmp_size = len(l)
            f1.write("Origin" + "," + "Destination" + "," + "Dept_Date" + "," + "Dept_Time" + "," + "Arr_Time" + "," + "Total_Fare" + "," + "Base_Fare" + "," + "Fuel_Fare" + "," + "Airways" + "," + "Available" + "," + "Duration" + "," + "Class_Type" + "," + "Flight Number"+ "," + "Flight Code" + "," + "FlightID" + "," + "Hopping" + "," +"Taken" +"\n")
            for i in range(tmp_size):  
                airways = l[i]['le'][0]['an'] 
                fare = l[i]['af']
                deptdate = l[i]['le'][0]['dep']
                depttime = l[i]['le'][0]['fdt']
                arrtime = l[i]['le'][0]['fat']
                avail = l[i]['le'][0]['flightFare']['bookingClass']['availability']
                basefare = l[i]['le'][0]['flightFare']['baseFare']
                fuel_surcharge = l[i]['le'][0]['flightFare']['fuelSurcharge']
                duration = l[i]['td']
                origin = l[i]['le'][0]['o']
                desti = l[i]['le'][0]['d']
                class_type = l[i]['le'][0]['cls']
                flight_number = l[i]['le'][0]['fn']
                flight_code = l[i]['le'][0]['oc']
                Flight_ID = l[i]['fi']
                hopping = l[i]['hff']

                '''
                if hopping == True :
                    arrtime = l[i]['le'][1]['fat']
                else :
                    arrtime = l[i]['le'][0]['fat']
                '''
                taken_date = str(datetime.today().date())
                
                f1.write(origin + "," + desti + "," + deptdate + "," + depttime + "," + arrtime + "," + str(fare) + "," + str(basefare) + "," + str(fuel_surcharge) + "," +airways+ "," + avail + ","+duration + "," + class_type + ","+ flight_number + "," + flight_code + ","  + Flight_ID + "," + str(hopping) + "," +taken_date+  "\n")
                



        
if __name__=="__main__":
    print
    print "="*30 
    origin = "DEL"
    destination = "GAU"
    
    #Range of dates in which we want the data
    a = date(2016, 10, 21)   
    b = date(2016, 11, 2)

    for dt in rrule(DAILY, dtstart=a, until=b):
        print dt.strftime("%d-%m-%Y")
        dept_date = str(dt.strftime("%d-%m-%Y"))
        bro = MakeMyTrip()
        f1=open('buff.csv', 'a') 
        bro.file_json(bro.journey_oneway(origin,destination,dept_date), destination, origin , dept_date)
        f1.close()
    

    