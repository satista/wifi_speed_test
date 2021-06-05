from time import sleep
import speedtest
import datetime
import os
import csv
from statistics import mean

#method to do a speed test. It will handle the speed testing elements of the script.
def do_speed_test(dl_arr, ul_arr, ping_arr, dt_arr):
    """
    Takes 4 inputs, download arr- an array to append calculated download times. Same for upload times, ping and date-time fields.
    """
    try:
        st = speedtest.Speedtest()
        dt = datetime.datetime.now()

        #Store the datetime. 
        dt_arr.append(dt.date())
        dt_arr.append(dt.time())

        #output to user.
        print(dt,"\n")
        print("Initiating Speed test.\n")
        print("Testing 3 times:\n")
        for x in range(0,3):
            st.get_best_server()

            #do download speed test first
            print("Test {}:".format(x+1))
            print("Testing Download Speed...\n")
            dl_speed = st.download()
            print("Download: {} Megabits/sec\n".format(dl_speed*1e-6))
            dl_arr.append(dl_speed*1e-6)

            #Do upload speed test
            print("Testing Upload Speed...\n")
            ul_speed = st.upload()
            print("Upload: {} Megabits/sec\n".format(ul_speed*1e-6))
            ul_arr.append(ul_speed*1e-6)

            
            #test for the average ping
            print("Testing Ping...\n")
            average_ping = [] 
            #loop and test 5 times
            for attempt in range(0,5):
                st.get_best_server()
                average_ping.append(st.results.ping)
            avg_ping = (sum(average_ping)/len(average_ping))
            print("The Average ping is ",avg_ping,"\n")
            ping_arr.append(avg_ping)
    except:
        print("Please make sure you are online, or have a stable connection.\n")

#Quick Test Elements        

def do_download_test(st):
    dl_speed = round(st.download()*1e-6,2)
    return dl_speed

def do_upload_test(st):
    ul_speed = round(st.upload()*1e-6,2)
    return ul_speed

def do_ping_test(st):
    st.get_best_server()
    return st.results.ping
        
def do_quick_test():
    """ Does a quick speed test and prints it out onto the command line.""" 
    try:
       st =  speedtest.Speedtest()
       st.get_best_server()
       print("Your Download Speed is ",do_download_test(st),"MegaBits/s\n")
       print("Your Upload Speed is ",do_upload_test(st),"MegaBits/s\n")

       pings = []

        #Get average ping
       for i in range(0,5):
           pings.append(do_ping_test(st))
       avg_ping = (sum(pings)/len(pings))
       print("Your average ping is ",avg_ping,"ms\n")

    except:
        print("Please make sure you are online, or have a stable connection.\n")

def is_number(num):
    """ Quick method to try and check if a number is a number."""
    #if decimal.
    if("." in num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    else:
        try:
            int(num)
            return True
        except ValueError:
            return False


print("""
  _____ _____  ______ ______ _____    _______ ______  _____ _______ 
 / ____|  __ \|  ____|  ____|  __ \  |__   __|  ____|/ ____|__   __|
| (___ | |__) | |__  | |__  | |  | |    | |  | |__  | (___    | |   
 \___ \|  ___/|  __| |  __| | |  | |    | |  |  __|  \___ \   | |   
 ____) | |    | |____| |____| |__| |    | |  | |____ ____) |  | |   
|_____/|_|    |______|______|_____/     |_|  |______|_____/   |_|   
                                                                    
                                                                                \n\n""")
print("""By Sathish Ravi \n 
This is a command line tool that has the capability to do a quick speed test or can be programmed to do a longer-term test, storing the results into a CSV file.
""")

exit_loop = 0

while exit_loop == 0:
    print("""Please Select one of the following options:

        1) Quick Test
        2) Long Test

    Enter any other key to exit... """)
    test_style = input()

    if test_style == "1" or test_style == "2":
        if test_style == "2":
            print("Please enter the number of hours you would like to run this program for from 0-24. Please enter any other option to go back to the menu.\n")

            run_time = input()
            if (is_number(run_time)):

                print("Checking Prerequisites.\n")
                #Create a log folder if it doesn't exist.
                if not os.path.exists('Log'):
                    print("Creating Folders.\n")
                    os.makedirs('Log')

                #Create a csv file if not exist.
                if not os.path.exists('.\Log\speed_test.csv'):
                    print("Creating CSV files.\n")
                    with open('.\Log\speed_test.csv', 'w', newline='') as csvfile:
                        headers =["Date","Time","Download speed (MB/s)","Upload speed (MB/s)","Ping (ms)"]
                        writer = csv.DictWriter(csvfile, delimiter=',',fieldnames=headers)
                        writer.writeheader()
                
                #run time into hours - seconds
                times_to_run = round((float(run_time) * 3600)/300)
                #we want it to run every 5 minutes.

                for time in range(0,times_to_run):

                    #Create arrays to populate data.
                    dl_arr = []
                    ul_arr = []
                    ping_arr = []
                    dt_arr = []

                    #print info to let them know which test we are on.
                    print("Running test ",time + 1," out of ",times_to_run,"\n")

                    #do the speed test, it will populate the arrays.
                    do_speed_test(dl_arr,ul_arr,ping_arr,dt_arr)

                    #if we obtain info.
                    if len(dl_arr) > 0 and len(ul_arr ) >0 and len(ping_arr) >0 and len(dt_arr) >0:
                        print("Test ",time + 1,"completed successfully, writing to CSV.\n")
                        #write the information into the CSV we created earlier.                   
                        with open('.\Log\speed_test.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([dt_arr[0],dt_arr[1], mean(dl_arr),mean(ul_arr),mean(ping_arr)])
                    else:
                        print("Test {} failed. \n".format(time + 1))

                    #it will take~ roughly 2 minutes for it to run, sleep for 3 minutes 
                    print("Sleeping for 3 minutes.\n")
                    sleep(180)


        else:
            print("Doing Quick Test. \n")
            do_quick_test()
        

    else:
        exit_loop = 1
        break
        
exit
