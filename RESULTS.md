# Results

## Noise robustness

The values below are five-fold means. Macro-F1 is averaged across the five outer test folds so the three solutions use the same aggregation rule.

| Condition | MFCC + SVM accuracy | CNN accuracy | YAMNet + SVM accuracy | MFCC + SVM macro-F1 | CNN macro-F1 | YAMNet + SVM macro-F1 |
|---|---:|---:|---:|---:|---:|---:|
| Clean | 0.5270 | 0.6245 | **0.8230** | 0.5180 | 0.6065 | **0.8218** |
| 20 dB | 0.3410 | 0.3660 | **0.6340** | 0.3126 | 0.3322 | **0.6255** |
| 10 dB | 0.1975 | 0.2015 | **0.4085** | 0.1591 | 0.1728 | **0.3917** |
| 5 dB | 0.1125 | 0.1110 | **0.2605** | 0.0791 | 0.0888 | **0.2476** |
| 0 dB | 0.0475 | 0.0445 | **0.1185** | 0.0229 | 0.0230 | **0.1047** |

## Model configurations

### Solution 1  MFCC and SVM

- Twenty MFCCs plus delta and delta-delta coefficients
- Mean and standard deviation summaries producing 120 features
- Fold-local ANOVA `SelectKBest`; 80 features selected in every fold
- Nested three-fold grid search for RBF SVM hyperparameters
- Clean accuracy: 0.5270

### Solution 2  Spectrogram CNN

- Complete five-second recordings represented as 64 by 256 log-mel spectrograms
- Four convolutional blocks with 401,170 trainable parameters
- Training-only time shifts, time masks, frequency masks, and Gaussian perturbation
- Validation-selected training duration of 39 or 40 epochs followed by final retraining on all non-test folds
- Clean accuracy: 0.6245

### Solution 3  YAMNet embeddings and SVM

- Frozen YAMNet feature extractor pretrained externally on AudioSet
- Mean-pooled 1,024-dimensional embeddings
- Fold-local `SelectKBest` retaining 256 dimensions
- Standardization and a three-fold tuned RBF SVM
- Clean accuracy: 0.8230

## Computational measurements

| Model | Mean recorded fold time | Five-fold total | Recorded scope |
|---|---:|---:|---|
| MFCC + SVM | 17.145 s | 85.727 s | Feature selection, SVM tuning, and clean-fold prediction |
| Spectrogram CNN | 946.108 s | 4,730.539 s | Validation selection, final retraining, and clean-fold prediction |
| YAMNet + SVM | 137.598 s | 687.989 s | Standardization, feature selection, grid search, and refit |

The timing scopes and execution environments differ and should not be treated as a controlled hardware benchmark. Feature extraction was excluded from the table. YAMNet embedding extraction was recorded separately as 1.66 minutes for all 2,000 clips across the five conditions.

## Class-level findings

- YAMNet with SVM achieved the highest clean-audio F1 score in 47 of 50 classes.
- The CNN remained best for `door_wood_knock` and `mouse_click`.
- MFCC with SVM remained best for `airplane`.
- Under 0 dB noise, all models collapsed toward a small set of predicted classes. The `rain` class received approximately 71% of MFCC predictions, 73% of CNN predictions, and 52% of YAMNet predictions.

## Interpretation

External AudioSet pretraining transferred useful acoustic structure and produced the strongest model at every SNR. Nevertheless, YAMNet accuracy fell from 82.30% on clean recordings to 11.85% at 0 dB, retaining only 14.4% of its clean accuracy. Pretraining improved relative robustness but did not provide noise immunity.

Future work should evaluate training with real background recordings, reverberation, microphone and room changes, codec artifacts, and domain-adaptation methods rather than generalizing from additive Gaussian noise alone.

