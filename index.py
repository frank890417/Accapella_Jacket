import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy
import soundfile as sf
import math
import time
step = math.pow(2,1/12)
fs=44100
chord = [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24]
# from pydub import AudioSegment
# from pydub.playback import play
duration=1
def sampleSound(duration=1):
    fs=44100
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
    print("Recording Audio")
    sd.wait()
    print("Audio recording complete , Play Audio")
    sd.play(myrecording, fs)
    sd.wait()
    print("Play Audio Complete")
    return myrecording

sound1 = sampleSound(1)
sound2 = sampleSound(1)
sound3 = sampleSound(1)
sound4 = sampleSound(1)
sound5 = sampleSound(1)
sound6 = sampleSound(1)

def getFreq(pitch):
    step = math.pow(2,1/12)
    pitch = -pitch
    nfs =  math.pow(step,pitch) * fs
    return nfs
    
def getPan(sound,pitch,volume=1):
    step = math.pow(2,1/12)
    pitch = -pitch
    nfs = int ( math.pow(step,pitch) * fs / step )
    sound = np.concatenate((np.array(sound),np.zeros(30000)))
#     print(np.arange(0,44100,1/nfs*fs))
#     ftsam = np.arange(0,1,1/nfs)*nfs
    indexes = [ int(val) for val in np.arange(0,len(sound),1/nfs*fs)]
    result = np.concatenate((np.array(sound[indexes]),np.zeros(30000)))
    return result*volume

layers = [
    {
        "label": "main",
        "sample": sound2,
        "volume": 4,
        "pan": 0,
        "song": list("1155665044332210"),
        "slice_factor": 16
    },
    {
        "label": "second",
        "sample": sound2,
        "volume": 4,
        "pan": 0.01,
        "song": list("1133443-2211221-"),
        "slice_factor": 16
    },
    {
        "label": "bass",
        "sample": sound1,
        "volume": 10,
        "pan": -12,
        "song": list("1-1-1-1-1-1-1-1-"),
        "slice_factor": 4
    },
#     {
#         "label": "bass2",
#         "sample": sound1,
#         "volume": 5,
#         "pan": -12,
#         "song": list("-5-5-5-5-5-5-5-5"),
#         "slice_factor": 8
#     },
    {
        "label": "bassdrum",
        "sample": sound4,
        "volume": 2,
        "pan": 0,
        "song": list("1---1---1---1---"),
        "slice_factor": 4
    },
    {
        "label": "snaredrum",
        "sample": sound5,
        "volume": 3,
        "pan": 0,
        "song": list("--1---1---1---1-"),
        "slice_factor": 4
    },
    {
        "label": "hihat",
        "sample": sound6,
        "volume": 3,
        "pan": 0,
        "song": list("-1-1-1-1-1-1-1-1"),
        "slice_factor": 4
    }
]

layers2 = [
    {
        "label": "main",
        "sample": sound1,
        "volume": 10,
        "pan": 0,
        "song": list("334554321123322-334554321123211-"),
        "slice_factor": 16
    },
    {
        "label": "main",
        "sample": sound1,
        "volume": 10,
        "pan": 0,
        "song": list("112332211122332-112332121123211-"),
        "slice_factor": 16
    },
    {
        "label": "main",
        "sample": sound1,
        "volume": 10,
        "pan": -12.01,
        "song": list("334554321123322-334554321123211-"),
        "slice_factor": 2
    },
    {
        "label": "bass",
        "sample": sound3,
        "volume": 10,
        "pan": -24,
        "song": list("111111111111111-111111111111111-"),
        "slice_factor": 4
    },
    
]


def smoother(data):
    for i in range(100):
        data[i] *= 1/ (1+math.pow(i,2))


noteSpan = 18000
al = noteSpan*2

rendered = []

songLen = len(layers[0]['song'])
songDataLen = songLen*(al+30000)+100000
allsong = np.zeros(songDataLen)

for layerIndex,layer in enumerate(layers):
    layerAudio= np.zeros(songDataLen)
    
    print("#{} {} (*{}): ".format(layerIndex,layer['label'],layer['volume']),end='')
    
    
    for index,note in enumerate(layer['song']):
        print(note,end='')
        useNote = int(note)-1 if note!="-" else 0
        useVolume = 1 if note!="-" else 0
        useFreq = getFreq(useNote)-44100
        startIndex = index*noteSpan
        
        SingleAudio =  getPan(layer['sample'][:,0],chord[useNote]+ layer['pan'],useVolume)
        SingleAudio =  np.concatenate((SingleAudio, np.zeros(50000)))[int(fs/layer['slice_factor']):]
        singleLen = len(SingleAudio)
        layerAudio = layerAudio +  np.concatenate((np.zeros(startIndex),SingleAudio,np.zeros(songDataLen-singleLen-startIndex)))
        
    print("")
    rendered.append(layerAudio*layer['volume'])

for layerRendered in rendered:
    allsong = allsong + np.resize(layerRendered,np.shape(np.array(allsong)))
        
sd.play(allsong,44100)