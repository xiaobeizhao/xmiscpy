
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Fri May 05 10:39:27 EDT 2017 -0400 (Week 18)
## 
## 
## Reference: 
## 
## 
## ************************************************************************

def get_subDpath(x):
  """
  !@brief Get all subfolders within a folder recursively
  @para x path a folder
  """  
  ret=[e[0] for e in os.walk(x)]
  return(ret)

