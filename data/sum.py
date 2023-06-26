import math
import matplotlib.pyplot as plt

x = [i/10 for i in range(100)]
y = [math.sin(i * math.pi) for i in x]
y2 = [math.sin(2 * i * math.pi) for i in x]
y3 = [math.sin(2 * i * math.pi + math.pi/8) for i in x]
sum = [y[i] + y2[i] for i in range(100)]
sum2 = [y[i] + y3[i] for i in range(100)]

sum3 = [sum2[i] - y2[i] for i in range(100)]

fig, ax = plt.subplots()

# # Plot the data
# ax.plot(x, y)
# ax.plot(x, y2)
# ax.plot(x, sum)
# ax.plot(x, sum2)
ax.plot(x, sum3)
ax.plot(x, y)

# ax.plot(self.x, self.filtred)

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Line Plot')

plt.grid()
# Show the plot
plt.show()