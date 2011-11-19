#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Download the latest version of the english iso text file
import urllib
iso_text = urllib.urlopen('http://www.iso.org/iso/list-en1-semic-3.txt').read().decode('ISO-8859-1').replace('\r', '').encode('utf-8').split('\n')
#iso_text = open('list-en1-semic-3.txt', 'rb').read().decode('ISO-8859-1').replace('\r', '').encode('utf-8').split('\n')

# Two arrays of country codes, names to codes and codes to names
names_to_codes = []
codes_to_names = []

# Find the first blank line, then split countries up
found_blank = False
for line in iso_text:
   if len(line) > 0:
      if found_blank:
         name,code = line.strip().split(';')
         names_to_codes.append((name.replace('\'', '\\\''),code)) # Do some escaping for later since I like ' over "
         title_name = name.title() # The title case is sort of broken so do some ok fixing on it
         title_name = title_name.replace('Of The', 'of the').replace('Of', 'of').replace('And', 'and').replace('\'S', '\'s')
         codes_to_names.append((code,title_name.replace('\'', '\\\''))) 
   else:
      found_blank = True

# Generate some source code (explicit and ugly)
import codecs
iso_py = file('iso.py', 'wb')
iso_py.write(codecs.BOM_UTF8)
iso_py.write('#!/usr/bin/env python\n'.encode('utf-8'))
iso_py.write('# -*- coding: utf-8 -*-\n'.encode('utf-8'))
iso_py.write('\n'.encode('utf-8'))
iso_py.write('COUNTRY_TO_CODE = {\n'.encode('utf-8'))
for name_code_pair in names_to_codes:
   iso_py.write('   \'%s\':\'%s\',\n'.encode('utf-8') % name_code_pair)
iso_py.write('}\n\n'.encode('utf-8'))
iso_py.write('CODE_TO_COUNTRY = {\n'.encode('utf-8'))
for name_code_pair in codes_to_names:
   iso_py.write('   \'%s\':\'%s\',\n'.encode('utf-8') % name_code_pair)
iso_py.write('}\n'.encode('utf-8'))
iso_py.close()