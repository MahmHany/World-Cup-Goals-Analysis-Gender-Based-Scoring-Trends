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

# Add group and goals_scored columns
men_subset["group"] = "men"
women_subset["group"] = "women"
men_subset["goals_scored"] = men_subset["home_score"] + men_subset["away_score"]
women_subset["goals_scored"] = women_subset["home_score"] + women_subset["away_score"]

# Normality Check: Histogram for men's goals scored
men_subset["goals_scored"].hist()
plt.title("Distribution of Goals Scored - Men")
plt.xlabel("Goals Scored")
plt.ylabel("Frequency")
plt.show()
plt.clf()

# Combine datasets for testing
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

# Extract p-value and decision
p_val = results_pg["p-val"].values[0]
result = "reject" if p_val <= 0.01 else "fail to reject"
result_dict = {"p_val": p_val, "result": result}

# Print Results
print("Pingouin Mann-Whitney U Test Results:")
print(results_pg)
print("\nSciPy Mann-Whitney U Test Results:")
print(results_scipy)
print("\nConclusion:", result_dict)
