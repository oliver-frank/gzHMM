# HMM Classification of eye-tracking data to predict an observer's evaluation of a changing VR environment

## Objective:
- Preprocessing of raw eye tracking data into fixation, smooth pursuit and transition features from participants observing a sequentially moving agent in a VR environment
- Modelling HMMs on these preprocessed labeled datasets (goal-directed & non-goal-directed behavior)
- After performance saturation (EM with log loss) HMM model parameters were embedded into PCA spaces and classified (LDA)

## Hierarchy of actions
1. Transformation.py
2. Preprocessing.py
3. HMM.m - modelling
4. LDA.py
5. simulatedPC_visual.py - posthoc visualization


