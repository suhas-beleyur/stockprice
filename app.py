from flask import Flask, render_template, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    try:
        period = request.args.get('period', '1mo')

        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval="1d", auto_adjust=True)
        if hist.empty:
            hist = yf.download(symbol, period=period, interval="1d", auto_adjust=True)
        if hist.empty:
            return jsonify({'error': 'No data found for this symbol'}), 404

        info = getattr(stock, "fast_info", None) or {}
        current = info.get('last_price') or hist['Close'].iloc[-1]
        prev_close = info.get('previous_close') or hist['Close'].iloc[-2] if len(hist) > 1 else hist['Close'].iloc[-1]

        data = {
            'symbol': symbol.upper(),
            'currentPrice': float(current),
            'previousClose': float(prev_close),
            'change': round(current - prev_close, 2),
            'changePercent': round(((current - prev_close) / prev_close) * 100, 2) if prev_close else 0,
            'high': float(hist['High'].max()),
            'low': float(hist['Low'].min()),
            'volume': int(hist['Volume'].iloc[-1]),
            'marketCap': info.get('market_cap', 'N/A'),
            'history': [
                {
                    'date': i.strftime('%Y-%m-%d %H:%M:%S'),
                    'open': round(float(r['Open']), 2),
                    'high': round(float(r['High']), 2),
                    'low': round(float(r['Low']), 2),
                    'close': round(float(r['Close']), 2),
                    'volume': int(r['Volume'])
                } for i, r in hist.iterrows()
            ]
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f'Failed to fetch: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
