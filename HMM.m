%% Master Thesis - HMM Analysis %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The checking of the two assumptions of markov property and homogenity of 
% variances were made after this Script in the PCA.py.
% Both hold.


%% NegEval %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear
close all

[data_NegEval,SubjectIDs,TrialIDs] = read_xls_fixations('NegEval_Data.xls');

% the number of subjects
N_NegEval = length(data_NegEval);
% Stimuli 
StimImg_NegEval = 'Stimuli_NegEval.png';

% load image
img = imread(StimImg_NegEval);
imgsize = size(img);


%% Variational Bayesian Parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

K = 3;
vbopt.alpha0 = 0.1; % min: 0(concentrated prior, closer to the data); max: 1(uniform prior, added constant) - low impact 
vbopt.mu0    = [imgsize(2)/2;imgsize(1)/2;460];  % the image center, and 460ms avg duration - high impact 
vbopt.W0     = [0.0100, 0.0100, 0.0065]; % stdev of 100 pixels for ROIs, and stddev of 0.65 ms for duration - low impact 
vbopt.beta0  = 1; % Large values encourage estimated ROIs to be similar to the prior ROI, while small value ignores the prior
vbopt.v0     = 10; % default = 10; Larger values give preference to diagonal covariance matrices for the emissions
vbopt.epsilon0 = 0.1; % same meaning as for the alpha above, but for the transition matrix - low impact 
vbopt.showplot = 1;     % show each subject during learning
vbopt.bgimage = StimImg_NegEval;

vbopt.seed = 1000;  % set random state for reproducible results.

% Estimate hyperparameters automatically for each individual
% (remove this option to use the above hyps)
% vbopt.learn_hyps = 1;  

% Estimate hyperparameters automatically as a batch (all individuals share the same hyperparameters)
% (uncomment below to enable the option)
% vbopt.learn_hyps_batch = 1;

% names of files for saving results
matfile_individual = 'models_duration_individual.mat';
% matfile_group      = 'models_demo_faces_duration_group.mat';


% Learn the parameters on individual level 
[hmms_NegEval, Ls_NegEval] = vbhmm_learn_batch(data_NegEval, K, vbopt);

% plot one subject
vbhmm_plot(hmms_NegEval{7}, data_NegEval{7}, StimImg_NegEval);
figure; vbhmm_plot_compact(hmms_NegEval{7}, StimImg_NegEval);

% % plot all subject
% for i=1:N_NegEval
%   if mod(i,14)==1
%     figure
%   end
%   subtightplot(4,4,mod(i-1,14)+1)
%   vbhmm_plot_compact(hmms_NegEval{i}, StimImg_NegEval);
%   title(sprintf('Subject %d', i));
% end


%% PosEval %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[data_PosEval,SubjectIDs,TrialIDs] = read_xls_fixations('PosEval_Data.xls');

% the number of subjects
% We take the same number as for NegEval, as we don't have sequences for
% participant 's', which is participant 15 in the corresponding .xlsx file 
% Stimuli 
StimImg_PosEval = 'Stimuli_PosEval.png';


%% Variational Bayesian Parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Same as for NegEval
% load image
img = imread(StimImg_PosEval);
imgsize = size(img);

vbopt.mu0    = [imgsize(2)/2;imgsize(1)/2;465];
vbopt.bgimage = StimImg_PosEval;

% Learn the parameters on individual level 
[hmms_PosEval, Ls_posEval] = vbhmm_learn_batch(data_PosEval, K, vbopt);

% plot one subject
vbhmm_plot(hmms_PosEval{7}, data_PosEval{7}, StimImg_PosEval);
figure; vbhmm_plot_compact(hmms_PosEval{7}, StimImg_PosEval);

% % plot all subject
% for i=1:N_NegEval
%   if mod(i,14)==1
%     figure
%   end
%   subtightplot(4,4,mod(i-1,14)+1)
%   vbhmm_plot_compact(hmms_PosEval{i}, StimImg_PosEval);
%   title(sprintf('Subject %d', i));
% end


%% NegEval %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Create table with all necessary and structured data for export 
% Initialize the table with the first participant 
priorOne = hmms_NegEval{1}.prior
transOne = hmms_NegEval{1}.trans
pdfOneOne_mean = hmms_NegEval{1}.pdf{1}.mean
pdfOneOne_cov = hmms_NegEval{1}.pdf{1}.cov
pdfOneTwo_mean = hmms_NegEval{1}.pdf{2}.mean
pdfOneTwo_cov = hmms_NegEval{1}.pdf{2}.cov
pdfOneThree_mean = hmms_NegEval{1}.pdf{3}.mean
pdfOneThree_cov = hmms_NegEval{1}.pdf{3}.cov

dataOne = vertcat(priorOne(:), transOne(:), pdfOneOne_mean(:), pdfOneOne_cov(:), ...
    pdfOneTwo_mean(:), pdfOneTwo_cov(:), pdfOneThree_mean(:), pdfOneThree_cov(:))

finalTable_NegEval = array2table(transpose(dataOne),'VariableNames', {'prior1','prior2','prior3',...
    'trans1','trans2','trans3','trans4','trans5','trans6','trans7','trans8','trans9',...
    'pdf1', 'pdf2', 'pdf3', 'pdf4', 'pdf5', 'pdf6', 'pdf7', 'pdf8', 'pdf9', 'pdf10',...
    'pdf11', 'pdf12', 'pdf13', 'pdf14', 'pdf15', 'pdf16', 'pdf17', 'pdf18', 'pdf19', 'pdf20',...
    'pdf21', 'pdf22', 'pdf23', 'pdf24', 'pdf25', 'pdf26', 'pdf27', 'pdf28', 'pdf29', 'pdf30',...
    'pdf31', 'pdf32', 'pdf33', 'pdf34', 'pdf35', 'pdf36'})


for i = 2:14 
    priorCurrent = hmms_NegEval{i}.prior
    transCurrent = hmms_NegEval{i}.trans
    pdfCurrentOne_mean = hmms_NegEval{i}.pdf{1}.mean
    pdfCurrentOne_cov = hmms_NegEval{i}.pdf{1}.cov
    pdfCurrentTwo_mean = hmms_NegEval{i}.pdf{2}.mean
    pdfCurrentTwo_cov = hmms_NegEval{i}.pdf{2}.cov
    pdfCurrentThree_mean = hmms_NegEval{i}.pdf{3}.mean
    pdfCurrentThree_cov = hmms_NegEval{i}.pdf{3}.cov

    dataCurrent = vertcat(priorCurrent(:), transCurrent(:), pdfCurrentOne_mean(:), pdfCurrentOne_cov(:), ...
    pdfCurrentTwo_mean(:), pdfCurrentTwo_cov(:), pdfCurrentThree_mean(:), pdfCurrentThree_cov(:))
  
    
    tableCurrent = array2table(transpose(dataCurrent),'VariableNames', {'prior1','prior2','prior3',...
        'trans1','trans2','trans3','trans4','trans5','trans6','trans7','trans8','trans9',...
        'pdf1', 'pdf2', 'pdf3', 'pdf4', 'pdf5', 'pdf6', 'pdf7', 'pdf8', 'pdf9', 'pdf10',...
        'pdf11', 'pdf12', 'pdf13', 'pdf14', 'pdf15', 'pdf16', 'pdf17', 'pdf18', 'pdf19', 'pdf20',...
        'pdf21', 'pdf22', 'pdf23', 'pdf24', 'pdf25', 'pdf26', 'pdf27', 'pdf28', 'pdf29', 'pdf30',...
        'pdf31', 'pdf32', 'pdf33', 'pdf34', 'pdf35', 'pdf36'})
    
    finalTable_NegEval = [finalTable_NegEval; tableCurrent]
    
end 


%% PosEval %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Create table with all necessary and structured data for export 
% Initialize the table with the first participant 
priorOne = hmms_PosEval{1}.prior
transOne = hmms_PosEval{1}.trans
pdfOneOne_mean = hmms_PosEval{1}.pdf{1}.mean
pdfOneOne_cov = hmms_PosEval{1}.pdf{1}.cov
pdfOneTwo_mean = hmms_PosEval{1}.pdf{2}.mean
pdfOneTwo_cov = hmms_PosEval{1}.pdf{2}.cov
pdfOneThree_mean = hmms_PosEval{1}.pdf{3}.mean
pdfOneThree_cov = hmms_PosEval{1}.pdf{3}.cov

dataOne = vertcat(priorOne(:), transOne(:), pdfOneOne_mean(:), pdfOneOne_cov(:), ...
    pdfOneTwo_mean(:), pdfOneTwo_cov(:), pdfOneThree_mean(:), pdfOneThree_cov(:))

finalTable_PosEval = array2table(transpose(dataOne),'VariableNames', {'prior1','prior2','prior3',...
    'trans1','trans2','trans3','trans4','trans5','trans6','trans7','trans8','trans9',...
    'pdf1', 'pdf2', 'pdf3', 'pdf4', 'pdf5', 'pdf6', 'pdf7', 'pdf8', 'pdf9', 'pdf10',...
    'pdf11', 'pdf12', 'pdf13', 'pdf14', 'pdf15', 'pdf16', 'pdf17', 'pdf18', 'pdf19', 'pdf20',...
    'pdf21', 'pdf22', 'pdf23', 'pdf24', 'pdf25', 'pdf26', 'pdf27', 'pdf28', 'pdf29', 'pdf30',...
    'pdf31', 'pdf32', 'pdf33', 'pdf34', 'pdf35', 'pdf36'})


for i = 2:14 
    priorCurrent = hmms_PosEval{i}.prior
    transCurrent = hmms_PosEval{i}.trans
    pdfCurrentOne_mean = hmms_PosEval{i}.pdf{1}.mean
    pdfCurrentOne_cov = hmms_PosEval{i}.pdf{1}.cov
    pdfCurrentTwo_mean = hmms_PosEval{i}.pdf{2}.mean
    pdfCurrentTwo_cov = hmms_PosEval{i}.pdf{2}.cov
    pdfCurrentThree_mean = hmms_PosEval{i}.pdf{3}.mean
    pdfCurrentThree_cov = hmms_PosEval{i}.pdf{3}.cov

    dataCurrent = vertcat(priorCurrent(:), transCurrent(:), pdfCurrentOne_mean(:), pdfCurrentOne_cov(:), ...
    pdfCurrentTwo_mean(:), pdfCurrentTwo_cov(:), pdfCurrentThree_mean(:), pdfCurrentThree_cov(:))
  
    
    tableCurrent = array2table(transpose(dataCurrent),'VariableNames', {'prior1','prior2','prior3',...
        'trans1','trans2','trans3','trans4','trans5','trans6','trans7','trans8','trans9',...
        'pdf1', 'pdf2', 'pdf3', 'pdf4', 'pdf5', 'pdf6', 'pdf7', 'pdf8', 'pdf9', 'pdf10',...
        'pdf11', 'pdf12', 'pdf13', 'pdf14', 'pdf15', 'pdf16', 'pdf17', 'pdf18', 'pdf19', 'pdf20',...
        'pdf21', 'pdf22', 'pdf23', 'pdf24', 'pdf25', 'pdf26', 'pdf27', 'pdf28', 'pdf29', 'pdf30',...
        'pdf31', 'pdf32', 'pdf33', 'pdf34', 'pdf35', 'pdf36'})
    
    finalTable_PosEval = [finalTable_PosEval; tableCurrent]
    
end 


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%% Export the two tables as a .xlsx file %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
filename = 'hmms_negEval_5.xlsx';
writetable(finalTable_NegEval,filename)

filename = 'hmms_posEval_5.xlsx';
writetable(finalTable_PosEval,filename)

