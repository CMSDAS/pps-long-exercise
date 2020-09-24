#add the DeltaXi to the dataframes so it can be plotted as well
df_data_prep['DeltaXi'] = 1. - df_data_prep[ "Xi" ] / df_data_prep[ "XiMuMu" ]
df_bkg_prep['DeltaXi']  = 1. - df_bkg_prep[ "Xi" ] / df_bkg_prep[ "XiMuMu" ]  

#plot (use the definitions of the previous cell)
compareToBackgroundPrediction('DeltaXi',df_data_prep,msk_data,df_bkg_prep,msk_bkg,bins=np.linspace(-1,1,20))
