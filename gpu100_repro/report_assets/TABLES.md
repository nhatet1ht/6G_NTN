# Auto-generated report assets (GPU / 100-agent round)

### g100_ilcho_linear (3000 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  199.392 |  491.741 |
| ho       |    2.671 |    4.313 |
| hof      |   63.981 |   17.483 |
| se       |    2.077 |    2.413 |


![g100_ilcho_linear](report_assets/g100_ilcho_linear_training_curves.png)

### g100_ilcho_sigmoid (4000 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  -83.904 |  168.424 |
| ho       |    2.699 |    4.322 |
| hof      |   63.404 |   17.629 |
| se       |    2.082 |    2.411 |


![g100_ilcho_sigmoid](report_assets/g100_ilcho_sigmoid_training_curves.png)

### g100_lbsh (3000 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  230.504 |  543.200 |
| ho       |    2.958 |    4.086 |
| hof      |   61.662 |   16.679 |
| se       |    2.094 |    2.414 |


![g100_lbsh](report_assets/g100_lbsh_training_curves.png)

### g100_eval_hybrid - `hybrid`, 3 ep/point x 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |   11.244 |   11.022 |   11.603 |    9.695 |    7.816 |
| ILCHO-lin  |   11.378 |   10.806 |   10.369 |    9.284 |    6.737 |
| MD-CHO     |   15.467 |   11.811 |    4.397 |    0.081 |    0.000 |
| MVT-CHO    |    5.533 |    4.756 |    3.264 |    1.816 |    1.330 |
| HSNF       |   16.467 |   13.144 |   11.361 |   10.106 |   11.306 |
| LBSH       |   13.222 |   13.439 |   13.211 |   12.189 |   10.244 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.339 |    1.544 |    4.816 |    5.677 |
| ILCHO-lin  |    0.022 |    0.700 |    1.994 |    4.483 |    5.901 |
| MD-CHO     |    0.000 |   32.467 |   64.169 |   90.040 |   98.794 |
| MVT-CHO    |    0.022 |    6.333 |   16.428 |   20.525 |   22.091 |
| HSNF       |    0.022 |    0.022 |    0.028 |    0.016 |    0.080 |
| LBSH       |    0.067 |    0.150 |    0.864 |    1.846 |    3.568 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    2.776 |    2.687 |    2.553 |    2.490 |    2.453 |
| ILCHO-lin  |    2.870 |    2.798 |    2.631 |    2.512 |    2.479 |
| MD-CHO     |    3.427 |    2.956 |    2.418 |    1.973 |    1.786 |
| MVT-CHO    |    2.284 |    2.221 |    2.104 |    2.202 |    2.235 |
| HSNF       |    3.422 |    3.328 |    3.106 |    2.806 |    2.600 |
| LBSH       |    2.391 |    2.354 |    2.344 |    2.350 |    2.357 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.999 |    0.998 |    0.997 |    0.997 |    0.996 |
| ILCHO-lin  |    0.999 |    0.997 |    0.997 |    0.997 |    0.996 |
| MD-CHO     |    0.999 |    0.975 |    0.977 |    0.971 |    0.978 |
| MVT-CHO    |    0.999 |    0.996 |    0.990 |    0.985 |    0.983 |
| HSNF       |    0.999 |    0.998 |    0.998 |    0.993 |    0.992 |
| LBSH       |    0.997 |    0.997 |    0.997 |    0.997 |    0.996 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.005 |    0.038 |    0.085 |    0.146 |    0.183 |
| ILCHO-lin  |    0.005 |    0.039 |    0.088 |    0.146 |    0.192 |
| MD-CHO     |    0.010 |    0.063 |    0.126 |    0.184 |    0.208 |
| MVT-CHO    |    0.009 |    0.059 |    0.119 |    0.175 |    0.205 |
| HSNF       |    0.010 |    0.063 |    0.119 |    0.175 |    0.189 |
| LBSH       |    0.004 |    0.027 |    0.060 |    0.113 |    0.158 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.001 |    0.005 |    0.016 |    0.019 |
| ILCHO-lin  |    0.000 |    0.002 |    0.007 |    0.015 |    0.019 |
| MD-CHO     |    0.000 |    0.108 |    0.213 |    0.298 |    0.327 |
| MVT-CHO    |    0.000 |    0.021 |    0.054 |    0.068 |    0.073 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| LBSH       |    0.000 |    0.000 |    0.003 |    0.006 |    0.012 |


![fig_fairness_cdf.png](report_assets/g100_eval_hybrid_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/g100_eval_hybrid_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/g100_eval_hybrid_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/g100_eval_hybrid_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/g100_eval_hybrid_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/g100_eval_hybrid_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/g100_eval_hybrid_fig_se_vs_ue.png)

### g100_eval_oneweb_phase_1 - `oneweb_phase_1`, 3 ep/point x 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    2.244 |    1.894 |    1.394 |    0.151 |    0.192 |
| ILCHO-lin  |    3.667 |    2.856 |    1.444 |    0.163 |    0.230 |
| MD-CHO     |    7.089 |    2.239 |    0.000 |    0.000 |    0.000 |
| MVT-CHO    |    3.800 |    1.689 |    0.614 |    0.238 |    0.169 |
| HSNF       |    7.067 |    3.156 |    1.442 |    1.249 |    1.032 |
| LBSH       |    1.689 |    1.389 |    0.942 |    2.016 |    1.886 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    2.972 |    1.597 |  173.829 |  287.480 |
| ILCHO-lin  |    0.000 |    4.333 |    1.483 |  169.432 |  283.320 |
| MD-CHO     |    0.000 |   54.150 |   85.794 |  224.163 |  324.487 |
| MVT-CHO    |    0.000 |   26.272 |   43.517 |  198.533 |  307.241 |
| HSNF       |    0.000 |    0.000 |    0.053 |  154.659 |  273.340 |
| LBSH       |    0.000 |    0.272 |    0.556 |  153.116 |  273.704 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.755 |    0.761 |    0.735 |    0.465 |    0.332 |
| ILCHO-lin  |    0.789 |    0.763 |    0.734 |    0.469 |    0.336 |
| MD-CHO     |    0.975 |    0.729 |    0.549 |    0.359 |    0.257 |
| MVT-CHO    |    0.878 |    0.743 |    0.646 |    0.412 |    0.294 |
| HSNF       |    0.976 |    0.904 |    0.739 |    0.485 |    0.349 |
| LBSH       |    0.726 |    0.710 |    0.725 |    0.486 |    0.349 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.999 |    0.996 |    0.996 |    0.851 |    0.659 |
| ILCHO-lin  |    0.995 |    0.994 |    0.996 |    0.846 |    0.656 |
| MD-CHO     |    1.000 |    0.985 |    0.989 |    0.838 |    0.650 |
| MVT-CHO    |    0.999 |    0.994 |    0.994 |    0.836 |    0.650 |
| HSNF       |    1.000 |    0.999 |    0.996 |    0.856 |    0.680 |
| LBSH       |    0.997 |    0.994 |    0.996 |    0.855 |    0.666 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.041 |    0.162 |    0.191 |    0.068 |    0.049 |
| ILCHO-lin  |    0.027 |    0.158 |    0.196 |    0.069 |    0.048 |
| MD-CHO     |    0.046 |    0.175 |    0.191 |    0.063 |    0.053 |
| MVT-CHO    |    0.041 |    0.169 |    0.195 |    0.067 |    0.051 |
| HSNF       |    0.045 |    0.189 |    0.196 |    0.071 |    0.051 |
| LBSH       |    0.041 |    0.139 |    0.181 |    0.064 |    0.052 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.010 |    0.005 |    0.319 |    0.504 |
| ILCHO-lin  |    0.000 |    0.014 |    0.005 |    0.307 |    0.492 |
| MD-CHO     |    0.000 |    0.180 |    0.285 |    0.488 |    0.626 |
| MVT-CHO    |    0.000 |    0.087 |    0.145 |    0.405 |    0.568 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.261 |    0.459 |
| LBSH       |    0.000 |    0.001 |    0.002 |    0.259 |    0.459 |


![fig_fairness_cdf.png](report_assets/g100_eval_oneweb_phase_1_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/g100_eval_oneweb_phase_1_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/g100_eval_oneweb_phase_1_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/g100_eval_oneweb_phase_1_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/g100_eval_oneweb_phase_1_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/g100_eval_oneweb_phase_1_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/g100_eval_oneweb_phase_1_fig_se_vs_ue.png)

### g100_eval_starlink_phase_1a - `starlink_phase_1a`, 3 ep/point x 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    5.222 |    5.733 |    5.653 |    2.902 |    2.331 |
| ILCHO-lin  |    6.933 |    6.239 |    5.503 |    2.502 |    1.536 |
| MD-CHO     |   11.178 |    4.817 |    0.261 |    0.000 |    0.000 |
| MVT-CHO    |    5.111 |    3.600 |    2.183 |    1.203 |    0.942 |
| HSNF       |   10.822 |    7.361 |    6.631 |    3.046 |    1.602 |
| LBSH       |    5.489 |    5.411 |    4.728 |    3.268 |    3.453 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.022 |    0.461 |    1.989 |   24.014 |  136.178 |
| ILCHO-lin  |    0.022 |    1.161 |    2.156 |   23.946 |  138.750 |
| MD-CHO     |    0.044 |   52.239 |   85.358 |  115.176 |  208.133 |
| MVT-CHO    |    0.000 |   10.850 |   25.761 |   58.997 |  165.529 |
| HSNF       |    0.022 |    0.011 |    0.014 |   17.006 |  130.381 |
| LBSH       |    0.178 |    0.200 |    0.611 |   15.857 |  127.916 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    1.919 |    1.769 |    1.635 |    1.479 |    1.152 |
| ILCHO-lin  |    1.931 |    1.775 |    1.650 |    1.488 |    1.148 |
| MD-CHO     |    2.220 |    1.683 |    1.300 |    1.060 |    0.825 |
| MVT-CHO    |    1.959 |    1.863 |    1.632 |    1.341 |    1.037 |
| HSNF       |    2.213 |    2.048 |    1.827 |    1.516 |    1.173 |
| LBSH       |    1.567 |    1.570 |    1.585 |    1.511 |    1.182 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.998 |    0.995 |    0.994 |    0.986 |    0.894 |
| ILCHO-lin  |    0.997 |    0.997 |    0.995 |    0.983 |    0.900 |
| MD-CHO     |    0.999 |    0.984 |    0.977 |    0.963 |    0.875 |
| MVT-CHO    |    0.999 |    0.997 |    0.996 |    0.972 |    0.870 |
| HSNF       |    0.999 |    0.998 |    0.996 |    0.985 |    0.897 |
| LBSH       |    0.997 |    0.994 |    0.995 |    0.989 |    0.903 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.018 |    0.089 |    0.138 |    0.120 |    0.070 |
| ILCHO-lin  |    0.018 |    0.099 |    0.145 |    0.125 |    0.069 |
| MD-CHO     |    0.030 |    0.144 |    0.203 |    0.129 |    0.074 |
| MVT-CHO    |    0.024 |    0.129 |    0.206 |    0.131 |    0.073 |
| HSNF       |    0.029 |    0.144 |    0.199 |    0.127 |    0.075 |
| LBSH       |    0.016 |    0.073 |    0.123 |    0.121 |    0.072 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.002 |    0.007 |    0.055 |    0.247 |
| ILCHO-lin  |    0.000 |    0.004 |    0.007 |    0.054 |    0.252 |
| MD-CHO     |    0.000 |    0.174 |    0.283 |    0.351 |    0.480 |
| MVT-CHO    |    0.000 |    0.036 |    0.085 |    0.166 |    0.338 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.032 |    0.226 |
| LBSH       |    0.001 |    0.001 |    0.002 |    0.030 |    0.221 |


![fig_fairness_cdf.png](report_assets/g100_eval_starlink_phase_1a_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/g100_eval_starlink_phase_1a_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/g100_eval_starlink_phase_1a_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/g100_eval_starlink_phase_1a_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/g100_eval_starlink_phase_1a_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/g100_eval_starlink_phase_1a_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/g100_eval_starlink_phase_1a_fig_se_vs_ue.png)

### g100_eval_starlink_phase_2a - `starlink_phase_2a`, 3 ep/point x 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |   10.400 |   10.100 |   10.400 |    7.616 |    4.256 |
| ILCHO-lin  |   12.022 |   10.856 |   10.144 |    7.490 |    4.179 |
| MD-CHO     |   15.467 |   11.811 |    4.397 |    0.067 |    0.000 |
| MVT-CHO    |    6.933 |    6.422 |    5.169 |    3.483 |    2.412 |
| HSNF       |   16.489 |   13.117 |   11.317 |    9.887 |    5.543 |
| LBSH       |    9.556 |    9.722 |    8.642 |    6.875 |    3.941 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.022 |    0.244 |    1.497 |    3.056 |    4.952 |
| ILCHO-lin  |    0.000 |    1.528 |    1.347 |    2.479 |    4.611 |
| MD-CHO     |    0.000 |   32.467 |   64.169 |   90.116 |  100.587 |
| MVT-CHO    |    0.022 |    3.972 |    9.664 |   20.979 |   30.552 |
| HSNF       |    0.022 |    0.022 |    0.025 |    0.040 |    3.368 |
| LBSH       |    0.022 |    0.200 |    0.950 |    1.722 |    3.279 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    2.934 |    2.837 |    2.666 |    2.533 |    2.498 |
| ILCHO-lin  |    3.036 |    2.877 |    2.625 |    2.512 |    2.501 |
| MD-CHO     |    3.427 |    2.956 |    2.418 |    1.976 |    1.770 |
| MVT-CHO    |    3.019 |    2.981 |    2.861 |    2.582 |    2.353 |
| HSNF       |    3.423 |    3.329 |    3.104 |    2.805 |    2.554 |
| LBSH       |    2.438 |    2.375 |    2.402 |    2.473 |    2.503 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.998 |    0.998 |    0.997 |    0.996 |    0.995 |
| ILCHO-lin  |    0.996 |    0.996 |    0.995 |    0.994 |    0.995 |
| MD-CHO     |    0.999 |    0.975 |    0.977 |    0.969 |    0.974 |
| MVT-CHO    |    0.997 |    0.997 |    0.997 |    0.995 |    0.980 |
| HSNF       |    0.999 |    0.998 |    0.998 |    0.993 |    0.992 |
| LBSH       |    0.993 |    0.992 |    0.992 |    0.994 |    0.994 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.008 |    0.059 |    0.111 |    0.143 |    0.141 |
| ILCHO-lin  |    0.011 |    0.062 |    0.095 |    0.138 |    0.142 |
| MD-CHO     |    0.016 |    0.094 |    0.173 |    0.204 |    0.150 |
| MVT-CHO    |    0.009 |    0.079 |    0.153 |    0.195 |    0.148 |
| HSNF       |    0.016 |    0.094 |    0.160 |    0.188 |    0.142 |
| LBSH       |    0.008 |    0.044 |    0.091 |    0.137 |    0.142 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.001 |    0.005 |    0.010 |    0.016 |
| ILCHO-lin  |    0.000 |    0.005 |    0.004 |    0.008 |    0.015 |
| MD-CHO     |    0.000 |    0.108 |    0.213 |    0.298 |    0.332 |
| MVT-CHO    |    0.000 |    0.013 |    0.032 |    0.069 |    0.099 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.010 |
| LBSH       |    0.000 |    0.001 |    0.003 |    0.006 |    0.011 |


![fig_fairness_cdf.png](report_assets/g100_eval_starlink_phase_2a_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/g100_eval_starlink_phase_2a_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/g100_eval_starlink_phase_2a_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/g100_eval_starlink_phase_2a_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/g100_eval_starlink_phase_2a_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/g100_eval_starlink_phase_2a_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/g100_eval_starlink_phase_2a_fig_se_vs_ue.png)

### g100_reward_ablation - `starlink_phase_2a`, 3 ep/point x 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |   10.400 |   10.100 |   10.400 |    7.616 |    4.256 |
| ILCHO-lin  |   12.022 |   10.856 |   10.144 |    7.490 |    4.179 |
| MD-CHO     |   15.467 |   11.811 |    4.397 |    0.067 |    0.000 |
| MVT-CHO    |    6.933 |    6.422 |    5.169 |    3.483 |    2.412 |
| HSNF       |   16.489 |   13.117 |   11.317 |    9.887 |    5.543 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.022 |    0.244 |    1.497 |    3.056 |    4.952 |
| ILCHO-lin  |    0.000 |    1.528 |    1.347 |    2.479 |    4.611 |
| MD-CHO     |    0.000 |   32.467 |   64.169 |   90.116 |  100.587 |
| MVT-CHO    |    0.022 |    3.972 |    9.664 |   20.979 |   30.552 |
| HSNF       |    0.022 |    0.022 |    0.025 |    0.040 |    3.368 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    2.934 |    2.837 |    2.666 |    2.533 |    2.498 |
| ILCHO-lin  |    3.036 |    2.877 |    2.625 |    2.512 |    2.501 |
| MD-CHO     |    3.427 |    2.956 |    2.418 |    1.976 |    1.770 |
| MVT-CHO    |    3.019 |    2.981 |    2.861 |    2.582 |    2.353 |
| HSNF       |    3.423 |    3.329 |    3.104 |    2.805 |    2.554 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.998 |    0.998 |    0.997 |    0.996 |    0.995 |
| ILCHO-lin  |    0.996 |    0.996 |    0.995 |    0.994 |    0.995 |
| MD-CHO     |    0.999 |    0.975 |    0.977 |    0.969 |    0.974 |
| MVT-CHO    |    0.997 |    0.997 |    0.997 |    0.995 |    0.980 |
| HSNF       |    0.999 |    0.998 |    0.998 |    0.993 |    0.992 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.008 |    0.059 |    0.111 |    0.143 |    0.141 |
| ILCHO-lin  |    0.011 |    0.062 |    0.095 |    0.138 |    0.142 |
| MD-CHO     |    0.016 |    0.094 |    0.173 |    0.204 |    0.150 |
| MVT-CHO    |    0.009 |    0.079 |    0.153 |    0.195 |    0.148 |
| HSNF       |    0.016 |    0.094 |    0.160 |    0.188 |    0.142 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.001 |    0.005 |    0.010 |    0.016 |
| ILCHO-lin  |    0.000 |    0.005 |    0.004 |    0.008 |    0.015 |
| MD-CHO     |    0.000 |    0.108 |    0.213 |    0.298 |    0.332 |
| MVT-CHO    |    0.000 |    0.013 |    0.032 |    0.069 |    0.099 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.010 |


![fig_fairness_cdf.png](report_assets/g100_reward_ablation_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/g100_reward_ablation_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/g100_reward_ablation_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/g100_reward_ablation_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/g100_reward_ablation_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/g100_reward_ablation_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/g100_reward_ablation_fig_se_vs_ue.png)


### analysis


![fig5_accessible_vs_latitude.png](report_assets/analysis_fig5_accessible_vs_latitude.png)


![ho_interval_hist.png](report_assets/analysis_ho_interval_hist.png)


![link_budget_vs_elevation.png](report_assets/analysis_link_budget_vs_elevation.png)


### g100_sensitivity


![sensitivity.png](report_assets/g100_sensitivity_sensitivity.png)
