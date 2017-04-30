function plotExperiments1Through3(simulationData, startingStateIndex, numTrialsPerOuterParamVal)
% Name: plotExperiments1Through3
% Description: called to produce plot figures for experiments 1 and 2.
%   Three plots are created. The first displays final proportions of
%   altruists as a function of extra reproduction probability. The second
%   displays final proportions of altruists as a function of target group 
%   size. And the third shows the relationship between target group size 
%   the average standard deviation of altruist proportions among groups for
%   each trial.
% Format of call: plotExperiments1And2(simulationData, startingStateIndex, vecLengthPerGroupSize)
% Inputs: simulationData is the entire matrix of data for an experiment, 
%   startingStateIndex is the column index in which initial dependant 
%   variable values are located, and numTrialsPerOuterParamVal is the
%   number of trials simulated for each value of the parameter of the outer
%   for loop of the python script that produced the data
% Output: none
% William Edgecomb, Spring 2017
% Project: Multilevel_Selection_Simulations
% Course: COSI 210a, Independent study with Professor Jordan Pollack

    % for trials where the ending population is greater than
    % zero but less than than the starting population, replace the final
    % population with NaN so that these data points, which prone to be
    % misleading, are omitted when plotted
    simulationData = omitProportionsOfLowPopulations(simulationData, startingStateIndex);

    % entire column of starting group sizes
    redundantGroupSizes = simulationData(:, 1);
    % keep every third value, thus just one value for each trial
    groupSizes = redundantGroupSizes(1:4:end);
    
    % total number of trials
    numTrials = size(groupSizes,1);

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
    % plot one line for each target group size and add line spec to legend
    for i = 1:numTrialsPerOuterParamVal:size(prosocialityBenefits)
        % plot single line, relationship between value of extra reproduction
        % probability and the final proportion of altruists
        x = prosocialityBenefits(i:numTrialsPerOuterParamVal+i-1);
        y = prosocialProportions(i:numTrialsPerOuterParamVal+i-1);
        z = groupSizes(i:numTrialsPerOuterParamVal+i-1);
        
        plot(x,y, lineSpecs{lineSpecIndex}, 'DisplayName', num2str(z(1)))
        lineSpecIndex = lineSpecIndex + 1;
    end
    title('Benefit Conferred by Altruism''s Effect on Altruists'' Fitness');
    xlabel('Extra Reproduction Probability')
    ylabel('Final Proportion of Altruists')
    leg = legend('location', 'NEO');
    title(leg, 'Group Size')
    % add reference lines
    startingProportionLine = refline(0, .53);
    startingProportionLine.Color = 'r';
    fiftyPercentProportionLine = refline(0, .5);
    fiftyPercentProportionLine.Color = 'k';
    legend('show')

    %%%% PLOT FIGURE 2: Target Group Size vs. Final Altruist Proportions

    lineSpecIndex = 1;
    figure
    hold on
     % plot one line for each extra reproduction probability and add line 
     % spec to legend
    for i = 1:1:numTrialsPerOuterParamVal
        % plot single line, relationship between target group size and
        % and the final proportion of altruists
        x = groupSizes(i:numTrialsPerOuterParamVal:end);
        y = prosocialProportions(i:numTrialsPerOuterParamVal:end);
        z = prosocialityBenefits(i:numTrialsPerOuterParamVal:end);

        plot(x,y, lineSpecs{lineSpecIndex}, 'DisplayName', num2str(z(1)))
        lineSpecIndex = lineSpecIndex + 1;
    end
    title('Effect of Target Group Size on Altruists'' Fitness');
    xlabel('Target Group Size')
    ylabel('Final Proportion of Altruists')
    leg = legend('location', 'NEO');
    title(leg, 'p(Extra Reproduction)')
    % add reference lines
    startingProportionLine = refline(0, .53);
    startingProportionLine.Color = 'r';
    fiftyPercentProportionLine = refline(0, .5);
    fiftyPercentProportionLine.Color = 'k';
    legend('show')

    %%%% PLOT FIGURE 3: Group Size vs. Average Standard Deviation of 
    %%%% Altruist Proportions
    
    lineSpecIndex = 1;
    figure
    hold on
    % plot one line for each extra reproduction probability and add line 
    % spec to legend
    for i = 1:1:numTrialsPerOuterParamVal
        % plot single line, relationship between target group size and
        % average standard deviation of altruist proportion among groups
        x = groupSizes(i:numTrialsPerOuterParamVal:end);
        y = avgStdDeviations(i:numTrialsPerOuterParamVal:end);
        z = prosocialityBenefits(i:numTrialsPerOuterParamVal:end);

        plot(x,y, lineSpecs{lineSpecIndex}, 'DisplayName', num2str(z(1)))
        lineSpecIndex = lineSpecIndex + 1;
    end
    title('Effect of Group Size on Deviation in Altruist Proportions')
    xlabel('Target Group Size')
    ylabel('Average Standard Deviation of Altruist Proportions')
    leg = legend('location', 'NEO');
    title(leg, 'p(Extra Reproduction)')
    xlim([0 22])
    ylim([0 0.5])
    legend('show')