def ComputeXi(dataframe):
    
    """ computes the proton csi based on the central system kinematics"""

    sqrts=13000.
    dataframe['recXi_pos'] = (1./sqrts)*(dataframe['Lep0Pt']*np.exp(dataframe['Lep0Eta'])+dataframe['Lep1Pt']*np.exp(dataframe['Lep1Eta']))
    dataframe['recXi_neg'] = (1./sqrts)*(dataframe['Lep0Pt']*np.exp(-dataframe['Lep0Eta'])+dataframe['Lep1Pt']*np.exp(-dataframe['Lep1Eta']))
    
    return dataframe
