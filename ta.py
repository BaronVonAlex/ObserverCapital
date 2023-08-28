import numpy
import talib
from numpy import genfromtxt


my_data = genfromtxt('5minCandle.csv', delimiter=',')
print(my_data)

close = my_data[:,4]

print(close)
# close = numpy.random.random(50)

# print(close)


# moving_average = talib.SMA(close, timeperiod = 10)

# print(moving_average)

rsi = talib.RSI(close)
print(rsi)