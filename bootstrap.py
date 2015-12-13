# vim: ft=python shiftwidth=2 tabstop=2 expandtab 
import os
import shutil
import sys
import urllib
import zipfile

TRADERVUE_DIR = os.path.join(os.path.realpath(os.getcwd()), 'tradervue')

def install_zip(url, name, target):
  # Install the tradervue module from github
  tmp_zipfile = '%s.zip' % (name)
  urllib.urlretrieve(url, tmp_zipfile)
  z = zipfile.ZipFile(tmp_zipfile, 'r')
  z.extractall()
  os.remove(tmp_zipfile)

  if not os.path.isdir(target):
    os.mkdir(target)

  src = '%s-master' % (name)
  for entry in os.listdir(src):
    shutil.move(os.path.join(src, entry), target)
  os.rmdir(src)

def main(argv):
  if not os.path.isdir(TRADERVUE_DIR):
    os.mkdir(TRADERVUE_DIR)
  os.chdir(TRADERVUE_DIR)
  install_zip('https://github.com/nall/py-tradervue-api/archive/master.zip', 'py-tradervue-api', 'tradervue')
  install_zip('https://github.com/nall/pythonista-tradervue/archive/master.zip', 'pythonista-tradervue', os.getcwd())

  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))

