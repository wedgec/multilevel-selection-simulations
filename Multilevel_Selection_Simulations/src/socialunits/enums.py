'''
Module description: 
    defines several Enum classes. Note that for Python 2.7, 
    used here, Enum requires special installation
Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from enum import Enum

class ReproductionType(Enum):
    
    '''
    Instances of socialunits.individual.Individual, socialunits.group.SocialGroup,
    and simulation.mls_simulatar.MLS_simulator are all associated with one or the 
    other reproduction type
    '''
    
    asexual = 0
    sexual = 1
    
class Genotype(Enum):
    
    '''
    Each instance of socialunits.individual.Individual has a genotype. A and S are 
    genotypes for asexual individuals and map onto altruistic and selfish phenotypes 
    respectively. AA, Aa, aa are genotypes for sexually reproducing individuals. The 
    set is heterozygous dominant--thus AA and Aa correspond with the altruistic 
    phenotype, while only aa corresponds with the selfish phenotype 
    '''

    A = 0
    S = 1
    AA = 2
    Aa = 3
    aa = 4
    
class Phenotype(Enum):
    
    '''
    Instances of socialunits.individual.Individual are each associated with a phenotype,
    which is determined by the individual's genotype. See docstring for 
    socialunits.enums.Genotype for genotype-phenotype correspondences
    '''
    
    altruistic = 0
    selfish = 1
    
class AltruismType(Enum):
    
    '''
    Instances of socialunits.individual.Individual are each associated with a type of altruism.
    Strong altruism means that an altruist cannot be the beneficiary of its own generosity, whereas
    this is allowed in cases of weak altruism. Still with weak altruism, it should be the case that 
    the expected benefit of an altruistic act for oneself should be outweighed by the expected cost
    '''
    
    weak = 0
    strong = 1