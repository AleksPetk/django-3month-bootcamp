import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, expect, it, vi } from 'vitest'
import { useApi } from '../hooks/useApi'
import PlaceDetailPage from './PlaceDetailPage'

vi.mock('../hooks/useApi', () => ({ useApi: vi.fn() }))
vi.mock('../context/AuthContext', () => ({ useAuth: () => ({ user: null }) }))

const place = {
  id: 1,
  name: 'Akihabara',
  slug: 'akihabara',
  description: 'Electric town.',
  image_url: '/media/main.jpg',
  status: 'published',
  created_at: '2026-01-01T00:00:00Z',
  average_rating: 4.5,
  review_count: 0,
  rating_distribution: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
  prefecture: { name: 'Tokyo', region: { label: 'Kanto' } },
  author: { id: 2, display_name: 'Traveler' },
  best_season: 'year_round',
  city: '',
  google_maps_url: '',
  official_website: '',
  travel_tips: '',
  can_edit: false,
  is_favorite: false,
  is_visited: false,
  reviews: [],
  gallery_images: [
    { id: 10, image_url: '/media/gallery-1.jpg', thumbnail_url: '/media/thumb-1.jpg', caption: 'Night view' },
    { id: 11, image_url: '/media/gallery-2.jpg', thumbnail_url: '/media/thumb-2.jpg', caption: 'Street view' },
  ],
  related_places: [],
  nearby_places: [],
}

beforeEach(() => useApi.mockReturnValue({ data: place, loading: false, error: null }))

it('keeps the main image separate and renders additional photos before reviews', () => {
  const { container } = render(<MemoryRouter><PlaceDetailPage /></MemoryRouter>)

  expect(container.querySelectorAll('.place-main-image img')).toHaveLength(1)
  expect(container.querySelector('.place-main-image img')).toHaveAttribute('src', '/media/main.jpg')
  expect(container.querySelectorAll('.place-photo-gallery__grid img')).toHaveLength(2)
  expect(screen.getByRole('heading', { name: 'Gallery' })).toBeInTheDocument()

  const gallery = container.querySelector('.place-photo-gallery')
  const reviews = container.querySelector('.reviews')
  expect(gallery.compareDocumentPosition(reviews) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
})
