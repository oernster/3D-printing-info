import os


documents_folder = 'C:\\Users\\INSERTWINDOWSUSERNAMEHERE\Documents'

for each in os.listdir(documents_folder):
    if each.endswith('.gcode'):
        print(each)
        gx_filename = each.replace('.gcode', '.gx')
        print(os.path.join(documents_folder, gx_filename))
        os.rename(os.path.join(documents_folder, each), os.path.join(documents_folder, gx_filename))

