import pandas as pd
import h5py
import numpy as np
import mplhep

def GetData(flist,chunk_size=None,is2018=False):
    
    """ 
    opens a summary file or list of summary files and convert them to a pandas dataframe 
    if given the chunk_size will be used to collect events in chunks of this size
    """
    
    flist=flist if isinstance(flist,list) else [flist]
    
    df,df_counts=[],[]
    
    for filename in flist:
    
        with h5py.File(filename, 'r') as f:

            print('Collecting data from',filename)
            
            dset            = f['protons']
            dset_columns    = f['columns']
            dset_selections = f['selections']
            dset_counts     = f['event_counts']
            
            #read the data
            columns = list( dset_columns )
            columns_str = [ item.decode("utf-8") for item in columns ]
            if chunk_size is None:
                start=[0]
                stop=[dset.shape[0]]
            else:
                entries = dset.shape[0]
                start = list( range( 0, entries, chunk_size ) )
                stop = start[1:] + [entries]
                
            for idx in range( len( start) ):
                print('\tCollecting events',start[idx], stop[idx] )

                df.append( pd.DataFrame( dset[start[idx]:stop[idx]], 
                                         columns=columns_str ) )
               
                if is2018:
                    cols=['Run', 'EventNum', 'MultiRP', 'Arm', 'RPId1', 'Xi', 'T', 'ThX', 'ThY',
                          'Lep0Pt', 'Lep0Eta', 'Lep0Phi', 'Lep1Pt', 'Lep1Eta', 'Lep1Phi',
                          'InvMass', 'PV_ndof', 'Acopl', 'XiMuMuPlus', 'XiMuMuMinus']
                    coltypes={ "Run": "int64",
                               "EventNum": "int64",
                               "MultiRP": "int32",
                               "Arm": "int32",
                               "RPId1": "int32",
                               "PV_ndof": "int32" }
                else:
                    cols=['Run', 'LumiSection', 'EventNum', 'CrossingAngle', 
                          'MultiRP', 'Arm', 'RPId1',
                          'Xi', 'T', 'XiMuMuPlus', 'XiMuMuMinus',
                          'Lep0Pt', 'Lep1Pt', 'InvMass', 'ExtraPfCands_v2', 'Acopl']
                    coltypes={ "Run": "int64",
                               "LumiSection": "int64",
                               "EventNum": "int64",
                               "MultiRP": "int32",
                               "Arm": "int32",
                               "RPId1": "int32",
                               "ExtraPfCands_v2": "int32" }
                df[-1]=df[-1][cols].astype(coltypes)
              
            #read the selection counters
            selections = list( dset_selections )
            selections_str = [ item.decode("utf-8") for item in selections ]        
            df_counts.append( pd.Series( list( dset_counts ), index=selections_str ) )
    
    n=len( df ) 
    print('\tReturning the result of %d merged datasets'%n)
    df_final=pd.concat(df)
    
    #merge the counts
    df_counts_final = df_counts[0]
    for idx in range( 1, len(df_counts) ):
        df_counts_final = df_counts_final.add( df_counts[idx] )

    #merge the data
    return df_final,df_counts_final
