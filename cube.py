import json

class Part:
  def __init__(self, number, tiles):
    self.number = number
    self.tiles = tiles
  
  @classmethod
  def fromstrings(cls, number, tiles_0, tiles_1 = "000\n000\n000"):
    tilesstr = [[],[],[["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]]
    
    for l in tiles_0.split("\n"):
      if len(l) > 0:
        tilesstr[0].append(list(l))
    for l in tiles_1.split("\n"):
      if len(l) > 0:
        tilesstr[1].append(list(l))
    
    tiles = set()
    for z in range(0, 3):
      for y in range(0, 3):
        for x in range(0, 3):
          if tilesstr[z][y][x] == "1":
            tiles.add((x,y,z))

    return cls(number, tiles)

  def __str__(self):
    out = ["", "", ""]
    for z in range(0, 3):
      for y in range(0, 3):
        for x in range(0, 3):
          out[y] += str(self.number) if (x,y,z) in self.tiles else "0"
      out[0] += " "
      out[1] += " "
      out[2] += " "
      
    return f"{out[0]}\n{out[1]}\n{out[2]}\n"

  def shift(self, x, y, z):
    shifted_tiles = set()
    for t in self.tiles:
      r = (t[0] + x, t[1] + y, t[2] + z)
      if r[0] > 2 or r[0] < 0 or r[1] > 2 or r[1] < 0 or r[2] > 2 or r[2] < 0:
        return None
      shifted_tiles.add(r)
    return Part(self.number, shifted_tiles)

  def shift_to_zero(self):
    lowest = [9,9,9]
    for t in self.tiles:
      lowest[0] = t[0] if t[0] < lowest[0] else lowest[0]
      lowest[1] = t[1] if t[1] < lowest[1] else lowest[1]
      lowest[2] = t[2] if t[2] < lowest[2] else lowest[2]
    return self.shift(-lowest[0], -lowest[1], -lowest[2])

  def isdisjoint_all(self, others):
    for o in others:
      if not self.tiles.isdisjoint(o.tiles):
        return False
    return True

  def get_highest_base_position(self):
    highest = [0,0,0]
    for t in self.tiles:
      highest[0] = t[0] if t[0] > highest[0] else highest[0]
      highest[1] = t[1] if t[1] > highest[1] else highest[1]
      highest[2] = t[2] if t[2] > highest[2] else highest[2]
    return highest

  rotate_map = {
    (0,0):(2,0),
    (2,0):(2,2),
    (2,2):(0,2),
    (0,2):(0,0),
    (1,0):(2,1),
    (2,1):(1,2),
    (1,2):(0,1),
    (0,1):(1,0),
    (1,1):(1,1)
  }

  @staticmethod
  def rotate_single(addr):
    return rotate_map[addr]
      
  def rotate(self, axis):
    nonaxis = [0,1,2]
    nonaxis.pop(axis)
    rotated_tiles = set()
    for t in self.tiles:
      r = Part.rotate_map[(t[nonaxis[0]], t[nonaxis[1]])]
      tpl = (
        t[0] if axis == 0 else r[0],
        t[1] if axis == 1 else (r[0] if axis == 0 else r[1]),
        t[2] if axis == 2 else r[1]
      )
      rotated_tiles.add(tpl)
    return Part(self.number, rotated_tiles)

parts = [Part.fromstrings(1, """
110
100
000""", """
100
000
000"""), Part.fromstrings(2, """
111
010
000"""), Part.fromstrings(3, """
110
100
000""", """
000
100
100"""), Part.fromstrings(4, """
110
000
000""", """
011
010
000"""), Part.fromstrings(5, """
110
100
000""", """
000
100
000"""), Part.fromstrings(6, """
110
100
100""", """
000
100
000""")]

allparts = []

for p in parts:
  arr = [p]
  p_r = p
  for roll in range(0,3):
    if roll > 0:
      p_r = p_r.rotate(0)
    p_p = p_r
    for pitch in range(0,3):
      if pitch > 0:
        p_p = p_p.rotate(1)
      p_y = p_p
      for yaw in range(0,3):
        if yaw > 0:
          p_y = p_y.rotate(2)
        arr.append(p_y)

  print(f"Rotations done for #{p.number}, {len(arr)} rotations total")
  rotnum = 0
  shifted_arr = []
  # rotations done, now look if we can shift them
  for rot in arr:
    rotnum += 1

    zero = rot.shift_to_zero()
    hbp = zero.get_highest_base_position()

    for x in range(0, 3 - hbp[0]):
      for y in range(0, 3 - hbp[1]):
        for z in range(0, 3 - hbp[2]):
          shifted_arr.append(zero.shift(x, y, z))

  allparts.append(shifted_arr)

for prt in allparts:
  print(f"Part #{prt[0].number}: {len(prt)} rotations/shifts")


def check_part_fit(used_cparts, new_part_id):
  for new_cpart in allparts[new_part_id]:
    if new_cpart.isdisjoint_all(used_cparts):
      # we can use this new_cpart!
      if new_part_id == 5:
        return used_cparts + [new_cpart] # we did it!
      result = check_part_fit(used_cparts + [new_cpart], new_part_id + 1)
      if result is not None:
        return result

result = check_part_fit([], 0)
print()
print("#### RESULT ####")
print()
for result_part in result:
  print(result_part)

def printall(result):
  out = ["", "", ""]
  for z in range(0, 3):
    for y in range(0, 3):
      for x in range(0, 3):
        found = False
        for rp in result:
          if (x,y,z) in rp.tiles:
            found = True
            out[y] += str(rp.number)
            break
        if not found:
          out[y] += "0"
    out[0] += " "
    out[1] += " "
    out[2] += " "
    
  print(f"{out[0]}\n{out[1]}\n{out[2]}\n")

printall(result)