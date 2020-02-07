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
        
fun.send_key_byte(0x01)
array = [0x01, 0x03, 0x05, 0x07, 0x09, 0x0b, 0x0d, 0x0f, 0x1f, 0x2f]

while True:
    start = time.time()
    for x in array:
        fun.send_data_byte(x)
        val = fun.get_byte()
        time.sleep(1)
    print("Transaction finished. Time = ", time.time()-start)
