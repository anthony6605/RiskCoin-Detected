import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search, TrendingUp, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { searchCoins } from "@/lib/mockData";

const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<ReturnType<typeof searchCoins>>([]);
  const navigate = useNavigate();

  const handleSearch = (value: string) => {
    setQuery(value);
    const results = searchCoins(value);
    setSuggestions(results);
  };

  const handleSelect = (coinId: string) => {
    navigate(`/coin/${coinId}`);
    setQuery("");
    setSuggestions([]);
  };
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && query.length > 2) {
      // Navigate to first suggestion or create dynamic coin page
      if (suggestions.length > 0) {
        handleSelect(suggestions[0].id);
      } else {
        handleSelect(query.toLowerCase().replace(/\s+/g, '-'));
      }
    }
  };

  return (
    <div className="relative w-full max-w-2xl mx-auto">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
        <Input
          type="text"
          placeholder="Search 10,000+ coins (e.g., BTC, Ethereum, Cardano)..."
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          onKeyPress={handleKeyPress}
          className="pl-12 pr-4 h-14 text-lg bg-card border-border/50 focus:border-primary/50 focus:ring-primary/20"
        />
        {query.length === 0 && (
          <div className="absolute right-4 top-1/2 -translate-y-1/2">
            <Badge variant="secondary" className="gap-1 text-xs">
              <Sparkles className="w-3 h-3" />
              10,000+ Coins
            </Badge>
          </div>
        )}
      </div>

      {/* Suggestions Dropdown */}
      {suggestions.length > 0 && (
        <div className="absolute top-full mt-2 w-full bg-card border border-border/50 rounded-lg shadow-elevated overflow-hidden z-50 animate-slide-up">
          {suggestions.map((coin) => (
            <button
              key={coin.id}
              onClick={() => handleSelect(coin.id)}
              className="w-full px-4 py-3 flex items-center gap-3 hover:bg-card-elevated transition-colors text-left"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold">{coin.name}</span>
                  <span className="text-sm text-muted-foreground">{coin.symbol}</span>
                  {coin.rank > 20 && (
                    <Badge variant="outline" className="text-xs">
                      #{coin.rank}
                    </Badge>
                  )}
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <span className="font-mono">${coin.current_price.toLocaleString()}</span>
                  <span className={coin.price_change_percentage_24h >= 0 ? 'text-success' : 'text-destructive'}>
                    {coin.price_change_percentage_24h >= 0 ? '+' : ''}
                    {coin.price_change_percentage_24h.toFixed(2)}%
                  </span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-muted-foreground mb-1">Risk</div>
                <div className="text-lg font-bold" style={{ color: `hsl(${120 - coin.risk_score * 1.2} 70% 50%)` }}>
                  {coin.risk_score}
                </div>
              </div>
            </button>
          ))}
        </div>
      )}
      
      {/* No results but query exists */}
      {query.length > 2 && suggestions.length === 0 && (
        <div className="absolute top-full mt-2 w-full bg-card border border-border/50 rounded-lg shadow-elevated overflow-hidden z-50 animate-slide-up p-4 text-center">
          <p className="text-sm text-muted-foreground mb-2">
            Press <kbd className="px-2 py-1 text-xs bg-muted rounded">Enter</kbd> to analyze "{query}"
          </p>
          <p className="text-xs text-muted-foreground">
            Our system can analyze any cryptocurrency
          </p>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
