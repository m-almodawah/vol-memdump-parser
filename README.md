# vol-memdump-parser

Author: Mohammed Almodawah<br />
Date: 18/4/2020<br />
version: v 1.0<br />

Description:
This library provides an easy way to parse memory segments dumped by Volatility.
Volatility enables users to dump allocated memory of a given process by concatenating
all memory segments into a single bulky file.
This library takes the memory dump file created by the "memdump" option and the
memory map file created by the "memmap" option and provides an easy way to interact
with every memory segment individually.
<br />
Tested on Volatility 2.6
<br /><br />
Usage:<br />
Let's say that you have a memroy dump file of a Windows 10 machine named pcdump.dump and you want to analyze memory segments allocated to the process with the PID 1234.
First, you need to dump process memory by running:<br />
volatility -f pcdump.dump --profile=Win10x64 -p 1234 memdump --dump-dir ./<br />
This will produce a process memory dump file.
Next you would run:<br />
volatility -f pcdump.dump --profile=Win10x64 memmap 1234 > memmap.txt <br />
This will produce memmap.txt describing every memory segment allocated to the process with the PID 1234
Finally, use both files to create an object of the library which will allow you to interact with every memory segment individually.
Check test.py for a code sample. The sample will produce the below output:
<br /><br />
Virtual Address: 0x00000056bee28000<br />
Physical Address: 0x000000000c70c000<br />
Size: 0x1000<br />
Dump File Offset: 0x17000<br />
Payload:<br />
00 00 00 00 00 00 00 00 00 00 c8 c4 56 00 00 00<br />
00 c0 c6 c4 56 00 00 00 00 00 00 00 00 00 00 00<br />
00 1e 00 00 00 00 00 00 00 00 00 00 00 00 00 00<br />
00 80 e2 be 56 00 00 00 00 00 00 00 00 00 00 00<br />
54 1e 00 00 00 00 00 00 e8 45 00 00 00 00 00 00<br />
00 00 00 00 00 00 00 00 a0 7f b6 fc 37 02 00 00<br />
00 20 e3 be 56 00 00 00 e5 03 00 00 00 00 00 00<br />
................<br />
................<br />
................<br />
<br />
Supported functions for each memory segment:<br />
<br />
get_virtual_address()<br />
get_physical_address()<br />
get_segment_size()<br />
get_dump_file_offset()<br />
get_segment_payload() #returns the memory segment payload as a byte array<br />
beautify_payload_hex() #returns the memory segment payload as a nice hex string<br />
dump_segment() #Prints all information related to a memory segment<br />
