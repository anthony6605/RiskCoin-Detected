import { Coin } from "@/types/crypto";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, Activity, Shield } from "lucide-react";
import { Link } from "react-router-dom";

interface CoinCardProps {
  coin: Coin;
  index: number;
}

const CoinCard = ({ coin, index }: CoinCardProps) => {
  const isPositive = coin.price_change_percentage_24h >= 0;
  
  const getRiskColor = (score: number) => {
    if (score < 35) return "text-success";
    if (score < 50) return "text-warning";
    return "text-destructive";
  };
  
  const getRiskLabel = (score: number) => {
    if (score < 35) return "Low Risk";
    if (score < 50) return "Medium Risk";
    return "High Risk";
  };

  return (
    <Link to={`/coin/${coin.id}`}>
      <Card className="p-4 hover:bg-card-elevated transition-all duration-300 cursor-pointer border-border/50 hover:border-primary/30 hover:shadow-[0_0_20px_hsl(var(--primary)/0.1)] animate-fade-in group">
        <div className="flex items-center gap-4">
          {/* Rank */}
          <div className="flex-shrink-0 w-8 text-center">
            <span className="text-lg font-bold text-muted-foreground">#{index + 1}</span>
          </div>
          
          {/* Coin Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="font-bold text-foreground text-base truncate">{coin.name}</h3>
              <Badge variant="secondary" className="text-xs px-2 py-0">
                {coin.symbol}
              </Badge>
            </div>
            
            <div className="flex items-center gap-4 text-sm">
              <div>
                <span className="font-mono font-semibold text-foreground">
                  ${coin.current_price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
              </div>
              
              <div className={`flex items-center gap-1 ${isPositive ? 'text-success' : 'text-destructive'}`}>
                {isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                <span className="font-medium">
                  {isPositive ? '+' : ''}{coin.price_change_percentage_24h.toFixed(2)}%
                </span>
              </div>
            </div>
          </div>
          
          {/* Risk Score */}
          <div className="flex-shrink-0 text-right">
            <div className="flex items-center gap-2 mb-1">
              <Shield className={`w-4 h-4 ${getRiskColor(coin.risk_score)}`} />
              <span className={`text-xs font-semibold ${getRiskColor(coin.risk_score)}`}>
                {getRiskLabel(coin.risk_score)}
              </span>
            </div>
            <div className="text-2xl font-bold" style={{ color: `hsl(${120 - coin.risk_score * 1.2} 70% 50%)` }}>
              {coin.risk_score}
            </div>
          </div>
          
          {/* Metrics */}
          <div className="hidden lg:flex flex-col gap-1 text-xs text-muted-foreground min-w-[120px]">
            <div className="flex justify-between">
              <span>Vol 24h:</span>
              <span className="font-mono">${(coin.total_volume / 1e9).toFixed(2)}B</span>
            </div>
            <div className="flex justify-between">
              <span>Liquidity:</span>
              <span className="font-semibold text-primary">{coin.liquidity_score}/100</span>
            </div>
          </div>
        </div>
      </Card>
    </Link>
  );
};

export default CoinCard;
