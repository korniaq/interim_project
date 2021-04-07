import numpy as np
import fileinput
import os
import subprocess
from pyGPGO.covfunc import squaredExponential
from pyGPGO.acquisition import Acquisition
from pyGPGO.surrogates.GaussianProcess import GaussianProcess
from pyGPGO.GPGO import GPGO

scrFile = "geom.scr"
params_tested = []


def change_parameters(file_name, new_s, new_n):
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
    command = "gmsh " + file_name + " -2 -o geom.msh -order 9"
    print(command)
    os.system(command)
    command = "NekMesh geom.msh geom.xml:xml:uncompress"
    print(command)
    os.system(command)
    command = "ADRSolver geom.xml conditions.xml"
    print(command)
    os.system(command)

    command = "rm geom.bak*.fld"
    os.system(command)


def get_integral(s, n):
    change_parameters(scrFile, s, n)
    solve(scrFile)

    integral = 0.
    output = str(subprocess.check_output("FieldConvert geom.xml geom.fld -m mean geom.plt", shell=True)).splitlines()[0].split('\\n') #ugh
    for o in output:
        if o.startswith('Integral'):
            integral = float(o.replace('Integral (variable u) : ', ''))
    os.system("rm geom.plt")
    params_tested.append([s, n, integral])
    return integral


sexp = squaredExponential()
gp = GaussianProcess(sexp)
acq = Acquisition(mode='ExpectedImprovement')
param = {'s': ('cont', [0, 0.9]),
         'n': ('cont', [2, 4])}

np.random.seed(23)
gpgo = GPGO(gp, acq, get_integral, param)
gpgo.run(max_iter=20)
max_params, max_int = gpgo.getResult()

change_parameters(scrFile, max_params['s'], max_params['n'])
solve(scrFile)

os.system("rm geom.vtu")
os.system("FieldConvert geom.xml geom.fld geom.vtu")
os.system("rm ~/Shared/geom.vtu")
os.system("cp geom.vtu ~/Shared/geom.vtu")

print("parameters tested:")
for par in params_tested:
    print('for s = {:.4f} \t n = {:.4f} \t obtained integral: {:.4f}'.format(par[0], par[1], par[2]))
print('optimal parameters are s = {:.4f} \t n = {:.4f}'.format(max_params['s'], max_params['n']))
print('value of maximum integral is: {:.4f}'.format(max_int))
