import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';

export function StatsCard({ title, value, trend, trendValue, icon: Icon, className }) {
  const isPositive = trend === 'up';
  const isNeutral = trend === 'neutral';

  return (
    <Card className={cn("overflow-hidden relative border-border/50 hover:shadow-md transition-all duration-300", className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground tracking-wide uppercase">
          {title}
        </CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold tracking-tight">{value}</div>
        <div className="flex items-center mt-1 space-x-2">
          <div className={cn(
            "flex items-center text-xs font-medium px-2 py-0.5 rounded-full",
            isPositive ? "text-emerald-500 bg-emerald-500/10" : 
            isNeutral ? "text-yellow-500 bg-yellow-500/10" : 
            "text-red-500 bg-red-500/10"
          )}>
            {isPositive ? <ArrowUpRight className="h-3 w-3 mr-1" /> : 
             isNeutral ? <Minus className="h-3 w-3 mr-1" /> : 
             <ArrowDownRight className="h-3 w-3 mr-1" />}
            {trendValue}
          </div>
          <p className="text-xs text-muted-foreground">from last month</p>
        </div>
      </CardContent>
      
      {/* Decorative gradient blob */}
      <div className="absolute -right-6 -bottom-6 w-24 h-24 rounded-full bg-primary/5 blur-2xl pointer-events-none" />
    </Card>
  );
}
