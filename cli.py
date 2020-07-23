#!/usr/bin/env python2
# pylint: disable=invalid-name
'''Command-line interface for prsconv2.py, which only accesses cli.parser'''

import argparse

desc = '''Read data from Tombo per-read statistics file into a CSV file.
The script has to read the whole per-read stats file into memory, so make
sure your available memory is bigger than the file-size.'''

epilog = "Version 2.1"

parser = argparse.ArgumentParser(description=desc, epilog=epilog)

# TODO: Add some print statements with a --verbose argument
# mutex_grp = parser.add_mutually_exclusive_group()
# mutex_grp.add_argument('-v', '--verbose', help='Print lots', dest='v',
#                        action='store_true')
# mutex_grp.add_argument('-q', '--quiet', help='Print only errors',
#                        action='store_true')

parser.add_argument('-o', '--overwrite', help='Overwrite the CSV if it '
                    + 'exists', action='store_true')

parser.add_argument('prs_path', help='Path of the .tombo.per_read_stats '
                    + 'file', metavar='PRS-FILEPATH', type=str)

parser.add_argument('output_path', help='Path of the CSV file to be '
                    + 'written (including the .csv extension)',
                    metavar='OUTPUT-FILEPATH', type=str)

parser.add_argument('--chromosome', help='Name of the chromosome for '
                    + 'which to give statistics (DEFAULT: '
                    + '"truncated_hiv_rna_genome")', metavar='CHROMOSOME',
                    default='truncated_hiv_rna_genome', type=str)

parser.add_argument('--strand', help='Either "+" or "-" (DEFAULT: "+")',
                    metavar='STRAND', default='+', type=str)

parser.add_argument('--start', help='Beginning of the genomic region for '
                    'which you want statistics (DEFAULT: 0)', metavar='START',
                    default=0, type=int)

parser.add_argument('--end', help='End of the genomic region for which you '
                    + 'want statistics (DEFAULT: 1,000,000,000)',
                    metavar='END', default=10**9, type=int)
