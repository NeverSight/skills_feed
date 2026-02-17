---
name: pymc
description: Use when "PyMC", "Bayesian", "MCMC", "probabilistic programming", or asking about "Bayesian regression", "hierarchical model", "NUTS sampler", "posterior distribution", "prior predictive", "credible intervals", "uncertainty quantification"
version: 1.0.0
---

<!-- Adapted from: claude-scientific-skills/scientific-skills/pymc -->

# PyMC Bayesian Modeling

Probabilistic programming with MCMC - build and fit Bayesian models.

## When to Use

- Bayesian regression and classification
- Hierarchical/multilevel models
- Uncertainty quantification
- Prior/posterior predictive checks
- Model comparison (LOO, WAIC)

## Quick Start

```python
import pymc as pm
import arviz as az
import numpy as np

# Build model
with pm.Model() as model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Likelihood
    mu = alpha + beta * X
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)

    # Sample
    idata = pm.sample(2000, tune=1000, chains=4)

# Analyze
az.summary(idata)
az.plot_posterior(idata)
```

## Model Building

```python
coords = {'predictors': ['var1', 'var2', 'var3']}

with pm.Model(coords=coords) as model:
    # Priors with dimensions
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Linear model
    mu = alpha + pm.math.dot(X, beta)

    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
```

## Common Models

### Linear Regression

```python
with pm.Model() as linear_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_features)
    sigma = pm.HalfNormal('sigma', sigma=1)

    mu = alpha + pm.math.dot(X, beta)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs)
```

### Logistic Regression

```python
with pm.Model() as logistic_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_features)

    logit_p = alpha + pm.math.dot(X, beta)
    y = pm.Bernoulli('y', logit_p=logit_p, observed=y_obs)
```

### Hierarchical Model

```python
with pm.Model(coords={'groups': group_names}) as hierarchical:
    # Hyperpriors
    mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=10)
    sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)

    # Group-level (non-centered parameterization)
    alpha_offset = pm.Normal('alpha_offset', mu=0, sigma=1, dims='groups')
    alpha = pm.Deterministic('alpha', mu_alpha + sigma_alpha * alpha_offset)

    # Likelihood
    sigma = pm.HalfNormal('sigma', sigma=1)
    y = pm.Normal('y', mu=alpha[group_idx], sigma=sigma, observed=y_obs)
```

## Sampling

```python
with model:
    # MCMC (default NUTS)
    idata = pm.sample(
        draws=2000,
        tune=1000,
        chains=4,
        target_accept=0.9,
        random_seed=42
    )

    # Variational inference (faster, approximate)
    approx = pm.fit(n=20000, method='advi')
```

## Diagnostics

```python
import arviz as az

# Check convergence
print(az.summary(idata, var_names=['alpha', 'beta', 'sigma']))

# R-hat should be < 1.01
# ESS should be > 400

# Trace plots
az.plot_trace(idata)

# Check divergences
print(f"Divergences: {idata.sample_stats.diverging.sum().values}")
```

## Predictive Checks

```python
with model:
    # Prior predictive (before fitting)
    prior_pred = pm.sample_prior_predictive(1000)
    az.plot_ppc(prior_pred, group='prior')

    # Posterior predictive (after fitting)
    pm.sample_posterior_predictive(idata, extend_inferencedata=True)
    az.plot_ppc(idata)
```

## Model Comparison

```python
# Fit models with log_likelihood
with model1:
    idata1 = pm.sample(idata_kwargs={'log_likelihood': True})

with model2:
    idata2 = pm.sample(idata_kwargs={'log_likelihood': True})

# Compare using LOO
comparison = az.compare({'model1': idata1, 'model2': idata2})
print(comparison)
```

## Predictions

```python
with model:
    pm.set_data({'X': X_new})
    post_pred = pm.sample_posterior_predictive(idata)

# Extract intervals
y_pred_mean = post_pred.posterior_predictive['y'].mean(dim=['chain', 'draw'])
y_pred_hdi = az.hdi(post_pred.posterior_predictive)
```

## Best Practices

1. **Standardize predictors** for better sampling
2. **Use weakly informative priors** (not flat)
3. **Non-centered parameterization** for hierarchical models
4. **Check diagnostics** before interpretation (R-hat, ESS)
5. **Prior predictive checks** before fitting
6. **Posterior predictive checks** after fitting

## Troubleshooting

- **Divergences** → Increase `target_accept=0.95`, use non-centered
- **Low ESS** → More draws, reparameterize
- **High R-hat** → Run longer chains

## Resources

- Docs: <https://www.pymc.io/projects/docs/>
- Examples: <https://www.pymc.io/projects/examples/>
