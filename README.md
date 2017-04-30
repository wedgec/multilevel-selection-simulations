# multilevel-selection-simulations
### Evolutionary Modeling to Investigate Multilevel Selection Theory as an Explanation for Altruism

This is the repository for my Spring 2017 independent study with 
Professor <a href="http://www.cs.brandeis.edu/~pollack/">Jordan Pollack</a>. 
The project is to design, run, and visualize evolutionary simulations in order to investigate <a href="https://en.wikipedia.org/wiki/Group_selection">multi-level selection theory</a>  as an explanation for biological altruism.

#### Project Directory and File Organization

**Multilevel_Selection_Simulation/src (folder)** -- implements model and runs experiments, all Python code
+ socialunits (folder) -- defines social units of organization and their behavior, e.g. groups, individuals
  + *files*: individual.py, group.py, enums.py
+ simulation (folder) -- defines behavior of simulator and contains experiment scripts
    + *files*: evo_simluator.py, migration.py, experiment1_MLS_by_stochastic_dynamics.py, experiment2_weak_selection_control.py,      experiment3_phenotype_stratisfied_migration_control.py, experiment4_phenotype_stratisfied_migration.py, experiment5_random_redistribution.py, experiment6_reciprocity.py
