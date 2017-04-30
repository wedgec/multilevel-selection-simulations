function simulationData = omitProportionsOfLowPopulations(simulationData, startingPopulationIndex)
% Name: omitProportionsOfLowPopulations
% Description: for trials where the ending population is greater than
%   zero but less than than the starting population, replaces the final
%   population with NaN so that these data points are omitted when plotted
% Format of call: omitProportionsOfLowPopulations(simulationData, startingPopulationIndex)
% Inputs: simulationData is the entire matrix of data for an experiment,
%   and startingPopulationIndex is the column index in which initial
%   population counts are found
% Output: mutated matrix simulationData
% William Edgecomb, Spring 2017
% Project: Multilevel_Selection_Simulations
% Course: COSI 210a, Independent study with Professor Jordan Pollack

[numRows, numCols] = size(simulationData);

% 1 iteration for each trial
for i = 1:4:numRows
    startingPopulation = simulationData(i+1, startingPopulationIndex);
    % final proportions found at last column index of matrix
    endingPopulation = simulationData(i+1, numCols);
    if endingPopulation < startingPopulation && endingPopulation > 0
        simulationData(i, numCols) = NaN;
    end
end

    