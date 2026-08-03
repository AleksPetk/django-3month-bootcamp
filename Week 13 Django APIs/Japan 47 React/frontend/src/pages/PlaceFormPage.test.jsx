import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, expect, it, vi } from 'vitest'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import PlaceFormPage from './PlaceFormPage'

vi.mock('../api/client', () => ({ api: vi.fn() }))
vi.mock('../hooks/useApi', () => ({ useApi: vi.fn() }))

const prefecture = { id: 1, name: 'Tokyo', region: { label: 'Kanto' } }
const prefectures = [prefecture]
const place = {
  id: 7,
  name: 'Akihabara',
  slug: 'akihabara',
  description: 'Electric town.',
  image_url: '/media/main.jpg',
  city: '',
  google_maps_url: '',
  official_website: '',
  travel_tips: '',
  best_season: 'year_round',
  latitude: null,
  longitude: null,
  prefecture,
  gallery_images: [
    { id: 20, image_url: '/media/gallery.jpg', thumbnail_url: '/media/gallery-thumb.jpg', caption: 'Night' },
  ],
}

beforeEach(() => {
  api.mockReset()
  api.mockImplementation((path) => path === '/places/7/' ? Promise.resolve({ id: 7, slug: 'akihabara' }) : Promise.resolve(null))
  useApi.mockImplementation((path) => path === '/prefectures/'
    ? { data: prefectures, loading: false, error: null }
    : { data: place, loading: false, error: null })
})

it('shows existing images and submits explicit main and gallery removals', async () => {
  render(<MemoryRouter initialEntries={['/places/7/edit']}><Routes><Route path="/places/:id/edit" element={<PlaceFormPage />} /><Route path="/places/:id/:slug" element={<p>Saved</p>} /></Routes></MemoryRouter>)

  expect(screen.getByText('Current main image')).toBeInTheDocument()
  expect(screen.getByAltText('Night')).toBeInTheDocument()
  expect(screen.getByText(/3 slots available/)).toBeInTheDocument()

  await userEvent.click(screen.getByRole('button', { name: 'Remove image' }))
  await userEvent.click(screen.getByRole('button', { name: 'Remove photo' }))
  await userEvent.click(screen.getByRole('button', { name: 'Save changes' }))

  await waitFor(() => expect(api).toHaveBeenCalledWith('/places/7/images/20/', { method: 'DELETE' }))
  const updateCall = api.mock.calls.find(([path]) => path === '/places/7/')
  expect(updateCall[1].body.get('remove_image')).toBe('true')
  expect(await screen.findByText('Saved')).toBeInTheDocument()
})
