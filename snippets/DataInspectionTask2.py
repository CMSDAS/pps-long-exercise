def ComputeXi(dataframe):
    
    """ computes the proton csi based on the central system kinematics"""

    sqrts=13000.
    dataframe['recXi_pos'] = (1./sqrts)*(dataframe['Muon0Pt']*np.exp(dataframe['Muon0Eta'])+dataframe['Muon1Pt']*np.exp(dataframe['Muon1Eta']))
    dataframe['recXi_neg'] = (1./sqrts)*(dataframe['Muon0Pt']*np.exp(-dataframe['Muon0Eta'])+dataframe['Muon1Pt']*np.exp(-dataframe['Muon1Eta']))
    
    return dataframe
