'use client';

import React, { useRef } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowRight, BarChart2, Shield, Zap, Layers, ArrowDown, DollarSign, TrendingUp, Activity, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { StatsCard } from '@/components/dashboard/StatsCard';
import { RevenueChart, MarketShareChart } from '@/components/dashboard/OverviewCharts';

export default function LandingPage() {
  const previewRef = useRef(null);

  const scrollToPreview = () => {
    previewRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      {/* Navbar */}
      <nav className="fixed w-full top-0 z-50 glass border-b border-white/10">
        <div className="w-full px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold">
                CT
              </div>
              <span className="font-bold text-xl tracking-tight">ACID</span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Features</a>

              <Link href="/setup">
                <Button variant="default" className="bg-primary hover:bg-primary/90 text-white rounded-full px-6 shadow-lg shadow-primary/25">
                  Launch Dashboard
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_center,_var(--tw-gradient-stops))] from-primary/20 via-background to-background" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Badge variant="secondary" className="mb-6 px-4 py-1 rounded-full bg-secondary/10 text-secondary border-secondary/20 text-sm font-medium">
              🚀 #1 Competitive Intelligence Platform
            </Badge>
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-primary via-purple-400 to-accent pb-2">
              Dominate Your Market <br /> With Real-Time Intel.
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
              Track competitors, monitor pricing changes, and predict market trends before they happen. The dashboard for winners.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/setup">
                <Button size="lg" className="h-14 px-8 text-lg rounded-full bg-primary hover:bg-primary/90 shadow-xl shadow-primary/30 hover:shadow-primary/50 transition-all hover:scale-105">
                  Get Started Now <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>

            </div>
          </motion.div>

          {/* Scroll CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
            className="mt-20 flex justify-center"
          >
            <motion.button
              onClick={scrollToPreview}
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              animate={{ y: [0, 5, 0] }}
              transition={{
                y: { duration: 2, repeat: Infinity, ease: "easeInOut" },
                default: { duration: 0.2 }
              }}
              className="group flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 hover:bg-white/10 backdrop-blur-md border border-primary/20 shadow-lg shadow-primary/10 text-sm font-medium transition-all cursor-pointer"
            >
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent font-semibold">
                Scroll to live dashboard
              </span>
              <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                <ArrowDown className="w-3 h-3 text-primary" />
              </div>
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* Dashboard Preview Section */}
      <section ref={previewRef} className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-sm font-bold tracking-[0.2em] text-primary uppercase mb-2">Dashboard Preview</h3>
            <h2 className="text-3xl font-bold">See the power in action</h2>
          </div>

          <div className="relative rounded-xl border border-border/50 bg-card/50 backdrop-blur-xl shadow-2xl shadow-primary/10 overflow-hidden">
            {/* Mock Browser Bar */}
            <div className="h-10 border-b border-border/50 bg-muted/20 flex items-center px-4 gap-2">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50" />
                <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50" />
              </div>
              <div className="flex-1 mx-4 h-6 bg-background/50 rounded-md border border-border/30 flex items-center justify-center text-xs text-muted-foreground font-mono">
                app.com/dashboard
              </div>
            </div>

            {/* Dashboard Content Preview */}
            <div className="p-6 md:p-8 bg-background/40">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-6">
                <StatsCard title="Total Revenue" value="$12.4M" trend="up" trendValue="12.5%" icon={DollarSign} />
                <StatsCard title="Market Share" value="28%" trend="up" trendValue="2.1%" icon={TrendingUp} />
                <StatsCard title="Competitor Events" value="145" trend="down" trendValue="15%" icon={Activity} />
                <StatsCard title="Sentiment Score" value="78" trend="neutral" trendValue="0%" icon={Users} />
              </div>
              <div className="grid gap-4 md:grid-cols-4">
                <RevenueChart />
                <MarketShareChart />
              </div>
            </div>

            {/* Overlay Gradient for "Live" feel */}
            <div className="absolute inset-0 pointer-events-none bg-gradient-to-t from-background via-transparent to-transparent opacity-20" />
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-24 bg-secondary/5 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Everything you need to stay ahead</h2>
            <p className="text-muted-foreground text-lg">
              Comprehensive tools designed for market leaders. Stop guessing and start knowing exactly what your competitors are up to.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Layers,
                title: "Market Overview",
                desc: "Get a bird's eye view of the entire landscape with real-time market share visualization."
              },
              {
                icon: Shield,
                title: "Threat Detection",
                desc: "AI-powered algorithms identify potential threats before they impact your bottom line."
              },
              {
                icon: Zap,
                title: "Instant Alerts",
                desc: "Receive immediate notifications when competitors change pricing, launch features, or hire key roles."
              }
            ].map((feature, i) => (
              <motion.div
                key={i}
                whileHover={{ y: -5 }}
                className="p-8 rounded-2xl bg-card border border-border shadow-sm hover:shadow-xl hover:shadow-primary/5 transition-all"
              >
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary mb-6">
                  <feature.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-primary/5" />
        <div className="max-w-4xl mx-auto px-4 text-center relative z-10">
          <h2 className="text-4xl font-bold mb-6">Ready to outsmart the competition?</h2>
          <p className="text-xl text-muted-foreground mb-10">Join 500+ enterprises using ACID to dominate their industry.</p>
          <Link href="/setup">
            <Button size="lg" className="bg-foreground text-background hover:bg-foreground/90 h-14 px-8 rounded-full text-lg">
              Get Started Now
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-card border-t border-border py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-primary flex items-center justify-center text-white text-xs font-bold">
              CT
            </div>
            <span className="font-bold text-lg">CompetiTrack</span>
          </div>
          <div className="text-muted-foreground text-sm">
            © 2024 CompetiTrack Inc. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
