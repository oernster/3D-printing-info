# Sailfish/Makerbot Superslicer setup guide for Windows...
(Note this is for windows; I'm not going to describe how to do it on mac or linux because you're probably far more IT savvy in that scenario but the script will also work fine on a mac if you set the path correctly in flashforge-postprocess.py).

WHY are we doing this?  Because Sailfish/Makerbot printers like .gx files not .gcode files.  This is a simple script to rename the sliced by superslicer gcode file to a gx file so you can use it with your printer and you can just slice normally.  Superslicer generates gcode files.  You MUST set the firmware in superslicer to Sailfish/Makerbot if you have e.g. a Flashforge Adventurer Pro or other Sailfish firmware based printer.

## Install python3 latest from here:

https://www.python.org

When installing python, ensure you tick the PYTHONPATH check box.

# Install virtualenv:

First create a directory to work in, for example...

mkdir c:\Flashforge

Now, open up a command prompt as administrator.  Click on the windows button and type cmd, then launch it as admin.

Use cd (change directory) to change to c:\Flashforge as follows: cd c:\Flashforge

Enter the command:

pip install virtualenv

Enter the command:

virtualenv venv

Enter the command:

venv\Scripts\activate

Now run:

pip install pyinstaller

Next, in the file in this repository called flasforge-postprocess.py, edit it to your username where it assigns the string in quotes to documents_folder on your local machine.  You will also need to download or clone setup.py.

Next, run:

pyinstaller flashforge-postprocess.py 

(it doesn't matter what this file is called, you can rename it to your sailfish printer if appropriate)

This will create a subdirectory called dist and inside that is another folder called flashforge-postprocess.

Copy the entire flashforge-postprocess folder somewhere onto your PC that is convenient.

Now, in super slicer, under print settings, output options, post processing scripts, add the path and filename to the executable in the flashforge-postprocess folder that you located on your PC.

You're DONE!

