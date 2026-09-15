# ======================================================================================================================
# Master Thesis - Application of LDA algorithm on HMM parameters
# ======================================================================================================================


# Prior Knowledge sourced from https://machinelearningmastery.com/linear-discriminant-analysis-with-python/

# - LDA is very robust against violation of assumptions
# - machine learning linear classification algorithm, seperation by line and hyperplanes by dimensionality reduction
# - predicts new sequence belonging to one of the two classes PosEval or NegEval by calculating the conditional
# probabilities; simple Bayes Theorem
# - assumptions: normally distributed data; numeric; same variance; input variables are not correlated
#     > if that is not the case, it might be good to transfrom the data so that it has a gaussian distribution
#     or standardize it
# - features: priors, transition matrix, pdf (emissions(mean, covariance))


########################################################################################################################
# todo Load transformed and final data
########################################################################################################################
import os
import pandas as pd
os.chdir('C:/Users/olive/OneDrive/Desktop/Master/03_Data Preprocess/RawData')
# Information about the transformed excel files
PosEval = pd.read_excel('PosEval_Data.xlsx')
NegEval = pd.read_excel('NegEval_Data.xlsx')
########################################################################################################################


########################################################################################################################
# todo Assumption check for modelling the HMMs as parametric functions for each participant individually
########################################################################################################################
# The two main assumptions for the Hidden Markov Model parameter are
# 1: markov property: that the observations are conditionally independent from each other,
# except for the ones that are consecutive in two time steps. > CHECK
# 2: that the transition probabilites are homogenous. > CHECK
########################################################################################################################
########################################################################################################################
# Assumption 1:
# To see if the observations are time independent between time steps further away than the consecutive one, we can appply
# an autocorrelation function. Does only make sense within a participant and within sequences, as these are the only observations
# that really happened in consecutive time order.

from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
########################################################################################################################
# PosEval - FixX
########################################################################################################################
# Number of trials per participant
TrialID_PosEval = [7,11,9,6,10,8,13,2,3,9,5,7,5,13]
# Loop through all participants, whenever a trials has more than one observations, apply the autocorrelation function and
# plot it
for i in range(1,15):
    print(i)
    for j in range(1,TrialID_PosEval[i-1]+1):
        print(j)
        if len(PosEval['FixX'][PosEval['SubjectID'] == i][PosEval['TrialID'] == j]) > 1:
            plot_acf(PosEval['FixX'][PosEval['SubjectID'] == i][PosEval['TrialID'] == j])
            plt.show()




from pandas.plotting import autocorrelation_plot
plt.figure()
autocorrelation_plot(PosEval['FixX'])
plt.show()
plt.figure()
autocorrelation_plot(PosEval['FixY'])
plt.show()
plt.figure()
autocorrelation_plot(NegEval['FixX'])
plt.show()
plt.figure()
autocorrelation_plot(NegEval['FixY'])
plt.show()



########################################################################################################################
# PosEval - FixY
########################################################################################################################
# Same as above, just different variable
for i in range(1,15):
    print(i)
    for j in range(1,TrialID_PosEval[i-1]+1):
        print(j)
        # there have to be at least two observations in a sequence to use the autocorrelation function
        if len(PosEval['FixY'][PosEval['SubjectID'] == i][PosEval['TrialID'] == j]) > 1:
            plot_acf(PosEval['FixY'][PosEval['SubjectID'] == i][PosEval['TrialID'] == j])
            plt.show()

# The results show, that the observations of the different sequences are time independent!
# todo plot that nicely for the thesis
########################################################################################################################


########################################################################################################################
# NegEval - FixX
########################################################################################################################
# Same as above, just different variable from different valence dataset
TrialID_NegEval = [6,9,6,7,16,22,9,7,4,4,7,4,3,11]
for i in range(1,15):
    print(i)
    for j in range(1,TrialID_NegEval[i-1]+1):
        print(j)
        if len(NegEval['FixX'][NegEval['SubjectID'] == i][NegEval['TrialID'] == j]) > 1:
            plot_acf(NegEval['FixX'][NegEval['SubjectID'] == i][NegEval['TrialID'] == j])
            plt.show()

########################################################################################################################
# NegEval - FixY
########################################################################################################################
# Same as above, just different variable
for i in range(1,15):
    print(i)
    for j in range(1,TrialID_NegEval[i-1]+1):
        print(j)
        if len(NegEval['FixY'][NegEval['SubjectID'] == i][NegEval['TrialID'] == j]) > 1:
            plot_acf(NegEval['FixY'][NegEval['SubjectID'] == i][NegEval['TrialID'] == j])
            plt.show()

# The results show, that the observations of the different sequences are time independent
# todo plot that nicely for the thesis
########################################################################################################################


########################################################################################################################
########################################################################################################################
# Assumption 2:
# We check if we have variance homogenity of the transition matrices between subjects. To see if we have to use the bartlett
# (sensitive to normal distribution violation) or leneve test we will conduct a test for normal distribution.


########################################################################################################################
# This second assumption can not be examined before the extraction of the HMM parameters. It is
# more an assumption that allows us to estimate the model parameters as we do it. So, we expect the
# assumption to be right, so that we can continue to extract the HMM parameters.
########################################################################################################################



########################################################################################################################
# todo Assumption check for applying the HMM parameters on the LDA algorithm
########################################################################################################################
# The three main assumptions for the Hidden Markov Model parameter to be plugged in
# the LDA Algorithm are,..
# 1: that the HMM variables are normally distributed
# 2: that the variables have variance homogeneity
# 3: that there are no sig. correlations between the HMM variables
########################################################################################################################
########################################################################################################################
# Assumption 1:
########################################################################################################################
# Test for Normal distribution - hmms_posEval
########################################################################################################################

import os
import pandas as pd
os.chdir('C:/Users/olive/OneDrive/Desktop/Master/05_Modelling/HMM Analysis - MATLAB')
# Information about the transformed excel files
hmms_posEval = pd.read_excel('hmms_posEval.xlsx')
hmms_negEval = pd.read_excel('hmms_negEval.xlsx')

from scipy import stats

for column in hmms_posEval:
    print(column)
    k2, p = stats.normaltest(hmms_posEval[column], axis=0)
    alpha = 1e-3
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected")
        print(p)
    else:
        print("The null hypothesis cannot be rejected")
        print(p)
    hmms_posEval[column].hist()
    plt.show()

# H0 rejected for pdf6, pdf10, pdf15, pdf24, pdf28, pdf29, pdf31, pdf32, pdf36 (9/48)
# all others are significantly normal distributed
# todo plot that nicely for the thesis


########################################################################################################################
# Test for Normal distribution - hmms_negEval
########################################################################################################################
for column in hmms_negEval:
    print(column)
    k2, p = stats.normaltest(hmms_negEval[column], axis=0)
    alpha = 1e-3
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected")
        print(p)
    else:
        print("The null hypothesis cannot be rejected")
        print(p)
    hmms_negEval[column].hist()
    plt.show()

# H0 rejected for trans8, pdf3, pdf8, pdf9, pdf11, pdf12, pdf16, pdf17,
# pdf19, pdf21, pdf23, pdf24, pdf27, pdf36 (14/48)
# all others are significantly normal distributed
# todo plot that nicely for the thesis

########################################################################################################################
# On both datasets we have some violations of the normal distribution on different variables
# The LDA algorithm is not very sensitive on that violation, for now we keep it like that
########################################################################################################################


########################################################################################################################
# Assumption 2:
########################################################################################################################
# Variance Homogenity Check
########################################################################################################################
# As we have the violation of normal distribution for many variables, we will take the leneve test to
# check for variance homogenity

########################################################################################################################
# PosEval - Variance Homogenity Check
########################################################################################################################
stat, p = stats.levene(hmms_posEval['prior1'], hmms_posEval['prior2'], hmms_posEval['prior3'],\
                       hmms_posEval['trans1'], hmms_posEval['trans2'], hmms_posEval['trans3'],\
                       hmms_posEval['trans4'], hmms_posEval['trans5'], hmms_posEval['trans6'],\
                       hmms_posEval['trans7'], hmms_posEval['trans8'], hmms_posEval['trans9'],\
                       hmms_posEval['pdf1'], hmms_posEval['pdf2'], hmms_posEval['pdf3'],\
                       hmms_posEval['pdf4'], hmms_posEval['pdf5'], hmms_posEval['pdf6'],\
                       hmms_posEval['pdf7'], hmms_posEval['pdf8'], hmms_posEval['pdf9'],\
                       hmms_posEval['pdf10'], hmms_posEval['pdf11'], hmms_posEval['pdf12'],\
                       hmms_posEval['pdf13'], hmms_posEval['pdf14'], hmms_posEval['pdf15'],\
                       hmms_posEval['pdf16'], hmms_posEval['pdf17'], hmms_posEval['pdf18'],\
                       hmms_posEval['pdf19'], hmms_posEval['pdf20'], hmms_posEval['pdf21'],\
                       hmms_posEval['pdf22'], hmms_posEval['pdf23'], hmms_posEval['pdf24'],\
                       hmms_posEval['pdf25'], hmms_posEval['pdf26'], hmms_posEval['pdf27'],\
                       hmms_posEval['pdf28'], hmms_posEval['pdf29'], hmms_posEval['pdf30'],\
                       hmms_posEval['pdf31'], hmms_posEval['pdf32'], hmms_posEval['pdf33'],\
                       hmms_posEval['pdf34'], hmms_posEval['pdf35'], hmms_posEval['pdf36'])

alpha = 5e-2
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("The null hypothesis can be rejected")
    print(p)
else:
    print("The null hypothesis cannot be rejected")
    print(p)
# 2.1259266908055656e-07 > we cannot hold the H0, so we have statistically sig. equal variances


########################################################################################################################
# NegEval - Variance Homogenity Check
########################################################################################################################
stat, p = stats.levene(hmms_negEval['prior1'], hmms_negEval['prior2'], hmms_negEval['prior3'],\
                       hmms_negEval['trans1'], hmms_negEval['trans2'], hmms_negEval['trans3'],\
                       hmms_negEval['trans4'], hmms_negEval['trans5'], hmms_negEval['trans6'],\
                       hmms_negEval['trans7'], hmms_negEval['trans8'], hmms_negEval['trans9'],\
                       hmms_negEval['pdf1'], hmms_negEval['pdf2'], hmms_negEval['pdf3'],\
                       hmms_negEval['pdf4'], hmms_negEval['pdf5'], hmms_negEval['pdf6'],\
                       hmms_negEval['pdf7'], hmms_negEval['pdf8'], hmms_negEval['pdf9'],\
                       hmms_negEval['pdf10'], hmms_negEval['pdf11'], hmms_negEval['pdf12'],\
                       hmms_negEval['pdf13'], hmms_negEval['pdf14'], hmms_negEval['pdf15'],\
                       hmms_negEval['pdf16'], hmms_negEval['pdf17'], hmms_negEval['pdf18'],\
                       hmms_negEval['pdf19'], hmms_negEval['pdf20'], hmms_negEval['pdf21'],\
                       hmms_negEval['pdf22'], hmms_negEval['pdf23'], hmms_negEval['pdf24'],\
                       hmms_negEval['pdf25'], hmms_negEval['pdf26'], hmms_negEval['pdf27'],\
                       hmms_negEval['pdf28'], hmms_negEval['pdf29'], hmms_negEval['pdf30'],\
                       hmms_negEval['pdf31'], hmms_negEval['pdf32'], hmms_negEval['pdf33'],\
                       hmms_negEval['pdf34'], hmms_negEval['pdf35'], hmms_negEval['pdf36'])

alpha = 5e-2
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("The null hypothesis can be rejected")
    print(p)
else:
    print("The null hypothesis cannot be rejected")
    print(p)
# 2.9139876198385585e-05 > we cannot hold the H0, so we have no statistically sig. equal variances

########################################################################################################################
# The variance homogenity for hmms_posEval can be slightly hold, the one for hmms_negEval not. Still it is said,
# that violation of these assumptions is not too bad for the LDA algorithm. We could standardize the data to get
# that, but then we would have the problem of data leakage, so we would have to split them before standardization.
# If we want to apply PCA, we can do this afterwards, if the assumptions are still not holding.
########################################################################################################################


########################################################################################################################
# Assumption 3:
########################################################################################################################
# Correlation of Variables
########################################################################################################################
# We don't want to have correlation between our variables when using them as features for our LDA algorithm.

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

########################################################################################################################
# hmms_posEval
########################################################################################################################
coorM_hmms_posEval = hmms_posEval.corr()
# Result: We have some high correlations
# todo plot that nicely for the thesis
sn.heatmap(coorM_hmms_posEval, center = 0, linewidth = .5)
plt.show()

########################################################################################################################
# hmms_negEval
########################################################################################################################
coorM_hmms_negEval = hmms_negEval.corr()
# Result: We have some high correlations
# todo plot that nicely for the thesis
sn.heatmap(coorM_hmms_negEval, center = 0, linewidth = .5)
plt.show()


########################################################################################################################
# As we have violations of almost all our assumptions, we will try to transform our variables before we plug them into
# our LDA algorithm. First we try to do is a PCA, so that we loose the correlation between the different features, loose
# also the amount of features and redundancies for lower computational costs.
# If that doesn't solve most of the problems, I will aplly a standardization after splitting the data into training and
# test batches to prevent data leakage, which would result in favor of classification accuracy.
########################################################################################################################

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
########################################################################################################################
# sklearn.decomposition.PCA
from sklearn.decomposition import PCA
import numpy as np
########################################################################################################################
# todo PCA - hmms_posEval
########################################################################################################################
# dimensionality reduction with PCA
pca_hmms_posEval = PCA()
pca_hmms_posEval.fit(hmms_posEval)
print(pca_hmms_posEval.explained_variance_ratio_)
print(pca_hmms_posEval.singular_values_)
# First two explain ~99% of the variance, so we could actually only use these two for the LDA algorithm
########################################################################################################################

########################################################################################################################
# PCA - hmms_negEval
########################################################################################################################
# dimensionality reduction with PCA
pca_hmms_negEval = PCA(n_components=14)
pca_hmms_negEval.fit(np.transpose(hmms_negEval))
print(pca_hmms_negEval.explained_variance_ratio_)
# First two explain 62% of the variance, so we could actually only use these two for the LDA algorithm
########################################################################################################################



########################################################################################################################
# todo Recheck of assumptions after Dimensionality Reduction of our feature space for the LDA algorithm
########################################################################################################################
# The three main assumptions for the Hidden Markov Model parameter to be plugged in
# the LDA Algorithm are,..
# 1: that the HMM variables are normally distributed
# 2: that the variables have variance homogenity
# 3: that there are no sig. correlations between the HMM variables
########################################################################################################################
########################################################################################################################
# Assumption 1:
########################################################################################################################
# Test for Normal distribution - hmms_posEval
########################################################################################################################
for i in range(0,len(pca_hmms_posEval_components.columns)):
    # print(column)
    k2, p = stats.normaltest(pca_hmms_posEval_components.iloc[:,i], axis=0)
    alpha = 1e-3
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected")
        print(p)
    else:
        print("The null hypothesis cannot be rejected")
        print(p)
    pca_hmms_posEval_components.iloc[:,i].hist()
    plt.show()


# H0 rejected for var1, var2, var3 (3/14)
# all others are significantly normal distributed
# todo plot that nicely for the thesis


########################################################################################################################
# Test for Normal distribution - hmms_negEval
########################################################################################################################
for i in range(0,len(pca_hmms_negEval_components.columns)):
    # print(column)
    k2, p = stats.normaltest(pca_hmms_negEval_components.iloc[:,i], axis=0)
    alpha = 1e-3
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected")
        print(p)
    else:
        print("The null hypothesis cannot be rejected")
        print(p)
    pca_hmms_negEval_components.iloc[:,i].hist()
    plt.show()


# H0 rejected for var1, var2, var10 (3/14)
# all others are significantly normal distributed
# todo plot that nicely for the thesis

########################################################################################################################
# On both datasets we still have some violations of the normal distribution on different variables
# The LDA algorithm is not very sensitive on that violation, so we accept it
########################################################################################################################


########################################################################################################################
# Assumption 2:
########################################################################################################################
# Variance Homogenity Check
########################################################################################################################
# As we have the violation of normal distribution for many variables, we will take the leneve test to
# check for variance homogenity

########################################################################################################################
# PosEval - Variance Homogenity Check
########################################################################################################################
stat, p = stats.levene(pca_hmms_posEval_components.iloc[:,0], pca_hmms_posEval_components.iloc[:,1],\
                       pca_hmms_posEval_components.iloc[:,2], pca_hmms_posEval_components.iloc[:,3],\
                       pca_hmms_posEval_components.iloc[:,4], pca_hmms_posEval_components.iloc[:,5],\
                       pca_hmms_posEval_components.iloc[:,6], pca_hmms_posEval_components.iloc[:,7],\
                       pca_hmms_posEval_components.iloc[:,8], pca_hmms_posEval_components.iloc[:,9],\
                       pca_hmms_posEval_components.iloc[:,10], pca_hmms_posEval_components.iloc[:,11],\
                       pca_hmms_posEval_components.iloc[:,12])
# Significance test
alpha = 5e-2
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("The null hypothesis can be rejected")
    print(p)
else:
    print("The null hypothesis cannot be rejected")
    print(p)
# 0.005972285584827235 > we cannot hold the H0, we don't have sig. equal variances


########################################################################################################################
# Same only for the first two components, that explain 98% of the variance
########################################################################################################################
stat, p = stats.levene(pca_hmms_posEval_components.iloc[:,0], pca_hmms_posEval_components.iloc[:,1])
# Significance test
alpha = 5e-2
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("The null hypothesis can be rejected")
    print(p)
else:
    print("The null hypothesis cannot be rejected")
    print(p)
# 0.1753599436095741 > we can hold the H0, so we have statistically sig. equal variances


########################################################################################################################
# NegEval - Variance Homogenity Check
########################################################################################################################
stat, p = stats.levene(pca_hmms_negEval_components.iloc[:,0], pca_hmms_negEval_components.iloc[:,1],\
                       pca_hmms_negEval_components.iloc[:,2], pca_hmms_negEval_components.iloc[:,3],\
                       pca_hmms_negEval_components.iloc[:,4], pca_hmms_negEval_components.iloc[:,5],\
                       pca_hmms_negEval_components.iloc[:,6], pca_hmms_negEval_components.iloc[:,7],\
                       pca_hmms_negEval_components.iloc[:,8], pca_hmms_negEval_components.iloc[:,9],\
                       pca_hmms_negEval_components.iloc[:,10], pca_hmms_negEval_components.iloc[:,11],\
                       pca_hmms_negEval_components.iloc[:,12])
# Significance test
alpha = 5e-2
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("The null hypothesis can be rejected")
    print(p)
else:
    print("The null hypothesis cannot be rejected")
    print(p)
# 0.0017431374521967643 > we cannot hold the H0, so we have no statistically sig. equal variances


########################################################################################################################
# Same only for the first two components, that explain 62% of the variance
########################################################################################################################
stat, p = stats.levene(pca_hmms_negEval_components.iloc[:,0], pca_hmms_negEval_components.iloc[:,1])
# Significance test
alpha = 5e-2
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("The null hypothesis can be rejected")
    print(p)
else:
    print("The null hypothesis cannot be rejected")
    print(p)
# 0.15725308571743282 > we can hold the H0, so we have statistically sig. equal variances

########################################################################################################################
# The variance homogenity for hmms_posEval with reduced dimensionality can be hold, the one for hmms_negEval not.
# If we take only the first two components that explain most variance, we can easily hold it for both.
########################################################################################################################


########################################################################################################################
# Assumption 3:
########################################################################################################################
# Correlation of Variables
########################################################################################################################
# We don't want to have correlation between our variables when using them as features for our LDA algorithm.

########################################################################################################################
# hmms_posEval
########################################################################################################################
coorM_pca_hmms_posEval_components = pca_hmms_posEval_components.corr()
# Result: Perfect decorrelated components
# todo plot that nicely for the thesis
sn.heatmap(coorM_pca_hmms_posEval_components, linewidth = .5)
plt.show()

########################################################################################################################
# hmms_posEval
########################################################################################################################
coorM_pca_hmms_negEval_components = pca_hmms_negEval_components.corr()
# Result: Perfect decorrelated components
# todo plot that nicely for the thesis
sn.heatmap(coorM_pca_hmms_negEval_components, linewidth = .5)
plt.show()


########################################################################################################################
# As expected we have completely decorrelated data after applying PCA on our feature space.
########################################################################################################################




########################################################################################################################
# todo Train and Predict with LDA and reduced component features
########################################################################################################################

########################################################################################################################
# todo Full PCA set - 14 features
########################################################################################################################

# PosEval
# Split the data into training (~80% - 11 samples) and test (~20% - 3 samples) batches
pca_hmms_posEval_components_trainingSet = pca_hmms_posEval_components.sample(frac=0.8)
pca_hmms_posEval_components_testSet = pca_hmms_posEval_components.drop(pca_hmms_posEval_components_trainingSet.index)

# NegEval
# Split the data into training (~80% - 11 samples) and test (~20% - 3 samples) batches
pca_hmms_negEval_components_trainingSet = pca_hmms_negEval_components.sample(frac=0.8)
pca_hmms_negEval_components_testSet = pca_hmms_negEval_components.drop(pca_hmms_negEval_components_trainingSet.index)


import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# function for plotting Kfold
def plot_cv_indices(cv, X, y, group, ax, n_splits, lw=10):
    """Create a sample plot for indices of a cross-validation object."""

    # Generate the training/testing visualizations for each CV split
    for ii, (tr, tt) in enumerate(cv.split(X=X, y=y, groups=group)):
        # Fill in indices with the training/test groups
        indices = np.array([np.nan] * len(X))
        indices[tt] = 1
        indices[tr] = 0

        # Visualize the results
        ax.scatter(
            range(len(indices)),
            [ii + 0.5] * len(indices),
            c=indices,
            marker="_",
            lw=lw,
            cmap=cmap_cv,
            vmin=-0.2,
            vmax=1.2,
        )

    # Plot the data classes and groups at the end
    ax.scatter(
        range(len(X)), [ii + 1.5] * len(X), c=y, marker="_", lw=lw, cmap=cmap_data
    )

    ax.scatter(
        range(len(X)), [ii + 2.5] * len(X), c=group, marker="_", lw=lw, cmap=cmap_data
    )

    # Formatting
    yticklabels = list(range(n_splits))
    ax.set(
        yticks=np.arange(n_splits) + 0.5,
        yticklabels=yticklabels,
        xlabel="Sample index",
        ylabel="CV iteration",
        ylim=[n_splits, -0.2],
        xlim=[0, 28],
    )
    ax.set_title("{}".format(type(cv).__name__), fontsize=15)
    return ax

# constant values for the plotting
cmap_cv = plt.cm.coolwarm
cmap_data = plt.cm.Paired
# Get the groups ndarray
groups = np.arange(14)


# Concatenate evaluation sets
X = np.vstack((np.array(pca_hmms_posEval_components),np.array(pca_hmms_negEval_components)))
# Create according labels
y = np.concatenate((np.zeros(14),np.ones(14)))
#split the dataset into training (70%) and testing (30%) sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
# Choose Learning algorithm
clf = LinearDiscriminantAnalysis()
# Train the model with dataset
clf.fit(X_train, y_train)
# define model evaluation method
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=1)
# evaluate model
scores = cross_val_score(clf, X_test, y_test, scoring='accuracy', cv=cv, n_jobs=-1)
# summarize result
print('Mean Accuracy: %.3f' % (sum(scores)/50))
# plot ten times kFold evaluation
fig, ax = plt.subplots()
plot_cv_indices(cv, X, y, groups, ax, 10)
plt.show()


########################################################################################################################
# todo Accuracy: 0.48
########################################################################################################################


########################################################################################################################
# todo first two features that explain 98% and 62% of variance
########################################################################################################################

# PosEval
# Split the data into training (~80% - 11 samples) and test (~20% - 3 samples) batches
pca_hmms_posEval_components_trainingSet = pca_hmms_posEval_components[[0,1]].sample(frac=0.8)
pca_hmms_posEval_components_testSet = pca_hmms_posEval_components[[0,1]].drop(pca_hmms_posEval_components_trainingSet.index)

# NegEval
# Split the data into training (~80% - 11 samples) and test (~20% - 3 samples) batches
pca_hmms_negEval_components_trainingSet = pca_hmms_negEval_components[[0,1]].sample(frac=0.8)
pca_hmms_negEval_components_testSet = pca_hmms_negEval_components[[0,1]].drop(pca_hmms_negEval_components_trainingSet.index)



# We want some value to rate our model accuracy, possiby with k-fold strategy
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

# Concatenate Training set
X = np.vstack((np.array(pca_hmms_posEval_components[[0,1]]),np.array(pca_hmms_negEval_components[[0,1]])))
# Create according labels
y = np.concatenate((np.zeros(14),np.ones(14)))
#split the dataset into training (70%) and testing (30%) sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
# Choose Learning algorithm
clf = LinearDiscriminantAnalysis()
# Train the model with dataset
clf.fit(X_train, y_train)
# define model evaluation method
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=1)
# evaluate model
scores = cross_val_score(clf, X_test, y_test, scoring='accuracy', cv=cv, n_jobs=-1)
# summarize result
print('Mean Accuracy: %.3f' % (sum(scores)/50))
# plot ten times kFold evaluation
fig, ax = plt.subplots()
plot_cv_indices(cv, X, y, groups, ax, 10)
plt.show()


########################################################################################################################
# todo Accuracy: 0.370
########################################################################################################################


########################################################################################################################
# todo original feature set
########################################################################################################################

# PosEval
# Split the data into training (~80% - 11 samples) and test (~20% - 3 samples) batches
hmms_posEval_trainingSet = hmms_posEval.sample(frac=0.8)
hmms_posEval_testSet = hmms_posEval.drop(hmms_posEval_trainingSet.index)

# NegEval
# Split the data into training (~80% - 11 samples) and test (~20% - 3 samples) batches
hmms_negEval_trainingSet = hmms_negEval.sample(frac=0.8)
hmms_negEval_testSet = hmms_negEval.drop(hmms_negEval_trainingSet.index)


# Concatenate Training set
X = np.vstack((np.array(hmms_posEval),np.array(hmms_negEval)))
# Create according labels
y = np.concatenate((np.zeros(14),np.ones(14)))
#split the dataset into training (70%) and testing (30%) sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
# Choose Learning algorithm
clf = LinearDiscriminantAnalysis()
# Train the model with dataset
clf.fit(X_train, y_train)
# define model evaluation method
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=1)
# evaluate model
scores = cross_val_score(clf, X_test, y_test, scoring='accuracy', cv=cv, n_jobs=-1)
# summarize result
print('Mean Accuracy: %.3f' % (sum(scores)/50))
# plot ten times kFold evaluation
fig, ax = plt.subplots()
plot_cv_indices(cv, X, y, groups, ax, 10)
plt.show()

########################################################################################################################
# todo Accuracy: 0.63
########################################################################################################################

