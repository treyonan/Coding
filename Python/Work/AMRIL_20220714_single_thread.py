# -*- coding: utf-8 -*-
"""
AMRIL (Autonomous Mobile Robot Interface Layer), version 1.2
Last edit 20220714

Features added:
- single thread design
"""

from threading import Thread
import time
import requests, json
import MiR_missions
from tkinter import *
import tkinter.font as font
from pylogix import PLC

with PLC() as comm:
    comm.IPAddress = "10.200.24.131"

AMR_ip_List = [     #List of available AMRs. The index will be read from PLC
    "192.168.12.20",
    "192.168.12.30"
]

host = 'http://192.168.12.20/api/v2.0.0/'   # default value for direct connection to AMR. Overwritten by PLC index if connected to PLC

# Format Headers
headers = {}
headers['Content-Type'] = 'application/json'
headers['Authorization'] = 'Basic RGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=='


def get_host() -> str:
    index = int(comm.Read('AMR_Index').Value)                    # Read index from PLC to determine which AMR ip to use
    ip = AMR_ip_List[index]
    host = 'http://' + ip + '/api/v2.0.0/'
    return host

def post_mission(host, headers, mission_string):
    mission_guid = MiR_missions.guid_table[mission_string]
    mission_id = {"mission_id": mission_guid}
    post_mission = requests.post(host + 'mission_queue', headers = headers, json = mission_id)
    print("Posted to AMR queue: " + mission_string)
    
def delete_queue(host, headers):
    requests.delete(host + 'mission_queue', headers = headers) 
    print("Deleted")

def change_state(host, headers, state_id_num):
    state_id = {"state_id": state_id_num}       # From API... Choices are: {3, 4, 11}, State: {Ready, Pause, Manualcontrol}
    requests.put(host + 'status', headers = headers, json = state_id)
    print("Status changed to " + str(state_id_num))

def clear_error_status(host, headers):
    clear_error = {"clear_error": bool(1)}
    requests.put(host + 'status', headers = headers, json = clear_error)
    print("Error status reset")

def read_AMR_PLC_register(host, headers, register_id) -> str:
    PLC_register_contents = requests.get(host + 'registers/' + str(register_id), headers = headers)
    json_dict = json.loads(PLC_register_contents.text)
    return json_dict['value']

def write_AMR_PLC_register(host, headers, register_id, new_value) -> str:
    json_PutRegister = {"value": new_value}
    PLC_register_set = requests.put(host + 'registers/' + str(register_id) , headers = headers, json = json_PutRegister)
    print("PLC Register: " + str(register_id) + " | Return: " + PLC_register_set.text)
    json_dict = json.loads(PLC_register_set.text)
    return json_dict['value']
    

def background():
    thread: Thread = Thread(target = __background__)
    thread.daemon = True
    thread.start()

def __background__():    
    global host
    
    # AMR PLC IDs
    door_id = 30
    east_id = 31
    west_id = 32

    # Initialization
    east_removing = False
    west_removing = False

    Post_Mission_Previous = False
    Delete_Queue_Previous = False
    Pause_Previous = False
    Start_Previous = False
    Post_Mission = False
    Delete_Queue = False
    Pause = False
    Start = False


    while True:
        east_AMR_status = read_AMR_PLC_register(host, headers, east_id)
        west_AMR_status = read_AMR_PLC_register(host, headers, west_id)

        # DOOR COMMANDS
        if comm.Read('Program:Haas_VF1_1.RobotOutput.Status').Value == 0 :                  # if robot status is idle (0)
            if read_AMR_PLC_register(host, headers, door_id) == 1 :                         # if amr plc register for door command (30) is 1
                comm.Write('Program:Haas_VF1_2.OpenSafetyDoor', 1)                          # open door
                write_AMR_PLC_register(host, headers, door_id, 0)               # write amr plc register for door command to 0

        if read_AMR_PLC_register(host, headers, door_id) == -1 :                            # if amr plc register for door command (30) is -1
            comm.Write('Program:Haas_VF1_2.OpenSafetyDoor', 0)                              # close door
            if comm.Read('Program:Haas_VF1_1.SafetyOutput.SafetyDoorClosed').Value == 1 :   # if the safety door is closed (according to sensor)
                write_AMR_PLC_register(host, headers, door_id, 0)               # write amr plc register for door command to 0


        # AUTO REMOVE EAST
        if east_removing == False : # if not already in east pallet removal process
            if comm.Read('Haas_VF1_1.PalletStatus').Value == 0 :  # if east pallet parts are complete (0)
                post_mission(host, headers, 'Remove East Pallet') # queue amr east removal mission
                east_removing = True

        if east_removing == True :
            if east_AMR_status == -2 : # if status is "Removed"
                comm.Write('Haas_VF1_1.PalletStatus', -1)
                write_AMR_PLC_register(host, headers, east_id, 0)               # write amr plc register for east mission status to "No action" (0)
                east_removing = False

        # AUTO REMOVE WEST
        if west_removing == False : # if not already in west pallet removal process
            if comm.Read('Haas_VF1_2.PalletStatus').Value == 0 :  # if west pallet parts are complete (0)
                post_mission(host, headers, 'Remove West Pallet') # queue amr west removal mission
                west_removing = True

        if west_removing == True :
            if west_AMR_status == -2 : # if status is "Removed"
                comm.Write('Haas_VF1_2.PalletStatus', -1)
                write_AMR_PLC_register(host, headers, west_id, 0)               # write amr plc register for east mission status to "No action" (0)
                west_removing = False


        # CATCH REFILLS, UPDATE PALLET STATUSES
        if east_AMR_status == 2 : # if east pallet has been refilled
            comm.Write('Haas_VF1_1.PalletStatus', 1)
            write_AMR_PLC_register(host, headers, east_id, 0)                   # reset PLC register to "No action" (0)
        if west_AMR_status == 2 : # if west pallet has been refilled
            comm.Write('Haas_VF1_1.PalletStatus', 1)
            write_AMR_PLC_register(host, headers, west_id, 0)                   # reset PLC register to "No action" (0)



        # PLC button-reading portion
        Post_Mission = comm.Read('AMR_Commands.PostMission').Value
        Delete_Queue = comm.Read('AMR_Commands.DeleteQueue').Value
        Pause = comm.Read('AMR_Commands.Pause').Value
        Start = comm.Read('AMR_Commands.Start').Value     
        mission_string = comm.Read('Mission.Name').Value          # Mission name read from PLC to use to look up guid    
        
        host = get_host()

        if (Post_Mission and not Post_Mission_Previous):
            comm.Write('AMR_Commands.PostMission', 0)
            command = post_mission(host, headers, mission_string)     
        
        if (Delete_Queue and not Delete_Queue_Previous):
            comm.Write('AMR_Commands.DeleteQueue', 0)
            command = delete_queue(host, headers)
        
        if (Pause and not Pause_Previous):
            comm.Write('AMR_Commands.Pause', 0)
            command = change_state(host, headers, 4)        
        
        if (Start and not Start_Previous):
            comm.Write('AMR_Commands.Start', 0)
            command = change_state(host, headers, 3)

        Post_Mission_Previous = Post_Mission    # Each of these lines: reset bits each loop
        Delete_Queue_Previous = Delete_Queue
        Pause_Previous = Pause
        Start_Previous = Start

        time.sleep(.1)
     

def main():
    background()


    window = Tk()
    window.title("AMR Interface Layer - MiR 200")
    window.geometry("770x400")
    window.configure(bg = 'gray')

    bigFont = font.Font(size = 20, weight = 'bold')
    right_col = 400

    btn1 = Button(window, text = 'Charging routine', command = lambda: post_mission(host, headers, 'Charging routine'))
    btn1.place(x=10, y=10)
    btn2 = Button(window, text = 'Refill east pallet', command = lambda: post_mission(host, headers, 'Refill east pallet'),bg='yellow')
    btn2.place(x=10, y=40)
    btn2['font'] = bigFont
    btn3 = Button(window, text = 'Refill west pallet', command = lambda: post_mission(host, headers, 'Refill west pallet'),bg='yellow')
    btn3.place(x=10, y=100)
    btn3['font'] = bigFont
    btn4 = Button(window, text = 'Remove east pallet', command = lambda: post_mission(host, headers, 'Remove east pallet'))
    btn4.place(x=10, y=160)
    btn5 = Button(window, text = 'Remove west pallet', command = lambda: post_mission(host, headers, 'Remove west pallet'))
    btn5.place(x=10, y=190)
    btn6 = Button(window, text = 'Go to idle position (demo 3)', command = lambda: post_mission(host, headers, 'LTNG_HC demo 3'))
    btn6.place(x=10, y=220)

    btn100 = Button(window, text = 'Delete Queue', command = lambda: delete_queue(host, headers))
    btn100.place(x=right_col, y=10)
    btn101 = Button(window, text = 'Pause', command = lambda: change_state(host, headers, 4))
    btn101.place(x=right_col, y=40)
    btn102 = Button(window, text = 'Ready/Play', command = lambda: change_state(host, headers, 3),bg='light green')
    btn102.place(x=right_col, y=70)
    btn103 = Button(window, text = 'Reset', command = lambda: clear_error_status(host, headers))
    btn103.place(x=right_col, y=100)
    btn104 = Button(window, text = 'Door open', command = lambda: comm.Write('Program:Haas_VF1_2.OpenSafetyDoor', 1))
    btn104.place(x=right_col, y=130)
    btn105 = Button(window, text = 'Tell AMR door is open', command = lambda: write_AMR_PLC_register(host, headers, 30, 0))
    btn105.place(x=right_col, y=160)
    btn106 = Button(window, text = 'Door close', command = lambda: comm.Write('Program:Haas_VF1_2.OpenSafetyDoor', 0))
    btn106.place(x=right_col, y=190)
    

    window.mainloop()



if __name__ == "__main__":
    main()