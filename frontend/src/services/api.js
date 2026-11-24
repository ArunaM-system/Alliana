/**
 * ALLINA API Service Client.
 * Centralized API calls with environment-configurable base URL.
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE_URL}/api/v1/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function fetchUsers() {
  const res = await fetch(`${API_BASE_URL}/api/v1/users/`);
  if (!res.ok) throw new Error(`Failed to fetch users: ${res.statusText}`);
  return res.json();
}

export async function triggerTask() {
  const res = await fetch(`${API_BASE_URL}/api/v1/run-task`);
  if (!res.ok) throw new Error(`Task trigger failed: ${res.statusText}`);
  return res.json();
}
