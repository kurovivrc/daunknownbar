import PyInstaller.__main__
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--clean',
    '--name=ZyaNight_Bar',
    '--icon=2.ico',
    '--add-data=00000000000000000000000026000000.zip;.',
]) 