import cx_Freeze
import os

executables = [cx_Freeze.Executable("main.py", base="WIN32GUI")]
os.environ['TCL_LIBRARY'] = r'D:\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\Anaconda3\tcl\tk8.6'
cx_Freeze.setup(
    name="flappyBox",
    options={"build_exe": {"packages":["pygame", "time", "random"], "include_files":[r"assets\background.png",r"assets\icon.png",r"assets\ground.png",r"assets\lower_pillar.png",r"assets\upper_pillar.png"]}},
    executables = executables,
    version="0.0.2"
    )