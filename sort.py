
# reject anything with space or $%^&*()+{}[]|\<>,.?/
# reject anything with the word rock in it.
# reject anything less than 5 or greater than 14
# randomly strip word list down to 2000 words.
# Take half and randomly hash to sha1,md5
# take other half set to md5crypt and SHA256 w/ salts
# sha1,md5 worth 1point each
# md5crypt SHA256 worth 4 points each.
# mix up list.
# write to file in format <hash><tab><points>

import sys, re

fname = 'all.txt'
clean_list = []


# Read in file.

with open(fname, 'r', encoding='ascii', errors='surrogateescape') as f:
    data = f.readlines()

for word in data:
    clean_list.append(word.encode('ascii', 'replace') )
    #print ( word.encode('ascii').strip() )
    #if not re.search('rock', word): # and not re.search([\$%^&*()+{}[\]|\\<>,.?/ ]):
        #print( word.encode("ascii", "ignore") )
        #clean_list.append(word.encode(utf-8))

print( clean_list )
