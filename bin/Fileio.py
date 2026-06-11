#!/usr/bin/env python3
import copy
import re
import sys

from scipy import *
from numpy import array, zeros


def Read_complex_multilines(D_name, skipline=0):
    """This function reads Sig.out file"""
    print("Reading a file ", D_name)
    fi = open(D_name, "r")
    for i in range(skipline):
        fi.readline()
    lines = fi.readlines()
    fi.close()
    m = len(lines[0].split())
    Nom = len(lines)
    om_data = zeros(Nom, dtype=float)
    orbital_count = (m - 1) // 2
    Data = zeros((orbital_count, Nom), dtype=complex)
    for iom, line in enumerate(lines):
        l = line.split()
        om_data[iom] = float(l[0])
        for ib in range(orbital_count):
            Data[ib, iom] = complex(float(l[1 + ib * 2]), float(l[2 + ib * 2]))
    return om_data, Data


def Read_float_multilines(D_name):
    """This function reads Sig.out file"""
    print("Reading a file ", D_name)
    fi = open(D_name, "r")
    lines = fi.readlines()
    fi.close()
    m = len(lines[0].split())
    Nom = len(lines)
    # om_data=zeros(Nom,dtype=float)
    Data = zeros((m, Nom))
    for iom, line in enumerate(lines):
        l = line.split()
        for ib in range(m):
            Data[ib, iom] = float(l[ib])
    return Data


def Read_float(D_name):
    """This function reads Sig.out file"""
    print("Reading a file ", D_name)
    fi = open(D_name, "r")
    lines = fi.readlines()
    fi.close()
    Data = array(list(map(float, lines[0].split())))
    return Data


def Read_complex_Data(D_name):
    """This function reads Sig.out file"""
    print("Reading a file ", D_name)
    fi = open(D_name, "r")
    line = fi.readline()
    val = re.search(r"TrSigmaG=(\-?\d+\.?\d*)", line)
    TrSigmaG = float(val.group(1))
    val = re.search(r"mu=(\-?\d+\.?\d*)", line)
    mu = float(val.group(1))
    val = re.search(r"Ekin=(\-?\d+\.?\d*)", line)
    Ekin = float(val.group(1))
    val = re.search(r"Epot=(\-?\d+\.?\d*)", line)
    Epot = float(val.group(1))
    val = re.search(r"nf=(\d+\.?\d*)", line)
    nf_q = float(val.group(1))
    mom = eval(line.split()[-1][4:])
    lines = fi.readlines()
    Nom = len(lines)
    m = len(lines[0].split())
    om_data = zeros(Nom, dtype=float)
    orbital_count = (m - 1) // 2
    Data = zeros((orbital_count, Nom), dtype=complex)
    iom = 0
    for line in lines:
        l = line.split()
        om_data[iom] = float(l[0])
        for ib in range(orbital_count):
            Data[ib, iom] = complex(float(l[1 + ib * 2]), float(l[2 + ib * 2]))
        iom = iom + 1
    if iom != Nom:
        print("Something is wrong!")
        sys.exit(1)
    if len(mom) != orbital_count:
        print("Something is wrong!")
        sys.exit(1)

    return (om_data, Data, TrSigmaG, Epot, nf_q, mom, Ekin, mu)


def Print_complex(data, mesh, filename):
    n1 = len(mesh)
    fi = open(filename, "w")
    for i in range(n1):
        print("%.14f " % (mesh[i]), end=" ", file=fi)
        print("%.14f %.14f " % (data[i].real, data[i].imag), file=fi)


def Print_complex_multilines(data, mesh, filename, headers=[]):
    n0 = len(data)
    n1 = len(mesh)
    fi = open(filename, "w")
    for header in headers:
        print(header, file=fi)
    for i in range(n1):
        for j in range(n0):
            if j == 0:
                print("%20.15f " % (mesh[i]), end=" ", file=fi)
            print(
                "%20.15f %20.15f " % (data[j, i].real, data[j, i].imag),
                end=" ",
                file=fi,
            )
        print("", file=fi)


def Print_float(data, filename):
    n0 = len(data)
    fi = open(filename, "w")
    for j in range(n0):
        print("%.14f " % (data[j]), end=" ", file=fi)
    print("", file=fi)


def Read_float(filename):
    fi = open(filename, "r")
    Data = array(list(map(float, fi.readline().split())))
    return Data


def Create_dmft_params(p, pC, N_atoms, atm_idx, sym_idx):
    f = open("dmft_params.dat", "w")
    print("# Number of k-points in Wannier basis=", file=f)
    print(p["q"][0], p["q"][1], p["q"][2], file=f)
    print("# Total number of electrons=", file=f)
    print(p["n_tot"], file=f)
    #   print >> f, "# Temperature [eV]="
    #   print >> f, 1.0/pC['beta'][0]
    print("# Number of om points for k-sum", file=f)
    print(p["noms"], file=f)
    print("# Number of iterations for mu", file=f)
    print(p["mu_iter"], file=f)
    print("# Number of total spin", file=f)
    print(p["nspin"], file=f)
    print("# Number of total correlated atoms", file=f)
    print(N_atoms, file=f)
    print("# Number of correlated orbitals per atom", file=f)
    #   print >> f, len(sym_idx[atm_idx[0]])
    print(len(sym_idx[atm_idx[0]]) // p["nspin"], file=f)
    print("# Orbital index for the self-energy at each atom", file=f)
    for i in range(N_atoms):
        for j in range(len(sym_idx[atm_idx[i]])):
            print(sym_idx[atm_idx[i]][j], end=" ", file=f)
        print("", file=f)
    f.close()


def Create_INPUT(p, pC, TB, T_high, noms_high, LFORCE=".FALSE."):
    atm_idx = []
    idx = 1
    for ats in p["cor_at"]:
        for at in ats:
            atm_idx.append(idx)
        idx += 1
    f = open("VASP.input", "w")
    print(LFORCE, file=f)
    print(TB.LHF, file=f)
    print(p["n_tot"], file=f)
    print(p["nspin"], file=f)
    print(p["nfine"], file=f)
    print(TB.ncor_orb, file=f)
    print(TB.max_cor_orb, file=f)
    if TB.LHF == ".TRUE.":
        print("1", file=f)
    else:
        print(p["noms"], file=f)
    if TB.LHF == ".TRUE.":
        print("1", file=f)
    else:
        print(noms_high, file=f)
    if TB.LHF == ".TRUE.":
        print("1", file=f)
    else:
        print(p["noms"] + p["nomlog"], file=f)
    print(1.0 / pC["beta"][0], file=f)
    print(T_high, file=f)
    for i in range(len(atm_idx)):
        print(atm_idx[i], end=" ", file=f)
    print("", file=f)
    for i in range(len(atm_idx)):
        print(p["U"][atm_idx[i] - 1], end=" ", file=f)
    print("", file=f)
    for i in range(len(atm_idx)):
        print(p["J"][atm_idx[i] - 1], end=" ", file=f)
    print("", file=f)
    for i in range(len(atm_idx)):
        print(p["alpha"][atm_idx[i] - 1], end=" ", file=f)
    print("", file=f)
    f.close()
    if TB.LHF == ".FALSE.":
        f = open("ksum.input", "w")
        print(p["q"][0], p["q"][1], p["q"][2], file=f)
        print(p["noms"], p["noms"] + p["nomlog"], file=f)
        print(p["nspin"], file=f)
        print(TB.ncor_orb, file=f)
        print(TB.max_cor_orb, file=f)
        for i in range(len(atm_idx)):
            print(atm_idx[i], end=" ", file=f)
        print("", file=f)
        print(1.0 / pC["beta"][0], file=f)
        #      print >> f, p['Nd_f']
        print(p["n_tot"], file=f)
        print(p["mu_iter"], file=f)
        print(p["mix_sig"], file=f)
        for i in range(len(atm_idx)):
            print(p["U"][atm_idx[i] - 1], end=" ", file=f)
        print("", file=f)
        for i in range(len(atm_idx)):
            print(p["alpha"][atm_idx[i] - 1], end=" ", file=f)
        print("", file=f)
        for i in range(len(atm_idx)):
            print(p["J"][atm_idx[i] - 1], end=" ", file=f)
        print("", file=f)
        f.close()
    else:
        f = open("ksum.input", "w")
        print(p["nspin"], file=f)
        print(TB.ncor_orb, file=f)
        print(TB.max_cor_orb, file=f)
        print(p["n_tot"], file=f)
        print(p["mu_iter"], file=f)
        for i in range(len(atm_idx)):
            print(atm_idx[i], end=" ", file=f)
        print("", file=f)
        for i in range(len(atm_idx)):
            print(p["U"][atm_idx[i] - 1], end=" ", file=f)
        print("", file=f)
        for i in range(len(atm_idx)):
            print(p["alpha"][atm_idx[i] - 1], end=" ", file=f)
        print("", file=f)
        for i in range(len(atm_idx)):
            print(p["J"][atm_idx[i] - 1], end=" ", file=f)
        print("", file=f)
        f.close()
