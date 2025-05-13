/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? "/Arya-New-Project" : "",
  assetPrefix: process.env.NODE_ENV === 'production' ? "/Arya-New-Project/" : "",
  trailingSlash: true,
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  publicRuntimeConfig: {
    basePath: process.env.NODE_ENV === 'production' ? "/Arya-New-Project" : "",
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000',
  },
};

module.exports = nextConfig;
