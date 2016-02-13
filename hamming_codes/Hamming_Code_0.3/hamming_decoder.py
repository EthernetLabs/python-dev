"""Hamming Codes Implementation: https://programmingpraxis.com/2012/05/22/hamming-codes/
"""
"""              DECODER CLASS           """

__author__ = "Weqaar Janjua & Ahmer Malik"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "0.3"


import numpy as np
import math
import print_header


class decoder:
    def __init__(self,H,ENC_DATA):
        self.H = H
        self.ENC_DATA=ENC_DATA

    def decoded_data(self):
        dec_data = np.dot(self.H,self.ENC_DATA)% 2
        print "Decode ="
        print dec_data


def main():
    p = print_header._header(__file__,__author__,__copyright__,__version__)
    p._print()
    


if __name__ == '__main__':
      main()
