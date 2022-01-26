import os
from statistics import median
import struct
import matplotlib.pyplot as plt
import math as m

dataFile = open(os.path.abspath("E:/DATA.hex"), mode='rb')

# Functions for handling data arrays
def smoothData(inArr, avgCount):
    avgCount -= 1
    outArr = []
    for ii in range(len(inArr)-avgCount):
        outArr.append(sum(inArr[ii:ii+avgCount]) /avgCount)
    return(outArr)

def dotProd(arrArr):
    outArr = []
    for ii in range(len(arrArr[0])):
        fooVal = 0
        for jj in range(len(arrArr)):
            # print(str(ii) + " " + str(jj))
            fooVal += pow(arrArr[jj][ii], 2)
        
        outArr.append(m.sqrt(fooVal))
    
    return(outArr)



dataRead = {
    "throttle": [],
    "acc_X": [],
    "acc_Y": [],
    "acc_Z": [],
    "gyro_X": [],
    "gyro_Y": [],
    "gyro_Z": [],
}

timeStamps = []
seconds = []
readGaps = []

while True:
    readVal = dataFile.read(4)
    if len(readVal) < 4: 
        break
    timeStamps.append(struct.unpack("I", readVal)[0])
    seconds.append(timeStamps[-1]/1000000)
    # print(timeStamps[-1])
    if len(timeStamps) > 1:
        readGaps.append(timeStamps[-1]-timeStamps[-2])
        # print(readGaps[-1])
    
    readVal = dataFile.read(2)
    dataRead["throttle"].append(10*struct.unpack("h", readVal)[0])
    
    readVal = dataFile.read(2)
    dataRead["acc_X"].append(struct.unpack("h", readVal)[0] /8192) # for range of 1-2 g, divide by 8192
    
    readVal = dataFile.read(2)
    dataRead["acc_Y"].append(struct.unpack("h", readVal)[0] /8192) # for range of 1-2 g, divide by 8192
    
    readVal = dataFile.read(2)
    dataRead["acc_Z"].append(struct.unpack("h", readVal)[0] /8192) # for range of 1-2 g, divide by 8192
    
    readVal = dataFile.read(2)
    dataRead["gyro_X"].append(struct.unpack("h", readVal)[0] /131) # for 250 deg/s range, div by 131
    
    readVal = dataFile.read(2)
    dataRead["gyro_Y"].append(struct.unpack("h", readVal)[0] /131) # for 250 deg/s range, div by 131
    
    readVal = dataFile.read(2)
    dataRead["gyro_Z"].append(struct.unpack("h", readVal)[0] /131) # for 250 deg/s range, div by 131
    # dataRead[""].append(struct.unpack("h", readVal)[0])
    # print(throttle[-1])
    
    readVal = dataFile.read(2)
    
    # readVal = dataFile.read(14)

    # readVal = dataFile.read(4) # ignore testing value
    
    # print("---")
    
#Done reading data    
dataFile.close()

print("Average sample time, Median sample time, Max sample time")
print(str(sum(readGaps) / len(readGaps)) + ',' + str(median(readGaps)) + ',' + str(max(readGaps)) )


# Code for custom color palletes I made a while ago, just pasting it in so the graphs are slightly prettier
#Uncomment one to select

# OG
# colorSet = ["13293d","e9d6ec", "66d7d1","559bb2", "445e93", "fcbf49","d62828"]

# Some Purple
# colorSet = ["000021", "FFDDD2", "86BBD8", "33658A", "4C1A57", "C45BAA", "DE1A1A"]

# Browns
colorSet = ["210124","e5fcf5",  "e28413", "dc6e27", "885053", "d5573b", "ec91d8","ffd3da"]

# Greens
# colorSet = ["351431","d1d3c4","4b5842","27463c","023436","5998c5","f87666"]

# Purple Gradient
# colorSet = ["420039","f6f2ff","dcccff","e07be0","932f6d","dea4f0","ba55a7","ff6663","ee4266"]

# Forest
# colorSet = ["1a1f16","efd0ca","68aa64","664a54","8f1429","345830","62362d","a5907e","d36135"]

# BlueGundy
# colorSet = ["220901","ffb997","2e5077","646e68","0fa3b1","598889","4ecdc4","b3dec1","bc4749","f67e7d"]

for ii in range(len(colorSet)): colorSet[ii] = "#" + colorSet[ii]

# load nice colors for reference
baseCol = colorSet[0]
textCol = colorSet[1]

lightCol = colorSet[2]
midCol = colorSet[3]
darkCol = colorSet[4]

goodCol = colorSet[-2]
badCol = colorSet[-1]

scatterColSet = colorSet[2:] + colorSet[0:2] #Use text and base cols last in case of emergency

plt.rcParams['text.color'] = textCol
plt.rcParams['axes.labelcolor'] = textCol
plt.rcParams['axes.edgecolor'] = textCol
plt.rcParams['xtick.color'] = textCol
plt.rcParams['ytick.color'] = textCol


fig, (ax_acc, ax_gyro) = plt.subplots(1, 2)
fig.suptitle('Bike IMU DAQ Test')
ax_acc.set_facecolor(baseCol +"ff")
ax_gyro.set_facecolor(baseCol +"ff")
fig.patch.set_facecolor(baseCol)

avgCount = 2
secSmooth = smoothData(seconds, avgCount)

ax_acc.plot(secSmooth, smoothData(dataRead["acc_X"], avgCount), label="acc_X", color= scatterColSet[0])
ax_acc.plot(secSmooth, smoothData(dataRead["acc_Y"], avgCount), label="acc_Y", color= scatterColSet[1])
ax_acc.plot(secSmooth, smoothData(dataRead["acc_Z"], avgCount), label="acc_Z", color= scatterColSet[2])

ax_acc.plot(secSmooth, smoothData(dotProd([dataRead["acc_X"],dataRead["acc_Y"],dataRead["acc_Z"]]), avgCount), label="acc_dot", color= scatterColSet[3])

ax_acc.set_title('Acceleration (g) vs time (s)')


# ax_acc.plot(seconds, dataRead["acc_X"], label="acc_X")
# ax_acc.plot(seconds, dataRead["acc_Y"], label="acc_Y")
# ax_acc.plot(seconds, dataRead["acc_Z"], label="acc_Z")

ax_gyro.plot(secSmooth, smoothData(dataRead["gyro_X"], avgCount), label="gyro_X", color= scatterColSet[0])
ax_gyro.plot(secSmooth, smoothData(dataRead["gyro_Y"], avgCount), label="gyro_Y", color= scatterColSet[1])
ax_gyro.plot(secSmooth, smoothData(dataRead["gyro_Z"], avgCount), label="gyro_Z", color= scatterColSet[2])

# ax_gyro.plot(secSmooth, smoothData(dotProd([dataRead["gyro_X"],dataRead["gyro_Y"],dataRead["gyro_Z"]]), avgCount), label="acc_dot")

ax_gyro.set_title('Gyro (deg/s) vs time (s)')

# ax_gyro.plot(seconds, dataRead["gyro_X"], label="gyro_X")
# ax_gyro.plot(seconds, dataRead["gyro_Y"], label="gyro_Y")
# ax_gyro.plot(seconds, dataRead["gyro_Z"], label="gyro_Z")

for ax_foo in [ax_acc, ax_gyro]:
    ax_foo.legend()
    legend = ax_foo.legend()
    frame = legend.get_frame()
    frame.set_facecolor(baseCol)
    frame.set_edgecolor(textCol)


plt.show()
plt.close()

# plt.hist(readGaps, bins = 100)
# plt.show()