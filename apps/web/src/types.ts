export type GameWithPlacement = {
  id: number
  bgg_id: number
  name: string
  year_published?: number | null
  thumbnail_url?: string | null
  image_url?: string | null
  fixture_id?: number | null
  slot?: string | null
}

export type Fixture = {
  id: number
  name: string
  rows: number
  cols: number
}

export type GridCell = {
  slot: string
  game: {
    id: number
    bgg_id: number
    name: string
    year_published?: number | null
    thumbnail_url?: string | null
    image_url?: string | null
  } | null
}

export type FixtureGrid = {
  fixture: Fixture
  cells: GridCell[]
}
