"""Hamming Codes Implementation: https://programmingpraxis.com/2012/05/22/hamming-codes/
"""
"""              ENCODER CLASS           """

__author__ = "Weqaar Janjua & Ahmer Malik"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "0.3"

import numpy as np
import math
import print_header
      
class encoder:
      data_bits = 0
      parity_bits = 0
      A=0
      G=0
      H=0
      enc_data=0
      def __init__(self,data):
             self.data=data
             encoder.data_bits=len(data)
             encoder.parity_bits=int(math.sqrt(encoder.data_bits))+2
             encoder.A=0
             encoder.G=0
             encoder.H=0
             encoder.enc_data=0

      
      def hamming_rule(self):
             
             H1 = encoder.data_bits + encoder.parity_bits +1
             H2 = 2**encoder.parity_bits

             while  H1 > H2:
                 H1 = encoder.data_bits + encoder.parity_bits +1
                 H2 = 2**encoder.parity_bits
                 encoder.parity_bits +=1

             encoder.parity_bits -=1
             # Hamming Code is described by (c,d)=(Hamming Word , Data)
             c = encoder.data_bits + encoder.parity_bits
             print ("Data Bits = %d"% encoder.data_bits)
             print ("Parity Bits = %d"% encoder.parity_bits)
             print ("Hamm_word c = d + p = %d"% c)

      #Now generate the matrices, G Generator Matrix & H Syndrome matrix

             
      #G(I:A) & H(A^T:I)
      #Generator Matrix is denoted by G = [I:A]
      def generator_matrix(self):
            I = np.eye(encoder.data_bits)        # Create a dxd identity matrix
            Comb =[bin(x)[2:].rjust(encoder.parity_bits, '0') for x in range(2**encoder.parity_bits)]
            encoder.A = np.zeros((encoder.data_bits,encoder.parity_bits))
            for i in xrange(0,encoder.data_bits):
                  for j in xrange(0,encoder.parity_bits):
                        encoder.A[i][j] = Comb[i][j]

            print encoder.A
            encoder.G = np.concatenate((I,encoder.A), axis=1)
            print "G ="
            print encoder.G

      #Syndrome Matrix is denoted by H = [A^T:I]
      def syndrome_matrix(self):
            
            I = np.eye(encoder.parity_bits)        # Create a pxp identity matrix
            A_Trans = zip(*encoder.A)
            encoder.H = np.concatenate((A_Trans,I), axis=1)
            print "H ="
            print encoder.H

      def encoded_data(self):
            encoder.enc_data = np.dot(self.data,encoder.G)% 2
            print "Encode ="
            print encoder.enc_data


def main():
      p = print_header._header(__file__,__author__,__copyright__,__version__)
      p._print()
      DATA = np.array([1, 0,1 , 1,1])
      enc = encoder(DATA)
      enc.hamming_rule()
      enc.generator_matrix()
      enc.syndrome_matrix()
      enc.encoded_data()
      

if __name__ == '__main__':
      main()







