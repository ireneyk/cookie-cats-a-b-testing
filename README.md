# Cookie Cats A/B Test - Product Analysis

## Objective
To determine if moving the first gameplay gate from level 30 to level 40 impacts player retention and engagement. We want to understand whether delaying the wait-time/paywall increases early user engagement without sacrificing long-term retention.

## Hypothesis
Moving the gate to level 40 delays the first "pause" in gameplay, which may improve early engagement (total game rounds played). However, we must ensure it doesn't negatively impact short-term (Day 1) or long-term (Day 7) retention.

## Key Metrics Tracked
* **Conversion / Volume**: Users assigned to `gate_30` vs `gate_40` test groups.
* **User Engagement**: The distribution of rounds played between the control and test groups.
* **Retention Rates**: Day-1 and Day-7 drop-off rates across both groups.

## Experiment Results
After analyzing a dataset of 90,000+ players using SQL and Python:
* **Engagement**: Players in the `gate_40` group tended to play slightly more rounds initially. This aligns with our hypothesis that delaying the gate keeps users playing longer in their very first sessions.
* **Day-1 Retention**: There was a slight decrease in 1-day retention when the gate was moved to level 40 (44.2% vs 44.8%).
* **Day-7 Retention**: There was a statistically significant drop in 7-day retention for the `gate_40` group (18.2% vs 19.0%). 

## Final Product Recommendation
**Do not move the gate to level 40.**
While it might seem counterintuitive to put a pause in gameplay earlier, hitting the gate at level 30 acts as a natural break for players. This "delayed gratification" actually improves their long-term Day-7 retention. Players are more likely to return to the game if they are forced to take a break, rather than playing until they burn out. Sticking with `gate_30` maximizes long-term player retention.

---
*Note: The data pipeline was upgraded to use a local SQLite database for robust SQL aggregation before running statistical tests in Python. A complementary Tableau/Power BI dashboard connects to this database for automated metric reporting.*
