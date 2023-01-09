// Created on Fri Oct 21 2022
// @author: cwhittaker1000
data {
  int<lower=0> K; // number of different lineage categories
  int<lower=0> N; // number of unique sampling timepoints
  int y[N, K]; // the responses (i.e. matrix where each column is total number of each lineage sampled at each timepoint, which are the rows)
               // note that the first column should be the reference lineage you want to compare to.
  vector[N] time; // the covariate (time) - scale this to be between 0 and 1 -> so max timepoint = 1
}

parameters {
  vector[K-1] alpha_raw; // lineage-specific parameter for intercept
  vector[K-1] beta_raw; // lineage-specific parameter for time-coefficient
}

transformed parameters {
  vector[K] alpha = to_vector(append_col(0.0, to_row_vector(alpha_raw))); // we set parameters for reference lineage to 0, as we're dealing with relative growth rates
  vector[K] beta = to_vector(append_col(0.0, to_row_vector(beta_raw))); // we set parameters for reference lineage to 0, as we're dealing with relative growth rates
  matrix[N, K] theta;
  for (i in 1:N) {
    theta[i, ] = to_row_vector(softmax(alpha + beta * time[i])); // softmax imposes a sum-to-one constraint (required as we're dealing with probabilities)
  }
}

model { 
  alpha ~ normal(0, 50);
  beta ~ normal(0, 50);
  for (n in 1:N) {
    target += multinomial_lpmf(y[n, ] | to_vector(theta[n, ]));
  }
}

