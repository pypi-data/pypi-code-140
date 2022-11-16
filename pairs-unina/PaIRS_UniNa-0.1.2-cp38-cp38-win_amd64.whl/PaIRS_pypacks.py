from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import*
from PySide6.QtGui import *
from PySide6.QtWidgets import*

import numpy as np
import scipy.io, pickle
from PIL import Image
from PIL.ImageQt import ImageQt
import sys, os, glob, copy, re, unidecode, time, traceback
from collections import namedtuple
from .plt_util import writePlt, readPlt
#from multiprocessing import cpu_count
from psutil import cpu_count

if __package__ or "." in __name__:
    from pkg_resources import resource_filename
    foldPaIRS=resource_filename(__package__,'')+"\\"
    foldPaIRS=foldPaIRS.replace('\\','/')
else:
    foldPaIRS='./'

icons_path=foldPaIRS+"icons/"

Flag_Print_DEBUG=False
SleepTime_Workers=0.5

#fontName='Inter'
#fontName='Cambria'
fontName='Arial'
basefold='./'
#basefold='L:/2022.02.23/Q5500_hd0/'

exts = Image.registered_extensions()
supported_exts = sorted({ex for ex, f in exts.items() if f in Image.OPEN})
text_filter = "All files (*"\
   + ");;"+" ;;".join(["{} ".format(fo[1:]) +"(*{})".format(fo) for fo in supported_exts])

def myStandardPath(path):
    #path=unidecode.unidecode(path)
    currpath=path
    if currpath:
        while currpath[-1]==" ": del currpath[-1]
    currpath=re.sub(r'\\+',r'/',currpath)
    currpath=currpath+'/'
    currpath=re.sub('/+', '/',currpath)
    return currpath

def myStandardRoot(root):
    #root=unidecode.unidecode(root)
    currroot=root
    if currroot:
        while currroot[-1]==" ": del currroot[-1]
    currroot=re.sub(r'\\+',r'/',currroot)
    currroot=re.sub('/+', '/',currroot)
    return currroot

def findFiles_sorted(pattern):
    list_files=glob.glob(pattern)
    files=sorted([re.sub(r'\\+',r'/',f) for f in list_files],key=str.lower)
    return files

def myprint(text):
    if Flag_Print_DEBUG:
        print(text)