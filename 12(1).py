import scipy as sy
import pylab as pyl

from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

import turtle

class frequency:
    def __init__(self,array_parsed,channel):
        self.pitch = []
        self.freq_data = self.get_frequency(array_parsed,channel)
        for a in self.freq_data:
            self.pitch.append(
                self.pitch_func(a)
            )

    def get_frequency(self,array_parsed,channel):
        self.freq_data = []
        self.freq_amp = []
        for i in range(len(array_parsed)):
            self.sub = []
            self.test = array_parsed[i]
            self.test = self.test[int(0.3*len(self.test)):]
            self.adjust_constant = int(AudioClip[0] / len(self.test))
            self.test *= self.adjust_constant
            for a in self.test:
                self.sub.append(a[0]+a[1])
            self.Sub = list(abs(fftpack.fft(self.sub)))
            self.Sub = self.Sub[:int(0.5 * len(self.Sub))]
            self.freq_amp.append(max(self.Sub))
            if max(self.Sub) > 1e+2:
                a = max(self.Sub)
                self.freq_data.append(self.Sub.index(a))
            else:
                self.freq_data.append(0)

        return self.freq_data

    def pitch_func(self, freq):
        lib_length = 49
        A2 = 110  # index=0
        alphabet = 'AaBCcDdEFfGg'
        freq_lib = []
        diff = []
        for a in range(lib_length):
            a = 2 ** (a / 12)
            freq_lib.append(int(A2 * a))
        for a in freq_lib:
            diff.append(abs(freq - a))
            x = min(diff)
            y = diff.index(x)
        if freq != 0:
            m = y // 12
            n = y % 12
            o = alphabet[n] + str(m+2)
        elif freq == 0:
            o = '0'
        return o

class parse:
    def __init__(self,bpm,acc,arr):
        self.data_per_second = self.bpm_parcing(bpm,acc)
        self.output = self.par(arr,self.data_per_second)

    def bpm_parcing(self,bpm,acc):
        bps = bpm/60
        sps = bps*acc
        data_ps = int(AudioClip[0]/sps)
        return data_ps

    def par(self,arr,data_ps):
        parse_output = []
        parse_temp = []
        index = 0
        for i in arr:
            index+=1
            parse_temp.append(i)
            if index == data_ps:
                parse_output.append(parse_temp)
                parse_temp = []
                index = 0
        return parse_output

bpm = 96
accuracy = 4
output = []
AudioClip = wavfile.read('C:\\Users\\T480S\\Desktop\\test8.wav',True)
array = np.array(AudioClip[1])
parsed = parse(bpm,accuracy,array)
array_parsed = parsed.output
print(array_parsed[0])

frequency_data = frequency(array_parsed,1) # Channel is 0 or 1(not effect)
print(frequency_data.freq_data, frequency_data.pitch)

'''
plt.figure()
plt.plot(frequency_data.freq_data,'b--',linewidth=1)
plt.grid(True)
plt.show()
'''

pitch_range = 5 # the number of acceptable range *12
alphabet = 'AaBCcDdEFfGg'
pitch_lib = []
for i in range(pitch_range*12+1):
    pitch_lib.append(alphabet[i%12]+str(i//12+2))
print(pitch_lib,len(pitch_lib))

length = len(frequency_data.pitch)*15+120
width = (len(pitch_lib)+1)*15+120

t = turtle.Turtle()
t.screen.screensize(length,width,"White")
t.speed(50)
t.hideturtle()

for a in range(len(pitch_lib)):
    t.pencolor('Grey')
    t.penup()
    t.goto(-length//2+60,-(width//2-30-(15*a)))
    t.pendown()
    t.goto(length//2-120,-(width//2-30-(15*a)))
    t.penup()
    t.goto(-length//2+30,-(width//2-30-(15*a)))
    t.write(pitch_lib[a], False, align="center", font=("Times New Roman", 15, "normal"))
for a in range(len(frequency_data.pitch)):
    if frequency_data.pitch[a] != '0':
        index = pitch_lib.index(frequency_data.pitch[a])
        t.penup()
        t.goto(-length // 2 + 60 + (15 * a), -(width // 2 - 45 - (15 * index)))
        t.dot(15, "Black")
    if a%accuracy== 0:
        t.penup()
        t.goto(-length// 2 + 60 + (15 * a),-(width//2-30))
        t.pendown()
        t.goto(-length// 2 + 60 + (15 * a),-(width//2-30-(15*len(pitch_lib))))
t.screen.exitonclick()