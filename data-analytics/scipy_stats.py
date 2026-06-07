"""
SciPy Statistics distributions, hypothesis testing, curve fitting.

SciPy builds on NumPy for scientific computing. The stats module
covers everything from basic statistics to advanced hypothesis testing.
"""
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit


# =============================================================================
# PROBABILITY DISTRIBUTIONS
# =============================================================================

def distributions():
    """Common probability distributions and their operations."""
    # Normal (Gaussian) distribution
    mu, sigma = 100, 15  # Mean, standard deviation
    normal = stats.norm(loc=mu, scale=sigma)

    print("--- Normal Distribution (μ=100, σ=15) ---")
    print(f"  PDF at x=100: {normal.pdf(100):.4f}")
    print(f"  CDF at x=115: {normal.cdf(115):.4f}")  # P(X ≤ 115)
    print(f"  P(85 < X < 115): {normal.cdf(115) - normal.cdf(85):.4f}")
    print(f"  95th percentile: {normal.ppf(0.95):.2f}")
    print(f"  Random samples: {normal.rvs(size=5, random_state=42).round(1)}")

    # Confidence intervals
    ci_95 = normal.interval(0.95)
    print(f"  95% CI: ({ci_95[0]:.1f}, {ci_95[1]:.1f})")

    # Binomial distribution number of successes in n trials
    n, p = 10, 0.7
    binom = stats.binom(n=n, p=p)
    print(f"\n--- Binomial (n={n}, p={p}) ---")
    print(f"  P(X=7): {binom.pmf(7):.4f}")
    print(f"  P(X≤7): {binom.cdf(7):.4f}")
    print(f"  Mean: {binom.mean():.1f}, Var: {binom.var():.2f}")

    # Poisson distribution events per time period
    lam = 5  # Average events per period
    poisson = stats.poisson(mu=lam)
    print(f"\n--- Poisson (λ={lam}) ---")
    print(f"  P(X=3): {poisson.pmf(3):.4f}")
    print(f"  P(X≤3): {poisson.cdf(3):.4f}")

    # Exponential time between events
    rate = 2.0
    exponential = stats.expon(scale=1/rate)
    print(f"\n--- Exponential (rate={rate}) ---")
    print(f"  Mean time: {exponential.mean():.2f}")
    print(f"  P(T < 1): {exponential.cdf(1):.4f}")


# =============================================================================
# DESCRIPTIVE STATISTICS
# =============================================================================

def descriptive_stats():
    """Comprehensive descriptive statistics."""
    np.random.seed(42)
    data = np.random.normal(50, 10, 200)

    print("--- Descriptive Statistics ---")
    print(f"  Mean:     {np.mean(data):.2f}")
    print(f"  Median:   {np.median(data):.2f}")
    print(f"  Std Dev:  {np.std(data, ddof=1):.2f}")  # ddof=1 for sample
    print(f"  Variance: {np.var(data, ddof=1):.2f}")
    print(f"  Skewness: {stats.skew(data):.4f}")
    print(f"  Kurtosis: {stats.kurtosis(data):.4f}")
    print(f"  IQR:      {stats.iqr(data):.2f}")

    # Percentiles
    percentiles = np.percentile(data, [25, 50, 75, 90, 95, 99])
    print(f"  Percentiles [25,50,75,90,95,99]: {percentiles.round(1)}")

    # Mode
    mode_result = stats.mode(np.round(data).astype(int), keepdims=True)
    print(f"  Mode: {mode_result.mode[0]} (count: {mode_result.count[0]})")

    # Normality test
    stat, p_value = stats.shapiro(data[:50])  # Shapiro-Wilk (n < 5000)
    print(f"\n  Shapiro-Wilk test: stat={stat:.4f}, p={p_value:.4f}")
    print(f"  → {'Normal' if p_value > 0.05 else 'Not normal'} (α=0.05)")


# =============================================================================
# HYPOTHESIS TESTING
# =============================================================================

def hypothesis_testing():
    """Common statistical tests."""
    np.random.seed(42)

    # --- T-TEST: Compare means ---
    print("--- T-Tests ---")

    # One-sample t-test: Is the mean different from a value?
    sample = np.random.normal(52, 10, 30)  # True mean = 52
    t_stat, p_value = stats.ttest_1samp(sample, popmean=50)
    print(f"\n  One-sample t-test (H₀: μ=50):")
    print(f"    t={t_stat:.3f}, p={p_value:.4f}")
    print(f"    → {'Reject H₀' if p_value < 0.05 else 'Fail to reject H₀'}")

    # Two-sample t-test: Are two groups different?
    group_a = np.random.normal(50, 10, 50)
    group_b = np.random.normal(55, 10, 50)
    t_stat, p_value = stats.ttest_ind(group_a, group_b)
    print(f"\n  Two-sample t-test (H₀: μ_A = μ_B):")
    print(f"    t={t_stat:.3f}, p={p_value:.4f}")
    print(f"    → {'Reject H₀' if p_value < 0.05 else 'Fail to reject H₀'}")

    # Paired t-test: Before/after on same subjects
    before = np.random.normal(100, 15, 30)
    after = before + np.random.normal(5, 8, 30)  # Improvement of ~5
    t_stat, p_value = stats.ttest_rel(before, after)
    print(f"\n  Paired t-test (H₀: no difference before/after):")
    print(f"    t={t_stat:.3f}, p={p_value:.4f}")
    print(f"    Mean improvement: {(after - before).mean():.2f}")

    # --- CHI-SQUARE TEST: Association between categories ---
    print("\n--- Chi-Square Test ---")
    observed = np.array([[50, 30], [20, 40]])  # Contingency table
    chi2, p_value, dof, expected = stats.chi2_contingency(observed)
    print(f"  χ²={chi2:.3f}, p={p_value:.4f}, dof={dof}")
    print(f"  → {'Dependent' if p_value < 0.05 else 'Independent'} variables")

    # --- MANN-WHITNEY U: Non-parametric alternative to t-test ---
    print("\n--- Mann-Whitney U Test (non-parametric) ---")
    u_stat, p_value = stats.mannwhitneyu(group_a, group_b, alternative="two-sided")
    print(f"  U={u_stat:.1f}, p={p_value:.4f}")

    # --- ANOVA: Compare 3+ group means ---
    print("\n--- One-way ANOVA ---")
    g1 = np.random.normal(50, 10, 30)
    g2 = np.random.normal(55, 10, 30)
    g3 = np.random.normal(60, 10, 30)
    f_stat, p_value = stats.f_oneway(g1, g2, g3)
    print(f"  F={f_stat:.3f}, p={p_value:.4f}")
    print(f"  → {'At least one group differs' if p_value < 0.05 else 'No significant difference'}")


# =============================================================================
# CORRELATION
# =============================================================================

def correlation():
    """Correlation analysis between variables."""
    np.random.seed(42)
    n = 100

    # Generate correlated data
    x = np.random.randn(n)
    y = 2 * x + np.random.randn(n) * 0.5  # Strong positive correlation
    z = -x + np.random.randn(n) * 2       # Weak negative correlation

    print("--- Correlation ---")

    # Pearson (linear relationship, assumes normality)
    r, p = stats.pearsonr(x, y)
    print(f"  Pearson(x, y): r={r:.4f}, p={p:.6f}")

    r, p = stats.pearsonr(x, z)
    print(f"  Pearson(x, z): r={r:.4f}, p={p:.6f}")

    # Spearman (monotonic relationship, rank-based)
    rho, p = stats.spearmanr(x, y)
    print(f"  Spearman(x, y): ρ={rho:.4f}, p={p:.6f}")

    # Kendall Tau (ordinal association)
    tau, p = stats.kendalltau(x, y)
    print(f"  Kendall(x, y): τ={tau:.4f}, p={p:.6f}")


# =============================================================================
# CURVE FITTING
# =============================================================================

def curve_fitting():
    """Fit custom functions to data using least squares."""
    np.random.seed(42)

    # Generate noisy data from a known function
    x = np.linspace(0, 10, 50)
    # True function: y = 3*sin(0.5*x) + 0.1*x²
    y_true = 3 * np.sin(0.5 * x) + 0.1 * x**2
    y_noisy = y_true + np.random.normal(0, 0.5, len(x))

    # Define model function
    def model(x, a, b, c):
        return a * np.sin(b * x) + c * x**2

    # Fit the model to noisy data
    params, covariance = curve_fit(model, x, y_noisy, p0=[1, 1, 0.1])
    errors = np.sqrt(np.diag(covariance))

    print("--- Curve Fitting ---")
    print(f"  Model: y = a·sin(b·x) + c·x²")
    print(f"  True:   a=3.000, b=0.500, c=0.100")
    print(f"  Fitted: a={params[0]:.3f}±{errors[0]:.3f}, "
          f"b={params[1]:.3f}±{errors[1]:.3f}, "
          f"c={params[2]:.3f}±{errors[2]:.3f}")

    # R-squared
    y_pred = model(x, *params)
    ss_res = np.sum((y_noisy - y_pred) ** 2)
    ss_tot = np.sum((y_noisy - np.mean(y_noisy)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print(f"  R² = {r_squared:.4f}")

    # Linear regression (simpler alternative)
    print("\n--- Linear Regression ---")
    x_linear = np.random.rand(50) * 10
    y_linear = 2.5 * x_linear + 3 + np.random.randn(50) * 2

    slope, intercept, r_value, p_value, std_err = stats.linregress(x_linear, y_linear)
    print(f"  y = {slope:.3f}x + {intercept:.3f}")
    print(f"  R² = {r_value**2:.4f}, p = {p_value:.6f}")
    print(f"  Std error: {std_err:.4f}")


# =============================================================================
# CONFIDENCE INTERVALS AND EFFECT SIZE
# =============================================================================

def confidence_intervals():
    """Calculate confidence intervals and effect sizes."""
    np.random.seed(42)

    data = np.random.normal(100, 15, 50)

    print("--- Confidence Intervals ---")

    # CI for the mean using t-distribution
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)  # Standard error of the mean

    for confidence in [0.90, 0.95, 0.99]:
        ci = stats.t.interval(confidence, df=n-1, loc=mean, scale=se)
        print(f"  {confidence*100:.0f}% CI: ({ci[0]:.2f}, {ci[1]:.2f})")

    # Effect size (Cohen's d)
    print("\n--- Effect Size (Cohen's d) ---")
    group1 = np.random.normal(50, 10, 40)
    group2 = np.random.normal(55, 10, 40)

    pooled_std = np.sqrt(
        ((len(group1) - 1) * group1.std(ddof=1)**2 +
         (len(group2) - 1) * group2.std(ddof=1)**2) /
        (len(group1) + len(group2) - 2)
    )
    cohens_d = (group2.mean() - group1.mean()) / pooled_std
    print(f"  Cohen's d = {cohens_d:.3f}")
    print(f"  Interpretation: {'small' if abs(cohens_d) < 0.5 else 'medium' if abs(cohens_d) < 0.8 else 'large'}")


if __name__ == "__main__":
    print("=" * 60)
    print("SciPy Statistics Demo")
    print("=" * 60)

    print("\n")
    distributions()

    print("\n")
    descriptive_stats()

    print("\n")
    hypothesis_testing()

    print("\n")
    correlation()

    print("\n")
    curve_fitting()

    print("\n")
    confidence_intervals()
