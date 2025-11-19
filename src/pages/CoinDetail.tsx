import { useParams, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, TrendingUp, Bell } from "lucide-react";
import StabilityChart from "@/components/StabilityChart";
import MetricsPanel from "@/components/MetricsPanel";
import { getMockCoinDetail, generateMockPriceData } from "@/lib/mockData";
import { useToast } from "@/hooks/use-toast";

const CoinDetail = () => {
  const { coinId } = useParams<{ coinId: string }>();
  const { toast } = useToast();
  const coin = getMockCoinDetail(coinId || "bitcoin");
  const priceData = generateMockPriceData(30);

  const handleWatchlist = () => {
    toast({
      title: "Added to Watchlist",
      description: `${coin.name} has been added to your watchlist.`,
    });
  };

  const handleAlert = () => {
    toast({
      title: "Alert Set",
      description: `You'll be notified when ${coin.symbol} risk score changes significantly.`,
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <div className="border-b border-border/50 bg-card/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="container mx-auto px-4 py-4">
          <Link to="/">
            <Button variant="ghost" size="sm" className="gap-2">
              <ArrowLeft className="w-4 h-4" />
              Back to Rankings
            </Button>
          </Link>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-4xl font-bold">{coin.name}</h1>
              <Badge variant="secondary" className="text-lg px-3 py-1">
                {coin.symbol}
              </Badge>
              <Badge variant="outline">
                Rank #{coin.rank}
              </Badge>
            </div>
            <div className="flex items-center gap-4 text-lg">
              <span className="font-mono font-bold text-2xl">
                ${coin.current_price.toLocaleString(undefined, { minimumFractionDigits: 2 })}
              </span>
              <span className={`flex items-center gap-1 font-semibold ${coin.price_change_percentage_24h >= 0 ? 'text-success' : 'text-destructive'}`}>
                <TrendingUp className={`w-5 h-5 ${coin.price_change_percentage_24h < 0 ? 'rotate-180' : ''}`} />
                {coin.price_change_percentage_24h >= 0 ? '+' : ''}
                {coin.price_change_percentage_24h.toFixed(2)}%
              </span>
            </div>
          </div>

          <div className="flex gap-3">
            <Button onClick={handleWatchlist} size="lg" className="gap-2">
              <TrendingUp className="w-4 h-4" />
              Add to Watchlist
            </Button>
            <Button onClick={handleAlert} variant="outline" size="lg" className="gap-2">
              <Bell className="w-4 h-4" />
              Set Alert
            </Button>
          </div>
        </div>

        {/* Metrics */}
        <MetricsPanel
          riskScore={coin.risk_score}
          volatilityScore={coin.volatility_score}
          liquidityScore={coin.liquidity_score}
          sentimentScore={coin.sentiment_score}
          volume24h={coin.total_volume}
          marketCap={coin.market_cap}
        />

        {/* Chart */}
        <StabilityChart data={priceData} coinSymbol={coin.symbol} />

        {/* Additional Info */}
        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-3 p-6 bg-card rounded-lg border border-border/50">
            <h3 className="text-lg font-semibold mb-4">Market Information</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">All-Time High</span>
                <span className="font-mono font-semibold">${coin.ath.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">All-Time Low</span>
                <span className="font-mono font-semibold">${coin.atl.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Circulating Supply</span>
                <span className="font-mono font-semibold">
                  {(coin.circulating_supply / 1e6).toFixed(2)}M {coin.symbol}
                </span>
              </div>
              {coin.max_supply && (
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Max Supply</span>
                  <span className="font-mono font-semibold">
                    {(coin.max_supply / 1e6).toFixed(2)}M {coin.symbol}
                  </span>
                </div>
              )}
            </div>
          </div>

          <div className="space-y-3 p-6 bg-card rounded-lg border border-border/50">
            <h3 className="text-lg font-semibold mb-4">About {coin.name}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {coin.description}
            </p>
            <div className="pt-4">
              <h4 className="text-sm font-semibold mb-2">Risk Analysis</h4>
              <p className="text-sm text-muted-foreground">
                This coin's risk score of <strong>{coin.risk_score}</strong> is calculated from volatility metrics, 
                on-chain activity, market liquidity, and sentiment analysis. Lower scores indicate more stable investments.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CoinDetail;
