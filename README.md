#  Cookie Cats A/B Testing: Retention Analysis

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-Statistical_Testing-8CAAE6.svg?style=for-the-badge&logo=scipy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)

##  Executive Summary

**Goal:** Evaluate the impact of moving an in-app progression gate from Level 30 to Level 40 on player retention in the mobile game *Cookie Cats*.

> **Verdict: Reject the rollout.** > The A/B test data strongly indicates that moving the gate to Level 40 causes a statistically significant decrease in 7-day retention (p < 0.05).

**Recommendation:** Keep the gate at Level 30. The early gate acts as a natural break, preventing hedonic adaptation (player burnout) and extending the overall lifecycle and monetization window of the user. Our bootstrap analysis indicates a **99.9% probability** that keeping the gate at Level 30 results in higher long-term retention.

---

##  Project Context

*Cookie Cats* is a hugely popular mobile puzzle game. As players progress, they encounter "gates" that force them to wait or make an in-app purchase to continue.

**The Experiment:**
* **Control Group (`gate_30`):** Players encounter the first gate at Level 30.
* **Treatment Group (`gate_40`):** Players encounter the first gate at Level 40.

**The Objective:** Determine if delaying the first gate increases, decreases, or has no effect on user engagement and retention.

---

##  Methodology & Statistical Rigor

This project goes beyond basic averages to apply industry-standard statistical rigor to a dataset of **90,000+ players**:

* **Data Cleaning & Outlier Detection:** Identified and removed extreme anomalies (e.g., users with 49,000+ game rounds in 14 days) using 99.9th percentile thresholding to prevent skewed means.
* **Sample Ratio Mismatch (SRM) Check:** Conducted a Goodness-of-Fit Chi-Square test to verify the integrity of the randomized 50/50 split (p > 0.05, no SRM detected).
* **Categorical Testing (Retention):** Deployed **Chi-Square Tests of Independence** to measure the statistical significance of 1-Day and 7-Day retention rate changes.
* **Continuous Testing (Game Rounds):** Utilized the non-parametric **Mann-Whitney U Test** to analyze total game rounds, bypassing the T-Test due to the heavily right-skewed nature of gaming engagement data.
* **Bootstrapping:** Resampled the dataset 10,000 times to construct a confidence interval for the percent difference in retention, proving the superiority of the Control group with ~99.9% certainty.

---

##  Key Findings

| Metric | Statistical Result | Business Impact |
| :--- | :--- | :--- |
| **Day 1 Retention** | No significant impact (p > 0.05) | Moving the gate does not affect immediate drop-off. |
| **Day 7 Retention** | **Significant drop** (p < 0.05) | Delaying the gate actively harms long-term user retention. |
| **Game Rounds** | **Significant difference** | The Mann-Whitney U test favored the earlier gate for overall engagement. |

### The "So What?"
While it seems intuitive to let players play longer before hitting a paywall, forcing a break earlier (Level 30) creates positive friction. This prevents players from bingeing the game too heavily in one sitting, thereby mitigating **hedonic adaptation** and ensuring they return the following week.

---

## 🚀 How to Run the Analysis

1. **Clone this repository:**
   ```bash
   git clone [https://github.com/yourusername/cookie-cats-ab-testing.git](https://github.com/yourusername/cookie-cats-ab-testing.git)
