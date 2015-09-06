#!/usr/bin/env python3
import lock_ctrl
import NFCreader
import authentication
import door
import status_manager
import time

def card_on_door(ident):
	print(ident)
	al=auth.auth(ident)
	status=lock.is_locked()
	if stat.enter(ident,al):
		if status:
			lock.open()
		else:
			lock.latch()

def card_on_exit(ident):
	print(ident)
	lab_status=stat.leave(ident)
	if lab_status==stat.NO_MORE_TRUSTED:
		reader_door.beep(99)
	elif lab_status==stat.EMPTY:
		reader_door.beep(20)
	#if stat.is_empty():
	lock.close(reader_exit.beep)

stat=status_manager.Status_manager()
door=door.Door(30)
lock=lock_ctrl.Lock_ctrl(door,IO_open=95,IO_close=67,IO_latch=23)
auth=authentication.Auth_file('/etc/door_access')
reader_door=NFCreader.NFCreader(dev='/dev/ttyS1',on_card=card_on_door)
reader_door.start()
reader_exit=NFCreader.NFCreader(dev='/dev/ttyS2',on_card=card_on_exit)
reader_exit.start()
