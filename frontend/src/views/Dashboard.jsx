import React, { useEffect, useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

import { RevenueChart, MarketShareChart, ActivityBarChart } from '@/components/dashboard/OverviewCharts';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { Skeleton } from '@/components/ui/skeleton';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  /* -----------------------------
     Read setup data from localStorage
  ------------------------------ */
  const setupData = useMemo(() => {
    try {
      const data = JSON.parse(localStorage.getItem('competition_mode_data') || '{}');

      return {
        businessName: data.businessName || 'Not set',
        businessWebsite: data.businessWebsite || 'Not set',
        industry: data.industry || 'Not set',
        mode: data.mode || 'Not set',
        competitorWebsites: data.competitorWebsites || [],
        timestamp: data.timestamp || null
      };
    } catch (err) {
      console.error('Failed to parse setupData:', err);
      return {
        businessName: 'Not set',
        businessWebsite: 'Not set',
        industry: 'Not set',
        mode: 'Not set',
        competitorWebsites: [],
        timestamp: null
      };
    }
  }, []);

  /* -----------------------------
     Generate mock competitor events
     (replace later with real intelligence)
  ------------------------------ */
  const competitorEvents = useMemo(() => {
    if (!setupData.competitorWebsites.length) return [];

    const eventTypes = [
      'Pricing Change',
      'New Feature Launch',
      'Partnership Announcement',
      'Design Update',
      'Performance Improvement'
    ];
    const impacts = ['High', 'Medium', 'Low'];
    const timeframes = ['2h ago', '5h ago', '1d ago', '2d ago', '3d ago'];

    const events = [];

    setupData.competitorWebsites.forEach((url, index) => {
      const domain = new URL(url).hostname.replace('www.', '');

      for (let i = 0; i < 2; i++) {
        events.push({
          company: domain,
          type: eventTypes[(index + i) % eventTypes.length],
          impact: impacts[(index + i) % impacts.length],
          date: timeframes[(index + i) % timeframes.length]
        });
      }
    });

    return events.slice(0, 5);
  }, [setupData.competitorWebsites]);

  /* -----------------------------
     Load dashboard stats (API)
  ------------------------------ */
  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await api.get('/dashboard/stats');
        setStats(data);
      } catch (err) {
        console.error('Failed to load dashboard stats:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  /* -----------------------------
     Animations
  ------------------------------ */
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  /* -----------------------------
     Loading State
  ------------------------------ */
  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map(i => (
          <Skeleton key={i} className="h-32 rounded-xl" />
        ))}
      </div>
    );
  }

  /* -----------------------------
     Render
  ------------------------------ */
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="space-y-8"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard Overview</h2>
      </div>

      {/* Company Info */}
      <motion.div variants={item} className="grid gap-4 md:grid-cols-4">
        <div className="rounded-xl border bg-card p-4">
          <p className="text-xs text-muted-foreground uppercase">Company</p>
          <p className="text-xl font-bold mt-1">{setupData.businessName}</p>
        </div>

        <div className="rounded-xl border bg-card p-4">
          <p className="text-xs text-muted-foreground uppercase">Industry</p>
          <p className="text-xl font-bold mt-1">{setupData.industry}</p>
        </div>

        <div className="rounded-xl border bg-card p-4">
          <p className="text-xs text-muted-foreground uppercase">Mode</p>
          <Badge className="mt-2">{setupData.mode}</Badge>
        </div>

        <div className="rounded-xl border bg-card p-4">
          <p className="text-xs text-muted-foreground uppercase">
            Competitors Tracked
          </p>
          <p className="text-xl font-bold mt-1">
            {setupData.competitorWebsites.length}
          </p>
        </div>
      </motion.div>

      {/* Charts */}
      <motion.div variants={item} className="grid gap-4 md:grid-cols-4">
        <RevenueChart />
        <MarketShareChart />
      </motion.div>

      {/* Bottom Section */}
      <div className="grid gap-4 md:grid-cols-7">
        {/* Recent Moves */}
        <motion.div
          variants={item}
          className="col-span-4 rounded-xl border bg-card"
        >
          <div className="p-6 flex justify-between items-center">
            <div>
              <h3 className="text-lg font-semibold">
                Recent Competitor Moves
              </h3>
              <p className="text-sm text-muted-foreground">
                High-impact changes detected recently
              </p>
            </div>
            <Button variant="ghost" size="sm" className="gap-1">
              View All <ArrowRight className="w-4 h-4" />
            </Button>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Company</TableHead>
                <TableHead>Event</TableHead>
                <TableHead>Impact</TableHead>
                <TableHead className="text-right">When</TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              {competitorEvents.length ? (
                competitorEvents.map((e, i) => (
                  <TableRow key={i}>
                    <TableCell className="font-medium">
                      {e.company}
                    </TableCell>
                    <TableCell>{e.type}</TableCell>
                    <TableCell>
                      <Badge
                        variant="outline"
                        className={
                          e.impact === 'High'
                            ? 'border-destructive text-destructive'
                            : e.impact === 'Medium'
                            ? 'border-yellow-500 text-yellow-500'
                            : 'border-blue-500 text-blue-500'
                        }
                      >
                        {e.impact}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right text-muted-foreground">
                      {e.date}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={4}
                    className="text-center text-muted-foreground py-6"
                  >
                    No competitor data available
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </motion.div>

        {/* Activity Chart */}
        <motion.div
          variants={item}
          className="col-span-3 rounded-xl border bg-card p-6"
        >
          <h3 className="text-lg font-semibold mb-4">
            Activity by Category
          </h3>
          <ActivityBarChart />
        </motion.div>
      </div>
    </motion.div>
  );
}
