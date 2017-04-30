'''
Module description: defines a single custom class, Individual 
Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from enums import ReproductionType, Phenotype, Genotype
from random import random
    
class Individual:
   
    '''
    Description: single organismal unit, smallest unit of social organization. Reproduction
        occurs within Individual class
       
    Instance variables:
    # self.genotype: member of socialunits.enums.Genotype (A, S, R, AA, Aa, or aa)
    # self.phenotype: member of socialunits.enums.Phenotype (altruistic, selfish, or reciprocating)
    # self.reproduction: member of socialunits.enums.ReproductionType (sexual or asexual)
    # self.mutationRate: rate at which genotype mutations occur during 
        reproduction (range [0,1])
    # self.prosocialCostIncurred: cost incurred as the result of exhibiting altruistic or 
        reciprocally altruistic behavior. Value will modulate reproduction probability
    # self.extraReproductionChances: number of reproduction opportunities gained beyond 
        base number of reproduction opportunities (comes into play for methods 
        playSocialGame and deathAndReproduction of class simulation.group.SocialGroup)
    # self.oppositeGenotype: initialized only for asexually reproducing individuals. Represents 
        the only other asexual genotype in play for the population (used for reproduction 
        when mutation rate is positive)
        
    Constructor method signature: __init__(self, genotype, reproduction, mutationRate=0.0)
        
    Public methods:
    # attemptReproduction(mate=None, reproductionProbability=1.0): 
        attempts reproduction for single offspring, w/ success/failure modulated by
        reproductionProbability, and offspring's resulting genotype modulated by mutation rate. 
        Requires input of another instance of class if individual's reproduction type is 
        sexual. Returns new instance of Individual if reproduction successful, None otherwise
    '''
    
    def __init__(self, genotype, reproduction, mutationRate=0.0):
        
        '''
        Parameters:
        # genotype: member of socialunits.enums.Genotype (A, S, R AA, Aa, or aa). Determines phenotype
        # reproduction: member of socialunits.enums.ReproductionType (sexual or asexual)
        # mutationRate: rate at which genotype mutations occur during 
            reproduction (range [0,1])
        
        Errors:
        # TypeError: raised if reproduction or genotype is not of proper enum
        # RuntimeError: raised (in subsidiary function) if asexual individual has 
            sexual genotype (i.e. AA, Aa, or aa instead of A or S) or vice versa
        '''
        
        if not isinstance(reproduction, ReproductionType):
            raise TypeError('reproduction must be of type socialunits.enums.ReproductionType')
        if not isinstance(genotype, Genotype):
            raise TypeError('genotype must be of type socialunits.enums.Genotype')
        
        self.genotype = genotype
        self.reproduction = reproduction
        self.mutationRate=mutationRate
        self.prosocialCostIncurred = 0.0
        self.extraReproductionChances = 0
        
        # self.phenotype, self.oppositeGenotype, set via private methods
        if reproduction == ReproductionType.asexual:
            self._setInstanceVarsAsexual(self.genotype)
        if reproduction == ReproductionType.sexual:
            self._setInstanceVarsSexual(self.genotype)
    
    def _setInstanceVarsAsexual(self, genotype):
        if genotype == Genotype.A:
            self.phenotype = Phenotype.altruistic
            self.oppositeGenotype = Genotype.S
        elif genotype == Genotype.S:
            self.phenotype = Phenotype.selfish
            self.oppositeGenotype = Genotype.A
        elif self.genotype == Genotype.R:
            self.phenotype = Phenotype.reciprocating
            self.oppositeGenotype = Phenotype.selfish
        else:
            raise RuntimeError('genotype must be socialunits.enums.Genotype.A, '
                               'socialunits.enums.Genotype.S, or socialunits.enums.Genotype.R '
                               'for asexual individuals')  
        
    def _setInstanceVarsSexual(self, genotype):
        raise RuntimeError('sexual reproduction not implemented yet')
    
    def attemptReproduction(self, reproductionProbability=1.0, mate=None):
        
        '''
        Description: attempts reproduction of single offspring. Success of reproduction, 
            as well as offspring's genotype, are probabilistic. This is a public wrapper 
            method that calls a different subsidiary method depending on reproduction type
        
        Parameters:
        # mate: instance of Individual class to mate with, None if reproduction is asexual
        # reproductionProbability: probability that one offspring is returned, range [0,1].
            Alternatively None is returned
            
        Returns: single new instance of Individual or None
        
        Warnings: generic warning raised if non-None mate parameter is inputted for an
            asexually reproducing individual
        '''
        
        if (not mate == None) and self.reproduction == ReproductionType.asexual:
            raise Warning('A mate was inputted as a sexual partner for an asexually reproducing individual') 
        
        if random() < reproductionProbability:
            return (self._reproduceAsexual() if self.reproduction == ReproductionType.asexual
                    else self._reproduceSexual(mate))
        else:
            return None 
    
    def _reproduceAsexual(self):
        
        '''
        returns new instance of individual. Value of self.mutationRate is the probability that offspring
        will have same genotype as parent. 1-self.mutationRate is probability that offspring will have 
        opposite genotype
        '''
        
        return (Individual(self.genotype, self.reproduction, self.mutationRate) if random() < (1.0-self.mutationRate)
                else Individual(self.oppositeGenotype, self.reproduction, self.mutationRate))
        
    def _reproduceSexual(self, mate):
        raise RuntimeError('Sexual Reproduction not implemented yet')