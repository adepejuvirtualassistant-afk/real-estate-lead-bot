/**
 * Frontend API client.
 * All backend communication should go through this module.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export async function healthCheck() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

// Future: chat, leads, etc.
