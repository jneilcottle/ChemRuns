import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import yt
from yt.units import dimensions
import trident as tri
from mpl_toolkits.axes_grid1 import AxesGrid
from massFracs import *
from yt.funcs import mylog
mylog.setLevel(40) # This sets the log level to "ERROR"

kpc = 3.086e21 #cm

#define the runs and ions
run1 = {'Name':'M1-v480-T1-chem',
    'times': ['0030']}
run3 = {'Name':'M6.2-v3000-T1-chem',
    'times':['0100' ]}
run2 = {'Name':'M3.6-v3000-T3-chem',
    'times':['0110']}


run4 = {'Name':'T1_v480_chi1000',
    'times':['0009']}
run5 = {'Name':'T3_v3000_chi3000',
    'times':['0021']}
run6 = {'Name':'T1_v3000_chi1000',
    'times':['0022']}


ion1 = {'atom':'H',
    'ion':'I',
    'name':'HI',
    'chem': 'fracHI_chem',
    'tri': 'fracHI_tri',
    'ionfolder':'/HI/',
    'rest_wave': 1215.67,
        'data_file': '../Files/S1226-o6-forJNeil',
        'sigma': 4.3394e-18,
        'massNum': 1.0}
ion2 = {'atom':'Mg',
    'ion':'II',
    'name':'MgII',
    'chem': 'fracMgII_chem',
    'tri': 'fracMgII_tri',
    'ionfolder':'/MgII/',
    'rest_wave': 1239.92,
        'data_file': '../Files/S1226-o6-forJNeil',
        'sigma': 6.60717e-21,
        'massNum': 24.3050}
ion3 = {'atom':'C',
    'ion':'III',
    'name':'CIII',
    'chem': 'fracCIII_chem',
    'tri': 'fracCIII_tri',
    'ionfolder':'/CIII/',
    'rest_wave': 977.02,
        'data_file': '../Files/S1226-o6-forJNeil',
        'sigma': 6.359e-18,
        'massNum': 12.0107}
ion4 = {'atom':'C',
    'ion':'IV',
    'name':'CIV',
    'chem': 'fracCIV_chem',
    'tri': 'fracCIV_tri',
    'ionfolder':'/CIV/',
    'rest_wave': 1548.18,
    'data_file': '../Files/S1226-redward-forJNeil',
    'sigma': 2.5347e-18,
    'massNum': 12.0107}
ion5 = {'atom':'N',
    'ion':'V',
    'name':'NV',
    'chem': 'fracNV_chem',
    'tri': 'fracNV_tri',
    'ionfolder':'/NV/',
    'rest_wave': 1242.8,
    'data_file': '../Files/S1226-redward-forJNeil',
    'sigma': 8.3181e-19,   #UM. is it actually e-19?   -12/7/17
    'massNum': 14.0067}
ion6 = {'atom':'O',
    'ion':'VI',
    'name':'OVI',
    'chem': 'fracOVI_chem',
    'tri': 'fracOVI_tri',
    'ionfolder':'/OVI/',
    'rest_wave': 1031.91,
    'data_file': '../Files/S1226-o6-forJNeil',
    'sigma': 1.1776e-18,
    'massNum': 15.9994}
ion7 = {'atom':'Ne',
    'ion':'VIII',
    'name':'NeVIII',
    'chem': 'fracNeVIII_chem',
    'tri': 'fracNeVIII_tri',
    'ionfolder':'/NeVIII/',
    'rest_wave': 770.406,
        'data_file': '../Files/S1226-o6-forJNeil',
        'sigma': 6.74298e-19,
        'massNum': 20.1797}

ionList = []
#ionList.append(ion1)
ionList.append(ion2)
#ionList.append(ion3)
ionList.append(ion4)
#ionList.append(ion5)
ionList.append(ion6)
ionList.append(ion7)

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")

#settings for setting lowest value of colorbar to white
viridis = cm.get_cmap('viridis', 256)
newcolors = viridis(np.linspace(0, 1, 256))
white = np.array([255/256, 255/256, 255/256, 1])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors)

fig = plt.figure()
grid = AxesGrid(fig, (0.1, 0.075, 0.85, 0.85),
            nrows_ncols = (3, 4),
            axes_pad = 0.05,
            cbar_size="3%",
            cbar_pad="0%",
            share_all=False,
            label_mode="1",
            cbar_location="right",
            cbar_mode="single")

run_new = run3
run_old = run6
for i in range(len(run_new['times'])):
    data1 = yt.load('../'+run_new['Name']+'/chkfiles/CT_hdf5_chk_'+run_new['times'][i])
    #add metallicity for Trident estimation fraction fields
    data1.add_field(('gas', 'metallicity'), function=_metallicity, display_name='Metallicity', units='Zsun')

    #open old run
    data2 = yt.load('/Volumes/GiantDrive1/Blob_paper1/Files/'+run_old['Name']+'/KH_hdf5_chk_'+run_old['times'][i])
    #add metallicity for Trident estimation fraction fields
    data2.add_field(('gas', 'metallicity'), function=_metallicity, display_name='Metallicity', units='Zsun')
    fields_tri = []
    fields_chem = []
    #add ion fields
    for ion in ionList:
        ionName = ion['ion']
        atom = ion['atom']
        #add the fields you want to plot
        _ = addfield(data1, atom, ionName, 'frac', 'chem')
        _ = addfield(data1, atom, ionName, 'frac', 'tri')

        #add fields to the old runs
        _ = addfield(data2, atom, ionName, 'frac', 'tri')

        fields_tri.append(ion['tri'])
        fields_chem.append(ion['chem'])

    # Create the plot.  Since SlicePlot accepts a list of fields, we need only
    # do this once.
    fields1 = fields_tri+fields_chem
    p1 = yt.SlicePlot(data1, 'z', fields1, origin='native', width = (0.8, 'kpc'), center = (0, 0.4*kpc, 0))
    p1.set_cmap('all', cmap=newcmp)
    p1.set_zlim('all', 9e-4, 1.)

    p2 = yt.SlicePlot(data2, 'z', fields_tri, origin='native', width = (0.8, 'kpc'), center = (0, 0.4*kpc, 0))
    p2.set_cmap('all', cmap=newcmp)
    p2.set_zlim('all', 9e-4, 1.)


    # For each plotted field, force the SlicePlot to redraw itself onto the AxesGrid
    for j, field in enumerate(fields_tri):
        plot = p2.plots[field]
        plot.figure = fig
        plot.axes = grid[j].axes
        plot.axes.title = "Test"
        plot.cax = grid.cbar_axes[j]

    for j, field in enumerate(fields1):
        plot = p1.plots[field]
        plot.figure = fig
        plot.axes = grid[j+4].axes
        plot.axes.title = "Test"
        plot.cax = grid.cbar_axes[j+4]


    # Finally, redraw the plot on the AxesGrid axes.
    p1._setup_plots()
    p2._setup_plots()

    plt.savefig('oldvnewTrident_'+run_new['Name']+'.png', tight_layout=True)
