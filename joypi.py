import time
import signal
import pygame
import sys
import RPi.GPIO as GPIO
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
# The following is an example code written to controll the l298n motor contoller
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) #input-1
GPIO.setup(12, GPIO.OUT) #input-2
GPIO.setup(15, GPIO.OUT) #input-3
GPIO.setup(16, GPIO.OUT) #input-4
GPIO.setup(7, GPIO.IN) #Front Edge
GPIO.setup(13, GPIO.IN) #Back Edge
  
pygame.init()
 
done = False
# Initialize the joysticks
pygame.joystick.init()

################ Movement Definitions BEGIN #######################
def forward_left():
    print "FL"
    GPIO.output(11, False)
    GPIO.output(12, False)
    GPIO.output(16, True)
    GPIO.output(15, False)

def forward_right():
    print "FR"
    GPIO.output(11, True)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(15, False)
 
def backward_left():
    print "BL"
    GPIO.output(11, False)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(15, True)

def backward_right():
    print "BR"
    GPIO.output(11, False)
    GPIO.output(12, True)
    GPIO.output(16, False)
    GPIO.output(15, False)
   
def forward():
    print "F"
    GPIO.output(11, True)
    GPIO.output(12, False)
    GPIO.output(16, True)
    GPIO.output(15, False)

def backward():
    print "B"
    GPIO.output(11, False)
    GPIO.output(12, True)
    GPIO.output(16, False)
    GPIO.output(15, True)

def left():
    print "L"
    GPIO.output(11, False)
    GPIO.output(12, True)
    GPIO.output(16, True)
    GPIO.output(15, False)

def right():
    print "R"
    GPIO.output(11, True)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(15, True)

def nutral():
    print "N"
    GPIO.output(11, False)
    GPIO.output(12, False)
    GPIO.output(16, False)
    GPIO.output(15, False)
########################## Movement Definitions END ########################

#GPIO.output(18, True) #Status-LED-On
def sigint_handler(signum, frame): #Catching Ctrl+c
    #GPIO.output(18, False) #Status-LED-Off
    pygame.quit()
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)
if (mc.get("d1") == "None"):
    pygame.quit()
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            #GPIO.output(18, False) #Status-LED-Off
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print ("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print ("Joystick button released.")
           
 
    joystick_count = pygame.joystick.get_count() #Get Joystick Count
    #if joystick_count == 0:
        #GPIO.output(18, False) #Status-LED-Off
     
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    #Sensor Input
    fedge = GPIO.input(7)
    bedge = GPIO.input(13)
    #Start Writing Yout Code From Here

    if (fedge == 0 and bedge == 0):
              nutral()

    elif (fedge == 0):
              if (joystick.get_axis(1) > 0.5 and joystick.get_axis(2) < -0.5): #Backward_Left
                   backward_left()
              elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(2) > 0.5): #Backward_Right
                   backward_right()
              elif (joystick.get_axis(1) > 0.5): #backward
                   backward()
              else:
                   nutral()

    elif (bedge == 0):
              if (joystick.get_axis(1) < -0.5 and joystick.get_axis(2) < -0.5): #Forward_Left
                   forward_left()
              elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(2) > 0.5): #Forward_Right
                   forward_right()
              elif (joystick.get_axis(1) < -0.5): #Forward
                   forward()
              else:
                   nutral()


    elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(2) < -0.5): #Forward_Left
              forward_left()
    elif (joystick.get_axis(1) < -0.5 and joystick.get_axis(2) > 0.5): #Forward_Right
                forward_right()
    elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(2) < -0.5): #Backward_Left
                backward_left()
    elif (joystick.get_axis(1) > 0.5 and joystick.get_axis(2) > 0.5): #Backward_Right
                backward_right()
    elif (joystick.get_axis(1) < -0.5): #Forward
                forward()
    elif (joystick.get_axis(1) > 0.5): #backward
                backward()
    elif (joystick.get_axis(2) < -0.5): #Left
                left()
    elif (joystick.get_axis(2) > 0.5): #Right
                right()
    else:
                nutral()



    time.sleep(0.05)  #refresh rate 
    # ALL CODE SHOULD GO ABOVE THIS COMMENT
    
# Use Ctrl+C to quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.

pygame.quit ()
