
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Mon Apr 24 09:41:19 EDT 2017 -0400 (Week 17)
## 
## 
## Reference:
## 
## conda install --channel https://conda.anaconda.org/conda-forge matplotlib
## python bar3d.py
## exec(open("bar3d.py").read(), {'__name__': 'external'})
##
## ## This piece of code was inspired sufficiently by online resources, - e.g.
## ## the `matplotlib` example pages, the `stackoverflow` forum, etc. -
## ## some of which are listed below.
## 
## https://matplotlib.org/examples/color/colormaps_reference.html
## http://stackoverflow.com/questions/27073373/matplotlib-bar3d-variable-alpha
## http://stackoverflow.com/questions/29041326/3d-plot-with-matplotlib-hide-axes-but-keep-axis-labels
## http://stackoverflow.com/questions/15042129/changing-position-of-vertical-z-axis-of-3d-plot-matplotlib
## http://stackoverflow.com/questions/18602660/matplotlib-bar3d-clipping-problems
## https://github.com/matplotlib/matplotlib/issues/7683
## https://tryolabs.com/blog/2013/07/05/run-time-method-patching-python/
## 
## ************************************************************************

import warnings
import types
import numpy as np
import math
import pandas as pd
from tabulate import tabulate

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_pdf import PdfPages
from xmisc.graphics.axes3d_import import bar3d_update,_get_coord_info_update ##XB


## ------------------------------------------------------------------------
## 
## ------------------------------------------------------------------------


def bar3ddata(
  n=3,nrow=None,ncol=None,
  dx=None,
  dy=None,
  dz=None,
  color=None,
  alpha=None
  ):
  if nrow is None:
    nrow=n
  if ncol is None:
    ncol=n
  if dy is None:
    dy=dx
  
  xpos = np.arange(0,nrow,1)
  ypos = np.arange(0,ncol,1)
  # xpos, ypos = np.meshgrid(xpos, ypos)
  ypos, xpos = np.meshgrid(ypos, xpos)
  xpos = xpos.flatten()
  ypos = ypos.flatten()  
  zpos = np.zeros(nrow*ncol)

  if dx is not None:
    dx_ = dx * np.ones_like(zpos)
  else:
    dx_ = None
  
  if dy is not None:
    dy_ = dy * np.ones_like(zpos)
  else:
    dy_ = None
    
  if dz is not None:
    dz_ = np.array(dz)
    dz_.resize(nrow*ncol)
  else:
    dz_ = np.arange(1,nrow*ncol+1,1).flatten()

  if alpha is not None:
    alpha_ = [alpha for i in range(nrow*ncol)]
  else:
    alpha_ = None
    
  if color is not None:
    color_ = [color for i in range(nrow*ncol)]
  else:
    color_ = None
  
  # print("color_",color_)
  
  dict_={
    "xpos":xpos,
    "ypos":ypos,
    "zpos":zpos,
    "dz":dz_
    }
  
  if dx_ is not None:
    dict_["dx"]=dx_
    
  if dy_ is not None:
    dict_["dy"]=dy_
    
  if color_ is not None:
    dict_["color"]=color_
    
  if alpha_ is not None:
    dict_["alpha"]=alpha_
    
    
  df=pd.DataFrame(dict_)
  return(df)


## ------------------------------------------------------------------------
## 
## ------------------------------------------------------------------------

def sph2cart(r, theta, phi):
  '''spherical to Cartesian transformation.'''
  x = r * np.sin(theta) * np.cos(phi)
  y = r * np.sin(theta) * np.sin(phi)
  z = r * np.cos(theta)
  return x, y, z

def sphview(ax):
  '''returns the camera position for 3D axes in spherical coordinates'''
  r = np.square(np.max([ax.get_xlim(), ax.get_ylim()], 1)).sum()
  theta, phi = np.radians((90-ax.elev, ax.azim))
  return r, theta, phi

def ravzip(*itr):
    '''flatten and zip arrays'''
    return zip(*map(np.ravel, itr))

def bar3dplot(
  x,
  elev=45, #30,
  azim=60, #300,
  verbose=False,
  shade=False,
  title=None,
  legend=None,

  ax=None,
  pdfFpath=None,#"PyPlot.pdf",
  figsize=(6.4,4.8),
  
  zpos=0,
  dx=0.9,
  dy=0.9,
  alpha=1,
  color="darkgray",
  edgecolor="gray",
  bgcolor='#ffffff00',
  panecolor='#ffffff00',
  
  xlab=None,
  ylab=None,
  zlab=None,

  grid=True,
  axis=True,
  
  xticks=True,
  yticks=True,
  zticks=True,
  
  xticksmajor=True,
  yticksmajor=True,
  zticksmajor=True,
  
  zsort=True
  ):
  '''
  @param x a pandas dataframe,
           with columns xpos,ypos,zpos,dx,dy,dz,color,alpha;
           columns xpos,ypos,dz are mandatory
  @param zsort None, or True (default) - to deal with bar clipping
           
  ''',

  
  ifDev=False # for developer use only
  zn=None     # for developer use only
  zmax=None   # for developer use only

  
  if not isinstance(x,pd.pandas.core.frame.DataFrame): 
    raise TypeError("`x` must be a pandas dataframe.")

  nrow_=x.shape[0]
  columns_=x.columns

  ##
  # # x.sort_values(['ypos','xpos'], ascending=[True, True], inplace=True)
  
  if not 'xpos' in columns_:
    raise Exception('`xpos` must be in the columns')
  if not 'ypos' in columns_:
    raise Exception('`ypos` must be in the columns')
  if not 'dz' in columns_:
    raise Exception('`dz` must be in the columns')
  
  if not 'zpos' in columns_:
    x['zpos']=[zpos] * nrow_
  if not 'dx' in columns_:
    x['dx']=[dx] * nrow_
  if not 'dy' in columns_:
    x['dy']=[dy] * nrow_
  if not 'alpha' in columns_:
    x['alpha']=[alpha] * nrow_
  if not 'color' in columns_:
    x['color']=[color] * nrow_

  ##
  if (verbose):
    print(tabulate(x, headers='keys', tablefmt='psql'))

  
  xpos = x['xpos'].tolist()
  ypos = x['ypos'].tolist()
  zpos = x['zpos'].tolist()
  dx = x['dx'].tolist()
  dy = x['dy'].tolist()
  dz = x['dz'].tolist()
  alpha = x['alpha'].tolist()
  color = x['color'].tolist()

  ## (for testing)
  if ifDev:
    if zmax in [None]:
      title_= "(None)"
    elif zmax in [False]:
      title_="(zo[%d][i])" %(zn)
    else:
      title_="(max(zo[%d]) - zo[%d][i])" %(zn,zn)
      
    if title is not None:
      title="%s %s" % (title,title_)
  
  ## ##
  if ax is None:
    fig = plt.figure(figsize=figsize)
    if title is not None:
      fig.suptitle(title)
    ##
    ax = fig.gca(projection='3d')  

  ## XB -  update to remove axes margins
  ax.xaxis._get_coord_info_ori=ax.xaxis._get_coord_info
  ax.yaxis._get_coord_info_ori=ax.yaxis._get_coord_info
  ax.zaxis._get_coord_info_ori=ax.zaxis._get_coord_info
  
  ax.xaxis._get_coord_info=types.MethodType(_get_coord_info_update,ax.xaxis)
  ax.yaxis._get_coord_info=types.MethodType(_get_coord_info_update,ax.yaxis)
  ax.zaxis._get_coord_info=types.MethodType(_get_coord_info_update,ax.zaxis)

  ## XB -  update to allow turning off `shade`
  ax.bar3d=types.MethodType(bar3d_update,ax) 
  
  ##
  ax.patch.set_facecolor(bgcolor)

  ##
  ax.grid(grid)
  if grid:
    # ax.zaxis._axinfo["grid"]['color'] = "#ee0009"
    ax.xaxis._axinfo["grid"]['linestyle'] = ":"
    ax.yaxis._axinfo["grid"]['linestyle'] = ":"
    ax.zaxis._axinfo["grid"]['linestyle'] = ":"

  ##
  if xticks is False:
    # ax.set_xticklabels([])
    if xticksmajor is False:
      ax.set_xticks([])
    else:
      for tic in ax.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
  
  if yticks is False:
    # ax.set_yticklabels([])
    if yticksmajor is False:
      ax.set_yticks([])
    else:
      for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False

  if zticks is False:
    # ax.set_zticklabels([])
    if zticksmajor is False:
      ax.set_zticks([])
    else:
      for tic in ax.zaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
      
  ###
  if xlab is not None:
    ax.xaxis.set_rotate_label(False)
    ax.set_xlabel(xlab, rotation=0)
    
  if ylab is not None:
    ax.yaxis.set_rotate_label(False)
    ax.set_ylabel(ylab, rotation=0)
    
  if zlab is not None:
    ax.zaxis.set_rotate_label(False)  # disable automatic rotation
    ax.set_zlabel(zlab, rotation=95)
  
  
  # Get rid of the pane colors
  # panecolor=(1.0, 1.0, 1.0, 0.0)
  panecolor=colors.to_rgba(panecolor)
  ax.w_xaxis.set_pane_color(panecolor)
  ax.w_yaxis.set_pane_color(panecolor)
  ax.w_zaxis.set_pane_color(panecolor)

  # Get rid of the spines
  ax.w_xaxis.line.set_color(panecolor) 
  ax.w_yaxis.line.set_color(panecolor) 
  ax.w_zaxis.line.set_color(panecolor)
  

  ## After removing axes margins in 3D plot
  # # ax.set_zlim3d(0, max(dz)+0)
  ax.set_ylim3d(0, max(ypos)+1)
  ax.set_xlim3d(0, max(xpos)+1)

  if axis in [None, False]:
    ax.set_axis_off()
    
  ## add legend
  if legend is not None:
    ax.legend(**legend)
    
  ## rotate the axes
  ax.view_init(elev=elev, azim=azim) #XB

  if azim > 90:
    warnings.warn('Possible bar clipping when `azim` is larger than 90')

  ## 
  if not zsort in [None, False, True]:
    raise Exception('`zsort` must be in [None, False, True]')
  
  ## reorder_z - None##
  if zsort in [None,False]:
    index_=range(nrow_)
    for i in index_:
      pl = ax.bar3d(
        xpos[i], ypos[i], zpos[i], dx[i], dy[i], dz[i],
        color=color[i],
        shade=shade,
        alpha=alpha[i], 
        edgecolor=edgecolor,
        linewidth=0.5
        )
  
 
  ## reorder_z - True##
  elif zsort in [True]:
    xyz = np.array(sph2cart(*sphview(ax)), ndmin=3).T
    zo = np.multiply([xpos,ypos,np.zeros_like(xpos)],xyz).sum(0)

    # # print("zo",zo)
    for i in range(len(xpos)):
      pl = ax.bar3d(
        xpos[i], ypos[i], zpos[i],
        dx[i], dy[i], dz[i],
        color=color[i],
        zsort='average',
        shade=shade,
        alpha=alpha[i],
        edgecolor=edgecolor,
        linewidth=0.5
        )
      # # pl._sort_zpos = zo[2][i]


      ## 
      if azim <= 90:
        pl._sort_zpos = max(zo[2])-zo[2][i] #or zo[2][i]
      elif azim < 135:
        pl._sort_zpos = None
      elif azim < 160:
        pl._sort_zpos = max(zo[0])-zo[0][i]
      elif azim <= 180:
        pl._sort_zpos = zo[0][i]
      elif azim <= 270:
        pl._sort_zpos = None
      elif azim <= 290:
        pl._sort_zpos = zo[1][i]
      elif azim <= 315:
        pl._sort_zpos = max(zo[1])-zo[1][i]
      elif azim < 360:
        pl._sort_zpos = None
      
      ## (for testing)
      if ifDev:
        if zmax in [None]:
          pl._sort_zpos = None
        elif zmax in [False]:
          pl._sort_zpos = zo[zn][i]
        else:
          pl._sort_zpos = max(zo[zn]) - zo[zn][i]
      
      
  ## ##
  if pdfFpath is None:
    # plt.show()
    return(None)
  else:
    pp = PdfPages(pdfFpath)
    pp.savefig(bbox_inches='tight')
    pp.close()
    return(None)


if __name__ == "__main__":
  data_=bar3ddata()
  print(tabulate(data_, headers='keys', tablefmt='psql'))

  data2_=bar3ddata(nrow=3,ncol=6)
  print(tabulate(data2_, headers='keys', tablefmt='psql'))
  
  # ## (for developer use only)
  # from xmisc.graphics.legoplot.lego import LegoBrickSet
  # if False:
  #   df=bar3ddata(n=3)
  
  #   obj2=LegoBrickSet(
  #     x=[
  #     [df for i in range(2)],
  #     [df for i in range(2)]
  #     ]
  #     )
  #   data_=obj2.data

  #   pdfFpath="bar3d_main_dev.pdf"
  #   pp = PdfPages(pdfFpath)

  #   for zn in [0,1,2]:
  #     for zmax in [False, True, None]:
  #       for angle in range(0, 360, 1):
  #         # raw_input('Press enter to show figure: ')
  #         print("angle: %d"%angle)
  #         fig=bar3dplot(x=data_,azim=angle,title="angle: %d"%angle,xlab="x",ylab="y",xticks=True,yticks=True,ifDev=True,zn=zn,zmax=zmax)
    
  #         pp.savefig(bbox_inches='tight',transparent=True)
  #         plt.close() # release memory
  #   ##
  #   pp.close()

