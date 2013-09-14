#!/usr/bin/env python
"""
 * s10gen.py
 *
 * s10gen - S10 Tracking Number Generator
 *
 * Copyright (C) 2013, Matt Davis (enferex)
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or (at
 * your option) any later version.
 *             
 * This program is distributed in the hope that it will be
 * useful, but WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 * PURPOSE.  See the GNU General Public License for more
 * details.
 *                             
 * You should have received a copy of the GNU
 * General Public License along with this program.  If not, see
 * <http://www.gnu.org/licenses/>.
"""

"""
What
====
This script generates UPU S10 numbers which is what the USPS uses for tracking
certain mail.


Usage Examples
==============
Example 1) Generate 42 sequential Tracking Codes starting at 10.
           The Service Indicator will be pseudo-random.
./s10gen.py -s 10 -n 42


Exmple 2) Generate 10 random tracking values.
          The Service Indicator and serial number will be pseudo-random.
./s10gen.py -n 10


Sources
=======
    * http://en.wikipedia.org/wiki/Tracking_number
    * http://en.wikipedia.org/wiki/S10_(UPU_standard)
    * http://pls.upu.int/document/2011/an/cep_c_4_gn_ep_4-1/src/d008_ad00_an01_p00_r00.pdf


Contact
=======
Matt Davis (enferex) mattdavis9@gmail.com
"""


import argparse, random, sys


# Specified in the UPU document
weight = (8, 6, 4, 2, 3, 5, 9, 7)


# https://tools.usps.com/go/TrackConfirmAction
service_indicators = ('RA', 'EA')


def csum(sn):
    """ Calculate check digit """
    s = sum([weight[i] * int(sn[i]) for i in range(len(weight))])
    cs = 11 - (s % 11)
    if cs == 10: return 0
    elif cs == 11: return 5
    else: return cs


def gen_fake_country_code():
    return 'US'


def gen_fake_service_indicator():
    return random.choice(service_indicators)


def gen_fake_serial(start_num):
    """ If start_num is None, then a random tracking value will be generated """
    if start_num is not None:
        start_num_str = str(start_num)
        sn_str = ''.join(['0' for x in range(8-len(start_num_str))])
        sn_str += start_num_str
    else:
        sn = [random.randint(0,9) for x in range(8)]
        sn_str = ''.join([str(x) for x in sn])
    return sn_str + str(csum(sn_str))

def main():
    """ 13 Number:
        AA NNN NNN NN C BB
        A: Service Indicator
        N: Serial Number
        C: Check Digit
        B: Country Code
    """
    parser = argparse.ArgumentParser(
        description='Generate USPS Tracking Numbers')
    parser.add_argument('-s', type=int,
                        help='Generate sequential (valid) ' +\
                        'tracking numbers starting from the specified value')
    parser.add_argument('-n',type=int,
                        help='Number of tracking numbers to generate')
    args = parser.parse_args()

    if args.n == None:
        parser.print_help()
        sys.exit(0)

    start_idx = None
    if args.s is not None:
        start_idx = int(args.s)

    for x in range(args.n):
        si = gen_fake_service_indicator()
        cc = gen_fake_country_code()
        if start_idx is not None:
            sn = gen_fake_serial(start_idx+x)
        else:
            sn = gen_fake_serial(None)
        print(si + sn + cc)

if __name__ == '__main__':
    main()
