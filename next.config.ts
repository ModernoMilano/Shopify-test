import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // pdfjs laadt zijn worker zelf; niet bundelen, anders faalt het inlezen van PDF-afschriften online
  serverExternalPackages: ["pdfjs-dist"],
  experimental: {
    // bankafschriften als PDF kunnen groter zijn dan de standaardlimiet van 1 MB
    serverActions: { bodySizeLimit: "20mb" },
  },
};

export default nextConfig;
