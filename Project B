# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 18:25:20 2024

@author: benac
"""
#94

import math
import inspect

"""The first function readFfile opens and reads the content of a file and returns
it as a string. The second function gets teh title from the structure file, the first
line of the file. The third function is geting sclaingfactor which is used to scale 
lattace vectors from the strucutre file.The getElements(strFile) extracts a list of
elements from the structure file. This is found after the lattice vectors.
getNumElements(strFile) returns a list of integers showing the number of atoms 
of each element in the structure with the last function extracting and returning 
a list of atom decorations in order from the file.
"""
 
def readFile(filename):
    content=""
    with open(filename,"r") as fin:
        content=fin.read()
    return content

def getTitle(strFile):
    lines = strFile.split('\n')  
    title = lines[0]  
    return title

def getScalingFactor(strFile):
    lines = strFile.split('\n')
    sfactor = lines[1].split()[0]
    return float(sfactor)

def getElements(strFile):
    lines = strFile.split('\n')
    elements = lines[5].split()  
    return elements

def getNumElements(strFile):
    lines = strFile.split('\n')
    nelements = [int(x) for x in lines[6].split()]
    return nelements

def getAtomDecorations(strFile):
    lines = strFile.split('\n') 
    decor = [line.split()[-1] for line in lines[8:] if line.strip()] 
    return decor
""" The first function combines parsing function to extract tht title, elements and counts 
from the file. GetElementsNew generates a new list of elements, replacing a specified element
with another. GetGCD calculates the greatest common divisor(GCD) among a list of integers.
GetTitleNew creates a new title based on the updated elements and count.
GetREducedComposition calculates the reduced composition of elements by 
dividing the count of each element by the GCD. replaceAtom adjusts atom positions 
with replacing elements. ReplaceElement is speccified element with another structure file, and
updating the title, elements list and atom positions.
"""

def parseStrFile(strFile):
    lines = strFile.split('\n')
    title = getTitle(strFile)
    elements=getElements(strFile)
    nelements=getNumElements(strFile)
    return title,elements,nelements

def getElementsNew(elements,element,replacement):
    elements_new=[]
    elements_new= elements[:]
    
    for index, value in enumerate(elements_new):
        
        if value==element:
            elements_new[index]=replacement
    return elements_new

  
def getGCD(lst_int):
    _gcd=math.gcd(*lst_int)
    return _gcd

def getTitleNew(elements_new,nelements_reduced):
    title_new = ""
    for index, value in enumerate(elements_new):
        title_new+=value +str(nelements_reduced[index])
    return title_new

def getReducedComposition(nelements):
    gcd = getGCD(nelements)
    nelements_reduced= [x // gcd for x in nelements]
    return nelements_reduced

def replaceAtomPositions(lines_new, nelements, elements_new, element, replacement):
    for index in range(8, len(lines_new)):  
        temp_line = lines_new[index].strip().split('  ')
        
        for index2, value in enumerate(temp_line):
            if value == element:
                temp_line[index2] = replacement
        
        lines_new[index] = '   '.join(temp_line)  
    return lines_new



def replaceElement(strFile, element, replacement):
    title, elements, nelements = parseStrFile(strFile)
    elements_new = getElementsNew(elements, element, replacement)
    nelements_reduced = getReducedComposition(nelements)
    title_new = getTitleNew(elements_new, nelements_reduced)
    
    lines = strFile.split('\n')
    lines[0] = title_new
    lines[5] = ' '.join(elements_new)
    lines = replaceAtomPositions(lines, nelements, elements_new, element, replacement)
    return '\n'.join(lines)

""" This first function extracts and returns the algorithm tolerance for 
supercell generation a float list. Then it returns the count and partial 
occupancy values for each element in a disordered system. Then it determines 
if two sets of corrdiantes are equivalent within the bounds. Then it udebtufues
abd returns indices of partially occupied sites. Then it calculates and 
returns the total number of atoms in ordered approximants for the system.
It then generates and reutrns atomic decoration for the supercell
ordered approximants in aa disordered material."""


def getPOCCTols(strFile):
    pocc_tols=[]
    lines = strFile.split('\n')
    temp=lines[1].split()
    for i in temp[1:]:
        pocc_tols.append(float(i))
        
    return pocc_tols

def getNumElementsPOCC(strFile):
    nelements=[]
    occs=[]
    lines = strFile.strip().split('\n')
    
    temp = lines[6].split()
    
    for i in temp:
        nelements.append(int(i[0]))
    for i in temp:
        occs.append(float(i[2:]))
    return nelements, occs

def coordsAreClose(coord1, coord2, tol):
    count=0
    for i in range(0, len(coord1[:-2])):
        
        if(float(coord2[i])-tol) <= float(coord1[i]) <= (float(coord2[i])+tol):
            count+=1
    if count ==len(coord1[:-2]):
        return True
    

def getPOCCSites(strFile):
    pocc_sites=[]
    lines=strFile.strip().split('\n')
    
    for index1, value1 in enumerate(lines[8:]):
        temp1=value1.strip().split()
        
        for index2, value2 in enumerate(lines[9+index1:]):
            temp2 =value2.strip().split()
            
            if coordsAreClose(temp1,temp2, 1 * (math.e ** -3)) == True:
                pocc_sites.append([index1,index2+index1+1])
    return pocc_sites

def getNAtomsPOCC(strFile, supercell_size):
    nelements, occs = getNumElementsPOCC(strFile)
    natoms_ordered = sum([n * occ for n, occ in zip(nelements, occs)]) * supercell_size
    return int(natoms_ordered)

def getAtomDecorationsPOCC(strFile,supercell_size):
    nelements, occs = getNumElementsPOCC(strFile)
    elements = getElements(strFile)
    decor = []
    for element, count, occ in zip (elements, nelements, occs):
        decor.extend([element] * int(count * occ * supercell_size))
    return decor

def main():
    strFile=readFile("POSCAR_AlNTi2")
    print("getTitle()=",getTitle(strFile))
    strFile=readFile("PARTCAR_SSeZn")
    print("getTitle()=",getTitle(strFile))


if __name__ == "__main__":
    main()
    
