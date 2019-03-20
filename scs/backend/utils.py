import sys, struct
from backend.backend_exceptions import NoHeapFound, HeapPermissionError

class KeyListener(object):
    """docstring for KeyListener."""
    def __init__(self, logger):
        super(KeyListener, self).__init__()
        self.logger = logger

    def log_key(self, key):
        k_text = "Pressed" if key.event_type == "down" else "Released"
        try:
            k_str = str(key.char).upper()
            self.logger.AppendText("%s: %s\n" % (k_text,k_str))
        except AttributeError:
            k_str = str(key.name).upper()
            self.logger.AppendText("%s: %s\n" % (k_text,k_str))


def read_write_heap(pid, address, newValue):
    """Replace value at @address with @newValue, @pid is for location process"""
    maps_filename = "/proc/{}/maps".format(pid)
    print("[*] maps: {}".format(maps_filename))
    mem_filename = "/proc/{}/mem".format(pid)
    print("[*] mem: {}".format(mem_filename))

    # try opening the maps file
    try:
        maps_file = open('/proc/{}/maps'.format(pid), 'r')
    except IOError as e:
        print("[ERROR] Can not open file {}:".format(maps_filename))
        print("        I/O error({}): {}".format(e.errno, e.strerror))
        sys.exit(1)

    for line in maps_file:
        sline = line.split(' ')
        # check if we found the heap
        if sline[-1][:-1] != "[heap]":
            continue

        # parse line
        addr = sline[0]
        perm = sline[1]
        offset = sline[2]
        device = sline[3]
        inode = sline[4]
        pathname = sline[-1][:-1]

        # check if there is read and write permission
        if perm[0] != 'r' or perm[1] != 'w':
            print("[*] {} does not have read/write permission".format(pathname))
            maps_file.close()
            exit(0)

        # open and read mem
        try:
            mem_file = open(mem_filename, 'rb+')
        except IOError as e:
            maps_file.close()
            exit(1)

        # read heap  
        mem_file.seek(address)
        # Pack integer as little endian int
        newValue = struct.pack("<i", newValue)
        mem_file.write(newValue)

        # close files
        maps_file.close()
        mem_file.close()

        # there is only one heap in our example
        break