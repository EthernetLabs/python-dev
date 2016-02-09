"""Hamming Codes Implementation: https://programmingpraxis.com/2012/05/22/hamming-codes/
"""
"""              MAIN CLASS           """

__author__ = "Weqaar Janjua & Ahmer Malik"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "0.3"

import hamming_encoder
import hamming_decoder
import print_header
import numpy as np

def main():
      p = print_header._header(__file__,__author__,__copyright__,__version__)
      p._print()
      DATA = np.array([1, 0,1 , 1,1])
      enc = hamming_encoder.encoder(DATA)
      enc.hamming_rule()
      enc.generator_matrix()
      enc.syndrome_matrix()
      enc.encoded_data()
      dec = hamming_decoder.decoder(hamming_encoder.encoder.H,hamming_encoder.encoder.enc_data)
      dec.decoded_data()
      

if __name__ == '__main__':
    main()

