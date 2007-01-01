#!/usr/bin/env python3
import lock_ctrl
from  IOctrl import gpio
from lock_behaviour import Lock_behaviour
import NFCreader
import authentication
import door
import status_manager
import time

def card_on_door(ident):
	print(ident)
	reader_door.beep(10)
	al=auth.auth(ident)
	if stat.enter(ident,al):
		lock.open()

def card_on_exit(ident):
	print(ident)
	lab_status=stat.leave(ident)
	if lab_status==stat.NO_MORE_TRUSTED:
		reader_door.beep(99)
	elif lab_status==stat.EMPTY:
		reader_door.beep(20)
	#if stat.is_empty():
	stat.flush()
	lock.close()

stat=status_manager.Status_manager()
door=door.Door(gpio(30))
lock_control=lock_ctrl.Lock_ctrl(IO_open=gpio(95),IO_close=gpio(67),IO_latch=gpio(23))
auth=authentication.Auth_file('/etc/door_access')
reader_door=NFCreader.NFCreader(dev='/dev/ttyS1',on_card=card_on_door)
reader_exit=NFCreader.NFCreader(dev='/dev/ttyS2',on_card=card_on_exit)
lock=Lock_behaviour(lock_control,door,reader_exit.beep)

reader_exit.start()
reader_door.start()
