'use client';

import { Sidebar } from "@/layouts/Sidebar";
import { TopNav } from "@/layouts/TopNav";

export default function DashboardLayout({ children }) {
    return (
        <div className="flex min-h-screen bg-background text-foreground">
            <Sidebar />
            <div className="flex-1 flex flex-col w-full min-w-0">
                <TopNav />
                <main className="flex-1 overflow-y-auto p-4 md:p-8">
                    <div className="max-w-7xl mx-auto w-full space-y-8">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
