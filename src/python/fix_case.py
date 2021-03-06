# swap_comment_character.py
import sys
import shutil
import os
import fnmatch

def swap_file(filename):
  f = open(filename,'r')
  f2 = open(filename+'.tmp','w')
  for line in f:
    if line.lstrip().startswith('FACE'):
      line2 = line.upper()
      f2.write(line2)
    else:
      f2.write(line)
  f.close()
  f2.close()
  # using shutil.move adds ^M to end of lines.
  os.remove(filename)
  shutil.copy(filename+'.tmp',filename)
  os.remove(filename+'.tmp')

suffix = '*.in'
for root, dirnames, filenames in os.walk('.'):
  for filename in fnmatch.filter(filenames,suffix):
    filename = os.path.join(root,filename)
    print(filename)
    swap_file(filename)

print('done')
