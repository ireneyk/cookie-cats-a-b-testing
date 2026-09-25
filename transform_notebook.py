import nbformat

with open('ab_testing_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

new_cells = []

# Cell 0: Imports
source_0 = """# 1. IMPORT ESSENTIAL LIBRARIES
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

# Set FAANG-standard visualization styles
plt.style.use('ggplot')
sns.set_theme(style="whitegrid", palette="muted")
import warnings
warnings.filterwarnings('ignore')

print("Environment Setup Complete. Ready for Analysis.")"""
cell_0 = nbformat.v4.new_code_cell(source_0)
new_cells.append(cell_0)

# Cell 1: Load to SQLite and query
source_1 = """# 2. LOAD DATA & INJECT SQL WORKFLOW
# Connect to local SQLite database
conn = sqlite3.connect('cookie_cats.db')

# Load CSV into pandas temporarily just to insert into the database
df_raw = pd.read_csv(r"C:\\Users\\Irene\\Downloads\\cookie-cats-a-b-testing-main\\cookie-cats-a-b-testing-main\\cookie-cats-ab-testing\\data\\cookie_cats.csv")
df_raw.to_sql('user_data', conn, if_exists='replace', index=False)

print("Data successfully loaded into local SQLite database: cookie_cats.db")

# Complex SQL Query: Aggregate key metrics per A/B test group
query_agg = \"\"\"
SELECT 
    version,
    COUNT(userid) AS total_users,
    SUM(sum_gamerounds) AS total_gamerounds,
    ROUND(AVG(sum_gamerounds), 2) AS avg_gamerounds,
    SUM(CASE WHEN retention_1 = 1 THEN 1 ELSE 0 END) AS retained_day_1,
    SUM(CASE WHEN retention_7 = 1 THEN 1 ELSE 0 END) AS retained_day_7,
    ROUND(CAST(SUM(CASE WHEN retention_1 = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(userid) * 100, 2) AS day_1_retention_pct,
    ROUND(CAST(SUM(CASE WHEN retention_7 = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(userid) * 100, 2) AS day_7_retention_pct
FROM user_data
GROUP BY version;
\"\"\"
df_agg = pd.read_sql(query_agg, conn)

print("\\n--- A/B Test Group Aggregated Metrics (Pulled via SQL) ---")
display(df_agg)

# Query raw data for Python visualization (excluding extreme outliers via SQL)
# We exclude the top 0.1% extreme users (e.g. played > 1000 rounds) to keep graphs readable
query_raw = \"\"\"
SELECT * 
FROM user_data 
WHERE sum_gamerounds <= 1000;
\"\"\"
df_clean = pd.read_sql(query_raw, conn)
print(f"\\nRaw data pulled for visualization: {df_clean.shape[0]:,} rows.")
"""
cell_1 = nbformat.v4.new_code_cell(source_1)
new_cells.append(cell_1)

# Cell 2: Data quality (keep from original nb.cells[2] but rename df to df_clean)
source_2 = nb.cells[2].source.replace("df.", "df_clean.")
cell_2 = nbformat.v4.new_code_cell(source_2)
new_cells.append(cell_2)

# Skip Cell 3 (SRM), Skip Cell 4 (Outliers - handled in SQL now)

# Cell 5: EDA (original index 5)
source_5 = nb.cells[5].source.replace("# 6.", "# 4.")
cell_5 = nbformat.v4.new_code_cell(source_5)
new_cells.append(cell_5)

# Cell 6: Baseline retention (original index 6)
source_6 = nb.cells[6].source.replace("# 7.", "# 5.")
cell_6 = nbformat.v4.new_code_cell(source_6)
new_cells.append(cell_6)

# Cell 7: Chi-square 1-day (original index 7)
source_7 = nb.cells[7].source.replace("# 8.", "# 6.")
cell_7 = nbformat.v4.new_code_cell(source_7)
new_cells.append(cell_7)

# Cell 8: Chi-square 7-day (original index 8)
source_8 = nb.cells[8].source.replace("# 9.", "# 7.")
cell_8 = nbformat.v4.new_code_cell(source_8)
new_cells.append(cell_8)

# Skip Cell 9 (Mann-Whitney)
# Skip Cell 10 (Bootstrapping)

# Create final markdown cell for Recommendation based on JD
source_11 = """# 8. Product Analysis & Final Recommendation

### Objective
Determine if moving the first gate from level 30 to level 40 impacts player retention and engagement.

### Hypothesis
Moving the gate to level 40 delays the first "pause" in gameplay, potentially improving early engagement (rounds played) but we need to ensure it doesn't negatively impact short-term (Day 1) or long-term (Day 7) retention.

### Key Metrics Tracked
* **Conversion / Volume**: Users assigned to `gate_30` vs `gate_40`
* **User Engagement**: Distribution of rounds played
* **Retention Rates**: Day 1 and Day 7 drop-off

### Experiment Results
* **Engagement**: Players in `gate_40` tend to play slightly more rounds, likely because they don't hit a paywall/wait-wall until level 40.
* **Day 1 Retention**: Minor decrease when the gate is moved to level 40.
* **Day 7 Retention**: Statistically significant drop in retention for `gate_40`.

### Final Product Recommendation
**Do not move the gate to level 40.**
While it might seem counterintuitive, hitting the gate earlier at level 30 actually acts as a natural break for players, improving their long-term Day 7 retention. This "delayed gratification" keeps players coming back, increasing the overall lifespan of the player in the game. Sticking with `gate_30` maximizes long-term player retention.
"""
cell_11 = nbformat.v4.new_markdown_cell(source_11)
new_cells.append(cell_11)

nb.cells = new_cells

with open('ab_testing_analysis.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook successfully transformed!")
