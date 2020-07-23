# prsconv2
Improved tool to convert Tombo per-read statistics files into CSV files

## Usage
Suppose you have a Tombo per-read statistics file at `/path/to/prs/file`, and you want to transform it into a CSV file at `/path/to/future/csv/file.csv`.
Then run something like this at your terminal:
```bash
$ python prsconv2.py --chromosome "truncated_hiv_rna_genome" --strand "+" --start 0 --end 1000000000 /path/to/prs/file /path/to/future/csv/file.csv
```
If you leave the --chromosome, --strand, --start, and --end options out, the script will default to the same values written explicitly in this example
The default values are probably correct for the people using this script in July 2020, but they won't work for every per-read statistics file.

This tool will not delete the per-read statistics file. It will not overwrite a preexisting csv file either (unless the user supplies the --overwrite option).

For hints on command-line usage, run
```bash
$ python prsconv2.py --help
```

## Output Format
The output CSV file will have a row for every read and a column for every nucleotide position.
The entry in row *x*, column *y* is a statistic representing the likelihood that read *x* was modified at position *y*.
This statistic is usually a *p*-value, but it can also be a log-likelihood ratio.
(It depends on the options that tombo used to produce the per-read statistics file.)

Rows are labeled by labeled by their read IDs (which look like "01c40adf-7144-4f6f-95d7-4cc08abc52d2").
The column label is a number representing a nucleotide position along the reference sequence that was used for resquiggling.
That means that if you resquiggled your reads to a reference fasta that looks like this:
```
> truncated_hiv_rna_genome
ACTGGTCAGATTACAACGTGTACCATGTCA...
```
then the column labeled as "2" corresponds to the same position as the first *T* in the reference Fasta.
(Note that this is a **zero-based** index; position 2 corresponds to *T*, not *C*.)

The first and last few columns will usually be *NaN* values.

## Troubleshooting
* Make sure Python is installed (or that a Python module is loaded). **This script was written to be run with Python 2.**
* Look at the reference sequence you used for resquiggling.
**If its name is something other than "truncated_hiv_rna_genome", you need to supply the `--chromosome` option.**
This script uses Tombo's Python API to read the per-read statistics file.
Unfortunately, Tombo's API requires us to specify upfront the name of the chromosome for which we want statistics.
If you really can't figure out the chromosome name, try opening up the per-read statistics file and looking for the `chrom` attribute.
On my per-read statistics files, the following command works. (You will have to tweak it.)
```bash
$ h5dump -a /Statistic_Blocks/Block_0/chrm test1_depth_50k_fisher_3_v14.tombo.per_read_stats
```

## Notes
* This script was not heavily tested. I did my best, but *be careful*.
