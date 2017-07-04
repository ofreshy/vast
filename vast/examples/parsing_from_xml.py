from vast.parsers import xml_parser
from vast.resources import INLINE_MULTI_FILES_XML_V2

# Say that you got an XML file that you need to parse
# Use the xml parser module to parse it
parsed_vast = xml_parser.from_xml_file(INLINE_MULTI_FILES_XML_V2)
print parsed_vast

# And not let your application logic deal with a defined model
