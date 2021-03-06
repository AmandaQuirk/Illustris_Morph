import pandas
import h5py
from PyML import machinelearning as pyml
import numpy as np

#need to pick a snapshot, filter, and camera
snapshot='snapshot_068'
filt='NC-F115W'
camera='CAMERA0'
#for file saving
z=2
Filter=115
C=0

#data files
morph_catalog= h5py.File("/astro/snyder_lab2/Illustris/MorphologyAnalysis/nonparmorphs_SB25_12filters_morestats.hdf5")
merg_catalog=h5py.File('/astro/snyder_lab2/Illustris/MorphologyAnalysis/imagedata_mergerinfo.hdf5')

#reads in values for each parameter--ONLY FOR ONE CAMERA
gini=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['GINI'].value
m20=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['M20'].value
asym=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['ASYM'].value
mprime=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['MID1_MPRIME'].value
d=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['MID1_DSTAT'].value
i_stat=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['MID1_ISTAT'].value
cc=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['CC'].value
mag=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['MAG'].value
RP=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['RP'].value
PIX_AS=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['PIX_ARCSEC'].value
mass=morph_catalog['nonparmorphs'][snapshot]['Mstar_Msun'].value
SFR=morph_catalog['nonparmorphs'][snapshot]['SFR_Msunperyr'].value
num_merg=merg_catalog['mergerinfo'][snapshot]['latest_NumMajorMergersLastGyr'].value
PSF=morph_catalog['nonparmorphs'][snapshot][filt]['CAMERA0']['APPROXPSF_ARCSEC'].value

#below gets rid of all rows with NaN values and saves finite numbers to arrays
gini_good=[]
m20_good=[]
asym_good=[]
mprime_good=[]
d_good=[]
i_good=[]
cc_good=[]
num_merg_good=[]
mag_good=[]
RP_good=[]
mass_good=[]
SFR_good=[]
for i in range(len(gini)):
	if np.isnan(gini[i])==False and np.isnan(m20[i])==False and np.isnan(asym[i])==False and np.isnan(mprime[i])==False and np.isnan(d[i])==False and np.isnan(i_stat[i])==False and np.isnan(cc[i])==False and np.isnan(num_merg[i])==False:
		gini_good.append(gini[i])
		m20_good.append(m20[i])
		asym_good.append(asym[i])
		mprime_good.append(mprime[i])
		d_good.append(d[i])
		i_good.append(i_stat[i])
		cc_good.append(cc[i])
		mag_good.append(mag[i])
		RP_good.append(RP[i])
		mass_good.append(mass[i])
		SFR_good.append(SFR[i])
		if num_merg[i]==0:
			num_merg_good.append(0)
		if num_merg[i]!=0:
			num_merg_good.append(1)

#creates an array for F(M20, Gini) and d(M20, gini)
Fgm20_good=[]
Dgm20_good=[]
for i in range(len(gini_good)):
	F=(-0.693*m20_good[i])+(4.95*gini_good[i])-3.85
	if gini_good[i]>= ((0.14*m20_good[i])+0.778):
		Fgm20_good.append(abs(F))
	if gini_good[i]< ((0.14*m20_good[i])+0.778):
                Fgm20_good.append(-abs(F))
	Dgm20_good.append(abs((-0.14*m20_good[i])-gini_good[i]+0.33)/(0.14))

#print(len(Fgm20_good))
#print(len(Dgm20_good))
#print(len(gini_good), len(m20_good), len(asym_good), len(mprime_good), len(d_good), len(i_good), len(cc_good), len(num_merg_good))

#creates cuts to limit the population
gini_cut=[]
m20_cut=[]
asym_cut=[]
mprime_cut=[]
d_cut=[]
i_cut=[]
cc_cut=[]
num_merg_cut=[]
Fgm20_cut=[]
Dgm20_cut=[]
for i in range(len(gini_good)):
	if (10**10.5)<mass_good[i] and (3*PSF[0])<(RP_good[i]*PIX_AS[0]) and 5<SFR_good[i] and 23>mag_good[i]:
		gini_cut.append(gini_good[i])
		m20_cut.append(m20_good[i])
		asym_cut.append(asym_good[i])
		mprime_cut.append(mprime_good[i])
		d_cut.append(d_good[i])
		i_cut.append(i_good[i])
		cc_cut.append(cc_good[i])
		num_merg_cut.append(num_merg_good[i])
		Fgm20_cut.append(Fgm20_good[i])
		Dgm20_cut.append(Dgm20_good[i])

#print(len(Fgm20_cut), len(Dgm20_cut))	
#print(len(gini_cut), len(m20_cut), len(asym_cut), len(mprime_cut), len(d_cut), len(i_cut), len(cc_cut), len(num_merg_cut))

#does PC analysis
#NEEDS TO BE GOOD FOR WHOLE POPULATION OR CUT FOR LIMITED POPULATION
parameters = ['C','M20','GINI','ASYM','MPRIME','I','D']
pcd = {}
pcd['C'] = cc_cut
pcd['M20'] = m20_cut
pcd['GINI'] = gini_cut
pcd['ASYM'] = asym_cut
pcd['MPRIME'] = mprime_cut
pcd['I'] = i_cut
pcd['D'] = d_cut

npmorph = pyml.dataMatrix(pcd, parameters)
pc=pyml.pcV(npmorph)
PCs=pandas.DataFrame(pc.X)
#can also do .values and .vectors

#creates a dictionary with the non NaN values
#_good for whole population _cut for subpopulation
dict={}
dict['GINI']=gini_cut
dict['M20']=m20_cut
dict['ASYM']=asym_cut
dict['MID1_MPRIME']=mprime_cut
dict['MID1_DSTAT']=d_cut
dict['MID1_ISTAT']=i_cut
dict['CC']=cc_cut
dict['FgM20']=Fgm20_cut
dict['DgM20']=Dgm20_cut
dict['mergerFlag']=num_merg_cut #the key must be mergerFlag
dict['PC1']=PCs[0]
dict['PC2']=PCs[1]
dict['PC3']=PCs[2]
dict['PC4']=PCs[3]
dict['PC5']=PCs[4]
dict['PC6']=PCs[5]
dict['PC7']=PCs[6]

#converts dictionary to a pandas format for random forest to use
df=pandas.DataFrame(dict)
#print(df)

#for running random forest-- labels and order must match that in the machinelearning.py script
cols=['GINI','M20','ASYM','MID1_MPRIME','MID1_DSTAT','MID1_ISTAT','CC', 'FgM20', 'DgM20', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7']

result, labels, label_probability = pyml.randomForestMC(df,iterations=1000)
#result = summary statistics, feature importances (N iterations x N statistics/importances)
#labels = labels following random forest (N galaxies x N iterations)
#label_probability = probability of label following random forest (N galaxies x N iterations)

#saves the output as a file
result.to_pickle('/Users/aquirk/Desktop/result_cut_PC_{}_{}_{}.pkl'.format(C,z,Filter))
labels.to_pickle('/Users/aquirk/Desktop/labels_cut_PC_{}_{}_{}.pkl'.format(C,z,Filter))
label_probability.to_pickle('/Users/aquirk/Desktop/label_probability_cut_PC_{}_{}_{}.pkl'.format(C,z,Filter))
PCs.to_pickle('/Users/aquirk/Desktop/pc_cut_{}_{}_{}.pkl'.format(C,z,Filter))
