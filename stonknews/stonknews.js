import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Search, Loader2, AlertCircle } from 'lucide-react';

const StockNewsAnalyzer = () => {
  const [ticker, setTicker] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');

  const analyzeStock = async () => {
    if (!ticker.trim()) {
      setError('Please enter a stock ticker');
      return;
    }

    setLoading(true);
    setError('');
    setAnalysis(null);

    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 1000,
          messages: [{
            role: 'user',
            content: `Search for the latest news about ${ticker.toUpperCase()} stock and analyze:
1. Current stock price trend (up/down/stable)
2. Recent news headlines affecting the stock
3. Sentiment analysis (positive/negative/neutral)
4. Key bullet points explaining why the stock is moving based on the news

Format your response as JSON with this structure:
{
  "ticker": "${ticker.toUpperCase()}",
  "trend": "up/down/stable",
  "currentPrice": "approximate price if available",
  "priceChange": "percentage change if available",
  "sentiment": "positive/negative/neutral",
  "headlines": ["headline 1", "headline 2", "headline 3"],
  "reasons": ["reason 1", "reason 2", "reason 3"],
  "summary": "brief overall summary"
}

Only return the JSON object, no other text.`
          }],
          tools: [{
            type: "web_search_20250305",
            name: "web_search"
          }]
        })
      });

      const data = await response.json();
      
      let fullText = '';
      if (data.content) {
        for (const item of data.content) {
          if (item.type === 'text') {
            fullText += item.text;
          }
        }
      }

      const jsonMatch = fullText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const cleanJson = jsonMatch[0].replace(/```json|```/g, '').trim();
        const parsed = JSON.parse(cleanJson);
        setAnalysis(parsed);
      } else {
        setError('Unable to parse analysis results');
      }
    } catch (err) {
      setError('Error analyzing stock: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      analyzeStock();
    }
  };

  const getSentimentColor = (sentiment) => {
    switch(sentiment?.toLowerCase()) {
      case 'positive': return 'text-green-600';
      case 'negative': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getTrendIcon = (trend) => {
    if (trend?.toLowerCase() === 'up') {
      return <TrendingUp className="text-green-600" size={32} />;
    } else if (trend?.toLowerCase() === 'down') {
      return <TrendingDown className="text-red-600" size={32} />;
    }
    return <div className="text-gray-600 text-2xl">→</div>;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Stock News Sentiment Analyzer
          </h1>
          <p className="text-gray-600 mb-6">
            Analyze how recent news impacts stock prices with AI-powered sentiment analysis
          </p>

          <div className="flex gap-3">
            <input
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              onKeyPress={handleKeyPress}
              placeholder="Enter stock ticker (e.g., AAPL, TSLA, NVDA)"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={analyzeStock}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin" size={20} />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search size={20} />
                  Analyze
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="text-red-600 flex-shrink-0" size={20} />
              <p className="text-red-800">{error}</p>
            </div>
          )}
        </div>

        {analysis && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex items-center justify-between mb-6 pb-6 border-b">
              <div>
                <h2 className="text-3xl font-bold text-gray-800">
                  {analysis.ticker}
                </h2>
                {analysis.currentPrice && (
                  <p className="text-2xl text-gray-700 mt-1">
                    ${analysis.currentPrice}
                    {analysis.priceChange && (
                      <span className={analysis.trend === 'up' ? 'text-green-600 ml-2' : 'text-red-600 ml-2'}>
                        ({analysis.priceChange})
                      </span>
                    )}
                  </p>
                )}
              </div>
              <div className="flex flex-col items-center gap-2">
                {getTrendIcon(analysis.trend)}
                <span className={`font-semibold text-lg ${getSentimentColor(analysis.sentiment)}`}>
                  {analysis.sentiment?.toUpperCase()}
                </span>
              </div>
            </div>

            {analysis.summary && (
              <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-2">Summary</h3>
                <p className="text-gray-700">{analysis.summary}</p>
              </div>
            )}

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">
                Recent Headlines
              </h3>
              <div className="space-y-2">
                {analysis.headlines?.map((headline, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                    <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0" />
                    <p className="text-gray-700">{headline}</p>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-3">
                Key Factors Driving Stock Movement
              </h3>
              <div className="space-y-3">
                {analysis.reasons?.map((reason, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-4 border-l-4 border-blue-600 bg-gray-50 rounded-r-lg">
                    <span className="font-bold text-blue-600 flex-shrink-0">
                      {idx + 1}.
                    </span>
                    <p className="text-gray-700">{reason}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="mt-6 text-center text-sm text-gray-600">
          <p>Try popular stocks: AAPL, TSLA, NVDA, MSFT, GOOGL</p>
        </div>
      </div>
    </div>
  );
};

export default StockNewsAnalyzer;