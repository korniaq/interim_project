import numpy as np


def change_parameters(file_name, new_s, new_n):
    import fileinput
    import os

    curr_dir = os.path.dirname(__file__)
    geom_file = os.path.join(curr_dir, file_name)
    temp_file = os.path.join(curr_dir, "temp-s{}-n{}".format(new_s, new_n))

    print("changing parameters...")
    with open(temp_file, "w") as temp:
        for line in fileinput.input(geom_file):
            if line.startswith("S="):
                temp.write("S={};\n".format(new_s))
            elif line.startswith("N="):
                temp.write("N={};\n".format(new_n))
            else:
                temp.write(line)

    with open(geom_file, "w") as file:
        for line in fileinput.input(temp_file):
            file.write(line)
    os.remove(temp_file)
    print("parameters changes successfully")


def solve(file_name):
    import os

    command = "gmsh " + file_name + " -2 -o geom.msh -order 9"
    print(command)
    os.system(command)
    command = "NekMesh geom.msh geom.xml:xml:uncompress"
    print(command)
    os.system(command)
    command = "ADRSolver geom.xml conditions.xml"
    print(command)
    os.system(command)
    command = "FieldConvert geom.xml geom.fld geom.vtu"
    print(command)
    os.system(command)

    command = "rm geom.bak*.fld"
    os.system(command)
    # command = "cp geom.vtu ~/Shared/geom.vtu"
    # os.system(command)


scrFile = "geom.scr"
NEW_S = 0.2
NEW_N = 3
change_parameters(scrFile, NEW_S, NEW_N)
solve(scrFile)