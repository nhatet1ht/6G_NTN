# Auto-generated report assets

### ilcho_linear (800 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  333.495 |  306.380 |
| ho       |    7.061 |    6.008 |
| hof      |    0.902 |    0.056 |
| se       |    3.295 |    2.975 |


![ilcho_linear](report_assets/ilcho_linear_training_curves.png)

### ilcho_linear_v3 (1800 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  323.847 |  299.199 |
| ho       |    6.664 |    5.818 |
| hof      |    2.292 |    0.118 |
| se       |    3.262 |    2.911 |


![ilcho_linear_v3](report_assets/ilcho_linear_v3_training_curves.png)

### ilcho_sigmoid_v2 (1200 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  103.017 |   54.406 |
| ho       |    7.066 |    6.010 |
| hof      |    0.869 |    0.063 |
| se       |    3.293 |    2.963 |


![ilcho_sigmoid_v2](report_assets/ilcho_sigmoid_v2_training_curves.png)

### ilcho_sigmoid_v3 (1800 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  301.812 |  279.681 |
| ho       |    6.664 |    6.191 |
| hof      |    2.295 |    0.186 |
| se       |    3.263 |    3.129 |


![ilcho_sigmoid_v3](report_assets/ilcho_sigmoid_v3_training_curves.png)

### ilcho_sigmoid_v3_p1a (1500 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |   53.305 |   68.416 |
| ho       |    3.868 |    3.862 |
| hof      |    5.600 |    0.532 |
| se       |    2.008 |    1.990 |


![ilcho_sigmoid_v3_p1a](report_assets/ilcho_sigmoid_v3_p1a_training_curves.png)

### lbsh (800 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  320.047 |  280.734 |
| ho       |    7.082 |    5.780 |
| hof      |    0.873 |    0.051 |
| se       |    3.294 |    2.879 |


![lbsh](report_assets/lbsh_training_curves.png)

### su_ilcho_linear (2000 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  311.887 |  398.018 |
| ho       |    6.809 |    7.016 |
| hof      |   20.496 |    4.225 |
| se       |    2.670 |    2.766 |


![su_ilcho_linear](report_assets/su_ilcho_linear_training_curves.png)

### su_ilcho_sigmoid (2800 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  192.251 |  256.523 |
| ho       |    6.799 |    6.920 |
| hof      |   20.633 |    3.888 |
| se       |    2.669 |    2.776 |


![su_ilcho_sigmoid](report_assets/su_ilcho_sigmoid_training_curves.png)

### su_lbsh (2000 episodes)

| metric | first 10% | last 10% |
|---|---|---|
| return   |  308.131 |  390.601 |
| ho       |    6.815 |    7.416 |
| hof      |   20.415 |    3.164 |
| se       |    2.671 |    2.709 |


![su_lbsh](report_assets/su_lbsh_training_curves.png)

### eval_phase1a - `starlink_phase_1a`, 5 ep/point × 1 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    6.040 |    6.060 |    5.580 |    5.580 |    4.655 |    3.708 |
| MD-CHO     |   11.200 |    9.680 |    4.880 |    1.540 |    0.370 |    0.000 |
| MVT-CHO    |    5.000 |    4.840 |    3.510 |    2.840 |    2.170 |    1.684 |
| HSNF       |   11.160 |    9.500 |    7.260 |    7.233 |    6.410 |    5.484 |
| LBSH       |    5.040 |    5.000 |    5.400 |    4.920 |    4.645 |    4.276 |

**Average # handover failures per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.420 |    1.750 |    4.013 |    5.595 |    7.724 |
| MD-CHO     |    0.040 |   15.260 |   51.230 |   72.847 |   85.755 |   91.476 |
| MVT-CHO    |    0.000 |    2.360 |   11.550 |   17.433 |   26.050 |   33.312 |
| HSNF       |    0.040 |    0.020 |    0.010 |    0.013 |    0.005 |    0.080 |
| LBSH       |    0.120 |    0.180 |    0.290 |    0.593 |    0.860 |    1.228 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    1.679 |    1.674 |    1.673 |    1.668 |    1.699 |    1.676 |
| MD-CHO     |    2.227 |    2.181 |    1.966 |    1.818 |    1.717 |    1.666 |
| MVT-CHO    |    2.005 |    1.978 |    1.900 |    1.851 |    1.760 |    1.684 |
| HSNF       |    2.218 |    2.216 |    2.055 |    1.933 |    1.837 |    1.727 |
| LBSH       |    1.631 |    1.624 |    1.616 |    1.614 |    1.619 |    1.602 |

**Jain fairness index**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    0.996 |    0.995 |    0.995 |    0.995 |    0.997 |    0.996 |
| MD-CHO     |    1.000 |    0.998 |    0.997 |    0.993 |    0.995 |    0.998 |
| MVT-CHO    |    0.999 |    0.999 |    0.998 |    0.997 |    0.998 |    0.996 |
| HSNF       |    0.999 |    0.999 |    0.998 |    0.997 |    0.996 |    0.995 |
| LBSH       |    0.997 |    0.996 |    0.996 |    0.995 |    0.997 |    0.997 |

**Channel-occupancy variance**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    0.018 |    0.052 |    0.101 |    0.139 |    0.176 |    0.185 |
| MD-CHO     |    0.030 |    0.081 |    0.144 |    0.180 |    0.202 |    0.203 |
| MVT-CHO    |    0.023 |    0.065 |    0.126 |    0.182 |    0.204 |    0.200 |
| HSNF       |    0.029 |    0.079 |    0.144 |    0.174 |    0.201 |    0.193 |
| LBSH       |    0.014 |    0.034 |    0.075 |    0.117 |    0.141 |    0.148 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| MD-CHO     |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| MVT-CHO    |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| LBSH       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |


![fig_fairness_cdf.png](report_assets/eval_phase1a_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/eval_phase1a_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/eval_phase1a_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/eval_phase1a_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/eval_phase1a_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/eval_phase1a_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/eval_phase1a_fig_se_vs_ue.png)

### eval_phase2a - `starlink_phase_2a`, 5 ep/point × 1 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    9.920 |   10.580 |   10.730 |   10.180 |    9.805 |    8.780 |
| MD-CHO     |   16.600 |   14.900 |   12.660 |    8.367 |    4.410 |    1.084 |
| MVT-CHO    |    7.200 |    6.920 |    6.510 |    5.600 |    5.150 |    4.632 |
| HSNF       |   14.880 |   16.180 |   13.080 |   12.313 |   11.335 |   10.728 |
| LBSH       |    7.320 |    6.960 |    6.600 |    7.020 |    7.285 |    6.932 |

**Average # handover failures per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.020 |    0.370 |    1.100 |    1.640 |    3.312 |
| MD-CHO     |    0.040 |    7.080 |   31.680 |   54.147 |   65.580 |   77.592 |
| MVT-CHO    |    0.000 |    0.360 |    3.800 |    7.933 |    9.740 |   12.144 |
| HSNF       |    0.080 |    0.020 |    0.030 |    0.027 |    0.010 |    0.028 |
| LBSH       |    0.000 |    0.020 |    0.020 |    0.233 |    0.405 |    0.760 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    2.888 |    2.810 |    2.801 |    2.752 |    2.739 |    2.696 |
| MD-CHO     |    3.442 |    3.439 |    3.252 |    3.059 |    2.946 |    2.841 |
| MVT-CHO    |    3.095 |    3.044 |    3.006 |    2.970 |    2.939 |    2.887 |
| HSNF       |    3.426 |    3.434 |    3.354 |    3.245 |    3.106 |    2.998 |
| LBSH       |    2.592 |    2.598 |    2.612 |    2.571 |    2.557 |    2.579 |

**Jain fairness index**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    0.997 |    0.996 |    0.997 |    0.997 |    0.997 |    0.997 |
| MD-CHO     |    0.999 |    0.999 |    0.995 |    0.992 |    0.994 |    0.995 |
| MVT-CHO    |    0.998 |    0.998 |    0.997 |    0.997 |    0.998 |    0.998 |
| HSNF       |    0.999 |    0.999 |    0.999 |    0.998 |    0.998 |    0.996 |
| LBSH       |    0.997 |    0.996 |    0.996 |    0.995 |    0.994 |    0.995 |

**Channel-occupancy variance**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    0.007 |    0.020 |    0.054 |    0.089 |    0.115 |    0.143 |
| MD-CHO     |    0.015 |    0.051 |    0.090 |    0.132 |    0.171 |    0.190 |
| MVT-CHO    |    0.009 |    0.027 |    0.077 |    0.117 |    0.157 |    0.185 |
| HSNF       |    0.016 |    0.046 |    0.098 |    0.135 |    0.163 |    0.184 |
| LBSH       |    0.007 |    0.018 |    0.042 |    0.072 |    0.095 |    0.118 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 40 UE | 50 UE |
|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| MD-CHO     |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| MVT-CHO    |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| LBSH       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |


![fig_fairness_cdf.png](report_assets/eval_phase2a_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/eval_phase2a_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/eval_phase2a_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/eval_phase2a_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/eval_phase2a_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/eval_phase2a_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/eval_phase2a_fig_se_vs_ue.png)

### xeval2_hybrid - `hybrid`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    9.000 |    9.722 |   10.450 |    9.467 |    9.893 |
| ILCHO-lin  |    9.978 |    9.778 |    9.972 |    8.257 |    6.909 |
| MD-CHO     |   15.467 |   11.811 |    4.397 |    0.081 |    0.000 |
| MVT-CHO    |    5.533 |    4.756 |    3.264 |    1.816 |    1.330 |
| HSNF       |   16.467 |   13.144 |   11.361 |   10.106 |   11.306 |
| LBSH       |    9.378 |   10.533 |   10.106 |    8.705 |    6.484 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.067 |    0.194 |    1.967 |    8.265 |   15.767 |
| ILCHO-lin  |    0.000 |    0.417 |    2.658 |    8.778 |   17.851 |
| MD-CHO     |    0.000 |   32.467 |   64.169 |   90.040 |   98.794 |
| MVT-CHO    |    0.022 |    6.333 |   16.428 |   20.525 |   22.091 |
| HSNF       |    0.022 |    0.022 |    0.028 |    0.016 |    0.080 |
| LBSH       |    0.067 |    0.106 |    0.742 |    2.100 |    4.869 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    2.723 |    2.655 |    2.605 |    2.521 |    2.333 |
| ILCHO-lin  |    2.761 |    2.743 |    2.642 |    2.576 |    2.412 |
| MD-CHO     |    3.427 |    2.956 |    2.418 |    1.973 |    1.786 |
| MVT-CHO    |    2.284 |    2.221 |    2.104 |    2.202 |    2.235 |
| HSNF       |    3.422 |    3.328 |    3.106 |    2.806 |    2.600 |
| LBSH       |    2.522 |    2.469 |    2.466 |    2.490 |    2.480 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.998 |    0.996 |    0.996 |    0.996 |    0.991 |
| ILCHO-lin  |    0.998 |    0.998 |    0.997 |    0.996 |    0.993 |
| MD-CHO     |    0.999 |    0.975 |    0.977 |    0.971 |    0.978 |
| MVT-CHO    |    0.999 |    0.996 |    0.990 |    0.985 |    0.983 |
| HSNF       |    0.999 |    0.998 |    0.998 |    0.993 |    0.992 |
| LBSH       |    0.998 |    0.997 |    0.997 |    0.997 |    0.996 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.005 |    0.038 |    0.091 |    0.156 |    0.164 |
| ILCHO-lin  |    0.004 |    0.039 |    0.092 |    0.163 |    0.189 |
| MD-CHO     |    0.010 |    0.063 |    0.126 |    0.184 |    0.208 |
| MVT-CHO    |    0.009 |    0.059 |    0.119 |    0.175 |    0.205 |
| HSNF       |    0.010 |    0.063 |    0.119 |    0.175 |    0.189 |
| LBSH       |    0.005 |    0.028 |    0.068 |    0.136 |    0.193 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.001 |    0.006 |    0.027 |    0.052 |
| ILCHO-lin  |    0.000 |    0.001 |    0.009 |    0.029 |    0.059 |
| MD-CHO     |    0.000 |    0.108 |    0.213 |    0.298 |    0.327 |
| MVT-CHO    |    0.000 |    0.021 |    0.054 |    0.068 |    0.073 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |
| LBSH       |    0.000 |    0.000 |    0.002 |    0.007 |    0.016 |


![fig_fairness_cdf.png](report_assets/xeval2_hybrid_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval2_hybrid_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval2_hybrid_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval2_hybrid_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval2_hybrid_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval2_hybrid_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval2_hybrid_fig_se_vs_ue.png)

### xeval2_reward_ablation - `starlink_phase_2a`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    8.467 |    9.050 |    8.861 |    7.429 |    3.561 |
| ILCHO-lin  |   10.200 |    9.572 |    9.764 |    7.440 |    3.414 |
| MD-CHO     |   15.467 |   11.811 |    4.397 |    0.067 |    0.000 |
| MVT-CHO    |    6.933 |    6.422 |    5.169 |    3.483 |    2.412 |
| HSNF       |   16.489 |   13.117 |   11.317 |    9.887 |    5.543 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.022 |    0.222 |    1.406 |    7.006 |   21.098 |
| ILCHO-lin  |    0.000 |    0.422 |    2.078 |    6.679 |   16.866 |
| MD-CHO     |    0.000 |   32.467 |   64.169 |   90.116 |  100.587 |
| MVT-CHO    |    0.022 |    3.972 |    9.664 |   20.979 |   30.552 |
| HSNF       |    0.022 |    0.022 |    0.025 |    0.040 |    3.368 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    2.870 |    2.792 |    2.721 |    2.597 |    2.391 |
| ILCHO-lin  |    2.798 |    2.766 |    2.673 |    2.589 |    2.424 |
| MD-CHO     |    3.427 |    2.956 |    2.418 |    1.976 |    1.770 |
| MVT-CHO    |    3.019 |    2.981 |    2.861 |    2.582 |    2.353 |
| HSNF       |    3.423 |    3.329 |    3.104 |    2.805 |    2.554 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.994 |    0.994 |    0.994 |    0.994 |    0.990 |
| ILCHO-lin  |    0.992 |    0.994 |    0.994 |    0.993 |    0.991 |
| MD-CHO     |    0.999 |    0.975 |    0.977 |    0.969 |    0.974 |
| MVT-CHO    |    0.997 |    0.997 |    0.997 |    0.995 |    0.980 |
| HSNF       |    0.999 |    0.998 |    0.998 |    0.993 |    0.992 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.008 |    0.053 |    0.122 |    0.178 |    0.142 |
| ILCHO-lin  |    0.007 |    0.054 |    0.113 |    0.171 |    0.144 |
| MD-CHO     |    0.016 |    0.094 |    0.173 |    0.204 |    0.150 |
| MVT-CHO    |    0.009 |    0.079 |    0.153 |    0.195 |    0.148 |
| HSNF       |    0.016 |    0.094 |    0.160 |    0.188 |    0.142 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.001 |    0.005 |    0.023 |    0.068 |
| ILCHO-lin  |    0.000 |    0.001 |    0.007 |    0.022 |    0.054 |
| MD-CHO     |    0.000 |    0.108 |    0.213 |    0.298 |    0.332 |
| MVT-CHO    |    0.000 |    0.013 |    0.032 |    0.069 |    0.099 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.010 |


![fig_fairness_cdf.png](report_assets/xeval2_reward_ablation_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval2_reward_ablation_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval2_reward_ablation_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval2_reward_ablation_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval2_reward_ablation_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval2_reward_ablation_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval2_reward_ablation_fig_se_vs_ue.png)

### xeval2_starlink_phase_1a - `starlink_phase_1a`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    5.178 |    4.844 |    4.253 |    2.354 |    1.022 |
| ILCHO-lin  |    5.867 |    5.644 |    4.778 |    2.067 |    0.801 |
| MD-CHO     |   11.178 |    4.817 |    0.261 |    0.000 |    0.000 |
| MVT-CHO    |    5.111 |    3.600 |    2.183 |    1.203 |    0.942 |
| HSNF       |   10.822 |    7.361 |    6.631 |    3.046 |    1.602 |
| LBSH       |    4.844 |    4.639 |    4.164 |    2.714 |    1.458 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.856 |    0.969 |   25.252 |  140.776 |
| ILCHO-lin  |    0.022 |    1.133 |    1.917 |   27.932 |  143.890 |
| MD-CHO     |    0.044 |   52.239 |   85.358 |  115.176 |  208.133 |
| MVT-CHO    |    0.000 |   10.850 |   25.761 |   58.997 |  165.529 |
| HSNF       |    0.022 |    0.011 |    0.014 |   17.006 |  130.381 |
| LBSH       |    0.089 |    0.111 |    0.433 |   18.421 |  131.317 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    1.686 |    1.671 |    1.630 |    1.484 |    1.138 |
| ILCHO-lin  |    1.724 |    1.661 |    1.626 |    1.477 |    1.131 |
| MD-CHO     |    2.220 |    1.683 |    1.300 |    1.060 |    0.825 |
| MVT-CHO    |    1.959 |    1.863 |    1.632 |    1.341 |    1.037 |
| HSNF       |    2.213 |    2.048 |    1.827 |    1.516 |    1.173 |
| LBSH       |    1.636 |    1.638 |    1.621 |    1.510 |    1.172 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.997 |    0.995 |    0.994 |    0.985 |    0.889 |
| ILCHO-lin  |    0.997 |    0.995 |    0.994 |    0.983 |    0.893 |
| MD-CHO     |    0.999 |    0.984 |    0.977 |    0.963 |    0.875 |
| MVT-CHO    |    0.999 |    0.997 |    0.996 |    0.972 |    0.870 |
| HSNF       |    0.999 |    0.998 |    0.996 |    0.985 |    0.897 |
| LBSH       |    0.997 |    0.995 |    0.994 |    0.985 |    0.900 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.018 |    0.090 |    0.155 |    0.127 |    0.071 |
| ILCHO-lin  |    0.014 |    0.086 |    0.145 |    0.129 |    0.070 |
| MD-CHO     |    0.030 |    0.144 |    0.203 |    0.129 |    0.074 |
| MVT-CHO    |    0.024 |    0.129 |    0.206 |    0.131 |    0.073 |
| HSNF       |    0.029 |    0.144 |    0.199 |    0.127 |    0.075 |
| LBSH       |    0.016 |    0.085 |    0.128 |    0.125 |    0.072 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.003 |    0.003 |    0.056 |    0.259 |
| ILCHO-lin  |    0.000 |    0.004 |    0.006 |    0.065 |    0.267 |
| MD-CHO     |    0.000 |    0.174 |    0.283 |    0.351 |    0.480 |
| MVT-CHO    |    0.000 |    0.036 |    0.085 |    0.166 |    0.338 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.032 |    0.226 |
| LBSH       |    0.000 |    0.000 |    0.001 |    0.035 |    0.229 |


![fig_fairness_cdf.png](report_assets/xeval2_starlink_phase_1a_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval2_starlink_phase_1a_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval2_starlink_phase_1a_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval2_starlink_phase_1a_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval2_starlink_phase_1a_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval2_starlink_phase_1a_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval2_starlink_phase_1a_fig_se_vs_ue.png)

### xeval2_starlink_phase_2a - `starlink_phase_2a`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    8.467 |    9.050 |    8.861 |    7.429 |    3.561 |
| ILCHO-lin  |   10.200 |    9.572 |    9.764 |    7.440 |    3.414 |
| MD-CHO     |   15.467 |   11.811 |    4.397 |    0.067 |    0.000 |
| MVT-CHO    |    6.933 |    6.422 |    5.169 |    3.483 |    2.412 |
| HSNF       |   16.489 |   13.117 |   11.317 |    9.887 |    5.543 |
| LBSH       |    8.489 |    8.922 |    7.647 |    6.530 |    4.061 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.022 |    0.222 |    1.406 |    7.006 |   21.098 |
| ILCHO-lin  |    0.000 |    0.422 |    2.078 |    6.679 |   16.866 |
| MD-CHO     |    0.000 |   32.467 |   64.169 |   90.116 |  100.587 |
| MVT-CHO    |    0.022 |    3.972 |    9.664 |   20.979 |   30.552 |
| HSNF       |    0.022 |    0.022 |    0.025 |    0.040 |    3.368 |
| LBSH       |    0.022 |    0.306 |    1.286 |    2.211 |    4.554 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    2.870 |    2.792 |    2.721 |    2.597 |    2.391 |
| ILCHO-lin  |    2.798 |    2.766 |    2.673 |    2.589 |    2.424 |
| MD-CHO     |    3.427 |    2.956 |    2.418 |    1.976 |    1.770 |
| MVT-CHO    |    3.019 |    2.981 |    2.861 |    2.582 |    2.353 |
| HSNF       |    3.423 |    3.329 |    3.104 |    2.805 |    2.554 |
| LBSH       |    2.490 |    2.406 |    2.456 |    2.492 |    2.502 |

**Jain fairness index**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.994 |    0.994 |    0.994 |    0.994 |    0.990 |
| ILCHO-lin  |    0.992 |    0.994 |    0.994 |    0.993 |    0.991 |
| MD-CHO     |    0.999 |    0.975 |    0.977 |    0.969 |    0.974 |
| MVT-CHO    |    0.997 |    0.997 |    0.997 |    0.995 |    0.980 |
| HSNF       |    0.999 |    0.998 |    0.998 |    0.993 |    0.992 |
| LBSH       |    0.994 |    0.992 |    0.993 |    0.994 |    0.994 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.008 |    0.053 |    0.122 |    0.178 |    0.142 |
| ILCHO-lin  |    0.007 |    0.054 |    0.113 |    0.171 |    0.144 |
| MD-CHO     |    0.016 |    0.094 |    0.173 |    0.204 |    0.150 |
| MVT-CHO    |    0.009 |    0.079 |    0.153 |    0.195 |    0.148 |
| HSNF       |    0.016 |    0.094 |    0.160 |    0.188 |    0.142 |
| LBSH       |    0.008 |    0.050 |    0.097 |    0.138 |    0.143 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 40 UE | 70 UE | 100 UE |
|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.001 |    0.005 |    0.023 |    0.068 |
| ILCHO-lin  |    0.000 |    0.001 |    0.007 |    0.022 |    0.054 |
| MD-CHO     |    0.000 |    0.108 |    0.213 |    0.298 |    0.332 |
| MVT-CHO    |    0.000 |    0.013 |    0.032 |    0.069 |    0.099 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.010 |
| LBSH       |    0.000 |    0.001 |    0.004 |    0.007 |    0.014 |


![fig_fairness_cdf.png](report_assets/xeval2_starlink_phase_2a_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval2_starlink_phase_2a_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval2_starlink_phase_2a_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval2_starlink_phase_2a_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval2_starlink_phase_2a_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval2_starlink_phase_2a_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval2_starlink_phase_2a_fig_se_vs_ue.png)

### xeval_hybrid - `hybrid`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |   11.733 |   11.656 |   11.500 |   11.004 |   13.136 |   11.320 |    7.341 |
| ILCHO-lin  |   10.489 |   10.611 |   10.833 |   11.048 |   11.491 |   10.450 |    8.591 |
| MD-CHO     |   15.978 |   14.889 |   12.011 |    8.378 |    1.027 |    0.024 |    0.000 |
| MVT-CHO    |    7.622 |    7.522 |    6.522 |    6.037 |    4.696 |    3.575 |    3.053 |
| HSNF       |   15.667 |   15.500 |   12.850 |   12.248 |   10.678 |    9.929 |   11.024 |
| LBSH       |    7.467 |    7.511 |    7.783 |    7.678 |    7.320 |    6.573 |    4.710 |

**Average # handover failures per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.044 |    0.022 |    0.756 |    2.652 |    4.233 |    7.855 |   20.564 |
| ILCHO-lin  |    0.044 |    0.044 |    0.089 |    0.315 |    1.238 |    3.834 |    5.509 |
| MD-CHO     |    0.000 |    6.956 |   32.894 |   54.507 |   76.713 |   92.616 |   98.763 |
| MVT-CHO    |    0.022 |    0.389 |    5.467 |    8.678 |   14.458 |   18.127 |   20.722 |
| HSNF       |    0.000 |    0.044 |    0.017 |    0.000 |    0.018 |    0.031 |    0.183 |
| LBSH       |    0.000 |    0.022 |    0.072 |    0.267 |    1.033 |    2.670 |    7.879 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    2.958 |    2.971 |    2.933 |    2.865 |    2.608 |    2.444 |    2.324 |
| ILCHO-lin  |    2.643 |    2.637 |    2.645 |    2.620 |    2.557 |    2.494 |    2.455 |
| MD-CHO     |    3.467 |    3.357 |    2.936 |    2.577 |    2.209 |    1.933 |    1.803 |
| MVT-CHO    |    2.701 |    2.757 |    2.650 |    2.602 |    2.530 |    2.468 |    2.389 |
| HSNF       |    3.442 |    3.431 |    3.333 |    3.230 |    2.996 |    2.781 |    2.602 |
| LBSH       |    2.561 |    2.632 |    2.577 |    2.571 |    2.579 |    2.578 |    2.512 |

**Jain fairness index**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.997 |    0.997 |    0.998 |    0.997 |    0.995 |    0.994 |    0.994 |
| ILCHO-lin  |    0.998 |    0.997 |    0.996 |    0.997 |    0.997 |    0.997 |    0.996 |
| MD-CHO     |    0.999 |    0.995 |    0.976 |    0.965 |    0.975 |    0.971 |    0.980 |
| MVT-CHO    |    0.997 |    0.997 |    0.997 |    0.996 |    0.996 |    0.994 |    0.994 |
| HSNF       |    0.999 |    0.999 |    0.998 |    0.998 |    0.997 |    0.994 |    0.992 |
| LBSH       |    0.998 |    0.997 |    0.997 |    0.996 |    0.997 |    0.997 |    0.995 |

**Channel-occupancy variance**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.006 |    0.019 |    0.052 |    0.086 |    0.111 |    0.136 |    0.171 |
| ILCHO-lin  |    0.005 |    0.014 |    0.031 |    0.055 |    0.096 |    0.143 |    0.174 |
| MD-CHO     |    0.013 |    0.039 |    0.073 |    0.111 |    0.164 |    0.206 |    0.206 |
| MVT-CHO    |    0.010 |    0.022 |    0.056 |    0.089 |    0.147 |    0.192 |    0.200 |
| HSNF       |    0.013 |    0.035 |    0.074 |    0.109 |    0.160 |    0.190 |    0.184 |
| LBSH       |    0.006 |    0.014 |    0.034 |    0.059 |    0.111 |    0.171 |    0.203 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.002 |    0.009 |    0.014 |    0.026 |    0.068 |
| ILCHO-lin  |    0.000 |    0.000 |    0.000 |    0.001 |    0.004 |    0.013 |    0.018 |
| MD-CHO     |    0.000 |    0.023 |    0.109 |    0.181 |    0.254 |    0.307 |    0.327 |
| MVT-CHO    |    0.000 |    0.001 |    0.018 |    0.029 |    0.048 |    0.060 |    0.068 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.001 |
| LBSH       |    0.000 |    0.000 |    0.000 |    0.001 |    0.003 |    0.009 |    0.025 |


![fig_fairness_cdf.png](report_assets/xeval_hybrid_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval_hybrid_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval_hybrid_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval_hybrid_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval_hybrid_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval_hybrid_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval_hybrid_fig_se_vs_ue.png)

### xeval_oneweb_phase_1 - `oneweb_phase_1`, 3 ep/point × 2 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 20 UE | 50 UE |
|---|---|---|---|
| ILCHO      |    3.000 |    2.750 |    0.017 |
| ILCHO-lin  |    2.333 |    1.933 |    0.017 |
| MD-CHO     |    7.133 |    2.242 |    0.000 |
| MVT-CHO    |    3.500 |    1.642 |    0.417 |
| HSNF       |    7.100 |    3.317 |    1.117 |
| LBSH       |    1.600 |    1.375 |    1.230 |

**Average # handover failures per UE**

| method | 5 UE | 20 UE | 50 UE |
|---|---|---|---|
| ILCHO      |    0.000 |    4.458 |   47.503 |
| ILCHO-lin  |    0.000 |    0.142 |   44.477 |
| MD-CHO     |    0.000 |   53.158 |  111.313 |
| MVT-CHO    |    0.000 |   27.667 |   76.507 |
| HSNF       |    0.000 |    0.017 |   29.863 |
| LBSH       |    0.000 |    0.267 |   30.810 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 20 UE | 50 UE |
|---|---|---|---|
| ILCHO      |    0.725 |    0.747 |    0.621 |
| ILCHO-lin  |    0.700 |    0.729 |    0.630 |
| MD-CHO     |    0.976 |    0.732 |    0.483 |
| MVT-CHO    |    0.861 |    0.737 |    0.561 |
| HSNF       |    0.982 |    0.908 |    0.650 |
| LBSH       |    0.721 |    0.713 |    0.648 |

**Jain fairness index**

| method | 5 UE | 20 UE | 50 UE |
|---|---|---|---|
| ILCHO      |    0.998 |    0.993 |    0.990 |
| ILCHO-lin  |    0.996 |    0.996 |    0.988 |
| MD-CHO     |    1.000 |    0.986 |    0.983 |
| MVT-CHO    |    0.999 |    0.995 |    0.990 |
| HSNF       |    1.000 |    0.999 |    0.993 |
| LBSH       |    1.000 |    0.996 |    0.994 |

**Channel-occupancy variance**

| method | 5 UE | 20 UE | 50 UE |
|---|---|---|---|
| ILCHO      |    0.036 |    0.149 |    0.106 |
| ILCHO-lin  |    0.029 |    0.120 |    0.104 |
| MD-CHO     |    0.044 |    0.176 |    0.105 |
| MVT-CHO    |    0.042 |    0.172 |    0.111 |
| HSNF       |    0.045 |    0.188 |    0.109 |
| LBSH       |    0.034 |    0.137 |    0.115 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 20 UE | 50 UE |
|---|---|---|---|
| ILCHO      |    0.000 |    0.015 |    0.114 |
| ILCHO-lin  |    0.000 |    0.000 |    0.103 |
| MD-CHO     |    0.000 |    0.177 |    0.330 |
| MVT-CHO    |    0.000 |    0.092 |    0.211 |
| HSNF       |    0.000 |    0.000 |    0.052 |
| LBSH       |    0.000 |    0.001 |    0.054 |


![fig_fairness_cdf.png](report_assets/xeval_oneweb_phase_1_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval_oneweb_phase_1_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval_oneweb_phase_1_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval_oneweb_phase_1_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval_oneweb_phase_1_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval_oneweb_phase_1_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval_oneweb_phase_1_fig_se_vs_ue.png)

### xeval_phase1a_native - `starlink_phase_1a`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    6.556 |    7.133 |    7.494 |    5.956 |    0.338 |    0.009 |    0.010 |
| MD-CHO     |   11.022 |    9.700 |    4.828 |    1.356 |    0.000 |    0.000 |    0.000 |
| MVT-CHO    |    5.200 |    4.867 |    3.606 |    2.811 |    1.720 |    1.173 |    0.961 |
| HSNF       |   11.044 |    9.544 |    7.256 |    7.141 |    5.429 |    2.493 |    1.554 |
| LBSH       |    5.644 |    5.433 |    5.200 |    5.093 |    4.238 |    3.203 |    3.268 |

**Average # handover failures per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.022 |    0.000 |    0.122 |    5.007 |   74.816 |  121.476 |  205.249 |
| MD-CHO     |    0.044 |   14.589 |   52.472 |   73.696 |   91.600 |  126.092 |  207.411 |
| MVT-CHO    |    0.089 |    2.533 |   10.856 |   18.052 |   31.133 |   71.856 |  163.631 |
| HSNF       |    0.000 |    0.011 |    0.022 |    0.011 |    0.093 |   30.830 |  128.013 |
| LBSH       |    0.133 |    0.100 |    0.272 |    0.704 |    1.420 |   31.181 |  129.520 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    1.851 |    1.876 |    1.874 |    1.856 |    1.306 |    1.038 |    0.839 |
| MD-CHO     |    2.219 |    2.071 |    1.673 |    1.429 |    1.217 |    1.024 |    0.830 |
| MVT-CHO    |    1.970 |    1.952 |    1.863 |    1.747 |    1.541 |    1.286 |    1.038 |
| HSNF       |    2.214 |    2.205 |    2.053 |    1.934 |    1.730 |    1.457 |    1.173 |
| LBSH       |    1.630 |    1.600 |    1.594 |    1.614 |    1.605 |    1.453 |    1.179 |

**Jain fairness index**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.997 |    0.998 |    0.997 |    0.996 |    0.993 |    0.959 |    0.880 |
| MD-CHO     |    0.999 |    0.993 |    0.984 |    0.974 |    0.992 |    0.960 |    0.867 |
| MVT-CHO    |    0.999 |    0.998 |    0.997 |    0.995 |    0.991 |    0.965 |    0.877 |
| HSNF       |    0.999 |    0.999 |    0.998 |    0.997 |    0.995 |    0.981 |    0.900 |
| LBSH       |    0.998 |    0.997 |    0.995 |    0.996 |    0.996 |    0.982 |    0.900 |

**Channel-occupancy variance**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.016 |    0.036 |    0.094 |    0.165 |    0.203 |    0.112 |    0.072 |
| MD-CHO     |    0.028 |    0.081 |    0.143 |    0.179 |    0.203 |    0.110 |    0.066 |
| MVT-CHO    |    0.026 |    0.072 |    0.130 |    0.177 |    0.198 |    0.110 |    0.072 |
| HSNF       |    0.031 |    0.079 |    0.141 |    0.176 |    0.193 |    0.110 |    0.071 |
| LBSH       |    0.015 |    0.035 |    0.077 |    0.117 |    0.143 |    0.106 |    0.074 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.000 |    0.017 |    0.248 |    0.355 |    0.471 |
| MD-CHO     |    0.000 |    0.049 |    0.174 |    0.244 |    0.304 |    0.367 |    0.479 |
| MVT-CHO    |    0.000 |    0.008 |    0.036 |    0.060 |    0.103 |    0.189 |    0.334 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.056 |    0.222 |
| LBSH       |    0.000 |    0.000 |    0.001 |    0.002 |    0.005 |    0.059 |    0.225 |


![fig_fairness_cdf.png](report_assets/xeval_phase1a_native_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval_phase1a_native_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval_phase1a_native_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval_phase1a_native_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval_phase1a_native_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval_phase1a_native_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval_phase1a_native_fig_se_vs_ue.png)

### xeval_reward_ablation - `starlink_phase_2a`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |   11.089 |   12.533 |   12.111 |   10.407 |    9.571 |    5.699 |    2.696 |
| ILCHO-lin  |    9.200 |    8.400 |    7.861 |    7.704 |    7.891 |    6.707 |    4.164 |
| MD-CHO     |   15.978 |   14.889 |   12.011 |    8.348 |    1.049 |    0.019 |    0.000 |
| MVT-CHO    |    7.000 |    6.867 |    6.328 |    5.830 |    4.520 |    3.299 |    2.391 |
| HSNF       |   15.644 |   15.511 |   12.817 |   12.270 |   10.651 |    9.461 |    5.553 |

**Average # handover failures per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.900 |    2.856 |   11.436 |   30.415 |   47.449 |
| ILCHO-lin  |    0.022 |    0.056 |    0.056 |    0.270 |    0.662 |    3.727 |    9.650 |
| MD-CHO     |    0.000 |    6.956 |   32.900 |   54.515 |   76.740 |   92.619 |  100.297 |
| MVT-CHO    |    0.022 |    0.378 |    4.322 |    6.489 |   12.753 |   22.081 |   30.211 |
| HSNF       |    0.000 |    0.056 |    0.017 |    0.004 |    0.016 |    0.083 |    3.397 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    3.116 |    3.110 |    3.050 |    2.991 |    2.707 |    2.404 |    2.184 |
| ILCHO-lin  |    2.750 |    2.678 |    2.653 |    2.649 |    2.637 |    2.591 |    2.466 |
| MD-CHO     |    3.467 |    3.357 |    2.936 |    2.577 |    2.208 |    1.933 |    1.777 |
| MVT-CHO    |    3.040 |    3.058 |    2.977 |    2.936 |    2.781 |    2.545 |    2.361 |
| HSNF       |    3.443 |    3.430 |    3.334 |    3.231 |    2.997 |    2.772 |    2.557 |

**Jain fairness index**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.998 |    0.997 |    0.998 |    0.998 |    0.994 |    0.984 |    0.981 |
| ILCHO-lin  |    0.995 |    0.996 |    0.996 |    0.996 |    0.996 |    0.995 |    0.992 |
| MD-CHO     |    0.999 |    0.995 |    0.976 |    0.966 |    0.974 |    0.971 |    0.975 |
| MVT-CHO    |    0.998 |    0.997 |    0.997 |    0.997 |    0.997 |    0.992 |    0.980 |
| HSNF       |    0.999 |    0.999 |    0.998 |    0.998 |    0.996 |    0.993 |    0.992 |

**Channel-occupancy variance**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.009 |    0.028 |    0.072 |    0.118 |    0.162 |    0.167 |    0.143 |
| ILCHO-lin  |    0.007 |    0.017 |    0.039 |    0.062 |    0.116 |    0.162 |    0.143 |
| MD-CHO     |    0.017 |    0.051 |    0.094 |    0.139 |    0.189 |    0.205 |    0.149 |
| MVT-CHO    |    0.014 |    0.030 |    0.077 |    0.114 |    0.182 |    0.195 |    0.148 |
| HSNF       |    0.017 |    0.047 |    0.095 |    0.136 |    0.185 |    0.182 |    0.143 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.003 |    0.009 |    0.038 |    0.101 |    0.156 |
| ILCHO-lin  |    0.000 |    0.000 |    0.000 |    0.001 |    0.002 |    0.012 |    0.031 |
| MD-CHO     |    0.000 |    0.023 |    0.109 |    0.181 |    0.254 |    0.307 |    0.331 |
| MVT-CHO    |    0.000 |    0.001 |    0.014 |    0.021 |    0.042 |    0.072 |    0.098 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.010 |


![fig_fairness_cdf.png](report_assets/xeval_reward_ablation_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval_reward_ablation_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval_reward_ablation_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval_reward_ablation_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval_reward_ablation_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval_reward_ablation_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval_reward_ablation_fig_se_vs_ue.png)

### xeval_starlink_phase_1a - `starlink_phase_1a`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    5.978 |    5.911 |    5.928 |    5.693 |    3.313 |    0.784 |    1.232 |
| ILCHO-lin  |    6.978 |    7.133 |    6.811 |    5.837 |    3.469 |    1.514 |    1.601 |
| MD-CHO     |   11.289 |    9.778 |    4.928 |    1.515 |    0.000 |    0.000 |    0.000 |
| MVT-CHO    |    4.933 |    4.856 |    3.633 |    2.811 |    1.771 |    1.191 |    0.994 |
| HSNF       |   11.133 |    9.600 |    7.283 |    6.933 |    5.660 |    2.526 |    1.577 |
| LBSH       |    5.200 |    5.067 |    5.139 |    4.985 |    4.216 |    3.090 |    3.249 |

**Average # handover failures per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.022 |    0.056 |    1.667 |    3.196 |   11.929 |   66.138 |  162.659 |
| ILCHO-lin  |    0.111 |    0.133 |    2.044 |    4.230 |    7.802 |   46.043 |  141.851 |
| MD-CHO     |    0.089 |   14.700 |   52.656 |   73.385 |   91.224 |  125.923 |  206.853 |
| MVT-CHO    |    0.000 |    2.567 |   11.478 |   19.007 |   31.878 |   71.156 |  162.082 |
| HSNF       |    0.022 |    0.011 |    0.006 |    0.015 |    0.138 |   31.978 |  130.140 |
| LBSH       |    0.200 |    0.122 |    0.261 |    0.537 |    1.276 |   32.370 |  128.241 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    1.714 |    1.711 |    1.700 |    1.709 |    1.642 |    1.313 |    1.048 |
| ILCHO-lin  |    1.713 |    1.694 |    1.672 |    1.653 |    1.650 |    1.401 |    1.136 |
| MD-CHO     |    2.232 |    2.077 |    1.673 |    1.432 |    1.221 |    1.017 |    0.825 |
| MVT-CHO    |    1.946 |    1.951 |    1.850 |    1.749 |    1.538 |    1.285 |    1.036 |
| HSNF       |    2.212 |    2.204 |    2.051 |    1.933 |    1.728 |    1.459 |    1.179 |
| LBSH       |    1.615 |    1.617 |    1.599 |    1.603 |    1.600 |    1.446 |    1.174 |

**Jain fairness index**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.998 |    0.996 |    0.995 |    0.995 |    0.996 |    0.974 |    0.884 |
| ILCHO-lin  |    0.996 |    0.997 |    0.994 |    0.994 |    0.996 |    0.978 |    0.893 |
| MD-CHO     |    0.999 |    0.992 |    0.980 |    0.972 |    0.991 |    0.962 |    0.875 |
| MVT-CHO    |    0.999 |    0.998 |    0.997 |    0.995 |    0.990 |    0.967 |    0.879 |
| HSNF       |    0.999 |    0.999 |    0.998 |    0.997 |    0.994 |    0.980 |    0.898 |
| LBSH       |    0.997 |    0.998 |    0.996 |    0.995 |    0.996 |    0.981 |    0.901 |

**Channel-occupancy variance**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.019 |    0.049 |    0.100 |    0.145 |    0.199 |    0.111 |    0.072 |
| ILCHO-lin  |    0.017 |    0.048 |    0.098 |    0.137 |    0.180 |    0.108 |    0.067 |
| MD-CHO     |    0.029 |    0.081 |    0.144 |    0.179 |    0.203 |    0.107 |    0.070 |
| MVT-CHO    |    0.025 |    0.065 |    0.130 |    0.176 |    0.198 |    0.114 |    0.072 |
| HSNF       |    0.030 |    0.078 |    0.143 |    0.178 |    0.194 |    0.106 |    0.073 |
| LBSH       |    0.014 |    0.040 |    0.080 |    0.113 |    0.146 |    0.108 |    0.078 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.006 |    0.011 |    0.039 |    0.173 |    0.331 |
| ILCHO-lin  |    0.000 |    0.000 |    0.007 |    0.014 |    0.026 |    0.105 |    0.263 |
| MD-CHO     |    0.000 |    0.049 |    0.175 |    0.243 |    0.302 |    0.367 |    0.479 |
| MVT-CHO    |    0.000 |    0.009 |    0.038 |    0.063 |    0.105 |    0.188 |    0.331 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.058 |    0.225 |
| LBSH       |    0.001 |    0.000 |    0.001 |    0.002 |    0.004 |    0.061 |    0.223 |


![fig_fairness_cdf.png](report_assets/xeval_starlink_phase_1a_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval_starlink_phase_1a_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval_starlink_phase_1a_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval_starlink_phase_1a_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval_starlink_phase_1a_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval_starlink_phase_1a_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval_starlink_phase_1a_fig_se_vs_ue.png)

### xeval_starlink_phase_2a - `starlink_phase_2a`, 3 ep/point × 3 seed(s), horizon 600 s


**Average # handovers per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |   11.089 |   12.533 |   12.111 |   10.407 |    9.571 |    5.699 |    2.696 |
| ILCHO-lin  |   10.933 |   10.456 |    9.844 |    9.674 |    8.656 |    6.462 |    3.757 |
| MD-CHO     |   15.978 |   14.889 |   12.011 |    8.348 |    1.049 |    0.019 |    0.000 |
| MVT-CHO    |    7.000 |    6.867 |    6.328 |    5.830 |    4.520 |    3.299 |    2.391 |
| HSNF       |   15.644 |   15.511 |   12.817 |   12.270 |   10.651 |    9.461 |    5.553 |
| LBSH       |    7.067 |    6.800 |    7.139 |    7.167 |    7.011 |    6.296 |    4.290 |

**Average # handover failures per UE**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.900 |    2.856 |   11.436 |   30.415 |   47.449 |
| ILCHO-lin  |    0.000 |    0.011 |    0.072 |    0.393 |    3.264 |    8.471 |   15.902 |
| MD-CHO     |    0.000 |    6.956 |   32.900 |   54.515 |   76.740 |   92.619 |  100.297 |
| MVT-CHO    |    0.022 |    0.378 |    4.322 |    6.489 |   12.753 |   22.081 |   30.211 |
| HSNF       |    0.000 |    0.056 |    0.017 |    0.004 |    0.016 |    0.083 |    3.397 |
| LBSH       |    0.000 |    0.022 |    0.044 |    0.122 |    0.433 |    1.981 |    7.963 |

**Average spectral efficiency [bps/Hz]**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    3.116 |    3.110 |    3.050 |    2.991 |    2.707 |    2.404 |    2.184 |
| ILCHO-lin  |    2.763 |    2.768 |    2.745 |    2.755 |    2.688 |    2.593 |    2.427 |
| MD-CHO     |    3.467 |    3.357 |    2.936 |    2.577 |    2.208 |    1.933 |    1.777 |
| MVT-CHO    |    3.040 |    3.058 |    2.977 |    2.936 |    2.781 |    2.545 |    2.361 |
| HSNF       |    3.443 |    3.430 |    3.334 |    3.231 |    2.997 |    2.772 |    2.557 |
| LBSH       |    2.550 |    2.608 |    2.572 |    2.558 |    2.576 |    2.583 |    2.498 |

**Jain fairness index**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.998 |    0.997 |    0.998 |    0.998 |    0.994 |    0.984 |    0.981 |
| ILCHO-lin  |    0.993 |    0.996 |    0.996 |    0.996 |    0.996 |    0.995 |    0.990 |
| MD-CHO     |    0.999 |    0.995 |    0.976 |    0.966 |    0.974 |    0.971 |    0.975 |
| MVT-CHO    |    0.998 |    0.997 |    0.997 |    0.997 |    0.997 |    0.992 |    0.980 |
| HSNF       |    0.999 |    0.999 |    0.998 |    0.998 |    0.996 |    0.993 |    0.992 |
| LBSH       |    0.996 |    0.995 |    0.995 |    0.995 |    0.995 |    0.996 |    0.992 |

**Channel-occupancy variance**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.009 |    0.028 |    0.072 |    0.118 |    0.162 |    0.167 |    0.143 |
| ILCHO-lin  |    0.007 |    0.017 |    0.044 |    0.075 |    0.135 |    0.167 |    0.141 |
| MD-CHO     |    0.017 |    0.051 |    0.094 |    0.139 |    0.189 |    0.205 |    0.149 |
| MVT-CHO    |    0.014 |    0.030 |    0.077 |    0.114 |    0.182 |    0.195 |    0.148 |
| HSNF       |    0.017 |    0.047 |    0.095 |    0.136 |    0.185 |    0.182 |    0.143 |
| LBSH       |    0.009 |    0.019 |    0.040 |    0.070 |    0.113 |    0.158 |    0.145 |

**Outage fraction (UE-slots unserved)**

| method | 5 UE | 10 UE | 20 UE | 30 UE | 50 UE | 75 UE | 100 UE |
|---|---|---|---|---|---|---|---|
| ILCHO      |    0.000 |    0.000 |    0.003 |    0.009 |    0.038 |    0.101 |    0.156 |
| ILCHO-lin  |    0.000 |    0.000 |    0.000 |    0.001 |    0.011 |    0.028 |    0.052 |
| MD-CHO     |    0.000 |    0.023 |    0.109 |    0.181 |    0.254 |    0.307 |    0.331 |
| MVT-CHO    |    0.000 |    0.001 |    0.014 |    0.021 |    0.042 |    0.072 |    0.098 |
| HSNF       |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.000 |    0.010 |
| LBSH       |    0.000 |    0.000 |    0.000 |    0.000 |    0.001 |    0.006 |    0.025 |


![fig_fairness_cdf.png](report_assets/xeval_starlink_phase_2a_fig_fairness_cdf.png)


![fig_ho_vs_ue.png](report_assets/xeval_starlink_phase_2a_fig_ho_vs_ue.png)


![fig_hof_vs_ue.png](report_assets/xeval_starlink_phase_2a_fig_hof_vs_ue.png)


![fig_jfi_vs_ue.png](report_assets/xeval_starlink_phase_2a_fig_jfi_vs_ue.png)


![fig_load_balance.png](report_assets/xeval_starlink_phase_2a_fig_load_balance.png)


![fig_loadvar_vs_ue.png](report_assets/xeval_starlink_phase_2a_fig_loadvar_vs_ue.png)


![fig_se_vs_ue.png](report_assets/xeval_starlink_phase_2a_fig_se_vs_ue.png)


### analysis


![fig5_accessible_vs_latitude.png](report_assets/analysis_fig5_accessible_vs_latitude.png)


![ho_interval_hist.png](report_assets/analysis_ho_interval_hist.png)


![link_budget_vs_elevation.png](report_assets/analysis_link_budget_vs_elevation.png)


### sensitivity


![sensitivity.png](report_assets/sensitivity_sensitivity.png)


### sensitivity2


![sensitivity.png](report_assets/sensitivity2_sensitivity.png)
