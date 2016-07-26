import serial
import time

wake=b'\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x03\xfd\xd4\x14\x01\x17\x00'
read=b'\x00\x00\xff\x04\xfc\xd4\x4a\x01\x00\xe1\x00'

ser = serial.Serial('/dev/ttyAMA0', 115200)

print("Graw")
ser.write(wake)
print("Wrote")
print(ser.read(15))
time.sleep(0.1)
print("Started")

c = 0

while True:
    ser.write(read)
    rx = ser.read(25)
    id = "".join(list([str(x) for x in rx]))
    ids = {"00255025500025512244213751104842547226195360": "BBC",
           "00255025500025512244213751104841012498771530": "Go",
           "0025502550002551224421375110484154736416380": "QUT Student",
           "00255025500025512244213751102244522092532350": "USQ Student",
           "00255025500025512244213751104843322512567120": "Round"}
    if id in ids:
        print(str(c).zfill(4)+" That's the "+ids[id]+" card!")
    c+=1


ser.close()