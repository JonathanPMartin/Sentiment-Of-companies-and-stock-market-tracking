import numpy as np
from scipy.stats import linregress, pearsonr, ttest_ind

# Sample data (replace with your actual data)
public_sentiment = np.array([0.2, 0.3, 0.5, 0.4, 0.6])
stock_value = np.array([100, 105, 110, 115, 120])

# 1. Correlation Analysis
correlation_coefficient, _ = pearsonr(public_sentiment, stock_value)
print("Correlation Coefficient:")
print(correlation_coefficient)

# 2. Linear Regression
slope, intercept, _, _, _ = linregress(public_sentiment, stock_value)
print("Linear Regression Coefficients:")
print("Slope:", slope)
print("Intercept:", intercept)

# 3. Hypothesis Testing (t-test)
t_statistic, p_value = ttest_ind(public_sentiment, stock_value)
print("t-statistic:", t_statistic)
print("p-value:", p_value)

def compare(x,y):
    public_sentiment=np.array(x)
    stock_value=np.array(y)
    correlation_coefficient, _ = pearsonr(public_sentiment, stock_value)
    slope, intercept, _, _, _ = linregress(public_sentiment, stock_value)
    t_statistic, p_value = ttest_ind(public_sentiment, stock_value)
    ReturnObject={
        "correlation_coefficient":correlation_coefficient,
        "slope":slope,
        "intercept":intercept,
        "t_statistic":t_statistic,
        "p_value":p_value
    }
    return ReturnObject
test=compare([0.2, 0.3, 0.5, 0.4, 0.6],[100, 105, 110, 115, 120])
print(test["correlation_coefficient"])