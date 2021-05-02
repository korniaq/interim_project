import numpy as np
import fileinput
import os
import subprocess
from pyGPGO.covfunc import squaredExponential
from pyGPGO.acquisition import Acquisition
from pyGPGO.surrogates.GaussianProcess import GaussianProcess
from pyGPGO.GPGO import GPGO

geoFile = "channel.geo"
params_tested = [[]]
solver_path = "/home/sgepner/projects/Nektar/build/dist/bin/"

with open("../results.txt", "w") as file:
    file.write("parameters tested: \n")


def change_parameters(file_name, new_a, new_alpha):
    curr_dir = os.path.dirname(__file__)
    geom_file = os.path.join(curr_dir, file_name)
    temp_file = os.path.join(curr_dir, "temp-a{}-alpha{}".format(new_a, new_alpha))

    print("changing parameters...")
    with open(temp_file, "w") as temp:
        for line in fileinput.input(geom_file):
            if line.startswith("a = "):
                temp.write("a = {};\n".format(new_a))
            elif line.startswith("alpha = "):
                temp.write("alpha = {};\n".format(new_alpha))
            else:
                temp.write(line)

    with open(geom_file, "w") as file:
        for line in fileinput.input(temp_file):
            file.write(line)
    os.remove(temp_file)
    print("parameters changes successfully")


def solve(file_name):

    os.system("rm -r channel*.chk")
    os.system("rm -r channel.fld")
    os.system("rm -r channel_xml")

    command = "gmsh " + file_name + " -2 -o channel.msh -order 9"
    print(command)
    os.system(command)
    command = solver_path + "NekMesh channel.msh channel.xml"
    print(command)
    os.system(command)
    command = "mpirun -np 8 " + solver_path + "IncNavierStokesSolver channel.xml sett.xml"
    print(command)
    os.system(command)


def get_variance(alpha, fill):
    a = fill/(np.sin(alpha) + np.cos(alpha))
    change_parameters(geoFile, a, alpha)
    solve(geoFile)

    variance = 0.
    for i in range(1, 2001):
        output = str(subprocess.check_output(solver_path + "FieldConvert channel.xml channel_{}.chk out.stdout -m variance -r 8,10".format(i), shell=True)).splitlines()[0].split('\\n')
        for o in output:
            if o.startswith('Variance (variable phi) : '):
                variance += float(o.replace('Variance (variable phi) : ', ''))
                if i % 100 == 0:
                    print('variance at time {}: \t {}'.format(i/10, o.replace('Variance (variable phi) : ', '')))

    variance /= 2000
    params_tested.append([a, alpha, variance])
    with open("../results.txt", "a") as file:
        file.write('for a = {:.4f} \t alpha = {:.4f} \t obtained variance: {:.4f} \n'.format(a, alpha, variance))

    os.system("mv channel.fld ../results/channel_{:.4f}_{:.4f}.fld".format(a, alpha))
    os.system("mv channel.xml ../results/channel_{:.4f}_{:.4f}.xml".format(a, alpha))

    return -variance #minus because we want to minimize


# base problem
change_parameters(geoFile, 1, 0)
os.system("rm ../base/*.vtu")
os.system("rm -r channel*.chk")
os.system("rm -r channel.fld")
os.system("rm -r channel_xml")

base_variance = -get_variance(0, 1)
params_tested.append([1.0, 0.0, base_variance])

with open("../results.txt", "a") as file:
    file.write('for a = {:.4f} \t alpha = {:.4f} \t obtained variance: {:.4f} \n'.format(1, 0, base_variance))

os.system("for i in {0..2000..10}; do " + solver_path + "FieldConvert ../results/channel_1.0_0.xml channel_$i.chk ../base/channel_$[$i/10].vtu; done")


# optimization
sexp = squaredExponential()
gp = GaussianProcess(sexp)
acq = Acquisition(mode='ExpectedImprovement')
param = {'alpha': ('cont', [0, np.pi/4]),
         'fill': ('cont', [0.2, 1.5])}

np.random.seed(23)
gpgo = GPGO(gp, acq, get_variance, param)
gpgo.run(max_iter=30)
min_params, min_var = gpgo.getResult()
min_alpha = min_params['alpha']
min_a = min_params['fill']/(np.sin(min_alpha)+np.cos(min_alpha))

print("------------------------------------------------------")
print("parameters tested:")
for par in params_tested:
    print('for a = {:.4f} \t alpha = {:.4f} \t obtained variance: {:.4f}'.format(par[0], par[1], par[2]))
print('optimal parameters are a = {:.4f} \t alpha = {:.4f}'.format(min_a, min_alpha))
print('value of minimum variance is: {:.4f}'.format(-min_var))
print("------------------------------------------------------")

with open("../results.txt", "a") as file:
    file.write('optimal parameters are a = {:.4f} \t alpha = {:.4f} \n'.format(min_a, min_alpha))
    file.write('value of minimum variance is: {:.4f} \n'.format(-min_var))


# final solution
change_parameters(geoFile, min_a, min_alpha)
os.system("rm ../solution/*.vtu")
os.system("rm -r channel*.chk")
os.system("rm -r channel.fld")
os.system("rm -r channel_xml")

os.system("gmsh " + geoFile + " -2 -o channel.msh -order 9")
os.system(solver_path + "NekMesh channel.msh channel.xml")
os.system("mpirun -np 8 " + solver_path + "IncNavierStokesSolver channel.xml sett.xml")
os.system("for i in {0..2000..10}; do " + solver_path + "FieldConvert ../results/channel_{:.4f}_{:.4f}.xml channel_$i.chk ../solution/channel_$[$i/10].vtu; done".format(min_a, min_alpha))
