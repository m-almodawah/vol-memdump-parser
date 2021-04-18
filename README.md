# vol-memdump-parser

Author: Mohammed Almodawah<br />
Date: 18/4/2020<br />
version: v 1.0<br />

Description:<br />
This library provides an easy way to parse memory segments dumped by Volatility.
Volatility enables users to dump allocated memory of a given process by concatenating
all memory segments into a single bulky file.
This library takes the memory dump file created by the "memdump" option and the
memory map file created by the "memmap" option and provides an easy way to interact
with every memory segment individually.
<br /><br />
Tested on Volatility 2.6
<br /><br />
Usage:<br />
Let's say that you have a memroy dump file of a Windows 10 machine named pcdump.dump and you want to analyze memory segments allocated to the process with the PID 1234.
First, you need to dump process memory by running:<br /><br />
```
volatility -f pcdump.dump --profile=Win10x64 -p 1234 memdump --dump-dir ./
```
This will produce a process memory dump file.
Next you need to run:<br /><br />
```
volatility -f pcdump.dump --profile=Win10x64 memmap 1234 > memmap.txt
```
This will produce memmap.txt file describing every memory segment allocated to the process.
<br/>Finally, use both files to create an object of the VolMemdumpParser class which will allow you to interact with every memory segment individually.
Check test.py for a code sample. The sample will produce an output similar to the output below:
<br /><br />
test.py:
```
import binascii
import textwrap

from vol_memdump_parser import VolMemdumpParser

parser = VolMemdumpParser("path to your memdump file","path to your memmap file")

segments = parser.get_all_segments()
for segment in segments:
    print("Virtual Address: "+segment.get_virtual_address())
    print("Physical Address: "+segment.get_physical_address())
    print("Size: "+segment.get_segment_size())
    print("Dump File Offset: "+segment.get_dump_file_offset())
    print("Payload:")
    payload = segment.get_segment_payload()


    # Some string processing to print the payload in a nice hex string format
    payload_in_hex_str = ''.join('{:02x}'.format(x) for x in payload)
    payload_in_hex_str_with_spaces = " ".join(payload_in_hex_str[i:i+2] for i in range(0, len(payload_in_hex_str), 2))
    wrapped_payload_in_hex_str = '\n'.join(textwrap.wrap(payload_in_hex_str_with_spaces, 48, break_long_words=False))
    # End string processing

    print(wrapped_payload_in_hex_str)
    print("\n")
```
Output:
```
Virtual Address: 0x00000056bee28000
Physical Address: 0x000000000c70c000
Size: 0x1000
Dump File Offset: 0x17000
Payload:
00 00 00 00 00 00 00 00 00 00 c8 c4 56 00 00 00
00 c0 c6 c4 56 00 00 00 00 00 00 00 00 00 00 00
00 1e 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 80 e2 be 56 00 00 00 00 00 00 00 00 00 00 00
54 1e 00 00 00 00 00 00 e8 45 00 00 00 00 00 00
00 00 00 00 00 00 00 00 a0 7f b6 fc 37 02 00 00
00 20 e3 be 56 00 00 00 e5 03 00 00 00 00 00 00
................
................
................
```
Supported functions for each memory segment:<br />
```
get_virtual_address()

get_physical_address()

get_segment_size()

get_dump_file_offset()

#returns the memory segment payload as a byte array
get_segment_payload()

#returns the memory segment payload as a nice hex string
beautify_payload_hex() 

#Prints all information related to a memory segment
dump_segment()
```
