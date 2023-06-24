import smbus, time, math
import matplotlib.pyplot as plt
import numpy as np

b = smbus.SMBus(1)

address = 0x0e

def read (x):
    return b.read_byte_data(address, x)

def write(a, v):
    b.write_byte_data(address, a, v)

def read_component(register):
    unsigned = b.read_word_data(address, register)
    return (unsigned & 0x7fff) - (unsigned & 0x8000)

write(0x1b, 0b11011000)

write(0x5c, 0x00)
write(0x5d, 0x00)

write(0x1c, 0x0c)

memory_size = 600 # better don't change this
time_threshold= 5 # in s
memory_size*=time_threshold

write(0x1d, 0x40)

j = 0
runtime = 0

while True:
    start_time = time.time()
    curr_time = 0
    i = 0
    data = np.full((memory_size,4), -1, dtype=float)
    while curr_time <= time_threshold:
        x = read_component(0x10)
        y = read_component(0x12)
        z = read_component(0x14)
        curr_time = time.time() - start_time
        data[i, :] = np.array([x,y,z,runtime])
        i+=1
    runtime = j*time_threshold
    j+=1
    #print(i)
    mask = np.full(memory_size,True)
    mask[data[:,0]==-1] = False
    data = data[mask,:]
    #print(curr_time)
    data = np.mean(data, axis=0)
    sensordat = np.linalg.norm(data[:3])
    print(f"{sensordat=}, measurement={j}, {runtime=}\n")
    with open('sensorsave.dat', 'ab') as f:
         np.savetxt(f,np.array([sensordat,data[-1]]))
    
