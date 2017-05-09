
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Mon May 08 13:33:02 EDT 2017 -0400 (Week 19)
## 
## 
## Reference: 
## Reference: http://stackoverflow.com/questions/34035427/conditional-removal-of-labels-in-matplotlib-pie-chart
## 
## ************************************************************************


def autopct_generator(limit):
  '''  
  '''
  def inner_autopct(pct):
    return ('%.2f' % pct) if pct > limit else ''
  return inner_autopct
