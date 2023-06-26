import csv
import math
import matplotlib.pyplot as plt
file_path = 'data1.csv'

class Detector:
    def __init__(self):
        self.x = [0]
        self.y = [0]
        self.det = [0]

    def detect(self, data):
        if len(data) > 2:
            self.x.append(float(data[1])/1000000)
            self.y.append((float(data[0])))
            self.det.append((float(data[2])))
            # print(f"{float(data[1])/1000000}, {float(data[0])}")
        # self.filtred.append(self.filtred[-1]*0.8 + self.ylog[-1]*0.2)

    def draw(self):
        fig, ax = plt.subplots()

        ymax = max(self.y)
        self.det = [i*ymax for i in self.det]
        # Plot the data
        ax.plot(self.x, self.y)
        ax.plot(self.x, self.det)
        # ax.plot(self.x, self.filtred)

        # Set labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Line Plot')
        
        plt.grid()
        # Show the plot
        plt.show()
        



def main():
    detector = Detector()
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Process each row of data
                detector.detect(row)
    except FileNotFoundError:
        print("File not found.")

    detector.draw()


if __name__ == "__main__":
    main()