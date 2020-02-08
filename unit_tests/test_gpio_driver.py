#! /usr/bin/python 
import ctypes 
import sys
import os 
import time 

# gpio_dma.so loaded to the python file 
# using fun.myFunction(), 
# C function can be accessed 
# but type of argument is the problem. 
fun = ctypes.CDLL(os.path.abspath('../lib/gpio_driver.so'))
fun.get_byte.restype = ctypes.c_ubyte
#fun.get_byte.argtypes = [None]
fun.send_key_byte.argtypes = [ctypes.c_ubyte]
fun.send_data_byte.argtypes = [ctypes.c_ubyte]
fun.set_debug_flag(0x00)

# Now whenever argument  
# will be passed to the function                                                         
# ctypes will check it.             
#fun.usage.argtypes(ctypes.c_wchar_p) 
  
# now we can call this  
# function using instant (fun) 
# returnValue is the value  
# return by function written in C  
# code 
returnVale = fun.init()
        
fun.send_key_byte(0x6b)
array = [0x68, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x77, 0x6F, 0x72, 0x6C, 0x64]
print(array)
for i in range(0,9):
    start = time.time()
    values = []
    for x in array:
        fun.send_data_byte(x)
        val = fun.get_byte()
        values.append(val)
        time.sleep(.2)
    print(values)
    print("Transaction finished. Time = ", time.time()-start)
