"use client"

import React, { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { Sparkles, AlertTriangle } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { supabase } from "@/lib/supabaseClient"

export default function Insights() {
  const [content, setContent] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStrategy()
  }, [])

  async function loadStrategy() {
    const { data, error } = await supabase
      .from("llm_outputs")
      .select("content")
      .eq("type", "finalStategy")
      .order("created_at", { ascending: false })
      .limit(1)
      .single()

    if (!error && data?.content) {
      setContent(data.content)
    }

    setLoading(false)
  }

  if (loading) {
    return <p className="text-muted-foreground">Loading AI strategy…</p>
  }

  if (!content) {
    return (
      <div className="text-muted-foreground">
        No strategy available yet.
      </div>
    )
  }

  // Split by section headers
  const sections = content
    .split("## ")
    .filter(Boolean)
    .map((block) => {
      const [titleLine, ...rest] = block.split("\n")
      return {
        title: titleLine.trim(),
        body: rest.join("\n").trim(),
      }
    })

  return (
    <div className="space-y-10">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-yellow-500" />
          Final AI Strategy
        </h2>
        <p className="text-muted-foreground mt-1">
          Executive-grade strategic guidance based on competitive intelligence.
        </p>
      </div>

      {/* Strategy Sections */}
      <div className="space-y-6">
        {sections.map((section, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.05 }}
          >
            <Card className="border-border/50">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-xl">
                  {section.title}
                </CardTitle>

                {section.title.toLowerCase().includes("risk") && (
                  <Badge variant="destructive" className="gap-1">
                    <AlertTriangle className="w-3 h-3" />
                    Monitor
                  </Badge>
                )}
              </CardHeader>

              <CardContent className="space-y-4 text-sm leading-relaxed text-muted-foreground whitespace-pre-wrap">
                {section.body.split("\n").map((line, i) => {
                  // Numbered list
                  if (/^\d+\.\s/.test(line)) {
                    return (
                      <li key={i} className="ml-4 list-decimal">
                        {line.replace(/^\d+\.\s/, "")}
                      </li>
                    )
                  }

                  // Bold bullet
                  if (line.startsWith("**")) {
                    return (
                      <p key={i} className="font-medium text-foreground">
                        {line.replace(/\*\*/g, "")}
                      </p>
                    )
                  }

                  return <p key={i}>{line}</p>
                })}
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
