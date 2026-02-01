import type { Fixture, FixtureGrid, GameWithPlacement } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {})
    }
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${text}`)
  }
  return (await res.json()) as T
}

export const api = {
  listFixtures: () => apiFetch<Fixture[]>('/api/fixtures'),
  getFixtureGrid: (fixtureId: number) => apiFetch<FixtureGrid>(`/api/fixtures/${fixtureId}/grid`),
  listGames: (q?: string) => {
    const params = q ? `?q=${encodeURIComponent(q)}` : ''
    return apiFetch<GameWithPlacement[]>(`/api/games${params}`)
  },
  upsertPlacement: (fixtureId: number, slot: string, gameId: number) =>
    apiFetch(`/api/placements`, {
      method: 'PUT',
      body: JSON.stringify({ fixture_id: fixtureId, slot, game_id: gameId })
    }),
  clearSlot: (fixtureId: number, slot: string) =>
    apiFetch(`/api/placements/${fixtureId}/${encodeURIComponent(slot)}`, {
      method: 'DELETE'
    })
}
