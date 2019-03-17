from pynput import keyboard
import pickle
import time
import keyboard
import numpy as np
import sys
import os

t_btw_key = 0
char_map = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 
            'p':15, 'q':16, 'r':17, 's':18, 't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24, 'z':25, 'space':26, '.':27, 
            'esc':28, 'enter': 29, 'UNK':30}
MAP_SIZE = 35

reverse_char_map = {char_map[char]:char for char in char_map}

digraph = np.zeros((MAP_SIZE, MAP_SIZE, 2)) #


def scanDir():
    arr = os.listdir(os.getcwd()+'/players/')
    print(arr)
    
    
def calculateLoss(digraph1, digraph2):
    
    vector1 = []
    vector2 = []
    
    for x, y in zip(digraph1, digraph2):
        if x and y:
            vector1.append(x)
            vector2.append(y)
            
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
            
#     print(len(vector1))
#     print(len(vector2))
    
#     return np.dot(vector1, vector2)/(np.sqrt(np.dot(vector1, vector1)) * np.sqrt(np.dot(vector2, vector2)))
    return np.sqrt(np.sum((vector1-vector2)**2)) if len(vector1)>0 else  sys.maxsize
    
            
print('welcome to keystroke\npress \'esc\' to start')

countDownTime = 0

keyboard.wait('esc')         

while(countDownTime > 0):
    print(countDownTime)
    countDownTime -= 1
    time.sleep(1)
    

print('start!')
print('"this is a simple paragraph that is meant to be nice and easy to type which is why there will be mommas no periods' + '\n' +
'or any capital letters so i guess this means that it cannot really be considered a paragraph but just a series of' + '\n' +
'run onsentences this should help you get faster at typing as im trying not to use too many difficult words in it' + '\n' + 
'although i thinkthat i might start making it hard by including some more difficult letters I\'m typing pretty quickly ' + '\n' +
'so forgive me for anymistakes i think that i will not just tell you a story about the time i went to the zoo and ' + '\n' +
'found a monkey and a fox playingtogether they" \n credit: text from https://10fastfingers.com/text/119-A-simple-Paragraph-to-practice-simple-typing')

recorded = keyboard.record(until='esc')
event_list = [(event.name,event.time) for event in recorded if event.event_type=='down']


for i in range(1, len(event_list)):
    first = event_list[i-1]
    second = event_list[i]
    dif = second[1] - first[1]
    
    if (first[0] not in char_map):
        first = ('UNK', first[1])
    if (second[0] not in char_map):
        second= ('UNK', second[1])
        
    digraph[char_map[first[0]]][char_map[second[0]]][0] += dif
    digraph[char_map[first[0]]][char_map[second[0]]][1] += 1
    
    
digramDiff = []


for i in range(len(char_map)):
    for j in range(len(char_map)):
        if (digraph[i][j][1]):
            print(reverse_char_map[i], reverse_char_map[j], digraph[i][j][0]/digraph[i][j][1])
            digramDiff.append(digraph[i][j][0]/digraph[i][j][1])
        else:
            digramDiff.append(0)

            
while (input()):
    print('press enter to continue')
    pass


if (len(sys.argv) > 1):
    playerfile = open(os.getcwd()+"/players/"+sys.argv[1], 'wb')
    pickle.dump(digramDiff, playerfile)
else:
    print("player list ")
    scanDir()
    print("type player-1's name")
    p1name = input()
    print("type player-2's name")
    p2name = input()
    
    with open(os.getcwd()+"/players/"+p1name, 'rb') as file:
        p1 = pickle.load(file)
    
    with open(os.getcwd()+"/players/"+p2name, 'rb') as file:
        p2 = pickle.load(file)
    
    p1Loss = calculateLoss(p1, digramDiff)
    p2Loss = calculateLoss(p2, digramDiff)
    
    print(p1Loss)
    print(p2Loss)
    
    print('I guess it\'s '+ p1name if p1Loss < p2Loss else p2name)
    