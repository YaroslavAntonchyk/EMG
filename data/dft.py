import csv
import math
import matplotlib.pyplot as plt
import copy

# reference https://www.youtube.com/watch?v=ITnPS8HGqLo

file_path = 'data1.csv'

SIZE = 128
TRESHOLD = 0.01
sigPhase = math.pi / 4
sigK = 3
y = []

class CoefDFT:
    def __init__(self, freq, magnitude):
        self.freq = freq
        self.magnitude = magnitude
        self.magLength = self.length()

    def print(self):
        len  = math.sqrt(self.magnitude.real*self.magnitude.real + self.magnitude.imag*self.magnitude.imag) / SIZE
        print(f"freq {self.freq}, real {self.magnitude.real}, imag {self.magnitude.imag}, len {len}")

    def length(self):
        return math.sqrt(self.magnitude.real*self.magnitude.real + self.magnitude.imag*self.magnitude.imag) / SIZE

def dft(lst):
    N = SIZE
    K = N
    output = []
    for k in range(K):
        intSum = complex(0.0, 0.0)
        for n in range(N):
            realPart = math.cos(((2*math.pi)/N) * k * n)
            imagPart = math.sin(((2*math.pi)/N) * k * n)
            w = complex(realPart, -imagPart)
            intSum += lst[n] * w
        output.append(CoefDFT(k, intSum))
    output.append(CoefDFT(K, 0)) #add 0 conterpart
    # return [coef for coef in output if coef.length()] # > TRESHOLD]
    return output

def signalExtractor(sampleIds, coefsDftArr):
    signals = {}
    n = len(coefsDftArr)
    coefsDftArrSort = copy.deepcopy(coefsDftArr)
    coefsDftArrSort = coefsDftArrSort[0:math.ceil(n / 2)] #the second half is exactly the same
    coefsDftArrSort.sort(reverse=True, key=(lambda coefDft: coefDft.magLength))
    for coef in coefsDftArrSort:
        print(f"{coef.freq}, {coef.magLength}")
    for i in range(math.ceil(n / 2)):
        # if i in [coef.freq for coef in coefsDftArrSort]:
            yCosFront = [math.cos((2*math.pi)/SIZE * coefsDftArr[i].freq * sampleId) for sampleId in sampleIds]
            ySinFront = [math.sin((2*math.pi)/SIZE * coefsDftArr[i].freq * sampleId) for sampleId in sampleIds]
            yCosBack = [math.cos((2*math.pi)/SIZE * coefsDftArr[n - i - 1].freq * sampleId) for sampleId in sampleIds]
            ySinBack = [math.sin((2*math.pi)/SIZE * coefsDftArr[n - i - 1].freq * sampleId) for sampleId in sampleIds]
            signals[i] = [(yCosFront[id]*coefsDftArr[i].magnitude.real/SIZE - ySinFront[id]*coefsDftArr[i].magnitude.imag/SIZE) \
                            + (yCosBack[id]*coefsDftArr[n - i - 1].magnitude.real/SIZE - ySinBack[id]*coefsDftArr[n - i - 1].magnitude.imag/SIZE) for id in sampleIds]
            # signals.append([(yCosFront[id]*coefsDftArr[i].magnitude.real/SIZE - ySinFront[id]*coefsDftArr[i].magnitude.imag/SIZE) \
            #                + (yCosBack[id]*coefsDftArr[n - i - 1].magnitude.real/SIZE - ySinBack[id]*coefsDftArr[n - i - 1].magnitude.imag/SIZE) for id in sampleIds])
    return signals

def readData(filePath):
    data = {'value':[],
            'time':[],
            'state':[],
            'idx':[]}
    cnt = 0
    try:
        with open(filePath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Process each row of data
                if len(row) > 2:
                    data['value'].append(float(row[0]))
                    data['time'].append(float(row[1])/1000000)                    
                    data['state'].append(float(row[2]))
                    data['idx'].append(cnt)
                    cnt += 1

    except FileNotFoundError:
        print("File not found.")
    
    return data

def draw():
        fig, ax = plt.subplots()
        data = readData('data1.csv')
        offset = 3750 #1925 # Useful part of signal 
        x = data["idx"][offset:offset+SIZE]
        x = [i - offset for i in x] # start x from 0
        y = data["value"][offset:offset+SIZE]
        state = data["state"][offset:offset+SIZE]

        timePassed = 0
        for i in range(offset + 1, offset+SIZE):
            # print((data["time"][i] - data["time"][i - 1]) *1000000)
            timePassed += (data["time"][i] - data["time"][i - 1])
        print(f"Sampling time {int(timePassed/(SIZE-1)) * 1000000} us")
        samplingFreq = 1/(timePassed/(SIZE-1))
        
        
        # hardcoded testing vectors 
        # x = [i for i in range(SIZE)]
        # y = [complex(math.cos(((2*math.pi)/SIZE) * sigK * x1 + sigPhase) + 0.5*math.cos(((2*math.pi)/SIZE) * 20 * x1 + sigPhase), 0.0) for x1 in x]

        coefsDftArr = dft(y)
        correlatedSignals = signalExtractor(x, coefsDftArr)

        freq = []
        magLength = []
        for coefDft in coefsDftArr[1:int(SIZE/2)]:
           freq.append(int(coefDft.freq*samplingFreq/SIZE))
           magLength.append(coefDft.magLength)
        plt.bar(freq, magLength)

        ax.set_xlabel('Frequency')
        ax.set_ylabel('Magnitude')

        plt.show()

        # yReal = [i.real for i in y]
        # for coef in coefsDftArr:
        #     coef.print()
        # ax.plot(x, yReal, label="golden")
        # # ax.plot(x, [yReal[i] - correlatedSignals[8][i] for i in range(len(yReal))], label="modified") # example how to remove part of a signal 

        # term789 = [v1 + v2 + v3 for v1, v2, v3, v4 in zip(correlatedSignals[7], correlatedSignals[8], correlatedSignals[9], correlatedSignals[0])]
        # # ax.plot(x, term789, label="Max correlation ")

        # ax.plot(x, [yReal[i] - term789[i] for i in range(len(yReal))], label="modified")

        # #for i in correlatedSignals.keys():
        # #    ax.plot(x, correlatedSignals[i], label=f"dft{i}")

        # ax.plot(x, correlatedSignals[0], label=f"dft{0}")
        
        # ax.plot(x, [i*200 for i in state], label=f"state")

        # ax.legend()

        # # Set labels and title
        # ax.set_xlabel('X-axis')
        # ax.set_ylabel('Y-axis')
        # ax.set_title('Line Plot')
        
        # plt.grid()
        # # Show the plot
        # plt.show()

draw()
