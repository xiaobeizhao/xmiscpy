
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Fri May 05 11:09:36 EDT 2017 -0400 (Week 18)
## 
## 
## Reference: 
## 
## 
## ************************************************************************

from matplotlib import (cbook, colors as mcolors)
from mpl_toolkits.mplot3d import art3d

def bar3d_update(
  self, x, y, z, dx, dy, dz,
  color=None,
  zsort='average',
  shade=True,
  *args,
  **kwargs
  ): ##XB

  '''
  Generate a 3D bar, or multiple bars.

  When generating multiple bars, x, y, z have to be arrays.
  dx, dy, dz can be arrays or scalars.

  *color* can be:

   - A single color value, to color all bars the same color.

   - An array of colors of length N bars, to color each bar
     independently.

   - An array of colors of length 6, to color the faces of the
     bars similarly.

   - An array of colors of length 6 * N bars, to color each face
     independently.

   When coloring the faces of the boxes specifically, this is
   the order of the coloring:

    1. -Z (bottom of box)
    2. +Z (top of box)
    3. -Y
    4. +Y
    5. -X
    6. +X

  Keyword arguments are passed onto
  :func:`~mpl_toolkits.mplot3d.art3d.Poly3DCollection`
  '''
  had_data = self.has_data()

  if not cbook.iterable(x):
    x = [x]
  if not cbook.iterable(y):
    y = [y]
  if not cbook.iterable(z):
    z = [z]

  if not cbook.iterable(dx):
    dx = [dx]
  if not cbook.iterable(dy):
    dy = [dy]
  if not cbook.iterable(dz):
    dz = [dz]

  if len(dx) == 1:
    dx = dx * len(x)
  if len(dy) == 1:
    dy = dy * len(y)
  if len(dz) == 1:
    dz = dz * len(z)

  if len(x) != len(y) or len(x) != len(z):
    warnings.warn('x, y, and z must be the same length.')

  # FIXME: This is archaic and could be done much better.
  minx, miny, minz = 1e20, 1e20, 1e20
  maxx, maxy, maxz = -1e20, -1e20, -1e20

  polys = []
  for xi, yi, zi, dxi, dyi, dzi in zip(x, y, z, dx, dy, dz):
    minx = min(xi, minx)
    maxx = max(xi + dxi, maxx)
    miny = min(yi, miny)
    maxy = max(yi + dyi, maxy)
    minz = min(zi, minz)
    maxz = max(zi + dzi, maxz)

    polys.extend([
    ((xi, yi, zi), (xi + dxi, yi, zi),
      (xi + dxi, yi + dyi, zi), (xi, yi + dyi, zi)),
    ((xi, yi, zi + dzi), (xi + dxi, yi, zi + dzi),
      (xi + dxi, yi + dyi, zi + dzi), (xi, yi + dyi, zi + dzi)),

    ((xi, yi, zi), (xi + dxi, yi, zi),
      (xi + dxi, yi, zi + dzi), (xi, yi, zi + dzi)),
    ((xi, yi + dyi, zi), (xi + dxi, yi + dyi, zi),
      (xi + dxi, yi + dyi, zi + dzi), (xi, yi + dyi, zi + dzi)),

    ((xi, yi, zi), (xi, yi + dyi, zi),
      (xi, yi + dyi, zi + dzi), (xi, yi, zi + dzi)),
    ((xi + dxi, yi, zi), (xi + dxi, yi + dyi, zi),
      (xi + dxi, yi + dyi, zi + dzi), (xi + dxi, yi, zi + dzi)),
    ])

  facecolors = []
  if color is None:
    color = [self._get_patches_for_fill.get_next_color()]

  if len(color) == len(x):
    # bar colors specified, need to expand to number of faces
    for c in color:
      facecolors.extend([c] * 6)
  else:
    # a single color specified, or face colors specified explicitly
    facecolors = list(mcolors.to_rgba_array(color))
    if len(facecolors) < len(x):
      facecolors *= (6 * len(x))

  normals = self._generate_normals(polys)
  ##BEGIN - XB##
  if shade:
    sfacecolors = self._shade_colors(facecolors, normals)
  else:
    sfacecolors = facecolors
  ##END - XB##
  col = art3d.Poly3DCollection(
    polys,
    zsort=zsort,
    facecolor=sfacecolors,
    *args, **kwargs
    )
  self.add_collection(col)

  self.auto_scale_xyz((minx, maxx), (miny, maxy), (minz, maxz), had_data)

  return col



def _get_coord_info_update(self, renderer):
  mins, maxs, centers, deltas, tc, highs = self._get_coord_info_ori(renderer)
  mins += deltas / 4
  maxs -= deltas / 4
  ret=(mins, maxs, centers, deltas, tc, highs)
  return(ret)

