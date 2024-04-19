# -*- coding: utf-8 -*-
"""This code computes the coefficient of variation (CV) and some other stats for small samples (indicated by the * added to CV)
for a given set of measurements which are assumed to be for the same or similar object, using the same measurand.
Stats are adjusted for small sample size. Paper ref: Belz, Popovic & Mille (2022) Quantified Reproducibility Assessment of NLP Results,
ACL'22.

In this self-contained version, the set of measurements on which CV is computed is assigned to the variable set_of_set_of_measurements
(see examples in code below).

The reproducibility stats reported in the output are:
* the unbiased coefficient of variation
* the sample mean
* the unbiased sample standard deviation with 95% confidence intervals, estimated on the basis of the standard error of the unbiassed sample variance
* the sample size
* the percentage of measured valued within two standard deviations
* the percentage of measured valued within one standard deviation

Example narrative output:

The unbiased coefficient of variation is 1.5616560359100269 \
for a mean of 85.58285714285714 , \
unbiased sample standard deviation of 1.2904233075765223 with 95\% CI (0.4514829817654973, 2.1293636333875474) ,\
and a sample size of 7 . \
100.0 % of measured values fall within two standard deviations. \
71.429 % of measured values fall within one standard deviation.

NOTE:
* CV assumes all measurements are positive; if they're not, shift measurement scale to start at 0
* for fair comparison across studies, measurements on a scale that doesn't start at 0 need to be shifted to a scale that does start at 0

KNOWN ISSUES:

none
"""

import math
import numpy as np
from scipy.stats import t

# Configuration
from scipy.stats import pearsonr
from scipy.stats import spearmanr

# Correlations (always your Table 1 vs Table 3)
# w/ biased labeler
readability_original = [4.71, 4.08, 4.95]
readability_yours    = [4.52, 4.17, 4.71]
# Ours         => 4.10468050521186
# PAQ Baseline => 2.1752842715658565
# Groundtruth  => 4.954063558431569

relevancy_q_original = [4.39, 4.18, 4.92]
relevancy_q_yours    = [3.83, 3.61, 4.71]
# Ours         => 13.584500317159053
# PAQ Baseline => 14.590321333673446
# Groundtruth  => 4.348309680959793

relevancy_a_original = [3.99, 3.90, 4.83]
relevancy_a_yours    = [3.20, 3.20, 4.46]
# Ours         => 21.909156606290367
# PAQ Baseline => 19.659259261804127
# Groundtruth  => 11.022169047716464


# w/o biased labeler
readability_original = [4.71, 4.08, 4.95]
readability_yours    = [4.52, 4.13, 4.67]
# Ours         => 4.10468050521186
# PAQ Baseline => 1.2143791609431778
# Groundtruth  => 5.8037730045243014

relevancy_q_original = [4.39, 4.18, 4.92]
relevancy_q_yours    = [3.92, 3.62, 4.77]
# Ours         => 11.277797517043215
# PAQ Baseline => 14.315973411159922
# Groundtruth  => 3.086703687722461

relevancy_a_original = [3.99, 3.90, 4.83]
relevancy_a_yours    = [3.39, 3.42, 4.58]
# Ours         => 16.211468148526055
# PAQ Baseline => 13.07547922799151
# Groundtruth  => 5.2975839061336485


def print_stats(measurement_name, original, yours):
    print("-----------------")
    print(measurement_name)
    set_of_set_of_measurements = np.array([original, yours]).T
    pearson   = pearsonr(original, yours).statistic
    pearson_p = pearsonr(original, yours).pvalue
    spearman   = spearmanr(original, yours).statistic
    spearman_p = spearmanr(original, yours).pvalue
    print(f"Pearson correlation coefficient: {pearson}, p-value: {pearson_p}")
    print(f"Spearman correlation coefficient: {spearman}, p-value: {spearman_p}")

    # CV* (always your Table 1 vs Table 3)
    #set_of_set_of_measurements = [
    #    # Readability
    #    [4.71, 4.52], # Ours => 4.10468050521186
    #    [4.08, 4.17], # PAQ Baseline => 2.1752842715658565
    #    [4.95, 4.71], # Groundtruth => 4.954063558431569
    #]
    # End Configuration, the rest of the script calcualtes CV*
    # Other quality criteria are just done in the same way.



    for set_of_measurements in set_of_set_of_measurements:
      print(" ")
      if len(set_of_measurements) < 2:
        print(set_of_measurements, ": set of measurements is smaller than 2")
        break

      sample_mean = np.mean(set_of_measurements)
      if sample_mean <= 0:
        print(set_of_measurements, ": mean is 0 or negative")
        break

      sample_size = len(set_of_measurements)
      degrees_of_freedom = sample_size-1
      sum_of_squared_differences = np.sum(np.square(sample_mean-set_of_measurements))

      # unbiassed sample variance s^2
      unbiassed_sample_variance = sum_of_squared_differences/degrees_of_freedom
      # corrected sample standard deviation s
      corrected_sample_standard_deviation = np.sqrt(unbiassed_sample_variance)
      # Gamma(N/2)
      gamma_N_over_2 = math.gamma(sample_size/2)
      # Gamma((N-1)/2)
      gamma_df_over_2 = math.gamma(degrees_of_freedom/2)
      # c_4(N)
      c_4_N = math.sqrt(2/degrees_of_freedom)*gamma_N_over_2/gamma_df_over_2
      # unbiassed sample std dev s/c_4
      unbiassed_sample_std_dev_s_c_4 = corrected_sample_standard_deviation/c_4_N
      # standard error of the unbiassed sample variance (assumes normally distributed population)
      standard_error_of_unbiassed_sample_variance = unbiassed_sample_variance*np.sqrt(2/degrees_of_freedom)
      # estimated std err of std dev based on std err of unbiassed sample variance
      est_SE_of_SD_based_on_SE_of_unbiassed_sample_variance = standard_error_of_unbiassed_sample_variance/(2*unbiassed_sample_std_dev_s_c_4)

      # COEFFICIENT OF VARIATION CV
      coefficient_of_variation = (unbiassed_sample_std_dev_s_c_4/sample_mean)*100
      # SMALL SAMPLE CORRECTED COEFFICIENT OF VARIATION CV*
      small_sample_coefficient_of_variation = (1+(1/(4*sample_size)))*coefficient_of_variation

      # compute percentage of measured values within 1 and 2 standard deviations from the mean
      # initialise counts
      count_within_1_sd = 0
      count_within_2_sd = 0
      # for each measured value
      for m in set_of_measurements:
        # if it's within two std devs, increment count_within_2_sd
        if np.abs(m-sample_mean) < 2*unbiassed_sample_std_dev_s_c_4:
          count_within_2_sd += 1
          #if it's also within one std devs, increment count_within_1_sd
          if np.abs(m-sample_mean) < unbiassed_sample_std_dev_s_c_4:
            count_within_1_sd += 1

      # report results as described in code description above
      print("The unbiased coefficient of variation is",small_sample_coefficient_of_variation)
      print("for a mean of",sample_mean,", ")
      print("unbiased sample standard deviation of",unbiassed_sample_std_dev_s_c_4,", with 95\% CI",t.interval(0.95, degrees_of_freedom, loc=unbiassed_sample_std_dev_s_c_4, scale=est_SE_of_SD_based_on_SE_of_unbiassed_sample_variance),",")
      print("and a sample size of",sample_size,".")
      print(count_within_2_sd/sample_size*100,"% of measured values fall within two standard deviations.")
      print(round(count_within_1_sd/sample_size*100, 3),"% of measured values fall within one standard deviation.", )
    print("\n\n")


print_stats("Readability", readability_original, readability_yours)
print_stats("Question relevancy", relevancy_q_original, relevancy_q_yours)
print_stats("Answer relevancy", relevancy_a_original, relevancy_a_yours)
