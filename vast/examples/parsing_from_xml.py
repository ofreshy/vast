from vast.parsers import xml_parser
from vast.resources import INLINE_MULTI_FILES_XML


parsed_vast = xml_parser.from_xml_file(INLINE_MULTI_FILES_XML)
print parsed_vast

# your application logic goes here with parsed_vast
