import time
import os
import datetime

folder = "/var/www/html/csv"

def write_event(action, timer):
    if os.path.exists(folder+"/"+str(datetime.datetime.now().strftime('%m-%Y')+".csv")) == False:
        with open(folder+"/"+datetime.datetime.now().strftime("%m-%Y")+".csv", "w" ) as history_file:
            history_file.write("date;time;action;timer (in hours)" + "\n")
                  
    with open(folder+"/"+datetime.datetime.now().strftime("%m-%Y")+".csv", "a" ) as history_file:
        history_file.write( datetime.datetime.now().strftime("%d-%m-%Y")+";")
        history_file.write( datetime.datetime.now().strftime("%H:%M:%S")+";")
        history_file.write(action + ";")
        history_file.write(str(timer).replace(".", ",") + ";")
        history_file.write("\n")