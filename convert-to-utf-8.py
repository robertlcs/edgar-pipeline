import sys

def usage():
    print "Usage: python convert-to-utf-8.py <source> <target> <source-encoding>"

if len(sys.argv) < 4:
    usage()
    sys.exit(-1)

source_path = sys.argv[1]
target_path = sys.argv[2]
source_encoding = sys.argv[3]

sourceEncoding = "iso-8859-1"
targetEncoding = "utf-8"
source = open(source_path)
target = open(target_path, "w")

target.write(unicode(source.read(), sourceEncoding).encode(targetEncoding))