from cx_Freeze import setup, Executable
import sys

sys.setrecursionlimit(10000)

executables = [Executable(script='levitap.py')]

setup(
    name='LeviTap',
    version='1.0',
    description='Touchless Mouse',
    executables=executables
)