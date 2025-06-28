
# ⚽ Goals Scored Analysis: Men's vs Women's FIFA World Cup Matches

This project analyzes and compares goal-scoring patterns between men's and women's FIFA World Cup matches from 2002 onward. Using Python, we conduct data filtering, visualization, and non-parametric statistical testing to determine whether there is a significant difference in goals scored.

---

## 📌 Project Objectives

- Compare **goals scored** in men's and women's FIFA World Cup matches since 2002  
- Evaluate **distribution of goals** and assess normality  
- Conduct a **Mann-Whitney U test** to determine if women's matches tend to have more goals  

---

## 📁 Data Source

- `men_results.csv`: Match results for men's international teams  
- `women_results.csv`: Match results for women's international teams  

---

## 🔍 Key Steps & Code

### 🧹 1. Data Loading & Preparation

- Loads match data from CSVs  
- Filters matches played **after 2002** in the **FIFA World Cup**  
- Adds `goals_scored` and `group` columns

```python
import pandas as pd
import matplotlib.pyplot as plt
import pingouin
from scipy.stats import mannwhitneyu

# Load men's and women's datasets
men = pd.read_csv("men_results.csv")
women = pd.read_csv("women_results.csv")

# Filter for FIFA World Cup matches after 2002
men["date"] = pd.to_datetime(men["date"])
men_subset = men[(men["date"] > "2002-01-01") & (men["tournament"].isin(["FIFA World Cup"]))]
women["date"] = pd.to_datetime(women["date"])
women_subset = women[(women["date"] > "2002-01-01") & (women["tournament"].isin(["FIFA World Cup"]))]

# Add group and goals_scored
men_subset["group"] = "men"
women_subset["group"] = "women"
men_subset["goals_scored"] = men_subset["home_score"] + men_subset["away_score"]
women_subset["goals_scored"] = women_subset["home_score"] + women_subset["away_score"]
```

---

### 📈 2. Normality Check

- **Visualizes Distribution**: Plots histograms of `goals_scored` for men’s matches  
- **Conclusion**: Goals scored are **not normally distributed**, justifying the use of a **non-parametric** test

```python
men_subset["goals_scored"].hist()
plt.show()
plt.clf()
```

---

### 🔢 3. Statistical Testing

- **Mann-Whitney U Test (Pingouin)**: Tests if **women's matches have higher goals scored**  
- **Alternative SciPy Method**: Uses `scipy.stats.mannwhitneyu` to replicate the test  
- **Decision Rule**: Compares p-value to **significance level = 0.01**

```python
# Combine datasets
both = pd.concat([women_subset, men_subset], axis=0, ignore_index=True)
both_subset = both[["goals_scored", "group"]]
both_subset_wide = both_subset.pivot(columns="group", values="goals_scored")

# Pingouin Mann-Whitney U Test
results_pg = pingouin.mwu(
    x=both_subset_wide["women"],
    y=both_subset_wide["men"],
    alternative="greater"
)

# SciPy Alternative
results_scipy = mannwhitneyu(
    x=women_subset["goals_scored"],
    y=men_subset["goals_scored"],
    alternative="greater"
)

# p-value and decision
p_val = results_pg["p-val"].values[0]
result = "reject" if p_val <= 0.01 else "fail to reject"
result_dict = {"p_val": p_val, "result": result}
```

---

## 📊 Sample Insights

- ⚽ Women’s FIFA World Cup matches post-2002 may have **significantly more goals** than men's  
- 🔍 **Non-normal distribution** of scores validates the **Mann-Whitney U test**  
- 📉 The result (`p_val`, `reject`/`fail to reject`) provides statistical evidence for comparison  

---

## 💻 Tech Stack

- **Python**: Core data processing and analysis  
- **pandas**: Data manipulation, filtering, merging  
- **matplotlib**: Visualizations (goal distribution histograms)  
- **pingouin** & **SciPy**: Non-parametric hypothesis testing  
- **CSV files**: Input data for men's and women's match results  

---

## 🧠 Why This Project?

This analysis offers a statistically grounded comparison of scoring trends in elite international football. It can inform:

- 🧮 **Sports Analytics**: For scouting, coaching, and performance metrics  
- 📣 **Fan Engagement**: Use insights to highlight game dynamics  
- 🧪 **Statistical Learning**: Real-world example of using **non-parametric tests** on skewed data

---

