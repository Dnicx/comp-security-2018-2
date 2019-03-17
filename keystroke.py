from pynput import keyboard
import pickle
import time
import keyboard
import numpy as np
import sys
import os
    
def scanDir():
    arr = os.listdir(os.getcwd()+'/players/')
    print(arr)

t_btw_key = 0
char_map = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 
            'p':15, 'q':16, 'r':17, 's':18, 't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24, 'z':25, 'space':26, '.':27, 
            'esc':28, 'enter': 29, 'UNK':30}

reverse_char_map = {char_map[char]:char for char in char_map}

digraph = np.zeros((35, 35, 2))

            
print('welcome to keystroke\npress \'esc\' to start')

countDownTime = 3

keyboard.wait('esc')         

while(countDownTime > 0):
    print(countDownTime)
    countDownTime -= 1
    time.sleep(1)

print('start!')
print('"this is a simple paragraph that is meant to be nice and easy to type which is why there will be mommas no periods or any capital letters so i guess this means that it cannot really be considered a paragraph but just a series of run on sentences this should help you get faster at typing as im trying not to use too many difficult words in it although i think that i might start making it hard by including some more difficult letters I\'m typing pretty quickly so forgive me for any mistakes i think that i will not just tell you a story about the time i went to the zoo and found a monkey and a fox playing together they" \n credit: text from https://10fastfingers.com/text/119-A-simple-Paragraph-to-practice-simple-typing')
recorded = keyboard.record(until='esc')
event_list = [(event.name,event.time) for event in recorded if event.event_type=='down']
# print(event_list)
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
    
for i in range(31):
    for j in range(31):
        if (digraph[i][j][1]):
            print(reverse_char_map[i], reverse_char_map[j], digraph[i][j][0]/digraph[i][j][1])

while (input()):
    print
 
if (len(sys.argv) > 1):
    playerfile = open(os.getcwd()+"/players/"+sys.argv[1], 'wb')
    pickle.dump(digraph, playerfile)
else:
    print("player list ")
    scanDir()
    print("type player-1's name")
    p1 = input()
    print("type player-2's name")
    p2 = input()
    
    p1 = open(os.getcwd()+"/players/"+p1, 'wb')
    p1 = pickle.load(p1)
    
    p2 = open(os.getcwd()+"/players/"+p2, 'wb')
    p2 = pickle.load(p2)
    
    p1Loss = calculateLoss(p1, digraph)
    p2Loss = calculateLoss(p2, digraph)
    