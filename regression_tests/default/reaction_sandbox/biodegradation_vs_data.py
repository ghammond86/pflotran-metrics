import sys
import os
try:
  pflotran_dir = os.environ['PFLOTRAN_DIR']
except KeyError:
  try:
    pflotran_dir = '../../'
  except KeyError:
    print('PFLOTRAN_DIR must point to PFLOTRAN installation directory and be defined in system environment variables.')
    sys.exit(1)
sys.path.append(pflotran_dir + '/src/python')
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
import pflotran as pft

if len(sys.argv) < 2:
    print("\nPlease use one of the following commands:\n\n  python %s biodegradation-obs-0.pft\n  python %s biodegradation_hill-obs-0.pft\n  python %s flexible_biodegradation_hill-obs-0.pft\n"%(sys.argv[0],sys.argv[0],sys.argv[0]))
    sys.exit(0)

observation_filename = sys.argv[1]

legend_fontsize = 'small'

def plot_experimental(plt):
  data = []
  data.append([0.1,8.59e-4])
  data.append([0.9,5.6e-4])
  data.append([1.02,3.9e-4])
  data.append([1.45,2.4e-4])
  data.append([1.9,2.1e-4])
  data.append([2.23,8.36e-5])
  data.append([2.8,3.1e-5])
  data.append([3.14,1.1e-5])
  data.append([3.8,8.8e-6])
  data.append([4.41,2.42e-6])
  data.append([5.02,2.35e-6])
  data.append([6.3,1.54e-6])
  data.append([6.9,8.49e-7])
  x = []
  y = []
  for i in range(len(data)):
    x.append(data[i][0])
    y.append(data[i][1])
  plt.scatter(x,y,label='Aaq (exper.)',facecolors='none',edgecolors='black')

def plot_aqueous(plt,filename,scale_string):
  plt.xlabel('Time [d]')
  plt.ylabel('Aqueous Concentration [M]')

  plt.yscale(scale_string)

  maxval = -1.e20
  minval = 1.e-10
  columns = [2,3,4,5]
  for icol in range(len(columns)):
    data = pft.Dataset(filename,1,columns[icol])
    ydata = data.get_array('y')
    maxval = max(maxval,np.amax(ydata))
    plt.plot(data.get_array('x'),data.get_array('y'),
             label=aq_labels[icol],c=aq_colors[icol])
  if scale_string == 'linear':
    plt.ylim(-.05*maxval,1.05*maxval)
    legend_loc = 'upper right'
  else:
    plt.ylim(0.5*minval,2.*maxval)
    legend_loc = 'lower right'
  plot_experimental(plt)

  #'best'         : 0, (only implemented for axis legends)
  #'upper right'  : 1,
  #'upper left'   : 2,
  #'lower left'   : 3,
  #'lower right'  : 4,
  #'right'        : 5,
  #'center left'  : 6,
  #'center right' : 7,
  #'lower center' : 8,
  #'upper center' : 9,
  #'center'       : 10,
  # xx-small, x-small, small, medium, large, x-large, xx-large, 12, 14
  plt.legend(title='Aqueous',loc=legend_loc,fontsize=legend_fontsize)
  legend = plt.gca().get_legend()
  legend.get_frame().set_fill(False)
  legend.draw_frame(False)

def plot_immobile(plt,filename,scale_string):
  plt.twinx()
  plt.ylabel('Immobile Concentration [mol/m^3]')
  plt.yscale(scale_string)
  maxval = -1.e20
  minval = 1.e-10
  columns = [6]
  for icol in range(len(columns)):
    data = pft.Dataset(filename,1,columns[icol])
    ydata = data.get_array('y')
    maxval = max(maxval,np.amax(ydata))
    plt.plot(data.get_array('x'),data.get_array('y'),
             label=im_labels[icol],ls='--',c=im_colors[icol])
  if scale_string == 'linear':
    plt.ylim(-0.05*maxval,1.05*maxval)
    legend_loc = 'center right'
  else:
    plt.ylim(0.5*minval,2.*maxval)
    legend_loc = 'lower left'

  plt.legend(title='Immobile',loc=legend_loc,fontsize=legend_fontsize)
  legend = plt.gca().get_legend()
  legend.get_frame().set_fill(False)
  legend.draw_frame(False)

aq_labels = []
aq_labels.append('Aaq')
aq_labels.append('Baq')
aq_labels.append('Caq')
aq_labels.append('Daq')
aq_labels.append('Eaq')
aq_labels.append('Faq')

aq_colors = []
aq_colors.append('blue')
aq_colors.append('green')
aq_colors.append('red')
aq_colors.append('cyan')
aq_colors.append('magenta')
aq_colors.append('y')

im_labels = []
im_labels.append('Xim')
im_labels.append('Yim')

im_colors = []
im_colors.append('darkorange')
im_colors.append('navy')

f = plt.figure(figsize=(16,6))

#linear scale
plt.subplot(1,2,1)
plt.title('Time History - Linear Scale')
scale_string = 'linear'
plot_aqueous(plt,observation_filename,scale_string)
plot_immobile(plt,observation_filename,scale_string)

#log scale
plt.subplot(1,2,2)
plt.title('Time History - Log Scale')
scale_string = 'log'
plot_aqueous(plt,observation_filename,scale_string)

f.subplots_adjust(hspace=0.2,wspace=0.40,
                  bottom=.12,top=.92,
                  left=.08,right=.92)

plt.show()
