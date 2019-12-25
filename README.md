# BED PI
various, minimal stuff to get a push-and-hold button controlling some GPIOs(3) that control the BED RECLINE

* NO SECURITY
* ASSUMES VARIOUS pizero paths
* bad tempdir usage


## i forget systemd stuff

enable the systemd user units to have them exec on startup:
    
	$ ln -sf $(pwd)/gpio_handler.service /home/pi/.config/systemd/user/
	$ ln -sf $(pwd)/bed_rest.service /home/pi/.config/systemd/user/
	# um you also need to start
	$ systemctl --user enable gpio_handler
	$ systemctl --user enable bed_rest
	$ journalctl --user-unit gpio_handler
	$ journalctl --user-unit bed_rest
	# need this to start user services on boot
	$ sudo loginctl enable-linger pi