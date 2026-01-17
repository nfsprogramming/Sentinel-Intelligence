"use server";

import { exec } from "child_process";
import path from "path";
import util from "util";
import { MOCK_TRANSCENDENT_DATA } from "@/lib/mockData";

const execPromise = util.promisify(exec);

export async function getMarketPrediction(ticker: string, name: string) {
    // 1. Production Mode: Use Remote Render Backend (Hybrid Architecture)
    const apiUrl = process.env.NEXT_PUBLIC_API_URL; // e.g., https://sentinel-intelligence.onrender.com

    if (apiUrl && process.env.NODE_ENV === "production") {
        console.log(`📡 Connecting to Sentinel Cortex: ${apiUrl}`);
        try {
            const res = await fetch(`${apiUrl}/predict`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ticker, name }),
                cache: "no-store"
            });

            if (!res.ok) throw new Error(`Backend Error ${res.status}`);
            return await res.json();
        } catch (error) {
            console.error("❌ Remote Cortex Connection Failed:", error);
            // If remote fails, fall back to mock data (or local if configured)
            return MOCK_TRANSCENDENT_DATA;
        }
    }

    // 2. Local Mode: Run Python Script directly (for development)
    // Only runs if NOT in production cloud (Vercel)
    // 2. Local Mode: Use Local FastAPI Server (Keep models loaded for speed)
    if (process.env.NODE_ENV !== "production") {
        const localApiUrl = "http://127.0.0.1:8000";
        console.log(`⚡ Connecting to Local Neural Core: ${localApiUrl}`);

        try {
            const res = await fetch(`${localApiUrl}/predict`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ticker, name }),
                cache: "no-store"
            });

            if (!res.ok) {
                // If local server isn't running, this will throw
                throw new Error(`Local Cortex Offline (${res.status})`);
            }
            return await res.json();

        } catch (e) {
            console.warn("⚠️ Local Core Unreachable. Ensure backend/main.py is running.");
            console.error(e);
            // Fallthrough to mock data if server is down, or we could handle it UI side
        }
    }

    // 3. Fallback: Holographic Mock Data (Demo Mode)
    console.log("💎 Using Holographic Demo Data");
    await new Promise(resolve => setTimeout(resolve, 1500));
    return MOCK_TRANSCENDENT_DATA;
}
