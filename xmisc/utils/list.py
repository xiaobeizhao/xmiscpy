
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Tue Apr 25 03:24:06 EDT 2017 -0400 (Week 17)
## 
## 
## Reference: 
## 
## 
## ************************************************************************
import numpy as np
import math

def ldepth(x):
  """
  !@brief Get the deepest level a nested list
  @para x list
  """
  ret=(isinstance(x, type([])) or isinstance(x, type(np.array([])))) and max(map(ldepth, x))+1
  return(ret)


def lapply(x,FUNC):
  """
  !@brief Apply a function to every element in a (nested) list
  @para x list
  @para FUNC function
  """
  x_=[e for e in x]
  for i, elem in enumerate(x_):
    if not isinstance(elem, list):
      x_[i] = FUNC(elem)
    else:
      x_[i] = lapply(elem,FUNC)
  return(x_)


def altlapply(x,FUNCLIST,n=0):
  """
  !@brief Alternatively apply a set of functions to every element in a (nested) list
  @para x list
  @para FUNCLIST list of functions
  @para n int n-th function to start with 
  """
  l=len(FUNCLIST)
  x_=[e for e in x]
  for i, elem in enumerate(x_):
    FUNC=FUNCLIST[n%l]
    if not isinstance(elem, list):
      x_[i] = FUNC(elem)
    else:
      n+=1
      x_[i] = altlapply(elem,FUNCLIST,n=n)
  return(x_)



def lreshape(x,nrow=None,ncol=None,fill=None,byrow=False):
  if nrow is None and ncol is None:
    raise Exception('Either `nrow` or `ncol` must be specified')
  n=len(x)
  if nrow is None:
    nrow=math.ceil(n/ncol)
  if ncol is None:
    ncol=math.ceil(n/nrow)
  
  x += [fill] * (nrow*ncol - len(x))
  if byrow:
    ret = [[x[ncol*i+j] for j in range(ncol)] for i in range(nrow)]
  else:
    ret = [[x[nrow*i+j] for i in range(ncol)] for j in range(nrow)]
    
  return(ret)


if __name__ == "__main__":
  import numpy
  x = numpy.zeros((3,3,2)).tolist()
  ret=lapply(x,lambda x:x+1)
  print(ret)
  print(ldepth(ret))

  ret2=altlapply(x,[lambda x:x+1,lambda x:x+2])
  print(ret2)

  
  
