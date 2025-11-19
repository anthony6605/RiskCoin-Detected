import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Shield, Activity, Droplets, TrendingUp, BarChart3 } from "lucide-react";

interface MetricsPanelProps {
  riskScore: number;
  volatilityScore: number;
  liquidityScore: number;
  sentimentScore: number;
  volume24h: number;
  marketCap: number;
}

const MetricsPanel = ({
  riskScore,
  volatilityScore,
  liquidityScore,
  sentimentScore,
  volume24h,
  marketCap,
}: MetricsPanelProps) => {
  const getRiskColor = (score: number) => {
    if (score < 35) return { color: 'text-success', bg: 'bg-success/10', hsl: '150 100% 50%' };
    if (score < 50) return { color: 'text-warning', bg: 'bg-warning/10', hsl: '35 100% 50%' };
    return { color: 'text-destructive', bg: 'bg-destructive/10', hsl: '350 100% 62%' };
  };

  const getRiskLabel = (score: number) => {
    if (score < 35) return "Low Risk";
    if (score < 50) return "Medium Risk";
    return "High Risk";
  };

  const riskData = getRiskColor(riskScore);

  const ScoreBar = ({ value, color }: { value: number; color: string }) => (
    <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
      <div
        className={`h-full ${color} transition-all duration-500 ease-out`}
        style={{ width: `${value}%` }}
      />
    </div>
  );

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {/* Risk Score - Featured */}
      <Card className={`p-6 ${riskData.bg} border-2`} style={{ borderColor: `hsl(${riskData.hsl} / 0.3)` }}>
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-2">
            <Shield className={`w-5 h-5 ${riskData.color}`} />
            <h3 className="font-semibold">Risk Score</h3>
          </div>
          <Badge variant="secondary" className="text-xs">
            {getRiskLabel(riskScore)}
          </Badge>
        </div>
        <div className="flex items-end gap-2 mb-2">
          <div className="text-5xl font-bold" style={{ color: `hsl(${120 - riskScore * 1.2} 70% 50%)` }}>
            {riskScore}
          </div>
          <div className="text-muted-foreground mb-2">/100</div>
        </div>
        <p className="text-sm text-muted-foreground">
          Composite risk based on volatility, liquidity, and sentiment analysis
        </p>
      </Card>

      {/* Volatility */}
      <Card className="p-6 bg-card-elevated border-border/50">
        <div className="flex items-center gap-2 mb-4">
          <Activity className="w-5 h-5 text-primary" />
          <h3 className="font-semibold">Volatility</h3>
        </div>
        <div className="flex items-end gap-2 mb-3">
          <div className="text-4xl font-bold text-primary">{volatilityScore}</div>
          <div className="text-muted-foreground mb-1">/100</div>
        </div>
        <ScoreBar value={volatilityScore} color="bg-primary" />
        <p className="text-xs text-muted-foreground mt-2">
          30-day rolling standard deviation
        </p>
      </Card>

      {/* Liquidity */}
      <Card className="p-6 bg-card-elevated border-border/50">
        <div className="flex items-center gap-2 mb-4">
          <Droplets className="w-5 h-5 text-accent" />
          <h3 className="font-semibold">Liquidity</h3>
        </div>
        <div className="flex items-end gap-2 mb-3">
          <div className="text-4xl font-bold text-accent">{liquidityScore}</div>
          <div className="text-muted-foreground mb-1">/100</div>
        </div>
        <ScoreBar value={liquidityScore} color="bg-accent" />
        <p className="text-xs text-muted-foreground mt-2">
          Order book depth & 24h volume
        </p>
      </Card>

      {/* Market Cap */}
      <Card className="p-6 bg-card border-border/50">
        <div className="flex items-center gap-2 mb-3">
          <TrendingUp className="w-4 h-4 text-muted-foreground" />
          <h3 className="text-sm font-medium text-muted-foreground">Market Cap</h3>
        </div>
        <div className="text-2xl font-bold font-mono">
          ${(marketCap / 1e9).toFixed(2)}B
        </div>
      </Card>

      {/* Volume 24h */}
      <Card className="p-6 bg-card border-border/50">
        <div className="flex items-center gap-2 mb-3">
          <BarChart3 className="w-4 h-4 text-muted-foreground" />
          <h3 className="text-sm font-medium text-muted-foreground">Volume 24h</h3>
        </div>
        <div className="text-2xl font-bold font-mono">
          ${(volume24h / 1e9).toFixed(2)}B
        </div>
      </Card>

      {/* Sentiment */}
      <Card className="p-6 bg-card-elevated border-border/50">
        <div className="flex items-center gap-2 mb-4">
          <Activity className="w-5 h-5 text-chart-3" />
          <h3 className="font-semibold">Sentiment</h3>
        </div>
        <div className="flex items-end gap-2 mb-3">
          <div className="text-4xl font-bold text-chart-3">{sentimentScore}</div>
          <div className="text-muted-foreground mb-1">/100</div>
        </div>
        <ScoreBar value={sentimentScore} color="bg-chart-3" />
        <p className="text-xs text-muted-foreground mt-2">
          Social media & news sentiment
        </p>
      </Card>
    </div>
  );
};

export default MetricsPanel;
