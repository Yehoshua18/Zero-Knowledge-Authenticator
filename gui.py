import PySimpleGUI as sg
import time
from datetime import datetime
import serial as s
import random
import base64
from io import BytesIO
from PIL import Image, ImageTk


timePerEvent = 1#how long to wait on events - helpful for visual debugging
ffs_n = 4 #size of secret vector
ffs_t = 5 #number of times to repeat ffs the process
ffs_v = [
    3744408882063001396294212986181754183933885585535170396635241260553212535814524643482258517414709354259345424870989903393496092889322904873252705924305330704908057322007365128867533240900926677252[...]
    45651023775644004,
    110570283940336609,
    27168989764564521610019701636
]
hugePrime = 42128912467700374871094220277040581759072133206929937016960360003679041399273667850889159789015338717550634028262574112906901005657864893233410791958809102748651893371774096520055911214918[...]

#gets x from the tiva
def getx():
    global x
    device.write("what is x?\n".encode())
    x = int(device.readline().decode().replace("\r", "").replace("\n", ""))
    #print("x: ", x)
    if x == 0:
        return False
    return True

#send the binary numbers to the tiva
def sendbin():
    global a

    a = ""
    for i in range(ffs_n):
        a += str(random.randint(0, 1))
    device.write("here are a:\n".encode())
    device.write((a+"\n").encode())
    #print("a: ", a)

#get the y from the tiva
def gety():
    global y
    device.write("what is y?\n".encode())
    y = int(device.readline().decode().replace("\r", "").replace("\n", ""))
    #print("y: ", y)

#check that the tiva passed the round
def varifydevice():
    global x
    global a
    global y

    y2 = x
    for i in range(ffs_n):
        y2 *= ffs_v[i] ** int(a[i])
    #print("y2: ", y2)
    if y ** 2 % hugePrime != abs(y2) % hugePrime:
        return "DENIED"
    return "GRANTED"

#connect to the tiva and initiate two way handshake
def getDevice():
    global device
    #print("waiting 4 connection...")
    try:
        device = s.Serial(port="com12", baudrate=115200, timeout=.2)
        device.write(bytes("hello\n", 'utf-8'))
        answer = device.readline().decode().replace("\r", "").replace("\n", "")
        if answer == "world":
            #print("device connected.")
            return device
        else:
            pass
            #print(answer)
    except:
        pass
    device = None
    return False

#open the window
def init():
    global font1
    global gif
    global window
    global device

    device = None

    font1 = ("Courier New italic", 27)
    gif = sg.DEFAULT_BASE64_LOADING_GIF
    sg.theme('DarkGreen4')
    layout = [
        [sg.T(" ", size=(0, 10))],
        [sg.Text('Loading...', size=(200, 1),font=font1, key='text', justification='center')],
        [sg.T(" ", size=(0, 5))],
        [sg.ProgressBar(1000, size=(200, 10), bar_color='Black', key='progress')],
        [sg.T(" ", size=(0, 2))],
        [sg.Column([[sg.Image(data=gif, key='gif')]], justification="center")]
    ]
    window = sg.Window('Authenticating Tiva', layout, size=(900, 500))

#update the text and progress of the window and run the current stages function
def updateProgress(i, limit, eventInfo):
    global progBar
    global displayText
    global loadGif

    flag = False
    then = datetime.now()
    while flag == False:
        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            break
        displayText.update(eventInfo["text"].upper())
        loadGif.UpdateAnimation(gif, time_between_frames=100)
        if (i < limit):
            progBar.UpdateBar(i + 1)
            i += 1
        now = datetime.now()
        duration = now - then
        if duration.total_seconds() >= timePerEvent:
            flag = eventInfo["action"]() if eventInfo["action"] != None else None
            #print(flag)
    progBar.UpdateBar(limit)
    return flag

#main function which opens the window and authenticates a tiva
def main():
    global window
    global progBar
    global displayText
    global loadGif
    global accessGraned
    global device
    global authEvents

    authEvents = {
        "wait":{"event": "wait", "text": "waiting for device", "action": getDevice},
        "connect":{"event": "connect", "text": "connected...", "action": None},
        "getx":{"event": "getx", "text": "receiving X - round ", "action": getx},
        "sendbin":{"event": "sendbin", "text": "sending binary numbers - round ", "action": sendbin},
        "gety":{"event": "gety", "text": "receiving Y - round ", "action": gety},
        "varifydevice":{"event": "varifydevice", "text": "varifying device - round ", "action": varifydevice}
    }

    accessGranted = False
    init()
    progBar = window['progress']
    displayText = window['text']
    loadGif = window['gif']

    eventCount = len(authEvents)
    eventIndex = 0
    progress = 0
    progChunk= 1000 / (eventCount)

    #start the connection progress
    updateProgress(0 * progChunk, 1 * progChunk, authEvents["wait"])
    updateProgress(1 * progChunk, 2 * progChunk, authEvents["connect"])

    #run the tiva through the FFS authentication scheme
    for j in range(ffs_t):
        authEvents["getx"]["text"] += str(j+1)
        authEvents["sendbin"]["text"] += str(j + 1)
        authEvents["gety"]["text"] += str(j + 1)
        authEvents["varifydevice"]["text"] += str(j + 1)
        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            return
        updateProgress(2 * progChunk if j < 1 else 5 * progChunk, 3 * progChunk if j < 1 else 5 * progChunk, authEvents["getx"])
        updateProgress(3 * progChunk if j < 1 else 5 * progChunk, 4 * progChunk if j < 1 else 5 * progChunk, authEvents["sendbin"])
        updateProgress(4 * progChunk if j < 1 else 5 * progChunk, 5 * progChunk if j < 1 else 5 * progChunk, authEvents["gety"])
        flag = updateProgress(5 * progChunk if j < 1 else 5 * progChunk, 6 * progChunk if j == ffs_t - 1 else 5 * progChunk, authEvents["varifydevice"])
        authEvents["getx"]["text"] = authEvents["getx"]["text"][:-len(str(j+1))]
        authEvents["sendbin"]["text"] = authEvents["sendbin"]["text"][:-len(str(j+1))]
        authEvents["gety"]["text"] = authEvents["gety"]["text"][:-len(str(j+1))]
        authEvents["varifydevice"]["text"] = authEvents["varifydevice"]["text"][:-len(str(j+1))]
        if flag == "DENIED":
            #the tiva failed so exit
            accessGranted = False
            progBar.UpdateBar(6 * progChunk)
            break
        elif flag == "GRANTED" and j == ffs_t-1:
            accessGranted = True

    #the tiva passed - fetch image from tiva
    if accessGranted == True:
        displayText.update(text_color="green")
        displayText.update("ACCESS GRANTED")
        device.write("granted\n".encode())
        b64 = device.readline().decode().replace("\r", "").replace("\n", "")
        im = Image.open(BytesIO(base64.b64decode(b64)))
        image = ImageTk.PhotoImage(image=im)
        loadGif.update(data = image)

    #tiva failed
    else:
        loadGif.update(visible=False)
        displayText.update(text_color="red")
        displayText.update("ACCESS DENIED")

    #wait for window to close
    while True:
        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            return

if __name__ == "__main__":
    try:
        main()
    except:
        pass
