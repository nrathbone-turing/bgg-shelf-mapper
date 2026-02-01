import { useEffect, useMemo, useState } from 'react'
import { api } from '../api'
import type { GameWithPlacement } from '../types'

type Props = {
  fixtureId: number
  selectedSlot: string | null
  onChanged: () => void
}

export default function GameSearch({ fixtureId, selectedSlot, onChanged }: Props) {
  const [q, setQ] = useState('')
  const [games, setGames] = useState<GameWithPlacement[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function refresh() {
    setLoading(true)
    setError(null)
    try {
      const data = await api.listGames(q.trim() ? q.trim() : undefined)
      setGames(data)
    } catch (e: any) {
      setError(e?.message ?? String(e))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // initial fetch
    refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const selectedHint = useMemo(() => {
    return selectedSlot ? `Selected cube: ${selectedSlot}` : 'Select a cube to assign a game'
  }, [selectedSlot])

  async function assign(gameId: number) {
    if (!selectedSlot) {
      setError('Pick a cube first (click one in the grid).')
      return
    }
    setError(null)
    try {
      await api.upsertPlacement(fixtureId, selectedSlot, gameId)
      await refresh()
      onChanged()
    } catch (e: any) {
      setError(e?.message ?? String(e))
    }
  }

  async function clearSelected() {
    if (!selectedSlot) {
      setError('Pick a cube first (click one in the grid).')
      return
    }
    setError(null)
    try {
      await api.clearSlot(fixtureId, selectedSlot)
      await refresh()
      onChanged()
    } catch (e: any) {
      setError(e?.message ?? String(e))
    }
  }

  return (
    <div className="panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
        <div>
          <strong>Search & assign</strong>
          <div className="gameMeta">{selectedHint}</div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={clearSelected} disabled={!selectedSlot}>
            Clear cube
          </button>
          <button onClick={refresh} disabled={loading}>
            {loading ? 'Loading…' : 'Refresh'}
          </button>
        </div>
      </div>

      <div className="inputRow" style={{ marginTop: 10 }}>
        <input
          type="text"
          placeholder="Search games by name…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') refresh()
          }}
        />
        <button onClick={refresh} disabled={loading}>
          Search
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="gameList">
        {games.map((g) => (
          <div className="gameItem" key={g.id}>
            <div>
              <div>
                {g.name} {g.year_published ? `(${g.year_published})` : ''}
              </div>
              <div className="gameMeta">
                BGG #{g.bgg_id}
                {g.slot ? ` • placed: ${g.slot}` : ' • unplaced'}
              </div>
            </div>
            <div>
              <button onClick={() => assign(g.id)} disabled={!selectedSlot}>
                Put in {selectedSlot ?? '…'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
