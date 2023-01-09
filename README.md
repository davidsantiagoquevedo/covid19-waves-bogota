# Comparison between four waves of SARS-CoV-2 in Bogotá: a retrospective analysis over two years

In this repository we characterized and compared, using statistical tools, the first four consecutive epidemiological waves in the Bogotá, Colombia, that occurred between March 2020 and April 2022. We used the report of confirmed cases from the [District Health Secretary of Bogotá](https://datosabiertos.bogota.gov.co/dataset/numero-de-casos-confirmados-por-el-laboratorio-de-covid-19-bogota-d-c) , and the genomic surveillance data published by the [Global Initiative on Sharing All Influenza Data (GISAID)](https://gisaid.org/). We focused mainly on the estimation of:

1. The instantaneous reproduction number R(t).
2. The transmissibility advantage between variants.
3. The delay times for onset-to-hospitalization, onset-to-ICU, onset-to-death, hospital stay, and ICU stay., 
4. The characterization of severe outcomes using the proportion of cases using the general hospital and ICU services, as well, as deaths, and the severe ratios: Case Fatality Rate (CFR), Hospitalization Case Rate (HCR), and Hospitalization Fatality Rate (HFR) for each wave. 

## Data sources

1. Report of confirmed cases from the [District Health Secretary of Bogotá](https://datosabiertos.bogota.gov.co/dataset/numero-de-casos-confirmados-por-el-laboratorio-de-covid-19-bogota-d-c) (Private database - last update: )

2. Genomic surveillance data published by the [Global Initiative on Sharing All Influenza Data (GISAID)](https://gisaid.org/) (Public database - last update: 2022-08-02)

## Methods

1. Reproduction number R(t): we estimated the time-varying instantaneous reproduction number R(t) using the epidemiological package for R: [EpiEstim](https://cran.r-project.org/web/packages/EpiEstim/index.html)

2. Transmissibility advantage: we evaluated the transmissibility advantage using a multinomial logistic regression with a single explanatory variable $t$ given by:

$$f(v,t)=\alpha + \beta_{0,v}t$$

In the previous expression $\alpha$ is the intercept of the model and $\beta_{0,v}$ is the variant-specific parameter for the time covariate, which was computed with respect to a reference (or pivot) variant. Notice that $\beta_{0,v}$ represents the transmissibility advantage with respect to the pivot variant. The relative transmissibility advantages between other variants were computed as:

$$\beta_{w,v} = \beta_{0,w} - \beta_{0,v}$$

The multinomial regressions were run in stan through the library [PyStan](https://pystan.readthedocs.io/en/latest/) for python.

3. Probability distributions of delay times: we used a bayesian hierarchical model based on [this repository](https://github.com/mrc-ide/Brazil_COVID19_distributions). We fitted initial parameters for the district level and the sample the parameters for each wave. For that purpose we used a Hamiltonian Monte Carlo (HMC) algorithm implemented in Stan, setting four chains of 2000 iterations (1000 for warming up and 1000 for sampling). These models were also run using [PyStan](https://pystan.readthedocs.io/en/latest/).

4. Severe outcomes: we computed the proportion of severe outcomes (general hospitalization, ICU, and death) between the Covid-19 cases, with a confidence interval of 95% for binomial proportions; and the Case Fatality Rate (CFR), Hospitalization Case Rate (HCR), and Hospitalization Fatality Rate (HFR) for each wave, disaggregated by 10 years age-groups. Additionally, we calculated the contribution of waves to severe outcomes by age-groups.

## Repository description

All the folders, except [plots](/plots/) and [tables](/tables/), are organized following the same structure: a **scripts** subfolder that contains the necessary codes to run the models and the analysis, and an **outputs** subfolder that contains the results. 

1. The folder [epidemiological_distributions](/epidemiological_distributions/) contains the following scripts:
* The models implemented in stan for the distric level and the partial pooling implemented for the waves ([model_exponential_district.stan](/epidemiological_distributions/scripts/model_exponential_district.stan), [model_gamma_district.stan](/epidemiological_distributions/scripts/model_gamma_district.stan), [model_gln_district.stan](/epidemiological_distributions/scripts/model_gln_district.stan), [model_log_normal_district.stan](/epidemiological_distributions/scripts/model_log_normal_district.stan), [model_weibull_district.stan](/epidemiological_distributions/scripts/model_exponential_district.stan), [model_exponential_pool.stan](/epidemiological_distributions/scripts/model_exponential_pool.stan), [model_gamma_pool.stan](/epidemiological_distributions/scripts/model_gamma_pool.stan), [model_gln_pool.stan](/epidemiological_distributions/scripts/model_gln_pool.stan), [model_log_normal_pool.stan](/epidemiological_distributions/scripts/model_log_normal_pool.stan), [model_weibull_pool.stan](/epidemiological_distributions/scripts/model_exponential_pool.stan))
* The python scripts to run the model and extract the results ([run_exponential.py](/epidemiological_distributions/scripts/run_exponential.py), [run_gamma.py](/epidemiological_distributions/scripts/run_gamma.py), [run_gln.py](/epidemiological_distributions/scripts/run_gln.py), [run_log_normal.py](/epidemiological_distributions/scripts/run_log_normal.py), [run_weibull.py](/epidemiological_distributions/scripts/run_weibull.py)).
* A python script to calculate the bayes factor ([bayes_factor.py](/epidemiological_distributions/scripts/bayes_factors.py)).
* A python script that sumarizes the main results of the bayesian inference ([summarize_results.py](/epidemiological_distributions/scripts/summarize_results.py)).
* A python script with the functions used for preparing and cleaning data, and the statistical tools used in the analysis ([utilities_epi_dist.py](/epidemiological_distributions/scripts/utilities_epi_dist.py)).

2. The folder [genomics](/genomics/) contains the following scripts:
* A set of functions in R to process de genomic data ([genomics_functions.R](/genomics/scripts/genomics_functions.R) and [variants_record](/genomics/scripts/variants_recod.R)) and a python script to generate the necessary inputs for the model ([process_data.py](/genomics/scripts/process_data.py)).
* The multinomial model implemented in stan ([multinomial_model.stan](/genomics/scripts/multinomial_model.stan)) and the python script to run this model ([run_model.py](/genomics/scripts/run_model.py)).
* A python script to process the results from the multinomial model ([process_results](/genomics/scripts/process_results.py)).

3. The folder [rt](/rt/) contains the following script:
* An R script to estimate the Reproduction number using EpiEstim ([rt.R](/rt/scripts/rt.R))

4. The folder [severe_outcomes](/severe_outcomes/) contains the following scripts:
* A python script to calculate the percentages ([percentages.py](/severe_outcomes/scripts/percentages.py)).
* A python script to calculate the binomial proportions ([proportions.py](/severe_outcomes/scripts/proportions.py)).
* A python script to calculate the CFR, HCR, ICU-CR, HFR and ICU-FR ([rates.py](/severe_outcomes/scripts/rates.py)).
* A python script with the tools used in the analysis ([utilities_severity.py](/severe_outcomes/scripts/utilities_severity.py)).

5. The folder [waves](/waves/) contains the following scripts:
* A python script to find the roots of the epidemic curve using gaussian smoothing and interpolation ([roots_confirmed_cases.py](/waves/scripts/roots_confirmed_cases.py)).
* A python script to process the waves after visual inspection of the roots ([roots_confirmed_cases.py](/waves/scripts/roots_confirmed_cases.py)).
* A python script with the tools used in the analysis ([utilities_waves.py](/waves/scripts/utilities_waves.py)).

6. The folder [tables](/tables/) contains the following scripts:
* The python scripts to generate the tables of the supplementary materials included in the paper ([table_s1.py](/tables/table_s1.py), [table_s2.py](/tables/table_s2.py), [table_s4.py](/tables/table_s4.py), [table_s5.py](/tables/table_s5.py)). This scripts are usually importing and calling functions from the utilities of each section and results contained in the corresponding outputs subfolder.

7. The folder [plots](/tables/) contains the following scripts:
* A script with the customized style used to generate all the figures in python ([plot_style.mplstyle](/plots/plot_style.mplstyle)).
* The python scripts to generate the figures included in the main document ([figure_1.py](/plots/figure_1.py), [figure_2.py](/plots/figure_2.py), [figure_3.py](/plots/figure_3.py), [figure_4.py](/plots/figure_4.py), [figure_5.py](/plots/figure_5.py)).
* A python script to generate the individual plots included in the supplementary materials and some visualizations of the analysis ([individual_plots.py](/plots/individual_plots.py)).
* The scripts with the visualization functions related to every section of the analysis ([overview.py](/plots/overview.py), [results_epidemiological_distributions.py](/plots/results_epidemiological_distributions.py), [results_genomics.py](/plots/results_genomics.py), [results_rt.py](/plots/results_rt.py), [results_severe_outcomes.py](/plots/results_severe_outcomes.py), [results_waves.py](/plots/results_waves.py)).

### Config file
This [YAML file](/config.yml) contains information about the models, the paths used in the scripts and the roots selected for the waves. It called in the beginning of all the scripts.

## Authors and contributors
[davidsantiagoquevedo](https://github.com/davidsantiagoquevedo/), [ntorresd](https://github.com/ntorresd/), [cwhittaker1000](https://github.com/cwhittaker1000/)




