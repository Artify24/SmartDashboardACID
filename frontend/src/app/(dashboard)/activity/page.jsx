"use client";
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Page() {
    const router = useRouter();
    useEffect(() => {
        // Redirect away from removed Activity Feed page
        router.replace('/dashboard');
    }, [router]);
    return null;
}
