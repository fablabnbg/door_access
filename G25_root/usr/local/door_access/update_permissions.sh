#!/bin/sh

mount $DEVNAME /mnt 2>&1 >> /home/acme/test.txt
diff /mnt/door_access /etc/door_access
if [ $? -eq 1 ]; then
	cp /mnt/door_access /etc/door_access
fi
umount /mnt
