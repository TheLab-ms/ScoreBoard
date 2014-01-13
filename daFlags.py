# Author: Jason Wheeler
# E-mail: init6@init6.me
# Project: ScoreBoard for thelab.ms CTF
# 
# Lic: GPLv3
#

from datetime import date
import sys, re, sqlite3

class flag:
    """A Class to hold and check flags"""
    def flags(self):
        self.flags = [ 'wut', 'one', 'two', 'four' ]
    
    def check(self, flag):
        if flag in self.flags:
            return True
        else:
            return False 
        
