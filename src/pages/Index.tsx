import { useState } from "react";
import CoinCard from "@/components/CoinCard";
import SearchBar from "@/components/SearchBar";
import { mockTopCoins } from "@/lib/mockData";
import { Button } from "@/components/ui/button";
import { TrendingUp, Shield, Activity, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/card";

const Index = () => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-background via-card to-background border-b border-border/50">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,hsl(var(--primary)/0.1),transparent)]" />
        <div className="container mx-auto px-4 py-16 relative">
          <div className="text-center space-y-6 max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium mb-4">
              <Activity className="w-4 h-4" />
              <span>Tracking 10,000+ Cryptocurrencies</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
              Crypto Risk
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                Analyzer
              </span>
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Discover the top 20 coins to invest in today, or search any cryptocurrency for 
              comprehensive risk analysis. Powered by advanced data engineering analyzing volatility, 
              liquidity, sentiment, and on-chain metrics.
            </p>

            <div className="pt-6">
              <SearchBar />
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto pt-8">
              <Card className="p-4 bg-card/50 backdrop-blur-sm border-border/50">
                <div className="text-3xl font-bold text-primary mb-1">10K+</div>
                <div className="text-sm text-muted-foreground">Coins Available</div>
              </Card>
              <Card className="p-4 bg-card/50 backdrop-blur-sm border-border/50">
                <div className="text-3xl font-bold text-accent mb-1">24/7</div>
                <div className="text-sm text-muted-foreground">Live Updates</div>
              </Card>
              <Card className="p-4 bg-card/50 backdrop-blur-sm border-border/50">
                <div className="text-3xl font-bold text-success mb-1">5+</div>
                <div className="text-sm text-muted-foreground">Risk Metrics</div>
              </Card>
            </div>
          </div>
        </div>
      </div>

      {/* Top Coins Section */}
      <div className="container mx-auto px-4 py-12">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-primary" />
          <div>
            <h2 className="text-3xl font-bold">Top 20 Coins to Invest Today</h2>
            <p className="text-muted-foreground mt-1">
              Showing {mockTopCoins.length} coins • Featured coins ranked by risk score • Search above to analyze any cryptocurrency
            </p>
          </div>
          </div>
          
          <Button 
            onClick={handleRefresh}
            variant="outline"
            size="lg"
            className="gap-2"
            disabled={isRefreshing}
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh Data
          </Button>
        </div>

        <div className="space-y-3">
          {mockTopCoins.map((coin, index) => (
            <CoinCard key={coin.id} coin={coin} index={index} />
          ))}
        </div>

        {/* Info Footer */}
        <Card className="mt-12 p-8 bg-card-elevated border-border/50">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Shield className="w-5 h-5 text-primary" />
                <h3 className="font-semibold">Risk Scoring</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Our proprietary algorithm analyzes volatility, liquidity, on-chain activity, 
                and market sentiment to compute comprehensive risk scores.
              </p>
            </div>
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Activity className="w-5 h-5 text-accent" />
                <h3 className="font-semibold">Real-time Data</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Powered by Airflow-orchestrated ETL pipelines processing data from multiple 
                exchanges, sentiment APIs, and on-chain indexers.
              </p>
            </div>
            <div>
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-5 h-5 text-success" />
                <h3 className="font-semibold">Actionable Insights</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Interactive stability charts with volatility bands, moving averages, 
                and detailed metrics help you make informed decisions.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Index;
