"""
runs in the background watching for ./lines/* events
corresponding to handled gpio lines
"""
import errno
import os

import inotify.adapters
from gpiozero import LED

LINES_GPIOS = dict(
    line0=LED(17),
    line1=LED(27),
    line2=LED(22),
)
PATH_WATCH = '/tmp/lines'


def main():
    inotifier = inotify.adapters.Inotify()
    inotifier.add_watch(PATH_WATCH)

    for event in inotifier.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        line = filename
        if line not in LINES_GPIOS:
            print('skipped {}'.format(line))
            continue

        if 'IN_CREATE' not in type_names or 'IN_DELETE' not in type_names:
            print('skipped {}'.format(line))
            continue

        # debug
        print('path="{}" filename="{}" EVENT_TYPES={!s}'.format(
            path, filename, type_names))

        for event_type in type_names:
            if event_type == 'IN_CREATE':
                print('on {}'.format(line))
                LINES_GPIOS[line].on()
            elif event_type == 'IN_DELETE':
                print('off {}'.format(line))
                LINES_GPIOS[line].off()


if __name__ == '__main__':
    try:
        os.mkdir(PATH_WATCH)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    # turn everything off
    for line in LINES_GPIOS.values():
        line.off()
    main()
