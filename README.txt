various, minimal stuff to get a push-and-hold button controlling some GPIOs(3) that control the BED RECLINE


enable the systemd user units to have them exec on startup
	$ ln -sf $(pwd)/gpio_handler.service /home/pi/.config/systemd/user/
	$ ln -sf $(pwd)/bed_rest.service /home/pi/.config/systemd/user/
	$ systemctl --user enable gpio_handler
	$ systemctl --user enable bed_rest


	$ journalctl --user-unit gpio_handler
	$ journalctl --user-unit bed_rest