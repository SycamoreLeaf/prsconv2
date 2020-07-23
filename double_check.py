# NOTE!!!
# I'm putting this module aside. I don't think it would be worth the time to
# finish.

'''This module defines a function that is used to double-check the results of
prsconv2.py. Basically, it computes the same thing as that module via a
different method.'''
# pylint: disable=invalid-name,redefined-outer-name

def parse_h5file(prs_path):
    '''Open a Tombo per-read statistics file as an HDF5 file and return several
    things:
    
    block_stats, read_ids, read_id_vals : The three HDF5 datasets that are
        stored in a statistic block HDF5 group in Tombo's per-read statistics
        file format.
    blocks_as_expected : True if there is exactly one statistics block and its
        name is 'Block_0'. False otherwise.
    '''
    with h5py.File(prs_path, 'r') as hdf5file:
        block_stats = hdf5file['Statistic_Blocks']['Block_0']['block_stats']
        read_ids = hdf5file['Statistic_Blocks']['Block_0']['read_ids']
        read_id_vals = hdf5file['Statistic_Blocks']['Block_0']['read_id_vals']

        block_stats = np.asarray(block_stats)
        read_ids = np.asarray(read_ids)
        read_id_vals = np.asarray(read_id_vals)
        
        blocks_as_expected = hdf5file['Statistic_Blocks'].keys() == ['Block_0']
        
    return (
        block_stats,
        read_ids,
        read_id_vals,
        blocks_as_expected
    )

def row_num_to_read_id(read_ids, read_id_vals):
    

def convert_to_table(block_stats, read_ids, read_id_vals):
    '''Take three numpy arrays straight from the corresponding datasets in a
    statistics block of a Tombo per-read statistics file. 

    Assemble them into a pandas dataframe containing statistics (either p-values
    or log-likelihood ratios, depending on the per-read statistics file) for
    every position on every read; index this dataframe's rows by read id and
    its columns by nucleotide position.'''
    
    num_records = block_stats.shape[0]
    

def double_check(prs_path, reference_df):
    '''Open the HDF5 file at prs_path manually. Convert it to a a pandas
    dataframe containing statistics (either p-values or log-likelihood ratios,
    depending on the per-read statistics file) for every position on every
    read; index this dataframe's rows by read id and its columns by nucleotide
    position. Return True if the resulting dataframe equals reference_df.
    Otherwise return False.'''
    
    (
        BLOCK_STATS,
        READ_IDS,
        READ_ID_VALS,
        BLOCKS_AS_EXPECTED
    ) = parse_h5file(prs_path)
    
    if not BLOCKS_AS_EXPECTED: return False
    
    