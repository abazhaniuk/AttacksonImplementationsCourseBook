import numpy as np
import math
from aes_scripts.aes_xtimes import aes_xtimes

# function result = aes_mix_columns_8bit(input_data, encrypt)

# performs the AES MixColumns transformation like a 8-bit uC would
# 
# DESCRIPTION:
# 
# aes_mix_columns_8bit(input_data, encrypt)
# 
# This function performs an AES MixColumns operation on each line of the
# byte matrix 'input_data'. 'input_data' is a matrix of bytes with an
# arbitrary number of lines that are four bytes wide (or a width that is a
# multiple of four bytes - in this case the MixColumns operation is
# performed on the bytes 1..4, 5..8, 8..12,  ).
# 
# PARAMETERS:
# 
# - input_data:
#   A matrix of bytes with an arbitrary number of lines and a number of
#   :s that is a multiple of 4.
# - encrypt:
#   Paramter indicating whether an encryption or a decryption is performed
#   (1 = encryption, 0 = decryption). In case of a decrytion, an inverse
#   Mix:s operation is performed.
# 
# RETURNVALUES:
# 
# - result:
#   A matrix of bytes of the size of the 'data' matrix. Each line of this
#   matrix consists of the MixColumns result of the corresponding line of
#   'input_data'.
# 
# EXAMPLE:
# 
# aes_mix_columns_8bit([1, 2, 3, 4 5, 6, 7 ,8], 1)

# AUTHORS: Stefan Mangard, Mario Kirschbaum, Yossi Oren
# 
# CREATION_DATE: 31 July 2001
# LAST_REVISION: 30 June 2009


def aes_mix_columns_8bit(input_data, encrypt):
	n = np.shape(input_data)[1]

	times = math.ceil(n / 4)

	data = np.asmatrix(input_data)

	result = np.copy(data)

	for i in range(times):

		if encrypt == 0:
			# inverse mixcolumns  - 8 bit implementation
			tmp = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor( 
				data[:, 0+4*i], data[:, 1+4*i]),
				data[:, 2+4*i]), data[:, 3+4*i])         # Leak #0.1
			xtmp = aes_xtimes(tmp)                             # Leak #0.2
			h1 = np.bitwise_xor(np.bitwise_xor(
				xtmp, data[:, 0+4*i]), data[:, 2+4*i])   # Leak #0.3
			h1 = aes_xtimes(h1)                                # Leak #0.4
			h1 = aes_xtimes(h1)                                # Leak #0.5
			h1 = np.bitwise_xor(h1, tmp)                               # Leak #0.6
			h2 = np.bitwise_xor(np.bitwise_xor(
				xtmp, data[:, 1+4*i]), data[:, 3+4*i])   # Leak #0.7
			h2 = aes_xtimes(h2)                                # Leak #0.8
			h2 = aes_xtimes(h2)                                # Leak #0.9
			h2 = np.bitwise_xor(h2, tmp)                               # Leak #0.10

			tm = np.bitwise_xor(data[:, 0+4*i], data[:, 1+4*i])    # Leak #1.1
			tm = aes_xtimes(tm)                                  # Leak #1.2
			result[:, 0+4*i] = np.bitwise_xor(np.bitwise_xor(
				data[:, 0+4*i], tm), h1)                    # (output)

			tm = np.bitwise_xor(data[:, 1+4*i], data[:, 2+4*i])    # Leak #2.1
			tm = aes_xtimes(tm)                                  # Leak #2.2
			result[:, 1+4*i] = np.bitwise_xor(np.bitwise_xor(
				data[:, 1+4*i], tm), h2)

			tm = np.bitwise_xor(data[:, 2+4*i], data[:, 3+4*i])    # Leak #3.1
			tm = aes_xtimes(tm)                                  # Leak #3.2
			result[:, 2+4*i] = np.bitwise_xor(np.bitwise_xor(
				data[:, 2+4*i], tm), h1)                    # (output)

			tm = np.bitwise_xor(data[:, 3+4*i], data[:, 0+4*i])    # Leak #4.1
			tm = aes_xtimes(tm)                                  # Leak #4.2
			result[:, 3+4*i] = np.bitwise_xor(np.bitwise_xor(
				data[:, 3+4*i], tm), h2)                    # (output)
			# Total 18 extra leaks per column
		else:
			# mixcolumns  - 8 bit implementation
			tmp = np.bitwise_xor(np.bitwise_xor(np.bitwise_xor(
				data[:, 0+4*i], data[:, 1+4*i]),
				data[:, 2+4*i]), data[:, 3+4*i])         # Leak #0.1
			tm = np.bitwise_xor(data[:, 0+4*i], data[:, 1+4*i])    # Leak #1.1
			tm = aes_xtimes(tm)                                  # Leak #1.2
			result[:, 0+4*i] = np.bitwise_xor(np.bitwise_xor(
				data[:, 0+4*i], tm), tmp)                   # (output)

			tm = np.bitwise_xor(data[:, 1+4*i], data[:, 2+4*i])    # Leak #2.1
			tm = aes_xtimes(tm)                                  # Leak #2.2
			result[:, 1+4*i] = np.bitwise_xor(np.bitwise_xor(
				data[:, 1+4*i], tm), tmp)                   # (output)

			tm = np.bitwise_xor(data[:, 2+4*i], data[:, 3+4*i])    # Leak #3.1
			tm = aes_xtimes(tm)                                  # Leak #3.2
			result[:, 2+4*i] = np.bitwise_xor(np.bitwise_xor(
				data[:, 2+4*i], tm), tmp)                   # (output)

			tm = np.bitwise_xor(data[:, 3+4*i], data[:, 0+4*i])    # Leak #4.1
			tm = aes_xtimes(tm)                                  # Leak #4.2
			result[:, 3+4*i] = np.bitwise_xor(np.bitwise_xor(               # (output)
				data[:, 3+4*i], tm), tmp)
		# Total 9 extra leaks per column

	result = np.uint8(result)
	return result
