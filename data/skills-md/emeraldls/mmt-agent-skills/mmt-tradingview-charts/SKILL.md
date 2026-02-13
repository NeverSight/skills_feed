---
name: mmt-tradingview-charts
description: Best practices for building charting applications using MMT real-time crypto market data with TradingView Lightweight Charts. Use when creating price charts, volume charts, indicator overlays, multi-chart dashboards, or any visualization that renders MMT data using the TradingView Lightweight Charts library.
---

# MMT + TradingView Lightweight Charts

Rules for building charting applications that render MMT market data using TradingView Lightweight Charts (v5.x).

## Chart Setup
- [Chart Initialization](rules/chart-initialization.md): createChart config, container setup, autoSize, dark/light themes
- [Data Mapping](rules/data-mapping-mmt-to-tv.md): transform MMT types (OHLCVTPublic, etc.) to Lightweight Charts format

## Real-Time Updates
- [Live Candlestick Updates](rules/realtime-candlestick-updates.md): WS candle stream to series.update(), handling candle close vs in-progress
- [Live Trade Ticker](rules/realtime-trade-ticker.md): WS trade stream to line/marker overlays, trade volume histogram

## Multi-Chart Patterns
- [Multi-Pane Layout](rules/multi-pane-layout.md): price + volume + indicator panes, synchronized time scales
- [Multi-Symbol Comparison](rules/multi-symbol-comparison.md): overlay multiple symbols, normalize price scales

## Indicators & Overlays
- [Volume Histogram](rules/indicator-volume-histogram.md): buy/sell volume from MMT candles as colored histogram
- [Funding Rate Overlay](rules/indicator-funding-rate.md): stats channel funding rate as line/baseline series
- [Open Interest Overlay](rules/indicator-open-interest.md): OI candles as area/line on separate pane

## Data Management
- [Historical Data Loading](rules/data-historical-loading.md): REST fetch to setData, pagination for long ranges, loading states
- [Timeframe & Symbol Switching](rules/data-timeframe-switching.md): clear stores, flush timers, reload on tf/symbol/exchange change

## Interaction
- [Crosshair & Tooltips](rules/interaction-crosshair-tooltips.md): subscribeCrosshairMove, custom tooltip with MMT data fields
- [Chart Lifecycle](rules/interaction-chart-lifecycle.md): React/framework integration, cleanup, resize, memory management

## Framework Integration
- [React Integration Patterns](rules/react-integration-patterns.md): hooks, refs, lifecycle, state management, performance patterns
