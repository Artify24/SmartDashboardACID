/** @type {import('next').NextConfig} */
const nextConfig = {
    // reactStrictMode: true, // Next.js 13.4+ defaults to true in app dir usually, but good to be explicit or leave minimal
    // swcMinify: true,
    images: {
        unoptimized: true, // simplified for static exports or if image optimization isn't set up
    },
    eslint: {
        ignoreDuringBuilds: true,
    },
};

export default nextConfig;
