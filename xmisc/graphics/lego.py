
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Fri Apr 21 15:15:15 EDT 2017 -0400 (Week 16)
## 
## 
## Reference: 
## 
## ************************************************************************

import sys
import numpy as np
import pandas as pd
from pandas import DataFrame

from xmisc.utils.list import *
from xmisc.utils.dataframe import *
from xmisc.graphics.bar3d import bar3dplot,bar3ddata


def bind_pos(x,y,axis):
  x_=as_dataframe(x)
  y_=as_dataframe(y)
  
  df_ = pd.DataFrame(index=range(x_.shape[0]+y_.shape[0]), columns=x_.columns)
  for a in x_.columns:
    ix_=x_[a].tolist()
    iy_=y_[a].tolist()
    ##
    if (a in ["xpos"] and axis==0) \
      or (a in ["ypos"] and axis==1) \
      or (a in ["zpos"] and axis==2):
      ix_max=max(ix_)
      iy_=[e+ix_max+1 for e in iy_]
    ##
    df_[a]=ix_+iy_
  ##
  return(df_)

def rbind_pos(x,y):
  ret=bind_pos(x,y,axis=0)
  return(ret)

def cbind_pos(x,y):
  ret=bind_pos(x,y,axis=1)
  return(ret)

def zbind_pos(x,y):
  ret=bind_pos(x,y,axis=2)
  return(ret)


  

def bindLegobrick(x,axis,naValue=0,*args,**kwargs):
  """
  !@brief bind `Legobrick`
  @para axis `rbind` or `cbind`
  """
  # print("bindLegobrick:x")
  # print(x)
  tmp=bindlist(x,axis=axis,naValue=naValue,*args,**kwargs)
  ret=LegoBrick(data=tmp)
  return(ret)


def cbindLegobrick(x,*args,**kwargs):
  ret=bindLegobrick(x,axis=1,*args,**kwargs)
  return(ret)

def rbindLegobrick(x,*args,**kwargs):
  ret=bindLegobrick(x,axis=0,*args,**kwargs)
  return(ret)


class LegoBrick(DataFrame):
  """
  !@brief `LegoBrick`
  
  """
  def __init__(
    self,
    data=None,
    metadata=dict(),
    name=None
    ):
    super(LegoBrick, self).__init__(
      data=data
      )
    self.nrow=self.shape[0]
    self.ncol=self.shape[1]
    self.metadata = metadata
    self.name = name
    self.bar3ddata=self.get_bar3ddata()
    return(None)
  
  def __reduce__(self):
    return self.__class__, (
      DataFrame(self),
      self.metadata,
      self.name,
      )
  
  def __str__(self):
    ret = super(LegoBrick, self).__str__() + "\nAn instance of `LegoBrick`"
    return(ret)

  def get_bar3ddata(self):
    dz=self.values.flatten()
    ret=bar3ddata(nrow=self.nrow,ncol=self.ncol,dz=dz,**self.metadata)
    return(ret)

  def bind(self,other,axis):
    if not isinstance(other,LegoBrick):
      raise Exception('`other` must be an instance of `LegoBrick`')
    data_=bind(self,other,axis=axis,naValue=0) #XB
    ##
    ret=LegoBrick(data=data_)
    return(ret)

  def cbind(self,other):
    ret=self.bind(other,axis=1)
    return(ret)
    
  def rbind(self,other):
    ret=self.bind(other,axis=0)
    return(ret)

  def plot(self,FUNC_plot=bar3dplot,**kwargs):
    ret=FUNC_plot(x=self.bar3ddata,**kwargs)
    return(ret)


class LegoBrickSet(object):
  """
  !@brief A set of `LegoBrick`
  """
  def __init__(self,x):
    """
    @param x the bricks, a nested list of `pandas.DataFrame`
    """
    if ldepth(x)<2:
      raise Exception('`x` must be a nested list with depth of at lest 2')
    self.datalist=[[LegoBrick(data=ee) if not isinstance(ee,LegoBrick) else ee for ee in e] for e in x]
    self.bar3ddata=self.get_bar3ddata()

  def __str__(self):
    ret = self.datalist.__str__() + "\nBuilt by `LegoBrickSet`"
    return(ret)
    
  def get_bar3ddata(self):
    bar3ddata_list_=[[ee.bar3ddata for ee in e] for e in self.datalist]
    # # print(bar3ddata_list_)    
    ret=rbindlist([cbindlist(e,bindFunc=bind_pos) for e in bar3ddata_list_],bindFunc=bind_pos)
    return(ret)
    
  def plot(self,FUNC_plot=bar3dplot,**kwargs):
    ret=FUNC_plot(x=self.bar3ddata,**kwargs)
    return(ret)



if __name__ == "__main__":
  from tabulate import tabulate
  from matplotlib.backends.backend_pdf import PdfPages

  data_=np.arange(12,0,-1).reshape((3, 4))
  obj=LegoBrick(data=data_)
  print("obj")
  print(tabulate(obj, headers='keys', tablefmt='psql'))
  print("obj.bar3ddata")
  print(tabulate(obj.bar3ddata, headers='keys', tablefmt='psql'))


  print("obj.cbind(obj)",obj.cbind(obj))
  print("obj.rbind(obj)",obj.rbind(obj))
  
  blocklist_=[]
  colorlist_=["#ffff00","#009999","#ff0000","#00cc00","#0033cc","#663399"]
  for i in range(len(colorlist_)):
    block_=LegoBrick(data=data_.copy(),metadata={"color":colorlist_[i]})
    blocklist_.append(block_)

  ##
  blocklist_=lreshape(blocklist_,3,2)
  obj2=LegoBrickSet(blocklist_)
  
  
  print("obj2.bar3ddata")
  print(tabulate(obj2.bar3ddata, headers='keys', tablefmt='psql'))
  

  pdfFpath="lego_main.pdf"
  pp = PdfPages(pdfFpath)
  obj.plot(title="LegoBrick",xlab="x",ylab="y",xticks=True,yticks=True)
  pp.savefig(bbox_inches='tight',transparent=True)
  obj2.plot(title="LegoBrickSet",xlab="x",ylab="y",xticks=False,yticks=False,zlab="Freq.")
  pp.savefig(bbox_inches='tight',transparent=True)
  pp.close()
  
