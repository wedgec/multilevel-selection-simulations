# multilevel-selection-simulations
## Evolutionary Modeling to Investigate Multi-level Selection Theory as an Explanation for Altruism

This is the repository for my Spring 2017 independent study with 
Professor <a href="http://www.cs.brandeis.edu/~pollack/">Jordan Pollack</a>. 
The project is to design, run, and visualize evolutionary simulations in order to investigate <a href="https://en.wikipedia.org/wiki/Group_selection">multi-level selection theory</a>  as an explanation for biological altruism.

### Project Directory and File Organization

**Multilevel_Selection_Simulation/src (folder)** -- implements model and runs experiments, all Python code
+ socialunits (folder) -- defines social units of organization and their behavior, e.g. groups, individuals
  + *files*: individual.py, group.py, enums.py
+ simulation (folder) -- defines behavior of simulator and contains experiment scripts
    + *files*: evo_simluator.py, migration.py, experiment1_MLS_by_stochastic_dynamics.py, experiment2_weak_selection_control.py,      experiment3_phenotype_stratisfied_migration_control.py, experiment4_phenotype_stratisfied_migration.py, experiment5_random_redistribution.py, experiment6_reciprocity.py

**simulation_data (folder)** -- data outputed from experiments, all csv files
+ *files*: experiment1_MLS_by_stochastic_dynamics.csv, experiment2_weak_selection_control.csv,      experiment3_phenotype_stratisfied_migration_control.csv, experiment4_phenotype_stratisfied_migration.csv, experiment5_random_redistribution.csv, experiment6_reciprocity.csv

**matlab_scripts_and_functions (folder)** -- matlab code for visualizing the experimental data
+ *files*: plotExperiment1MLS_byStochasticDynamics.m, plotSxperiment2WeakSelectionControl.m,      plotExperiment3PhenotypeStratisfiedMigrationControl.m, plotExperiment4PhenotypeStratisfiedMigration.m, plotExperiment5RandomRedistribution.m, plotExperiment6Reciprocity.m, plotExperiments1Through3.m, plotExperiments4Through6.m, get21LineSpecs.m, omitProportionsOfLowPopulations.m

**matlab_generated_plots (folder)** -- matlab-generated plots that visualize the experimental data, 3 for each experiment. The figures for experiments 1 through 3 are exactly parallel, just populated with different data, and likewise for the figures of experiments 4 through 6
+ *files*: experiment1_figure1, experiment1_figure2, experiment1_figure3, experiment1_figure1, experiment2_figure2, experiment2_figure3, experiment2_figure1, experiment3_figure2, experiment3_figure3, experiment3_figure1, experiment4_figure2, experiment4_figure3, experiment4_figure1, experiment5_figure2, experiment5_figure3, experiment5_figure1, experiment5_figure2, experiment5_figure3,



