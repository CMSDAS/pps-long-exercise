import uproot4
import awkward1 as ak
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplhep
import numba as nb
import scipy.constants
import h5py
import argparse

from select_events import *

parser = argparse.ArgumentParser(description = 'Creates data table from ntuple')
parser.add_argument('--files', help = 'File paths' )
parser.add_argument('--label', help = 'Label suffix' )
parser.add_argument('--apply_exclusive', dest = 'apply_exclusive', action = 'store_true', required = False, help = '' )
parser.add_argument('--random_protons', dest = 'random_protons', action = 'store_true', required = False, help = '' )
parser.add_argument('--resample_factor', dest = 'resample_factor', type = int, required = False, default = -1, help = '' )
parser.add_argument('-s', '--start', dest = 'start', type = int, required = False, default = -1, help = 'First event to process' )
parser.add_argument('-n', '--events', dest = 'events', type = int, required = False, default = -1, help = 'Number of events to process' )
parser.add_argument('--read_size', dest = 'read_size', required = False, default = "150MB" , help = 'Input buffer size.' )
#parser.add_argument('-v', '--verbose', action = 'store_true', dest = 'verbose', required = False, help = 'Enable verbose' )
args = parser.parse_args()

fileNames_ = args.files.split(",")
print( "Reading files: " )
for item in fileNames_: print ( item )
label_ = args.label
print ( "Label: " + label_ ) 
apply_exclusive_ = False
if hasattr( args, 'apply_exclusive') and args.apply_exclusive: apply_exclusive_ = args.apply_exclusive
print ( "Apply exclusive selection: {}".format( apply_exclusive_ ) )
random_protons_ = False
if hasattr( args, 'random_protons') and args.random_protons: random_protons_ = args.random_protons
print ( "Random protons: {}".format( random_protons_ ) )
resample_factor_ = -1
if hasattr( args, 'resample_factor'): resample_factor_ = args.resample_factor
print ( "Resample factor: {}".format( resample_factor_ ) )
firstEvent_ = None
if hasattr( args, 'start' ) and args.start > 0: firstEvent_ = args.start
print ( "First event to process: {}".format( "All" if firstEvent_ is None else firstEvent_ ) )
maxEvents_ = None
if hasattr( args, 'events' ) and args.events > 0: maxEvents_ = args.events
print ( "Number of events to process: {}".format( "All" if maxEvents_ is None else maxEvents_ ) )
read_size_ = "150MB"
if hasattr( args, 'read_size' ): read_size_ = args.read_size
print ( "Input buffer size: {}".format( read_size_ ) )

resample_ = False
if resample_factor_ > 1: resample_ = True

entrystop_ = maxEvents_ if firstEvent_ is None else ( firstEvent_ + maxEvents_ )

np.random.seed( 42 )

dset_chunk_size = 50000

columns = ( "Run", "LumiSection", "BX", "EventNum", "CrossingAngle",
            "MultiRP", "Arm", "RPId1", "RPId2", "TrackX1", "TrackY1", "TrackX2", "TrackY2",
            "Xi", "T", "ThX", "ThY", "Time",
            "TrackThX_SingleRP", "TrackThY_SingleRP",
            "Track1ThX_MultiRP", "Track1ThY_MultiRP", "Track2ThX_MultiRP", "Track2ThY_MultiRP",
            "Muon0Pt", "Muon0Eta", "Muon0Phi", "Muon0VtxZ", "Muon1Pt", "Muon1Eta", "Muon1Phi", "Muon1VtxZ",
            "PrimVertexZ", "InvMass", "ExtraPfCands", "Acopl", "XiMuMuPlus", "XiMuMuMinus" )
protons_keys = {}
for col_ in columns:
    protons_keys[ col_ ] = col_
protons_keys[ "MultiRP" ] = "ismultirp"
protons_keys[ "Arm" ] = "arm"
protons_keys[ "RPId1" ] = "rpid1"
protons_keys[ "RPId2" ] = "rpid2"
protons_keys[ "TrackX1" ] = "trackx1"
protons_keys[ "TrackY1" ] = "tracky1"
protons_keys[ "TrackX2" ] = "trackx2"
protons_keys[ "TrackY2" ] = "tracky2"
protons_keys[ "Xi" ] = "xi"
protons_keys[ "T" ] = "t"
protons_keys[ "Time" ] = "time"
protons_keys[ "TrackThX_SingleRP" ] = "trackthx_single"
protons_keys[ "TrackThY_SingleRP" ] = "trackthy_single"
protons_keys[ "Track1ThX_MultiRP" ] = "trackthx_multi1"
protons_keys[ "Track1ThY_MultiRP" ] = "trackthy_multi1"
protons_keys[ "Track2ThX_MultiRP" ] = "trackthx_multi2"
protons_keys[ "Track2ThY_MultiRP" ] = "trackthy_multi2"
protons_keys[ "ExtraPfCands" ] = "nExtraPfCandPV3"

counts_label_protons_ = "Protons" if not random_protons_ else "ProtonsRnd"

with h5py.File( 'output-' + label_ + '.h5', 'w') as f:

    dset = f.create_dataset( 'protons', ( dset_chunk_size, len( columns ) ), compression="gzip", chunks=True, maxshape=( None , len( columns ) ) )
    print ( "Initial dataset shape: {}".format( dset.shape ) )

    protons_list = {}
    for col_ in columns:
        protons_list[ col_ ] = []
    
    selections = None
    counts = None
    
    dset_slice = 0
    dset_idx = 0
    dset_entries = 0

    for file_ in fileNames_:
        print ( file_ ) 
        root_ = uproot4.open( file_ )

        print ( "Number of events in tree: {}".format( np.array( root_["ggll_miniaod/ntp1/nMuonCand"] ).size ) )

        tree_ = root_["ggll_miniaod/ntp1"]
 
        keys = ["Run", "LumiSection", "BX", "EventNum", "CrossingAngle","nHLT", "HLT_Accept", "HLT_Prescl", "HLT_Name",
            "nMuonCand", "MuonCand_pt", "MuonCand_eta", "MuonCand_phi", "MuonCand_e", "MuonCand_charge", "MuonCand_vtxz", "MuonCand_istight",
            "nPrimVertexCand", "PrimVertexCand_z", "PrimVertexCand_chi2", "PrimVertexCand_ndof", "PrimVertexCand_tracks",
            "Weight", "PUWeightTrue"]
        keys.append( "nPfCand" )
        keys.extend( tree_.keys( filter_name="PfCand*" ) ) 
        keys.append( "nRecoProtCand" )
        keys.extend( tree_.keys( filter_name="ProtCand*" ) )  
        print ( keys )
        
        for events_ in tree_.iterate( keys , library="ak", how="zip", step_size=read_size_, entry_start=firstEvent_, entry_stop=entrystop_ ):
            print ( len(events_), events_ )
            
            #events_sel_ = select_events( events_, apply_exclusive_ )
            events_sel_, selections_, counts_ = select_events( events_, apply_exclusive=apply_exclusive_ )
    
            # Repeat events by resample factor
            if resample_:
                counts_ = counts_ * resample_factor_
    
            if selections is None:
                selections = selections_
                counts = counts_
            else:
                msk_selections = np.full_like( selections, False, dtype='bool' )
                for key in selections_:
                    msk_selections |= ( selections == key )
                counts[ msk_selections ] += counts_
    
            # Repeat events by resample factor
            if resample_:
                events_sel_ = ak.concatenate( ( [events_sel_] * resample_factor_ ), axis=0 )
                
            # Randomize proton arrays
            if random_protons_:
                protons_sel_ = events_sel_.ProtCand
            
                index_rnd_ = np.random.permutation( len( events_sel_ ) )
            
                protons_rnd_ = protons_sel_[ index_rnd_ ]
            
                events_sel_[ "ProtCandRnd" ] = protons_rnd_    
        
                print ( ak.num( events_sel_.ProtCand ) )
                print ( ak.num( events_sel_.ProtCandRnd ) )    
    
            #protons_ = select_protons( events_sel_ )
            protons_ = None
            if not random_protons_: protons_ = select_protons( events_sel_, "ProtCand" )
            else:                   protons_ = select_protons( events_sel_, "ProtCandRnd" )    
    
            counts_protons_ = len( protons_ )
            if not counts_label_protons_ in selections:
                selections = np.concatenate( ( selections, np.array( [ counts_label_protons_ ] ) ) )
                counts = np.concatenate( ( counts, np.array( [counts_protons_] ) ) )
            else:    
                counts[ selections == counts_label_protons_ ] += counts_protons_ 
    
            print ( selections )
            print ( counts )
    
            for col_ in columns:
                protons_list[ col_ ] = np.array( ak.flatten( protons_[ protons_keys[ col_ ] ] ) )

            arr_size_ = len( protons_list[ "Xi" ] )
            print ( "Flattened array size: {}".format( arr_size_ ) )

            dset_entries += arr_size_

            if dset_entries > dset_chunk_size:
                resize_factor_ = ( dset_entries // dset_chunk_size )
                chunk_resize_  = resize_factor_ * dset_chunk_size

                print ( "Resizing output dataset by {} entries.".format( chunk_resize_ ) )
                dset.resize( ( dset.shape[0] + chunk_resize_ ), axis=0 )
                print ( "Dataset shape: {}".format( dset.shape ) )
                        
                dset_slice += resize_factor_
                # Count the rest to the chunk size 
                dset_entries = ( dset_entries % dset_chunk_size )

            print ( "Stacking data." )
            data_ = np.stack( list( protons_list.values() ), axis=1 )
            print ( data_.shape )
            print ( data_ )

            dset_idx_next_ = dset_idx + arr_size_
            print ( "Slice: {}".format( dset_slice ) )
            print ( "Writing in positions ({},{})".format( dset_idx, dset_idx_next_ ) )
            dset[ dset_idx : dset_idx_next_ ] = data_
            dset_idx = dset_idx_next_ 

        # Iteration on input files
        root_.close()
    
    # Reduce dataset to its final size 
    print ( "Reduce dataset." )
    dset.resize( ( dset_idx ), axis=0 ) 
    print ( "Dataset shape: {}".format( dset.shape ) )

    print ( "Writing column names and event counts.")

    columns_ = np.array( columns, dtype='S' )
    print ( columns_ )
    
    event_counts_ = counts
    print ( event_counts_ )

    selections_ = np.array( selections, dtype='S' )
    print ( selections_ )

    dset_columns = f.create_dataset( 'columns', data=columns_ )
    dset_counts = f.create_dataset( 'event_counts', data=event_counts_ )
    dset_selections = f.create_dataset( 'selections', data=selections_ )

    print ( dset )
    print ( dset[-1] )   
    print ( dset_columns )
    print ( list( dset_columns ) )   
    print ( dset_counts )
    print ( list( dset_counts ) )
    print ( dset_selections )
    print ( list( dset_selections ) )

