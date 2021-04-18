##########################################################
#
#   Author: Mohammed Almodawah
#   Date: 18/4/2021
#   version: v 1.0
#
#   Description:
#   This library provides an easy way to parse memory segments dumped by Volatility.
#   Volatility enables users to dump allocated memory of a given process by concatenating
#   all memory segments into a single bulky file.
#   This library takes the memory dump file created by the "memdump" option and the
#   memory map file created by the "memmap" option and provides an easy way to interact
#   with every memory segment individualy.
#
#   Tested on Volatility 2.6
#
#   Check test.py for a code sample using this library
#
##########################################################

import binascii
import textwrap

class VolMemdumpParser:
    memdump_fd = 0
	
    def __init__(self,memdump_file_path,memmap_file_path):
        global memdump_fd
        self.__segments = []
        memmap_fd = open(memmap_file_path,"r")
        memdump_fd = open(memdump_file_path,"br")
        memmap_lines = memmap_fd.readlines()
        for i in range(3,len(memmap_lines)):
            entry = memmap_lines[i].split()
            if "0x" not in entry[0]:
                continue
            self.__segments.append(self.Segment(entry[0],entry[1],entry[2],entry[3]))
        memmap_fd.close()

    def get_all_segments(self):
        return self.__segments
		
    class Segment:
        def __init__(self,virtual,physical,size,dump_file_offset):
            self.__virtual = virtual
            self.__physical = physical
            self.__size = size
            self.__dump_file_offset = dump_file_offset

        def get_virtual_address(self):
            return self.__virtual

        def get_physical_address(self):
            return self.__physical

        def get_segment_size(self):
            return self.__size

        def get_dump_file_offset(self):
            return self.__dump_file_offset

        def get_segment_payload(self):
            global memdump_fd
            position = int(self.__dump_file_offset,16)
            size = int(self.__size,16)
            memdump_fd.seek(position)
            payload = memdump_fd.read(size)
            return payload

        def beautify_payload_hex(self):
            payload = self.get_segment_payload()
            payload_str = ''.join('{:02x}'.format(x) for x in payload)
            payload_str = " ".join(payload_str[i:i+2] for i in range(0, len(payload_str), 2))
            payload_str = '\n'.join(textwrap.wrap(payload_str, 48, break_long_words=False))
            return payload_str

        def dump_segment(self):
            beautiful_payload = self.beautify_payload_hex()
            print("Virtual Address: "+self.get_virtual_address())
            print("Physical Address: "+self.get_physical_address())
            print("Size: "+self.get_segment_size())
            print("Dump File Offset: "+self.get_dump_file_offset())
            print("Payload:")
            print(beautiful_payload)
