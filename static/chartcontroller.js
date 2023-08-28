function initializeWidget(symbol) {
    new TradingView.widget({
      container_id: 'tradingview-chart',
      symbol: 'BINANCE:' + symbol + 'PERP',
      // other options here...
    });
  }

  function updateChart(symbol) {
    // Remove existing widget
    document.getElementById('tradingview-chart').innerHTML = '';
    
    // Initialize a new widget with the selected symbol
    initializeWidget(symbol);
  }

  // Initialize the default symbol
  initializeWidget('1INCHUSDT');