#!/usr/bin/env python2
# pylint: disable=invalid-name
'''A tool to convert .tombo.per_read_stats files into CSV files'''


import argparse


if __name__ == '__main__':
    desc='''Read data from Tombo per-read statistics file into a CSV file.
    The script has to read the whole per-read stats file into memory, so make
    sure your available memory is bigger than the file-size. This script also
    relies on Tombo's library, which expects index file's name to follow a
    certain format. If it has been renamed, the script may throw an error.'''
    parser = argparse.ArgumentParser(description=desc)
    mutex_grp = parser.add_mutually_exclusive_group()
    # TODO: How many of these per-read stats are actually used?
    # TODO: Make required arguments required
    # TODO: Hyphenate multi-word metavars
    # TODO: Add some print statements
    mutex_grp.add_argument('-v', '--verbose', help='Print lots', dest='v',
                        metavar='\b')
    mutex_grp.add_argument('-q', '--quiet', help='Print only errors',
                        metavar='\b')
    # TODO: Implement overwrite-protection
    parser.add_argument('-o', '--overwrite', help='Overwrite the CSV if it '
                        + 'exists', metavar='\b')
    # TODO: Implement version option
    # TODO: Make version option mutually exclusive with other options
    parser.add_argument('--version', help='Print version and exit')
    # TODO: Check that Basecalled_000 is the correct default name
    # TODO: Specify whether basecalled subgroup is for experimental, control, both
    parser.add_argument('--basecalled-subgroup', help='Tombo\'s default '
                        + 'name for basecalled subgroups is basecalled_000',
                        metavar='BASECALLED SUBGROUP')
    parser.add_argument('--prs-path', help='Path of the .tombo.per_read_stats '
                        + 'file', metavar='PRS FILEPATH')
    parser.add_argument('--output-path', help='Path of the CSV file to be '
                        + 'written (including the .csv extension)',
                        metavar='OUTPUT FILEPATH')
    # TODO: Give the user hints on chromosome name and strand
    parser.add_argument('--chromosome', help='Name of the chromosome for '
                        + 'which to give statistics (probably '
                        + 'truncated_hiv_rna_genome)', metavar='CHROMOSOME')
    parser.add_argument('--strand', help='Either "+" or "-" (probably +)',
                        metavar='STRAND')
    args = parser.parse_args()

    import pandas as pd
    from tombo import tombo_helper, tombo_stats

    reg = tombo_helper.intervalData(
        chrm=args.chromosome,
        # TODO: fix start and end positions or add them as command-line args
        start=0,
        end=10**6,
        strand=args.strand,
    )

    prs_recarray = (
        tombo_stats.PerReadStats(args.prs_path)
        .get_region_per_read_stats(reg)
    )

    # The three operations below that involve 'stat_level' are just to delete
    # extraneous labelling information from the table before we export to CSV
    (
        pd.DataFrame(prs_recarray)
        .set_index(['read_id', 'pos'])
        .rename_axis('stat_level', axis=1)
        .unstack('pos')
        .stack('stat_level')
        .reset_index('stat_level', drop=True)
        .to_csv(args.output_path)
    )
