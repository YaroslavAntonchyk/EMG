import csv
import math
import matplotlib.pyplot as plt

file_path = 'data1.csv'

SIZE = 128
TRESHOLD = 0.01
sigPhase = math.pi / 4
sigK = 3
y = []

class CoefsDFT:
    def __init__(self, freq, magnitude):
        self.freq = freq
        self.magnitude = magnitude
        self.magLength = self.length(self.magnitude)

    def print(self):
        len  = math.sqrt(self.magnitude.real*self.magnitude.real + self.magnitude.imag*self.magnitude.imag) / SIZE
        print(f"freq {self.freq}, real {self.magnitude.real}, imag {self.magnitude.imag}, len {len}")

    def length(self, magnitude):
        return math.sqrt(magnitude.real*magnitude.real + magnitude.imag*magnitude.imag) / SIZE

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
        output.append(CoefsDFT(k, intSum))
    return [i for i in output if math.sqrt(i.magnitude.real*i.magnitude.real + i.magnitude.imag*i.magnitude.imag) / SIZE > TRESHOLD]

def signalExtractor(sampleIds, coefsDftArr):
    signals = []
    n = len(coefsDftArr)
    coefsDftArrSort = coefsDftArr
    coefsDftArrSort = [coefsDftArrSort[i] for i in range(0, math.ceil(len(coefsDftArrSort) / 2))]
    coefsDftArrSort.sort(reverse=True, key=(lambda coefDft: coefDft.magLength))
    coefsDftArrSort = coefsDftArrSort[0:6]
    for i in range(math.ceil(n / 2)):
        # if i in [coef.freq for coef in coefsDftArrSort]:
            yCosFront = [math.cos((2*math.pi)/SIZE * coefsDftArr[i].freq * sampleId) for sampleId in sampleIds]
            ySinFront = [math.sin((2*math.pi)/SIZE * coefsDftArr[i].freq * sampleId) for sampleId in sampleIds]
            yCosBack = [math.cos((2*math.pi)/SIZE * coefsDftArr[n - i - 1].freq * sampleId) for sampleId in sampleIds]
            ySinBack = [math.sin((2*math.pi)/SIZE * coefsDftArr[n - i - 1].freq * sampleId) for sampleId in sampleIds]
            signals.append([(yCosFront[id]*coefsDftArr[i].magnitude.real/SIZE - ySinFront[i]*coefsDftArr[i].magnitude.imag/SIZE) \
                            + (yCosBack[id]*coefsDftArr[n - i - 1].magnitude.real/SIZE - ySinBack[n - i - 1]*coefsDftArr[i].magnitude.imag/SIZE) for id in sampleIds])
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
        offset = 1925
        x = data["idx"][offset:offset+SIZE]
        x = [i - offset for i in x]
        y = data["value"][offset:offset+SIZE]
        # breakpoint()
        x = [i for i in range(SIZE)]
        y = [complex(math.cos(((2*math.pi)/SIZE) * sigK * x1 + sigPhase) + 0.5*math.cos(((2*math.pi)/SIZE) * 20 * x1 + sigPhase), 0.0) for x1 in x]
        coefsDftArr = dft(y)
        correlatedSignals = signalExtractor(x, coefsDftArr)

        yReal = [i.real for i in y]
        # ySum = [yReal[i] - ((yCos[i]*trusted[1][0].real/SIZE - ySin[i]*trusted[1][0].imag/SIZE) + (yCos1[i]*trusted[2][0].real/SIZE - ySin1[i]*trusted[2][0].imag/SIZE)) for i in x]
        for coef in coefsDftArr:
            coef.print() 
        yReal = [yReal[i] - correlatedSignals[0][i] for i in range(len(yReal))]
        ax.plot(x, yReal, label="golden")
        for i in range(0, len(correlatedSignals)):
            # if i == 7 or i == 8:
                ax.plot(x, correlatedSignals[i], label=f"dft{i}")

        ax.legend()

        # Set labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Line Plot')
        
        plt.grid()
        # Show the plot
        plt.show()

draw()
