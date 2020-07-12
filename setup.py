## This is the file that creates the executable. To run it, navigate one folder up
## (so you can see the Fireship folder), hold shift, and right-click the folder.
## One of the options should be "Open with Powershell" or "Open with Command Prompt".
## Hit that one. Once it opens and you can see the file path, type:
## python setup.py build
## Then wait as a bunch of text scrolls down your screen. Hopefully it won't give
## you an error. If it finishes without errors, you'll now have a "build" folder
## in your Fireship folder. Inside this is another folder, and inside that
## is the executable.
## FYI: I think the exe has to stay in the build folder, but you can move the
## build folder wherever you want. You can also create shortcuts for the exe.

import cx_Freeze
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable(script="main.py", icon="icon.ico")]

cx_Freeze.setup(
    name="Fireship build",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["fonts/",
                                            "images/",
                                            "sounds/",
                                            'background.py',
                                            'const.py',
                                            'dashboard.py',
                                            'game.py',
                                            'img.py',
                                            'levels.py',
                                            'menu.py',
                                            'radar.py',
                                            'room.py',
                                            'ship.py',
                                            'sound.py',
                                            'text.py',
                                            'tutorial.py',
                                            'util.py']}},
    executables=executables,
    version='1.0.0'
    )
