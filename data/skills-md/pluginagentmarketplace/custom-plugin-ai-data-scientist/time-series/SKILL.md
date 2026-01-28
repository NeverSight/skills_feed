---
name: time-series
description: ARIMA, SARIMA, Prophet, trend analysis, seasonality detection, anomaly detection, and forecasting methods. Use for time-based predictions, demand forecasting, or temporal pattern analysis.
sasmp_version: "1.3.0"
bonded_agent: 02-mathematics-statistics
bond_type: PRIMARY_BOND
---

# Time Series Analysis & Forecasting

Analyze temporal data patterns and build accurate forecasting models.

## Quick Start

### Data Preparation
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load time series data
df = pd.read_csv('sales.csv', parse_dates=['date'], index_col='date')

# Ensure proper datetime index
df.index = pd.DatetimeIndex(df.index, freq='D')

# Basic exploration
print(df.head())
print(df.describe())

# Visualize
df['value'].plot(figsize=(12, 4), title='Time Series')
plt.show()
```

### Decomposition
```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Additive decomposition
decomposition = seasonal_decompose(df['value'], model='additive', period=7)

fig, axes = plt.subplots(4, 1, figsize=(12, 10))
decomposition.observed.plot(ax=axes[0], title='Original')
decomposition.trend.plot(ax=axes[1], title='Trend')
decomposition.seasonal.plot(ax=axes[2], title='Seasonality')
decomposition.resid.plot(ax=axes[3], title='Residual')
plt.tight_layout()
plt.show()
```

## Statistical Tests

### Stationarity Tests
```python
from statsmodels.tsa.stattools import adfuller, kpss

def check_stationarity(series):
    """Test for stationarity using ADF and KPSS tests"""

    # ADF Test (H0: series has unit root, i.e., non-stationary)
    adf_result = adfuller(series, autolag='AIC')
    adf_pvalue = adf_result[1]

    # KPSS Test (H0: series is stationary)
    kpss_result = kpss(series, regression='c')
    kpss_pvalue = kpss_result[1]

    print("Stationarity Test Results:")
    print(f"ADF Statistic: {adf_result[0]:.4f}")
    print(f"ADF p-value: {adf_pvalue:.4f}")
    print(f"KPSS Statistic: {kpss_result[0]:.4f}")
    print(f"KPSS p-value: {kpss_pvalue:.4f}")

    if adf_pvalue < 0.05 and kpss_pvalue > 0.05:
        print("Conclusion: Series is STATIONARY")
        return True
    elif adf_pvalue > 0.05 and kpss_pvalue < 0.05:
        print("Conclusion: Series is NON-STATIONARY")
        return False
    else:
        print("Conclusion: Inconclusive - consider differencing")
        return None

is_stationary = check_stationarity(df['value'])
```

### Making Series Stationary
```python
def make_stationary(series, max_diff=2):
    """Apply differencing to make series stationary"""
    diff_series = series.copy()
    d = 0

    while d < max_diff:
        if check_stationarity(diff_series.dropna()):
            break
        diff_series = diff_series.diff()
        d += 1

    return diff_series.dropna(), d

stationary_series, d_order = make_stationary(df['value'])
print(f"Differencing order: {d_order}")
```

## ARIMA / SARIMA

### ACF/PACF Analysis
```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, axes = plt.subplots(1, 2, figsize=(14, 4))

plot_acf(stationary_series, lags=40, ax=axes[0])
axes[0].set_title('Autocorrelation (ACF)')

plot_pacf(stationary_series, lags=40, ax=axes[1])
axes[1].set_title('Partial Autocorrelation (PACF)')

plt.tight_layout()
plt.show()

# Reading ACF/PACF:
# - PACF cuts off after lag p -> AR(p)
# - ACF cuts off after lag q -> MA(q)
# - Both decay -> ARMA(p, q)
```

### Auto ARIMA
```python
from pmdarima import auto_arima

# Automatic order selection
auto_model = auto_arima(
    df['value'],
    start_p=0, max_p=5,
    start_q=0, max_q=5,
    d=None,  # Auto-detect differencing
    seasonal=True,
    m=7,  # Weekly seasonality
    start_P=0, max_P=2,
    start_Q=0, max_Q=2,
    D=None,
    trace=True,
    error_action='ignore',
    suppress_warnings=True,
    stepwise=True,
    information_criterion='aic'
)

print(auto_model.summary())
print(f"Best order: {auto_model.order}")
print(f"Seasonal order: {auto_model.seasonal_order}")
```

### Manual SARIMA
```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Train/test split
train = df['value'][:-30]
test = df['value'][-30:]

# Fit SARIMA model
model = SARIMAX(
    train,
    order=(1, 1, 1),           # (p, d, q)
    seasonal_order=(1, 1, 1, 7),  # (P, D, Q, m)
    enforce_stationarity=False,
    enforce_invertibility=False
)

results = model.fit(disp=False)
print(results.summary())

# Diagnostics
results.plot_diagnostics(figsize=(12, 8))
plt.tight_layout()
plt.show()

# Forecast
forecast = results.get_forecast(steps=30)
forecast_mean = forecast.predicted_mean
forecast_ci = forecast.conf_int()

# Plot
plt.figure(figsize=(12, 5))
plt.plot(train.index, train, label='Training')
plt.plot(test.index, test, label='Actual')
plt.plot(test.index, forecast_mean, label='Forecast', color='red')
plt.fill_between(
    test.index,
    forecast_ci.iloc[:, 0],
    forecast_ci.iloc[:, 1],
    alpha=0.3
)
plt.legend()
plt.title('SARIMA Forecast')
plt.show()
```

## Prophet

```python
from prophet import Prophet

# Prepare data (Prophet requires 'ds' and 'y' columns)
prophet_df = df.reset_index()
prophet_df.columns = ['ds', 'y']

# Initialize and fit
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='multiplicative',
    changepoint_prior_scale=0.05,
    seasonality_prior_scale=10
)

# Add custom seasonality
model.add_seasonality(name='monthly', period=30.5, fourier_order=5)

# Add holidays (optional)
model.add_country_holidays(country_name='US')

model.fit(prophet_df)

# Create future dataframe
future = model.make_future_dataframe(periods=30)

# Predict
forecast = model.predict(future)

# Visualize
fig1 = model.plot(forecast)
plt.title('Prophet Forecast')
plt.show()

# Components
fig2 = model.plot_components(forecast)
plt.show()

# Cross-validation
from prophet.diagnostics import cross_validation, performance_metrics

df_cv = cross_validation(
    model,
    initial='365 days',
    period='30 days',
    horizon='30 days'
)
df_metrics = performance_metrics(df_cv)
print(df_metrics[['horizon', 'mape', 'rmse', 'mae']])
```

## Exponential Smoothing

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Simple Exponential Smoothing
from statsmodels.tsa.api import SimpleExpSmoothing

ses_model = SimpleExpSmoothing(train).fit(
    smoothing_level=0.3,
    optimized=True
)

# Holt-Winters (Triple Exponential Smoothing)
hw_model = ExponentialSmoothing(
    train,
    trend='add',        # 'add', 'mul', or None
    seasonal='add',     # 'add', 'mul', or None
    seasonal_periods=7
).fit(
    smoothing_level=0.3,
    smoothing_trend=0.1,
    smoothing_seasonal=0.1,
    optimized=True
)

# Forecast
hw_forecast = hw_model.forecast(steps=30)

# Compare
plt.figure(figsize=(12, 5))
plt.plot(train, label='Training')
plt.plot(test, label='Test')
plt.plot(test.index, hw_forecast, label='Holt-Winters', color='red')
plt.legend()
plt.show()
```

## Deep Learning for Time Series

### LSTM
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

class LSTMForecaster(nn.Module):
    """LSTM for time series forecasting"""

    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            dropout=0.2
        )
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)

        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


def create_sequences(data, seq_length):
    """Create sequences for LSTM"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# Prepare data
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df['value'].values.reshape(-1, 1))

seq_length = 30
X, y = create_sequences(scaled_data, seq_length)

# Convert to tensors
X_tensor = torch.FloatTensor(X)
y_tensor = torch.FloatTensor(y)

# Train/test split
train_size = int(0.8 * len(X))
X_train, X_test = X_tensor[:train_size], X_tensor[train_size:]
y_train, y_test = y_tensor[:train_size], y_tensor[train_size:]

# Training
model = LSTMForecaster()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    output = model(X_train)
    loss = criterion(output, y_train)
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')
```

### Transformer for Time Series
```python
class TimeSeriesTransformer(nn.Module):
    """Transformer for time series forecasting"""

    def __init__(self, input_size=1, d_model=64, nhead=4,
                 num_layers=2, output_size=1, seq_length=30):
        super().__init__()

        self.embedding = nn.Linear(input_size, d_model)
        self.pos_encoding = nn.Parameter(torch.randn(1, seq_length, d_model))

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=256,
            dropout=0.1,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)

        self.fc = nn.Linear(d_model, output_size)

    def forward(self, x):
        x = self.embedding(x) + self.pos_encoding
        x = self.transformer(x)
        x = self.fc(x[:, -1, :])
        return x
```

## Anomaly Detection

```python
from sklearn.ensemble import IsolationForest
from scipy import stats

def detect_anomalies(series, method='zscore', threshold=3):
    """Detect anomalies using various methods"""

    if method == 'zscore':
        z_scores = np.abs(stats.zscore(series))
        anomalies = z_scores > threshold

    elif method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        anomalies = (series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)

    elif method == 'isolation_forest':
        model = IsolationForest(contamination=0.05, random_state=42)
        predictions = model.fit_predict(series.values.reshape(-1, 1))
        anomalies = predictions == -1

    elif method == 'rolling':
        rolling_mean = series.rolling(window=7).mean()
        rolling_std = series.rolling(window=7).std()
        upper = rolling_mean + threshold * rolling_std
        lower = rolling_mean - threshold * rolling_std
        anomalies = (series > upper) | (series < lower)

    return anomalies

# Detect and visualize
anomalies = detect_anomalies(df['value'], method='zscore')

plt.figure(figsize=(12, 5))
plt.plot(df.index, df['value'], label='Value')
plt.scatter(df.index[anomalies], df['value'][anomalies],
            color='red', label='Anomalies')
plt.legend()
plt.title('Anomaly Detection')
plt.show()
```

## Feature Engineering

```python
def create_time_features(df):
    """Create time-based features"""
    df = df.copy()

    # Calendar features
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['dayofmonth'] = df.index.day
    df['month'] = df.index.month
    df['quarter'] = df.index.quarter
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['weekofyear'] = df.index.isocalendar().week

    # Cyclical encoding (for periodic features)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['dayofweek_sin'] = np.sin(2 * np.pi * df['dayofweek'] / 7)
    df['dayofweek_cos'] = np.cos(2 * np.pi * df['dayofweek'] / 7)

    # Boolean features
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    df['is_month_start'] = df.index.is_month_start.astype(int)
    df['is_month_end'] = df.index.is_month_end.astype(int)

    return df


def create_lag_features(df, target_col, lags):
    """Create lag features"""
    df = df.copy()

    for lag in lags:
        df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)

    return df


def create_rolling_features(df, target_col, windows):
    """Create rolling window features"""
    df = df.copy()

    for window in windows:
        df[f'{target_col}_rolling_mean_{window}'] = df[target_col].rolling(window).mean()
        df[f'{target_col}_rolling_std_{window}'] = df[target_col].rolling(window).std()
        df[f'{target_col}_rolling_min_{window}'] = df[target_col].rolling(window).min()
        df[f'{target_col}_rolling_max_{window}'] = df[target_col].rolling(window).max()

    return df

# Apply feature engineering
df_features = create_time_features(df)
df_features = create_lag_features(df_features, 'value', [1, 7, 14, 30])
df_features = create_rolling_features(df_features, 'value', [7, 14, 30])
```

## Evaluation Metrics

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_forecast(actual, predicted):
    """Calculate forecasting metrics"""

    mae = mean_absolute_error(actual, predicted)
    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100

    # Symmetric MAPE (handles zeros better)
    smape = np.mean(2 * np.abs(actual - predicted) /
                    (np.abs(actual) + np.abs(predicted))) * 100

    print(f"MAE:   {mae:.4f}")
    print(f"RMSE:  {rmse:.4f}")
    print(f"MAPE:  {mape:.2f}%")
    print(f"sMAPE: {smape:.2f}%")

    return {'mae': mae, 'rmse': rmse, 'mape': mape, 'smape': smape}

metrics = evaluate_forecast(test, forecast_mean)
```

## Common Issues & Solutions

**Issue: Non-stationary series**
```
Solutions:
- Apply differencing (1st or 2nd order)
- Log transformation for variance stabilization
- Detrending (subtract moving average)
- Seasonal differencing for seasonal data
```

**Issue: Overfitting on training data**
```
Solutions:
- Use proper cross-validation (TimeSeriesSplit)
- Reduce model complexity
- Regularization
- More training data
```

**Issue: Poor forecast accuracy**
```
Solutions:
- Check for data quality issues
- Try different models
- Include external regressors
- Ensemble multiple models
- Feature engineering
```

## Best Practices

1. **Always visualize** your time series first
2. **Check stationarity** before modeling
3. **Use appropriate train/test split** (no shuffling!)
4. **Validate with time-based CV** (TimeSeriesSplit)
5. **Include confidence intervals** in forecasts
6. **Monitor model performance** over time
7. **Update models** as new data arrives
8. **Document seasonality** and trends
