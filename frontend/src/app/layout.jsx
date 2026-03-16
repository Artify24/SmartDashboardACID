import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import { ThemeProvider } from "@/components/ui/theme-provider";
import { Toaster } from "@/components/ui/sonner";
import "./globals.css";

const plusJakartaSans = Plus_Jakarta_Sans({
    subsets: ["latin"],
    variable: "--font-plus-jakarta-sans",
});
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata = {
    title: "Competitive Analytics",
    description: "Dashboard for competitive analytics",
};

export default function RootLayout({ children }) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body className={`${inter.variable} ${plusJakartaSans.variable} font-sans antialiased`}>
                <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme" attribute="class">
                    {children}
                    <Toaster />
                </ThemeProvider>
            </body>
        </html>
    );
}
