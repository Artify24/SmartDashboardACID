import React, { useMemo } from "react";
import Link from "next/link";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/ui/card";

/* ------------------------------------
   Helpers
------------------------------------ */
const getThreatLevel = () => {
  const levels = ["High Threat", "Medium Threat", "Low Threat"];
  return levels[Math.floor(Math.random() * levels.length)];
};

const getMarketShare = () => {
  return `${(Math.random() * 20 + 3).toFixed(1)}%`;
};

const formatNameFromDomain = (domain) => {
  return domain
    .replace("www.", "")
    .split(".")[0]
    .replace(/[-_]/g, " ")
    .replace(/\b\w/g, l => l.toUpperCase());
};

/* ------------------------------------
   Component
------------------------------------ */
export default function Competitors() {
  const competitors = useMemo(() => {
    try {
      const setupData = JSON.parse(localStorage.getItem("competition_mode_data") || "{}");
      const sites = setupData.competitorWebsites || [];

      return sites.map((url) => {
        const domain = new URL(url).hostname.replace("www.", "");
        return {
          id: domain,
          name: formatNameFromDomain(domain),
          domain,
          threat: getThreatLevel(),
          marketShare: getMarketShare(),
        };
      });
    } catch (err) {
      console.error("Failed to load competitors from localStorage", err);
      return [];
    }
  }, []);

  return (
    <div className="px-6 py-8 lg:px-12 max-w-7xl mx-auto">
      <h1 className="text-3xl md:text-4xl font-bold mb-2 tracking-tight">
        Competitors
      </h1>
      <p className="text-base text-muted-foreground mb-8">
        Automatically tracked competitors from your setup.
      </p>

      <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-3">
        {competitors.length ? (
          competitors.map((c) => (
            <Card
              key={c.id}
              className="transition-transform duration-200 hover:scale-[1.02] hover:shadow-lg border border-border/50"
            >
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center justify-between text-lg">
                  <span className="flex items-center gap-2">
                    <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-indigo-500 text-white text-xs font-bold">
                      {c.name[0]}
                    </span>
                    {c.name}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {c.domain}
                  </span>
                </CardTitle>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Market Share */}
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Market Share</span>
                  <span className="font-bold">{c.marketShare}</span>
                </div>

                {/* Threat Level */}
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground text-sm">
                    Threat Level
                  </span>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-semibold border ${
                      c.threat === "High Threat"
                        ? "border-red-500 text-red-400 bg-red-900/20"
                        : c.threat === "Medium Threat"
                        ? "border-yellow-500 text-yellow-300 bg-yellow-900/20"
                        : "border-blue-500 text-blue-300 bg-blue-900/20"
                    }`}
                  >
                    {c.threat}
                  </span>
                </div>

                {/* Full Report */}
                <div className="pt-4 flex justify-end">
                  <Link
                    href={`/competitors/${encodeURIComponent(c.id)}`}
                    className="text-indigo-400 font-semibold text-sm hover:underline hover:text-indigo-300 flex items-center gap-1"
                  >
                    Full Report →
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <p className="text-muted-foreground">
            No competitors found. Add competitors during setup.
          </p>
        )}
      </div>
    </div>
  );
}
