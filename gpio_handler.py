import errno
import os

import inotify.adapters
from gpiozero import LED

LINES_GPIOS = dict(
    line0=LED(17),
    line1=LED(27),
    line2=LED(22),
)


def main():
    inotifier = inotify.adapters.Inotify()
    inotifier.add_watch('/tmp/lines')

    for event in inotifier.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        # debug
        # print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
        #     path, filename, type_names))

        line = filename
        if line not in LINES_GPIOS:
            # print('skipped {}'.format(line))
            continue

        for event_type in type_names:
            if event_type == 'IN_CREATE':
                print('on {}'.format(line))
                LINES_GPIOS[line].on()
            elif event_type == 'IN_DELETE':
                print('off {}'.format(line))
                LINES_GPIOS[line].off()


if __name__ == '__main__':
    try:
        os.mkdir('/tmp/lines')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    # turn everything off
    for line in LINES_GPIOS.values():
        line.off()
    main()
