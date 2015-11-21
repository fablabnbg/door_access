#!/usr/bin/env python3
import lock_ctrl
from  IOctrl import gpio
from lock_behaviour import Lock_behaviour
from edge_detect import Edge_detect
import NFCreader
import decider
import door
import time
import config

def card_on_door(ident):
	print(ident)
	reader_door.beep(10)
	decide.execute('open',ident)

def card_on_exit(ident):
	print(ident)
	reader_exit.beep(10)
	decide.execute('close',ident)

door=door.Door(gpio(30))
lock_control=lock_ctrl.Lock_ctrl(IO_open=gpio(95),IO_close=gpio(67),IO_latch=gpio(29))
lock_led=Edge_detect(gpio(23,active_low=True))
lock_led.start()

# set unused but connected gpios to output
gpio(66,'out')
gpio(68,'out')

reader_door=NFCreader.NFCreader(dev='/dev/ttyS2',on_card=card_on_door)
reader_exit=NFCreader.NFCreader(dev='/dev/ttyS3',on_card=card_on_exit)
lock=Lock_behaviour(lock_control,door,lock_led,reader_exit.beep)
decide=decider.Decider_http(addr=config.decider_addr+config.door_name+'/',opener=lock.open,closer=lock.close)

reader_exit.start()
reader_door.start()
