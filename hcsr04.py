#!/usr/bin/env python
#
# HC-SR04 interface code for the Raspberry Pi
#
# William Henning @ http://Mikronauts.com
#
# uses joan's excellent pigpio library
#
# Does not quite work in one pin mode, will be updated in the future
#

import time
import pigpio
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
def _echo1(gpio, level, tick):
   global _high
   _high = tick

def _echo0(gpio, level, tick):
   global _done, _high, _time
   _time = tick - _high
   _done = True

def readDistance2(_trig, _echo):
   global pi, _done, _time
   _done = False
   pi.set_mode(_trig, pigpio.OUTPUT)
   pi.gpio_trigger(_trig,50,1)
   pi.set_mode(_echo, pigpio.INPUT)
   time.sleep(0.0001)
   tim = 0
   while not _done:
      time.sleep(0.001)
      tim = tim+1
      if tim > 50:
         return 9999
   return _time

pi = pigpio.pi('localhost',1234)

if __name__ == "__main__":
   my_echo1 = pi.callback(10, pigpio.RISING_EDGE,  _echo1)
   my_echo0 = pi.callback(10, pigpio.FALLING_EDGE, _echo0)
   my_echo1 = pi.callback(25, pigpio.RISING_EDGE,  _echo1)
   my_echo0 = pi.callback(25, pigpio.FALLING_EDGE, _echo0)
   my_echo1 = pi.callback(8, pigpio.RISING_EDGE,  _echo1)
   my_echo0 = pi.callback(8, pigpio.FALLING_EDGE, _echo0)
   my_echo1 = pi.callback(5, pigpio.RISING_EDGE,  _echo1)
   my_echo0 = pi.callback(5, pigpio.FALLING_EDGE, _echo0)
   my_echo1 = pi.callback(12, pigpio.RISING_EDGE,  _echo1)
   my_echo0 = pi.callback(12, pigpio.FALLING_EDGE, _echo0)
   my_echo1 = pi.callback(16, pigpio.RISING_EDGE,  _echo1)
   my_echo0 = pi.callback(16, pigpio.FALLING_EDGE, _echo0)

   while 1:

      #print "DISTANCE 1: ",(readDistance2(24,10)/58),"\tDISTANCE 2: ",(readDistance2(9,25)/58),"\tDI$
      #print "DISTANCE 2: ",(readDistance2(9,25)/58)
      #print "DISTANCE 3: ",(readDistance2(11,8)/58)
      #print "DISTANCE 4: ",(readDistance2(7,5)/58)
      #print "DISTANCE 5: ",(readDistance2(6,12)/58)
      #print "DISTANCE 6: ",(readDistance2(19,16)/58)
      mc.set("d1",(readDistance2(24,10)/58))
      mc.set("d2",(readDistance2(9,25)/58))
      mc.set("d3",(readDistance2(11,8)/58))
      mc.set("d4",(readDistance2(7,5)/58))
      mc.set("d5",(readDistance2(6,12)/58))
      mc.set("d6",(readDistance2(19,16)/58))
      time.sleep(0.1)

#   my_echo1.cancel()
#   my_echo0.cancel()
