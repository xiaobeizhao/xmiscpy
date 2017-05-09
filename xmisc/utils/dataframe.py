
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Sun May 07 04:53:59 EDT 2017 -0400 (Week 18)
## 
## 
## Reference: 
## 
## 
## ************************************************************************

import numpy as np
import pandas as pd

def as_dataframe(x):
  """
  !@brief convert to a pandas DataFrame
  @para x a list numpy array or pandas DataFrame
  """  
  type_list=[type([]), type(np.array([])), type(pd.DataFrame())]
  # print("as_dataframe:x")
  # print(x)
  if not any([isinstance(x,e) for e in type_list]):
    raise TypeError('`x` must be either list, numpy array or pandas DataFrame')
  
  if not isinstance(x,type(pd.DataFrame())):
    x_=pd.DataFrame(x)
  else:
    x_=x
    
  return(x_)

def bind(x,y,axis,naValue=None):
  x_=as_dataframe(x)
  y_=as_dataframe(y)
    
  ret = pd.concat([x_.reset_index(drop=True), y_.reset_index(drop=True)],axis=axis)

  if naValue is not None:
    ret.fillna(naValue, inplace=True)
  return(ret)


def rbind(x,y,*args,**kwargs):
  ret=bind(x,y,axis=0,*args,**kwargs)
  return(ret)


def cbind(x,y,*args,**kwargs):
  ret=bind(x,y,axis=1,*args,**kwargs)
  return(ret)


def bindlist(x,axis,bindFunc=bind,*args,**kwargs):
  """
  !@brief bind a list of dataframes
  @para axis 0, 1 or 2
  """
  type_list=[type([]), type(np.array([])), type(pd.DataFrame())]
  if not any([isinstance(x,e) for e in type_list]):
    raise TypeError('`x` must be either list or numpy array')
  
  if len(x)==0:
    raise Exception('`x` must not be empty')

  x_list=[as_dataframe(e) for e in x]

  if len(x_list)==1:
    return(x_list[0])

  self_=x_list[0]
  for i in range(1,len(x_list)):
    other_=x_list[i]
    self_=bindFunc(self_,other_,axis=axis,*args,**kwargs)
  return(self_)

def rbindlist(x,bindFunc=bind,*args,**kwargs):
  ret=bindlist(x,axis=0,bindFunc=bindFunc,*args,**kwargs)
  return(ret)

def cbindlist(x,bindFunc=bind,*args,**kwargs):
  ret=bindlist(x,axis=1,bindFunc=bindFunc,*args,**kwargs)
  return(ret)




def reshape(x,nrow=None,ncol=None):
  if nrow is None and ncol is None:
    raise Exception('Either `` or `` must be specified')
  n=len(x)
  if nrow is None:
    nrow=math.ceil(n/ncol)
  if ncol is None:
    ncol=math.ceil(n/nrow)
  ret = np.resize(x, nrow*ncol).reshape(nrow,ncol)
  return(ret)



if __name__ == "__main__":
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
  
  W_=[      
    [1,1,0,0,0,1,1],
    [1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1],
    [1,1,0,1,0,1,1],
    [1,1,0,0,0,1,1],
    [1,1,0,0,0,1,1]      
    ]
    
  tmp_cbind=cbind(H_,W_)
  print("tmp_cbind",tmp_cbind)

  tmp_rbind=rbind(H_,W_)
  print("tmp_rbind",tmp_rbind)

  tmp_rbind2=rbind(H_,l_,naValue=int(0))
  print("tmp_rbind2",tmp_rbind2)

  tmp_cbindlist=cbindlist([H_,[[0]],e_,[[0]],l_,[[0,0]],l_,[[0]],o_],naValue=int(0))
  print("tmp_cbindlist",tmp_cbindlist)

  
