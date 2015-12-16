#!/usr/bin/env python3
import lock_ctrl
from  IOctrl import gpio
from lock_behaviour import Lock_behaviour
from edge_detect import Edge_detect
import NFCreader
import decider
from door import Door
import time
import config
from message import Message
from keypad import Keypad
from identity_store import Identity_store
import pin
import beeper

def card_on_door(ident):
	print(ident)
	keypad.flush()
	ident_store.uid=None
	beep_door.confirm()
	response=decide.execute('open',ident,pin=None)
	if response=='pin':
		beep_door.wait_for_user(60)
		ident_store.uid=ident

def card_on_exit(ident):
	print(ident)
	beep_exit.confirm()
	decide.execute('close',ident)

def on_door_open():
	if lock_control.is_locked():
		print("Door opened while lock expected to be locked.")
		alarm.send('OPEN_WHILE_CLOSED')

def on_key(buf):
	beep_door.running=False
	beep_door.confirm()
	uid=ident_store.uid
	if not uid:
		return
	if pin.is_pin(buf):
		decide.execute('open',uid,pin=buf)
	pin_change=pin.is_pin_change(buf)
	if pin_change:
		old_pin=pin_change['oldpin']
		new_pin=pin_change['newpin']
		if pin.change_pin(config.decider_addr+config.door_name+'/change_pin',uid=uid,old_pin=old_pin,new_pin=new_pin):
			beep_door.ack()
		else:
			beep_door.nak()

ident_store=Identity_store()
door=Door(gpio(30),open_callback=on_door_open)
lock_control=lock_ctrl.Lock_ctrl(IO_open=gpio(95),IO_close=gpio(67),IO_latch=gpio(29))
lock_led=Edge_detect(gpio(23,active_low=True))
lock_led.start()

# set unused but connected gpios to output
gpio(66,'out')
gpio(68,'out')

keypad=Keypad(dev='/dev/ttyACM0',on_key=on_key)
keypad.start()

reader_door=NFCreader.NFCreader(dev='/dev/ttyS2',on_card=card_on_door)
reader_exit=NFCreader.NFCreader(dev='/dev/ttyS3',on_card=card_on_exit)
beep_door=beeper.Beeper(reader_door.beep)
beep_exit=beeper.Beeper(reader_exit.beep)

lock=Lock_behaviour(lock_control,door,lock_led,beep_exit)
decide=decider.Decider_http(addr=config.decider_addr+config.door_name+'/',opener=lock.open,closer=lock.close,ack=beep_door.ack,nak=beep_door.nak)

alarm=Message(addr=config.alarm_addr+config.door_name)
reader_exit.start()
reader_door.start()
