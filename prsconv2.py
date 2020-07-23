#!/usr/bin/env python2
# pylint: disable=invalid-name,redefined-outer-name
'''A tool to convert .tombo.per_read_stats files into CSV files'''

import os.path
import cli # Module from this directory that defines an argparse parser

def recarray_to_csv(recarray, output_path):
    '''Convert record array output from tombo.tombo_stats.PerReadStatistics
    into a 2D table with a row for every read and a column for every position,
    then write that table to a CSV file at output_path'''

    # The three operations below that involve 'stat_level' are just to delete
    # extraneous labelling information from the table before we export to CSV
    (
        pd.DataFrame(recarray)
        .set_index(['read_id', 'pos'])
        .rename_axis('stat_level', axis=1)
        .unstack('pos')
        .stack('stat_level')
        .reset_index('stat_level', drop=True)
        .to_csv(output_path)
    )

if __name__ == '__main__':
    import pandas as pd
    from tombo import tombo_helper, tombo_stats

    args = cli.parser.parse_args()

    ERRMESS = ("The file {} already exists. Consider using the --overwrite "
               + " option.").format(args.output_path)
    assert args.overwrite or not os.path.exists(args.output_path), ERRMESS

    reg = tombo_helper.intervalData(
        chrm=args.chromosome,
        start=args.start,
        end=args.end,
        strand=args.strand,
    )

    prs_recarray = (
        tombo_stats.PerReadStats(args.prs_path)
        .get_region_per_read_stats(reg)
    )

    recarray_to_csv(prs_recarray, args.output_path)
