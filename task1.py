
# Detect locally mounted disk (make sure it is local) with at least X MB free space,
# create Z files of size Y,
# run Z “dd” processes which where each process will fill the selected file with Data
# and print time took to complete the work.

import subprocess
import time
from optparse import OptionParser

pattern_filename = 'log{}.bin'


def detect_mounted_disk_with_free_space(free_space: int):
    subprocess.getoutput("df -h | sed 'if ($4 > {}) {{print $6}}'".format(free_space * 1024))


def create_files(amount, size):
    for i in range(amount):
        name = pattern_filename.format(i)
        with open(name, 'wb') as f:
            f.seek(size-1)
            f.write(b'\0')


def fill_data(amount, size):
    start = time.time()
    for i in range(amount):
        name = pattern_filename.format(i)
        subprocess.getoutput("dd if=/dev/urandom of={} bs={}M count=1".format(name, size))
    print('time: {:.3f} secs'.format(time.time() - start))


def main(free_space, amount_files, size_of_files):
    detect_mounted_disk_with_free_space(free_space)
    create_files(amount_files, size_of_files)
    fill_data(amount_files)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-X", type=int, help="free space(in MB)")
    parser.add_option("-Z", type=int, help="amount of files to create")
    parser.add_option("-Y", type=int, help="size of created files (in bytes)")

    (options, args) = parser.parse_args()
    main(options.X, options.Z, options.Y)

