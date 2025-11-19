import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TimeRange, PricePoint } from "@/types/crypto";
import { TrendingUp, Activity, BarChart3 } from "lucide-react";

interface StabilityChartProps {
  data: PricePoint[];
  coinSymbol: string;
}

const StabilityChart = ({ data, coinSymbol }: StabilityChartProps) => {
  const [timeRange, setTimeRange] = useState<TimeRange>("30D");
  const [showMA, setShowMA] = useState(true);
  const [showVolatility, setShowVolatility] = useState(true);

  const timeRanges: TimeRange[] = ["1D", "7D", "30D", "90D", "1Y"];

  // Calculate chart dimensions
  const prices = data.map(d => d.price);
  const minPrice = Math.min(...prices) * 0.95;
  const maxPrice = Math.max(...prices) * 1.05;
  const priceRange = maxPrice - minPrice;

  const getY = (price: number) => {
    return 100 - ((price - minPrice) / priceRange) * 100;
  };

  // Create SVG path for price line
  const createPath = (points: number[], accessor: (p: PricePoint, i: number) => number) => {
    return points
      .map((_, i) => {
        const value = accessor(data[i], i);
        if (value === undefined) return null;
        const x = (i / (points.length - 1)) * 100;
        const y = getY(value);
        return `${i === 0 ? 'M' : 'L'} ${x} ${y}`;
      })
      .filter(Boolean)
      .join(' ');
  };

  const pricePath = createPath(prices, (p) => p.price);
  const ma7Path = showMA ? createPath(prices, (p) => p.ma_7 || p.price) : '';
  const ma30Path = showMA ? createPath(prices, (p) => p.ma_30 || p.price) : '';

  const currentPrice = data[data.length - 1]?.price || 0;
  const firstPrice = data[0]?.price || 0;
  const priceChange = currentPrice - firstPrice;
  const priceChangePercent = (priceChange / firstPrice) * 100;

  return (
    <Card className="p-6 bg-card-elevated border-border/50">
      <div className="flex flex-col gap-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h3 className="text-2xl font-bold">Price & Stability Chart</h3>
              <Badge variant="secondary" className="text-sm">
                {coinSymbol}
              </Badge>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-3xl font-bold font-mono">
                ${currentPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </div>
              <div className={`flex items-center gap-1 text-lg ${priceChange >= 0 ? 'text-success' : 'text-destructive'}`}>
                <TrendingUp className={`w-5 h-5 ${priceChange < 0 ? 'rotate-180' : ''}`} />
                <span className="font-semibold">
                  {priceChange >= 0 ? '+' : ''}{priceChangePercent.toFixed(2)}%
                </span>
              </div>
            </div>
          </div>

          {/* Controls */}
          <div className="flex flex-col gap-2">
            <div className="flex gap-1">
              {timeRanges.map((range) => (
                <Button
                  key={range}
                  variant={timeRange === range ? "default" : "secondary"}
                  size="sm"
                  onClick={() => setTimeRange(range)}
                  className="min-w-[50px]"
                >
                  {range}
                </Button>
              ))}
            </div>
            <div className="flex gap-2">
              <Button
                variant={showMA ? "default" : "outline"}
                size="sm"
                onClick={() => setShowMA(!showMA)}
                className="text-xs"
              >
                <Activity className="w-3 h-3 mr-1" />
                MA
              </Button>
              <Button
                variant={showVolatility ? "default" : "outline"}
                size="sm"
                onClick={() => setShowVolatility(!showVolatility)}
                className="text-xs"
              >
                <BarChart3 className="w-3 h-3 mr-1" />
                Vol
              </Button>
            </div>
          </div>
        </div>

        {/* Chart */}
        <div className="relative w-full h-[400px] bg-background rounded-lg border border-border/30 overflow-hidden">
          <svg
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
            className="w-full h-full"
          >
            {/* Volatility bands (background) */}
            {showVolatility && (
              <g opacity="0.15">
                {data.map((point, i) => {
                  if (!point.volatility) return null;
                  const x = (i / (data.length - 1)) * 100;
                  const y = getY(point.price);
                  const bandHeight = (point.volatility * 100);
                  return (
                    <rect
                      key={i}
                      x={x - 0.5}
                      y={y - bandHeight / 2}
                      width="1"
                      height={bandHeight}
                      fill="hsl(var(--warning))"
                    />
                  );
                })}
              </g>
            )}

            {/* Moving averages */}
            {showMA && ma30Path && (
              <path
                d={ma30Path}
                fill="none"
                stroke="hsl(var(--accent))"
                strokeWidth="0.3"
                opacity="0.6"
              />
            )}
            {showMA && ma7Path && (
              <path
                d={ma7Path}
                fill="none"
                stroke="hsl(var(--primary))"
                strokeWidth="0.4"
                opacity="0.7"
              />
            )}

            {/* Price line with gradient */}
            <defs>
              <linearGradient id="priceGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.3" />
                <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity="0" />
              </linearGradient>
            </defs>
            <path
              d={`${pricePath} L 100 100 L 0 100 Z`}
              fill="url(#priceGradient)"
            />
            <path
              d={pricePath}
              fill="none"
              stroke="hsl(var(--primary))"
              strokeWidth="0.6"
              className="drop-shadow-[0_0_8px_hsl(var(--primary))]"
            />
          </svg>

          {/* Legend */}
          <div className="absolute bottom-4 left-4 flex gap-4 text-xs">
            <div className="flex items-center gap-2 bg-background/80 backdrop-blur-sm px-3 py-1.5 rounded-full border border-border/50">
              <div className="w-3 h-0.5 bg-primary"></div>
              <span>Price</span>
            </div>
            {showMA && (
              <>
                <div className="flex items-center gap-2 bg-background/80 backdrop-blur-sm px-3 py-1.5 rounded-full border border-border/50">
                  <div className="w-3 h-0.5 bg-primary opacity-70"></div>
                  <span>MA(7)</span>
                </div>
                <div className="flex items-center gap-2 bg-background/80 backdrop-blur-sm px-3 py-1.5 rounded-full border border-border/50">
                  <div className="w-3 h-0.5 bg-accent opacity-60"></div>
                  <span>MA(30)</span>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
};

export default StabilityChart;
