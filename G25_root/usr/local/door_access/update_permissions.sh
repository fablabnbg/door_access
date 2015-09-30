#!/bin/bash

mount $DEVNAME /mnt 2>&1 >> /home/acme/test.txt
diff -u /etc/door_access /mnt/door_access.csv > /mnt/last_change_tmp.diff
if [ $? -eq 1 ]; then
	cp /mnt/door_access.csv /etc/door_access
	mv /mnt/last_change_tmp.diff /mnt/last_change.diff
	mkdir -p /mnt/history

	lastnum=$(ls /mnt/history | sed 's/\..*$//' | sort -g | tail -n 1)
	num=$((lastnum+1))
	cp /mnt/last_change.diff /mnt/history/$num.diff
	cp /etc/door_access /mnt/history/$num.csv
else
	rm /mnt/last_change_tmp.diff
fi
umount /mnt
