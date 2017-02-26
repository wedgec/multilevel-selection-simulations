'''
Created on Feb 22, 2017

@author: Will_Masha
'''

from enum import Enum

class MigrationType(Enum):
    
    '''
    Instances of evo_simulator.MLS_Simulator are each associated with a type of migration.
    With totalRandomRedistributed, all individuals in population are randomly reshuffled into new groups
    after every round of the life cycle. With phenotypeStratisfied, at each round individuals are reassigned 
    to groups such that groups tend to have a preponderance either of altruistic types, or a preponderance
    of selfish types. With totalIsolation, individuals never migrate from the group in which they are
    initially assigned or born into. The total isolation condition serves as a control to test the effect
    that migration has on the outcome of an evolutionary simulation.
    '''
    
    totalRandomRedistribution = 0
    phenotypeStratified = 1
    totalIsolation = 2
    
def randomRedistribution(self):
        self._mergeGroups()
        self._resetGroups()
        self._assignToGroupsRandomly(self.allIndividuals)
        
migrationDict = {randomRedistribution : 0}
    