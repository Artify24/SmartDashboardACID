"use client"

import { useEffect, useState } from "react"
import { supabase } from "@/lib/supabaseClient"
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts"
import { ArrowUpRight } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"


/* -------------------------------
  Fallback Data
-------------------------------- */
const FALLBACK_DATA = [
  {
    id: "dummy-summary",
    type: "competitorSummary",
    created_at: new Date().toISOString(),
    content: `Competitors are aggressively positioning around AI automation, vertical-specific messaging, and trust-led differentiation.

Observed shifts include clearer pricing transparency, stronger enterprise security claims, and accelerated feature shipping cadence.`,
  },
  {
    id: "dummy-comparison",
    type: "comparisonReport",
    created_at: new Date().toISOString(),
    content: `Relative to competitors, your product demonstrates faster iteration velocity and stronger customization flexibility.

Competitors currently outperform in proof assets (case studies, certifications) and pricing clarity. Closing these gaps would materially improve win-rate.`,
  },
]

/* -------------------------------
  Charts Data
-------------------------------- */
const engagementData = [
  { month: "Sep", views: 4200, conversion: 2.1 },
  { month: "Oct", views: 5100, conversion: 2.3 },
  { month: "Nov", views: 5900, conversion: 2.8 },
  { month: "Dec", views: 6800, conversion: 3.2 },
  { month: "Jan", views: 7200, conversion: 3.5 },
  { month: "Feb", views: 8100, conversion: 3.9 },
]

const industryData = [
  { name: "Tech", value: 60, growth: 24 },
  { name: "Finance", value: 40, growth: 15 },
  { name: "Pharma", value: 35, growth: 18 },
  { name: "Consulting", value: 45, growth: 12 },
]

/* =========================================================
  MAIN COMPONENT
========================================================= */
export default function CompetitiveIntelligenceDashboard() {
  const [intel, setIntel] = useState([])
  const [loading, setLoading] = useState(true)

  const [showFullSummary, setShowFullSummary] = useState(false)
  const [showFullComparison, setShowFullComparison] = useState(false)

  const SUMMARY_LIMIT = 300
  const COMPARISON_LIMIT = 260

  useEffect(() => {
    async function loadIntel() {
      const { data, error } = await supabase
        .from("llm_outputs")
        .select("id, type, content, created_at")
        .in("type", ["competitorSummary", "comparisonReport"])
        .order("created_at", { ascending: false })

      if (error || !data || data.length === 0) {
        setIntel(FALLBACK_DATA)
      } else {
        setIntel(data)
      }

      setLoading(false)
    }

    loadIntel()
  }, [])

  const competitorSummary = intel.find((i) => i.type === "competitorSummary")
  const comparisonReport = intel.find((i) => i.type === "comparisonReport")

  return (
    <div className="min-h-screen bg-[#020202] text-white p-6 lg:p-12 space-y-10">
      {/* HEADER */}
      <div className="flex items-end justify-between border-b border-white/5 pb-6">
        <div>
          <Badge className="mb-2 bg-purple-500/10 text-purple-400 border-purple-500/20">
            Live Intelligence
          </Badge>
          <h1 className="text-4xl font-bold tracking-tight">
            Competitive Intelligence
          </h1>
          <p className="text-muted-foreground mt-2 max-w-xl">
            High-signal competitive insights derived from continuous monitoring.
          </p>
        </div>
        <button className="bg-purple-600 px-6 py-2 rounded-full font-semibold text-sm hover:bg-purple-500 flex items-center gap-2">
          Download Report <ArrowUpRight className="w-4 h-4" />
        </button>
      </div>

      {/* CHARTS */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="bg-black/40 border-purple-500/10">
          <CardHeader>
            <CardTitle className="text-sm">Market Engagement</CardTitle>
            <CardDescription>Traffic vs Conversion</CardDescription>
          </CardHeader>
          <CardContent className="h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={engagementData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(168,85,247,0.05)" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line dataKey="views" stroke="#a855f7" strokeWidth={3} />
                <Line dataKey="conversion" stroke="#c084fc" strokeDasharray="4 4" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="bg-black/40 border-purple-500/10">
          <CardHeader>
            <CardTitle className="text-sm">Industry Coverage</CardTitle>
            <CardDescription>Penetration vs Growth</CardDescription>
          </CardHeader>
          <CardContent className="h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={industryData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(168,85,247,0.05)" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#9333ea" />
                <Bar dataKey="growth" fill="#c084fc" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* ANALYSIS */}
      <Card className="bg-black/40 border-purple-500/10">
        <CardHeader>
          <CardTitle className="text-xl">Strategic Intelligence</CardTitle>
        </CardHeader>
        <CardContent className="grid md:grid-cols-2 gap-8">
          {/* Competitor Summary */}
          <div>
            <h4 className="text-xs uppercase tracking-widest text-purple-400 mb-3">
              Competitor Summary
            </h4>
            {loading ? (
              <Skeleton className="h-24 w-full bg-white/5" />
            ) : (
              <div className="text-sm whitespace-pre-wrap leading-relaxed text-white/80">
                {showFullSummary
                  ? competitorSummary?.content
                  : competitorSummary?.content?.slice(0, SUMMARY_LIMIT)}
                {!showFullSummary &&
                  competitorSummary?.content &&
                  competitorSummary.content.length > SUMMARY_LIMIT &&
                  "…"}
                {competitorSummary?.content &&
                  competitorSummary.content.length > SUMMARY_LIMIT && (
                    <button
                      onClick={() => setShowFullSummary(!showFullSummary)}
                      className="block mt-2 text-xs text-purple-400 hover:text-purple-300 underline"
                    >
                      {showFullSummary ? "Show less" : "Read full analysis"}
                    </button>
                  )}
              </div>
            )}
          </div>

          {/* Comparison Report */}
          <div className="bg-purple-500/5 border border-purple-500/20 rounded-xl p-6">
            <h4 className="text-xs uppercase tracking-widest text-purple-400 mb-3">
              Comparison Report
            </h4>
            {loading ? (
              <Skeleton className="h-24 w-full bg-white/5" />
            ) : (
              <div className="text-sm italic whitespace-pre-wrap text-purple-100/90">
                {showFullComparison
                  ? comparisonReport?.content
                  : comparisonReport?.content?.slice(0, COMPARISON_LIMIT)}
                {!showFullComparison &&
                  comparisonReport?.content &&
                  comparisonReport.content.length > COMPARISON_LIMIT &&
                  "…"}
                {comparisonReport?.content &&
                  comparisonReport.content.length > COMPARISON_LIMIT && (
                    <button
                      onClick={() =>
                        setShowFullComparison(!showFullComparison)
                      }
                      className="block mt-2 text-xs text-purple-300 hover:text-purple-200 underline"
                    >
                      {showFullComparison
                        ? "Show less"
                        : "Read full comparison"}
                    </button>
                  )}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
