#! /usr/bin/python 
import ctypes 
import sys
import os 

NUM = 16      
# gpio_dma.so loaded to the python file 
# using fun.myFunction(), 
# C function can be accessed 
# but type of argument is the problem. 
                         
fun = ctypes.CDLL(os.path.abspath('./gpio_dma.so'))
print fun

# Now whenever argument  
# will be passed to the function                                                         
# ctypes will check it.             
#fun.usage.argtypes(ctypes.c_wchar_p) 
  
# now we can call this  
# function using instant (fun) 
# returnValue is the value  
# return by function written in C  
# code 
returnVale = fun.usage(sys.argv[0])
