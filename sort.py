# Read in file.
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

import sys

