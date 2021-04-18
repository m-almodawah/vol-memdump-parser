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
