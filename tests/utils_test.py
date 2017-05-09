
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Fri May 05 10:10:56 EDT 2017 -0400 (Week 18)
## 
## 
## Reference: 
## 
## 
## ************************************************************************
import numpy
from xmisc.utils.list import *


def test_ldepth():
  x=[["a","b","c",],["d","e"],["f","g","h"]]
  ldepth(x)==2


def test_lapply():
  x = numpy.zeros((3,3,2)).tolist()
  ret=lapply(x,lambda x:x+1)
  y = numpy.ones((3,3,2)).tolist()
  ret==y

def test_altlapply():
  x = numpy.zeros((3,3,2)).tolist()
  ret=altlapply(x,[lambda x:x+1,lambda x:x+2])
  y = numpy.ones((3,3,2)).tolist()
  ret2=altlapply(y,[lambda x:x+0,lambda x:x+1])
  ret==ret2

def test_get_subDpath():
  True
