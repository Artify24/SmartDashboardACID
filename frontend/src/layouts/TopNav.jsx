'use client';

import React from "react";
import { Bell, Search, Moon, Sun } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { MobileSidebar } from "./Sidebar";
import { useTheme } from "@/components/ui/theme-provider";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

export function TopNav() {
  const { setTheme } = useTheme();

  return (
    <header
      className="
        sticky top-0 z-30
        h-16 w-full
        border-b border-border/40
        bg-background
        px-6
        flex items-center justify-between gap-4
      "
    >
      {/* Mobile sidebar */}
      <div className="flex items-center gap-4 md:hidden">
        <MobileSidebar />
      </div>

      {/* Search (desktop) */}
      <div className="hidden md:flex items-center flex-1 max-w-md relative">
        <Search className="w-4 h-4 absolute left-3 text-muted-foreground" />
        <Input
          placeholder="Search competitors, trends, or insights..."
          className="
            pl-10
            bg-secondary/20
            border-transparent
            focus-visible:ring-primary/20
            focus-visible:bg-background
            transition-all
          "
        />
      </div>

      {/* Right actions */}
      <div className="flex items-center gap-3 ml-auto">
        {/* Theme toggle */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="rounded-full relative"
            >
              <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
              <span className="sr-only">Toggle theme</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => setTheme("light")}>
              Light
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setTheme("dark")}>
              Dark
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setTheme("system")}>
              System
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        {/* Notifications popover (no red dot) */}
        <Popover>
          <PopoverTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="rounded-full relative text-muted-foreground hover:text-foreground"
            >
              <Bell className="w-5 h-5" />
            </Button>
          </PopoverTrigger>
          <PopoverContent
            side="bottom"
            align="end"
            className="
              w-72 mr-1
              rounded-xl
              bg-card
              border border-border/60
              shadow-xl
              animate-in fade-in-0 zoom-in-95
            "
          >
            <div className="space-y-2">
              <p className="text-sm font-semibold">Notifications</p>
              <p className="text-xs text-muted-foreground">
                You&apos;re all caught up. No notifications right now.
              </p>
            </div>
          </PopoverContent>
        </Popover>

        {/* Divider */}
        <div className="h-8 w-px bg-border mx-2" />

        {/* User profile dropdown on existing button */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              className="flex items-center gap-2 pl-1 pr-2 py-1 h-auto rounded-full hover:bg-secondary/20"
            >
              <Avatar className="w-8 h-8 border border-border">
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>JD</AvatarFallback>
              </Avatar>
              <div className="flex flex-col items-start text-xs hidden sm:flex">
                <span className="font-medium">John Doe</span>
                <span className="text-muted-foreground">Pro Member</span>
              </div>
            </Button>
          </DropdownMenuTrigger>

          <DropdownMenuContent
            align="end"
            className="w-64 p-3 rounded-xl border border-border/60 bg-card shadow-xl animate-in fade-in-0 zoom-in-95"
          >
            {/* Header */}
            <div className="flex items-center gap-3 pb-3 border-b border-border/40">
              <Avatar className="w-10 h-10 border border-border">
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>JD</AvatarFallback>
              </Avatar>
              <div>
                <p className="text-sm font-semibold">John Doe</p>
                <p className="text-xs text-muted-foreground">john@example.com</p>
              </div>
            </div>

            {/* Menu Options */}
            <div className="mt-3 flex flex-col gap-1 text-sm">
              <DropdownMenuItem className="cursor-pointer">
                My Profile
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer">
                Account Settings
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer">
                Billing
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer">
                Help Center
              </DropdownMenuItem>

              <div className="border-t border-border/40 my-2" />

              <DropdownMenuItem className="cursor-pointer text-destructive">
                Logout
              </DropdownMenuItem>
            </div>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
