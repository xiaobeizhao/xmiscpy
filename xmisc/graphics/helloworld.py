
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Sun May 07 03:57:20 EDT 2017 -0400 (Week 18)
## 
## 
## Reference: 
## 
## 
## ************************************************************************

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from xmisc.utils.logging import logsave
from xmisc.utils.dataframe import cbindlist
from xmisc.graphics.lego import LegoBrickSet
from xmisc.graphics.bar3d import bar3dplot


class HelloWorld(LegoBrickSet):
  """
  !@brief a representation of terminal-style 'Hello World' via `LegoBrickSet`
  """
  def __init__(
    self
    ):
    datalist_=self.get_datalist()
    super(HelloWorld, self).__init__(
      x=datalist_
      )
    self.grid2ddata=self.get_grid2ddata()
  
  def get_datalist(self):
    H_=[
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1],
      [1,1,1,1,1,1,1],
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1]
      ]
    e_=[
      [0,1,1,1,1,1,0],
      [1,1,0,0,0,0,0],
      [1,1,1,1,1,1,1],
      [1,1,0,0,0,1,1],
      [0,1,1,1,1,1,0]
      ]
    l_=[
      [1,1,1,1,1,1],
      [0,0,1,1,0,0],
      [0,0,1,1,0,0],
      [0,0,1,1,0,0],
      [0,0,1,1,0,0],
      [0,0,1,1,0,0],
      [0,1,1,1,0,0]
      ]
    o_=[
      [0,1,1,1,1,1,0],
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1],
      [0,1,1,1,1,1,0]      
      ]
    comma_=[
      [1,1,0],
      [0,1,1],
      [0,1,1]
      ]
    W_=[      
      [1,1,0,0,0,1,1],
      [1,1,1,0,1,1,1],
      [1,1,1,1,1,1,1],
      [1,1,1,1,1,1,1],
      [1,1,0,1,0,1,1],
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1]      
      ]
    r_=[
      [1,1,0,0,0,0],
      [1,1,0,0,0,0],
      [1,1,0,0,0,0],
      [1,1,1,0,0,0],
      [1,1,0,1,1,1]
      ]
    d_=[
      [0,1,1,1,1,1,1],
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1],
      [1,1,0,0,0,1,1],
      [0,1,1,1,1,1,1],
      [0,0,0,0,0,1,1],
      [0,0,0,0,0,1,1]      
      ]
    cursor_=[
      [1,1,1,1,1,1,1]
      ]

    # # marleft_=[[0 for i in range(7)]]
    # # marright_=[[0 for i in range(14)]]
    row_=[
      H_,[[0]],e_,[[0]],l_,[[0,0]],l_,[[0]],o_,[[0,0]],comma_,[[0,0,0,0,0]],W_,[[0]],o_,[[0,0]],r_,[[0]],l_,[[0,0]],d_,[[0]],cursor_
      ]
    # # row_=[np.array(e) for e in row_]
    # print(row_)
    datalist_=[row_]
    # # datalist_=[
    # #   [np.zeros((14,np.array(e).shape[1])) for e in row_],
    # #   row_,
    # #   [np.zeros((14,np.array(e).shape[1])) for e in row_]
    # #   ]
    return(datalist_)

  def get_bar3ddata(self):
    df_=LegoBrickSet.get_bar3ddata(self)
    df_=df_[df_.dz>0]
    df_=df_.assign(color="#000000")
    df_=df_.assign(color="#00ff00")
    df_=df_.assign(dx=1.0)
    df_=df_.assign(dy=1.0)

    (df_.xpos,df_.zpos)=(df_.zpos,df_.xpos)
    (df_.dx,df_.dz)=(df_.dz,df_.dx)
    # print("df_",df_)
    return(df_)

  def get_grid2ddata(self):
    df_=self.bar3ddata.copy()
    df_=df_.assign(dx=0.0)
    return(df_)

    
  def plot(self,FUNC_plot=bar3dplot,mode="3d",**kwargs):
    if mode in ["2d"]:
      ret=FUNC_plot(x=self.grid2ddata,**kwargs)
    elif mode in ["3d"]:
      ret=FUNC_plot(x=self.bar3ddata,**kwargs)
    else:
      raise ValueError('`mode` must either be "2d" or "3d".')
    return(ret)
  
  
def demo(verbose=False,pdfFpath="helloworld_demo.pdf"):
  obj=HelloWorld()
    
  
  pp = PdfPages(pdfFpath)
  
  obj.plot(mode="2d",figsize=(16,1),elev=0,azim=0,title="",color="#00ff00",edgecolor='gray',bgcolor='#000000',panecolor='#000000',grid=False,axis=False,verbose=verbose)
  pp.savefig(bbox_inches='tight',pad_inches=0,transparent=False)
  plt.close()
  
  pp.close()
  logsave(pdfFpath)

if __name__ == "__main__":
  # from tabulate import tabulate

  # obj=HelloWorld()
  # print("obj.LegoBrick")
  # print(tabulate(obj.LegoBrick, headers='keys', tablefmt='psql'))
  # print("obj.bar3ddata")
  # print(tabulate(obj.bar3ddata, headers='keys', tablefmt='psql'))

  demo()
  





