function plotExperiments4Through6(simulationData, startingStateIndex, numTrialsPerOuterParamVal, prosocialityType)
% Name: plotExperiments4Through6
% Description: called to produce plot figures for experiments 3 through 5.
%   Three plots are created. The first displays final proportions of
%   altruists as a function of extra reproduction probability. The second
%   displays final proportions of altruists as a function of the cost of 
%   altruism. And the third shows the relationship between the cost of
%   altruism and the average standard deviation of altruist proportions 
%   among groups for each trial.
% Format of call: plotExperiments3Through5(simulationData, startingStateIndex, vecLengthPerGroupSize)
% Inputs: simulationData is the entire matrix of data for an experiment, 
%   startingStateIndex is the column index in which initial dependant 
%   variable values are located,numTrialsPerOuterParamVal is the
%   number of trials simulated for each value of the parameter of the outer
%   for loop of the python script that produced the data, and
%   prosocialityType is a string with value 'altruistic' or 'reciprocating'
% Output: none
% William Edgecomb, Spring 2017
% Project: Multilevel_Selection_Simulations
% Course: COSI 210a, Independent study with Professor Jordan Pollack
    
    % for trials where the ending population is greater than
    % zero but less than than the starting population, replace the final
    % population with NaN so that these data points are omitted when plotted
    simulationData = omitProportionsOfLowPopulations(simulationData, startingStateIndex);

    % entire column of prosociality costs
    redundantProsocialityCosts = simulationData(:, 3);
    % keep every third value, thus just one value for each trial
    prosocialityCosts = redundantProsocialityCosts(1:4:end);

    numTrials = size(prosocialityCosts,1);

    % entire column of prosociality benefits
    redundantProsocialityBenefits = simulationData(:, 2);
    % keep every third value, thus just one value for each trial
    prosocialityBenefits = redundantProsocialityBenefits(1:4:end);

    % entire final column
    finalColumn = simulationData(:, end);
    % keep every third value, thus just one value for each trial
    prosocialProportions = finalColumn(1:4:end);

    % calculate vector of avg standard deviations of prosocial proportions
    avgStdDeviations = zeros(numTrials, 1);
    avgStdDeviationsIndex = 1;
    for i = 4:4:numTrials*4
        % for trials where the final prosocial proportion was replaced with 
        % NaN, set avg standard deviation of that trial also to NaN
        if isnan(prosocialProportions(avgStdDeviationsIndex))
            avgStdDeviations(avgStdDeviationsIndex) = NaN;
            avgStdDeviationsIndex = avgStdDeviationsIndex + 1;
        else
            stdDeviationsVec = simulationData(i, startingStateIndex:end);
            % replace negative ones, which indicate extinction in
            % population, with zeros
            for j = 1:size(stdDeviationsVec,2)
                if stdDeviationsVec(j) < 0
                    stdDeviationsVec(j) = 0;
                end
            end
            avgStdDeviations(avgStdDeviationsIndex) = mean(stdDeviationsVec);
            avgStdDeviationsIndex = avgStdDeviationsIndex + 1;
        end
    end

    %%%% PLOT FIGURE 1: Extra Reproduction Probability vs. Final Altruist
    %%%% Proportions
    
    % line specifications for plotting
    lineSpecs = get21LineSpecs();
    % increment after each line plotted
    lineSpecIndex = 1;

    figure
    hold on
    % plot one line for each prosociality cost and add line spec to legend
    for i = 1:numTrialsPerOuterParamVal:size(prosocialityBenefits)
        % plot single line, relationship between value of extra reproduction
        % probability and the final proportion of prosocial individuals
        z = prosocialityCosts(i:numTrialsPerOuterParamVal+i-1);
        x = prosocialityBenefits(i:numTrialsPerOuterParamVal+i-1);
        y = prosocialProportions(i:numTrialsPerOuterParamVal+i-1);
        
        plot(x,y, lineSpecs{lineSpecIndex}, 'DisplayName', num2str(z(1)))
        lineSpecIndex = lineSpecIndex + 1;
    end
    
    leg = legend('location', 'NEO');
    if strcmp(prosocialityType, 'altruistic')
        title('Benefit of Altruism''s Effect on Altruists'' Fitness');
        ylabel('Final Proportion of Altruists')
        title(leg, 'Altruism Cost')
    else
        title('Benefit From Reciprocator''s Effect on Reciprocators'' Fitness');
        ylabel('Final Proportion of Reciprocators')
        title(leg, 'Reciprocator Cost')
    end
    xlabel('Extra Reproduction Probability')
    % add reference lines
    startingProportionLine = refline(0, .53);
    startingProportionLine.Color = 'r';
    fiftyPercentProportionLine = refline(0, .5);
    fiftyPercentProportionLine.Color = 'k';
    legend('show')

    %%%% PLOT FIGURE 2: Prosociality Cost vs. Final Altruist Proportions

    lineSpecIndex = 1;
    figure
    hold on
    for i = 1:1:numTrialsPerOuterParamVal
        % plot single line, relationship between prosociality cost and
        % and the final proportion of altruists
        x = prosocialityCosts(i:numTrialsPerOuterParamVal:end);
        y = prosocialProportions(i:numTrialsPerOuterParamVal:end);
        z = prosocialityBenefits(i:numTrialsPerOuterParamVal:end);

        plot(x,y, lineSpecs{lineSpecIndex}, 'DisplayName', num2str(z(1)))
        lineSpecIndex = lineSpecIndex + 1;
    end
    leg = legend('location', 'NEO');
    if strcmp(prosocialityType, 'altruistic')
        title('Effect of Cost to Altruist on Altruists'' Fitness')
        xlabel('Altruism Cost')
        ylabel('Final Proportion of Altruists')
        title(leg, 'Altruism Benefit')
    else
        title('Effect of Cost to Reciprocator on Reciprocators'' Fitness')
        xlabel('Reciprocator''s Cost')
        ylabel('Final Proportion of Reciprocators')
        title(leg, 'Benefit From Reciprocator')
    end
    % add reference lines
    startingProportionLine = refline(0, .53);
    startingProportionLine.Color = 'r';
    fiftyPercentProportionLine = refline(0, .5);
    fiftyPercentProportionLine.Color = 'k';
    legend('show')

    %%%% PLOT FIGURE 3: Average Standard Deviations

    lineSpecIndex = 1;
    figure
    hold on
    for i = 1:1:numTrialsPerOuterParamVal
        % plot single line, relationship between prosociality cost and
        % average standard deviation of altruist proportion among groups
        x = prosocialityCosts(i:numTrialsPerOuterParamVal:end);
        y = avgStdDeviations(i:numTrialsPerOuterParamVal:end);
        z = prosocialityBenefits(i:numTrialsPerOuterParamVal:end);
        
        plot(x,y, lineSpecs{lineSpecIndex}, 'DisplayName', num2str(z(1)))
        lineSpecIndex = lineSpecIndex + 1;
    end
    if strcmp(prosocialityType, 'altruistic')
        title('Average Standard Deviations in Altruist Proportions')
        xlabel('Altruism Cost')
    else
        title('Average Standard Deviations in Reciprocator Proportions')
        xlabel('Reciprocator''s Cost')
    end
    ylabel('Average Standard Deviation of Altruist Proportions')
    leg = legend('location', 'NEO');
    title(leg, 'p(Extra Reproduction)')
    ylim([0 0.5])
    legend('show')