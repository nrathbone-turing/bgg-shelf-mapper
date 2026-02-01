import { useEffect, useState } from 'react'
import { api } from './api'
import type { Fixture, FixtureGrid } from './types'
import FixtureGridView from './components/FixtureGrid'
import GameSearch from './components/GameSearch'

export default function App() {
  const [fixtures, setFixtures] = useState<Fixture[]>([])
  const [activeFixtureId, setActiveFixtureId] = useState<number | null>(null)
  const [grid, setGrid] = useState<FixtureGrid | null>(null)
  const [selectedSlot, setSelectedSlot] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function refreshFixtures() {
    setError(null)
    const data = await api.listFixtures()
    setFixtures(data)
    if (!activeFixtureId && data.length > 0) {
      setActiveFixtureId(data[0].id)
    }
  }

  async function refreshGrid(fixtureId: number) {
    setError(null)
    const g = await api.getFixtureGrid(fixtureId)
    setGrid(g)
  }

  useEffect(() => {
    refreshFixtures().catch((e) => setError(e?.message ?? String(e)))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (!activeFixtureId) return
    refreshGrid(activeFixtureId).catch((e) => setError(e?.message ?? String(e)))
  }, [activeFixtureId])

  const activeFixture = fixtures.find((f) => f.id === activeFixtureId) ?? null

  return (
    <div className="container">
      <div className="header">
        <h2 style={{ margin: 0 }}>BGG Shelf Mapper</h2>

        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <label style={{ fontSize: 12, opacity: 0.8 }}>Fixture:</label>
          <select
            value={activeFixtureId ?? ''}
            onChange={(e) => {
              const id = Number(e.target.value)
              setActiveFixtureId(id)
              setSelectedSlot(null)
            }}
          >
            {fixtures.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name}
              </option>
            ))}
          </select>

          <button
            onClick={() => {
              if (activeFixtureId) refreshGrid(activeFixtureId)
            }}
            disabled={!activeFixtureId}
          >
            Reload grid
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {grid && activeFixture ? (
        <>
          <div className="row">
            <div style={{ flex: 2, minWidth: 340 }}>
              <FixtureGridView
                grid={grid}
                selectedSlot={selectedSlot}
                onSelectSlot={(slot) => setSelectedSlot(slot)}
              />
            </div>

            <GameSearch
              fixtureId={activeFixture.id}
              selectedSlot={selectedSlot}
              onChanged={() => refreshGrid(activeFixture.id)}
            />
          </div>
        </>
      ) : (
        <div style={{ marginTop: 16, opacity: 0.8 }}>
          Loading fixture… (If this hangs, make sure the API is running on port 8000.)
        </div>
      )}
    </div>
  )
}
