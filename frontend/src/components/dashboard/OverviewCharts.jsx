'use client';

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, Legend } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

const areaData = [
  { month: 'Jan', ourChanges: 4, competitorChanges: 7 },
  { month: 'Feb', ourChanges: 0, competitorChanges: 0 },
  { month: 'Mar', ourChanges: 0, competitorChanges: 0 },
  { month: 'Apr', ourChanges: 0, competitorChanges: 0 },
  { month: 'May', ourChanges: 0, competitorChanges: 0 },
  { month: 'Jun', ourChanges: 0, competitorChanges: 0 },
  { month: 'Jul', ourChanges: 0, competitorChanges: 0 },
];


const pieData = [
  { name: 'Us', value: 35, color: 'hsl(var(--primary))' },
  { name: 'Other', value: 65, color: 'hsl(var(--secondary))' },
];

const barData = [
  { name: 'Pricing', count: 12 },
  { name: 'Features', count: 19 },
  { name: 'Marketing', count: 8 },
  { name: 'Hiring', count: 5 },
];

export function RevenueChart() {
  return (

    <Card className="col-span-4 lg:col-span-3 border-border/50">
  <CardHeader>
    <CardTitle>Website Change Activity</CardTitle>
    <CardDescription>
      Number of detected content and structure changes from daily website scrapes.
    </CardDescription>
  </CardHeader>

  <CardContent className="pl-2">
    <div className="h-[350px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={areaData}>
          <defs>
            <linearGradient id="ourChanges" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="competitorChanges" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--secondary))" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(var(--secondary))" stopOpacity={0} />
            </linearGradient>
          </defs>

          <XAxis dataKey="month" tickLine={false} axisLine={false} />
          <YAxis tickLine={false} axisLine={false} />
          <CartesianGrid vertical={false} strokeDasharray="3 3" />
          <Tooltip />

          <Area
            type="monotone"
            dataKey="ourChanges"
            name="Your Website Changes"
            stroke="hsl(var(--primary))"
            fill="url(#ourChanges)"
          />
          <Area
            type="monotone"
            dataKey="competitorChanges"
            name="Competitor Changes"
            stroke="hsl(var(--secondary))"
            fill="url(#competitorChanges)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  </CardContent>
</Card>


  );
}

export function MarketShareChart() {
  return (
    <Card className="col-span-4 lg:col-span-1 border-border/50">
      <CardHeader>
        <CardTitle>Market Share</CardTitle>
        <CardDescription>Current distribution</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[200px] w-full relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
                stroke="none"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                itemStyle={{ color: 'hsl(var(--foreground))' }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span className="text-3xl font-bold">35%</span>
            <span className="text-xs text-muted-foreground">Market Leader</span>
          </div>
        </div>
        <div className="mt-4 space-y-2">
          {pieData.map((item) => (
            <div key={item.name} className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="text-muted-foreground">{item.name}</span>
              </div>
              <span className="font-medium">{item.value}%</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 

export function ActivityBarChart() {
  return (
    <div className="h-[200px] w-full mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={barData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <XAxis type="number" hide />
          <YAxis dataKey="name" type="category" width={80} tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }} axisLine={false} tickLine={false} />
          <Tooltip cursor={{ fill: 'hsl(var(--muted)/0.2)' }} contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))' }} />
          <Bar dataKey="count" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} barSize={20} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
