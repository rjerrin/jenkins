#!/usr/bin/python

import os
import re
from distutils.version import StrictVersion
from packaging.version import Version, LegacyVersion


workspace="/home/jery/workspace"

repodir="/home/jery/linuxbuilds"

compile_dir = "{}/{}".format(workspace,"compile_dir")

if os.path.isdir("{}/compile_dir".format(workspace)):
    os.system("rm -rf {}/compile_dir".format(workspace))


versions = lambda a,b: a if (Version(a) > Version(b)) else b
kversions = filter( ( lambda x:  re.match(r'(\d+\.\d+\.\d+$)|(\d+\.\d+$)',x))  , map ( lambda x: x.split('-')[1].split('.tar.gz')[0] , os.listdir('/home/jery/workspace/linux' ) ))

print ( "Available kernel versions {}", "\n".join(kversions) )

kernel = reduce( versions , kversions)

print ( "latest version {}".format ( kernel)  )

kernel_latest = "linux-" + "{}.tar.gz".format(kernel)

print ( "kernel_latest -> {}".format(kernel_latest))

kernel_uncomp = kernel_latest.replace(".tar.gz","").strip()

print(kernel_uncomp)

os.system("mkdir {}/compile_dir".format(workspace))

print("tar xvf {}/{} -C {}/compile_dir".format(workspace,kernel_latest,workspace))

os.system("tar xvf {}/linux/{} -C {}/compile_dir".format(workspace,kernel_latest,workspace))

print ("cd {}/{}/{}/{} && sudo make clean && sudo make mrproper && cp /boot/config`uname -r` .config && sudo make olddefconfig && sudo make deb-pkg".format(workspace,"linux",compile_dir,kernel_uncomp))

os.system("cd {}/compile_dir/{} && sudo make clean && sudo make mrproper && cp /boot/config-`uname -r` .config && sudo make olddefconfig && sudo make -j4 deb-pkg && for pkg in `ls *.deb`; do dpkg -i $pkg; done".format(workspace,kernel_uncomp))

os.system("mkdir -pv {}/stable/{}".format(repodir,kernel_uncomp))
for x in filter( lambda x:  not re.match(u'(tar\.gz$)|(.+\d$)',x),os.listdir("{}".format(compile_dir))):
    print(x)
    os.system(" cp -v {}/{} {}/stable/{}".format(compile_dir,x,repodir,kernel_uncomp))

os.system("cd {}/stable/{} && git add . && git commit -m \"version - {}\" && git push origin master".format(repodir,kernel_uncomp,kernel_uncomp))
    

    

