#!/usr/bin/env python3
from threading import Thread
import json
import os
import time

import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# 000 no movement
# 001 unknown
# 010 unknown
# 011 unknown
# 100 unknown
# 101 uknown
# 110 unkown
# 111 wasn't ever observed
TIME_HOLD_MS = 2000

# define which movement is triggered by
# raising which lines on the GPIO
MOVEMENT_TO_LINES = dict(
    top_up=('line0',),              # 001
    mid_up=('line1',),              # 010
    bot_down=('line0', 'line1'),    # 011
    bot_up=('line2',),              # 100
    top_down=('line0', 'line2'),    # 101
    mid_down=('line1', 'line2'),    # 110
    debug=('line0', 'line1', 'line2') # 111
)


def ms(time_time_float_secs):
    return int(round(time_time_float_secs * 1000))


# inteface to the gpio-handler interface for
# raising a line when a file exists.
# minimum TIME_HOLD after a request is received.
def move(movement_as_lines):
    # a movement is just a tuple of line names as above
    # write or re-touch all files

    for line_filename in movement_as_lines:
        path_line = '/tmp/lines/{}'.format(line_filename)
        touch(path_line)

    # tell the background handler to clear this file
    # in 500ms if it was not re-touched
    def delayed_remove():
        time.sleep((TIME_HOLD_MS + 50)/1000)
        stop(movement_as_lines)
    thread = Thread(target=delayed_remove)
    thread.daemon = True
    thread.start()


def stop(movement_as_lines):
    for line_filename in movement_as_lines:
        path_line = '/tmp/lines/{}'.format(line_filename)
        try:
            stat = os.stat(path_line)
        except FileNotFoundError:
            # file is already gone, that's ok
            pass

        # if the file was last changed > 500ms ago, delete it
        if ms(time.time()) > (ms(stat.st_ctime) + TIME_HOLD_MS):
            remove_f(path_line)
        # otherwise do nothing, someone touched it in the meantime
        else:
            pass


def remove_f(path):
    try:
        os.remove(path)
        print('removed {}'.format(path))
    except OSError as e:
        # errno.ENOENT = no such file or directory
        if e.errno != errno.ENOENT:
            raise
        print('path already removed {}'.format(path))


def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
            dir_fd=None if os.supports_fd else dir_fd, **kwargs)


@app.route('/bed_recline_movement_pulse/<movement>', methods=['GET'])
def bed_recline_movement_pulse(movement):
    """
    activate a movement for at least 500ms
    """
    movement_as_lines = MOVEMENT_TO_LINES[movement]
    move(movement_as_lines)

    return json.dumps({"success": True})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
