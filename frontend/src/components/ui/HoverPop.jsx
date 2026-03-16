// src/components/animated/HoverPop.jsx
import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

export function HoverPop({ children, className }) {
  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.99 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={cn("transition-shadow", className)}
    >
      {children}
    </motion.div>
  );
}
