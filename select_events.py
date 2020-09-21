import uproot4
import awkward1 as ak
import numpy as np
import pandas as pd
import numba as nb
import scipy.constants

def select_events( events, apply_exclusive=True ):

    selections_ = []
    counts_ = []

    selections_.append( "All" )
    counts_.append( len( events ) )
    
    msk_2muons = ( events.nMuonCand >= 2 )
    events_2muons = events[msk_2muons]    

    dphi = events_2muons.MuonCand.phi[:,0] - events_2muons.MuonCand.phi[:,1]
    
    dphi = np.where( dphi >=  scipy.constants.pi, dphi - 2*scipy.constants.pi, dphi)
    dphi = np.where( dphi <  -scipy.constants.pi, dphi + 2*scipy.constants.pi, dphi)
    acopl = 1. - np.abs(dphi)/scipy.constants.pi

    events_2muons["Acopl"] = acopl

    m1 = events_2muons.MuonCand[:,0]
    m2 = events_2muons.MuonCand[:,1]

    invariant_mass = np.sqrt( 2*m1.pt*m2.pt*( np.cosh(m1.eta - m2.eta) - np.cos(m1.phi - m2.phi) ) )

    events_2muons["InvMass"] = invariant_mass

    energy_com = 13000.
    xi_mumu_plus = (1./energy_com) * ( m1.pt*np.exp(m1.eta) + m2.pt*np.exp(m2.eta) )
    xi_mumu_minus = (1./energy_com) * ( m1.pt*np.exp(-m1.eta) + m2.pt*np.exp(-m2.eta) )

    events_2muons["XiMuMuPlus"] = xi_mumu_plus
    events_2muons["XiMuMuMinus"] = xi_mumu_minus

    pfCands_ = events_2muons.PfCand

    pfCands_["dR_0"] = np.sqrt( ( pfCands_.eta - events_2muons.MuonCand.eta[:,0] )**2 + ( pfCands_.phi - events_2muons.MuonCand.phi[:,0] )**2 )
    pfCands_["dR_1"] = np.sqrt( ( pfCands_.eta - events_2muons.MuonCand.eta[:,1] )**2 + ( pfCands_.phi - events_2muons.MuonCand.phi[:,1] )**2 )

    pfCands_sel1_ = pfCands_[
                    pfCands_.fromPV == 3.0 
                    ]
    pfCands_sel2_ = pfCands_sel1_[
                    pfCands_sel1_.dR_0 > 0.3 
                    ]
    pfCands_sel3_ = pfCands_sel2_[
                    pfCands_sel2_.dR_1 > 0.3 
                    ]
    events_2muons[ "nExtraPfCandPV3" ] = ak.num( pfCands_sel3_ )
    
    msk_muon = ( np.array( events_2muons.MuonCand.pt[:,0] >= 50. ) & np.array( events_2muons.MuonCand.pt[:,1] >= 50. ) &
                 np.array( events_2muons.MuonCand.istight[:,0] == 1 ) & np.array( events_2muons.MuonCand.istight[:,1] == 1 ) &
                 np.array( ( events_2muons.MuonCand.charge[:,0] * events_2muons.MuonCand.charge[:,1] ) == -1 ) )
    selections_.append( "Muon" )
    counts_.append( np.sum( msk_muon ) )
    
    msk_vtx = msk_muon & ( 
        np.array( np.abs( events_2muons.PrimVertexCand.z[:,0] ) <= 15. ) &
        np.array( np.abs( events_2muons.MuonCand.vtxz[:,0] - events_2muons.PrimVertexCand.z[:,0] ) <= 0.02 ) &
        np.array( np.abs( events_2muons.MuonCand.vtxz[:,1] - events_2muons.PrimVertexCand.z[:,0] ) <= 0.02 ) 
        )
    selections_.append( "Vertex" )
    counts_.append( np.sum( msk_vtx ) )
    
    events_sel = None
    if apply_exclusive:
        msk_excl = msk_vtx & ( np.array( events_2muons["InvMass"] >= 110. ) & 
                               np.array( events_2muons["Acopl"] <= 0.009 ) & 
                               np.array( events_2muons["nExtraPfCandPV3"] <= 1 ) )
        selections_.append( "Exclusive" )
        counts_.append( np.sum( msk_excl ) )

        events_sel = events_2muons[ msk_excl ]
    else:
        events_sel = events_2muons[ msk_vtx ]  

    selections_ = np.array( selections_ )
    counts_ = np.array( counts_ )
    
    return ( events_sel, selections_, counts_ )
        
def select_protons(events, branchName="ProtCand"):

    protons_ = events[ branchName ]

    protons_["Run"] = events[ "Run" ]
    protons_["LumiSection"] = events[ "LumiSection" ]
    protons_["BX"] = events[ "BX" ]
    protons_["EventNum"] = events[ "EventNum" ]
    
    protons_["CrossingAngle"] = events[ "CrossingAngle" ]
    
    protons_["Muon0Pt"] = events.MuonCand.pt[:,0]
    protons_["Muon0Eta"] = events.MuonCand.eta[:,0]
    protons_["Muon0Phi"] = events.MuonCand.phi[:,0]
    protons_["Muon0VtxZ"] = events.MuonCand.vtxz[:,0]
    protons_["Muon1Pt"] = events.MuonCand.pt[:,1]
    protons_["Muon1Eta"] = events.MuonCand.eta[:,1]
    protons_["Muon1Phi"] = events.MuonCand.phi[:,1]
    protons_["Muon1VtxZ"] = events.MuonCand.vtxz[:,1]

    protons_["PrimVertexZ"] = events.PrimVertexCand.z[:,0]
    
    protons_["InvMass"] = events[ "InvMass" ]
    protons_["nExtraPfCandPV3"] = events[ "nExtraPfCandPV3" ]
    protons_["Acopl"] = events[ "Acopl" ]

    protons_["XiMuMuPlus"] = events[ "XiMuMuPlus" ]
    protons_["XiMuMuMinus"] = events[ "XiMuMuMinus" ]
    
    msk_num_prot = ( ak.num( protons_.xi ) > 0 )
    protons_ = protons_[ msk_num_prot ]
    
    #print ( len(protons_) )
    
    return protons_
