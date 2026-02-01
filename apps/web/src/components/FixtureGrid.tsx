import type { FixtureGrid } from '../types'

type Props = {
  grid: FixtureGrid
  selectedSlot: string | null
  onSelectSlot: (slot: string) => void
}

export default function FixtureGridView({ grid, selectedSlot, onSelectSlot }: Props) {
  const { fixture, cells } = grid

  return (
    <div>
      <div>
        <strong>{fixture.name}</strong> — {fixture.rows} rows × {fixture.cols} cols
      </div>

      <div
        className="grid"
        style={{
          gridTemplateColumns: `repeat(${fixture.cols}, minmax(160px, 1fr))`
        }}
      >
        {cells.map((cell) => {
          const isSelected = cell.slot === selectedSlot
          return (
            <div
              key={cell.slot}
              className={`cell ${isSelected ? 'selected' : ''}`}
              onClick={() => onSelectSlot(cell.slot)}
              title="Click to select this cube"
            >
              <div className="cellTitle">{cell.slot}</div>
              <div className="cellGame">{cell.game ? cell.game.name : '— empty —'}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
