import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { AuthProvider } from '../context/AuthContext'
import AppRoutes from './AppRoutes'

const json = (body, status = 200) => Promise.resolve(new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } }))
const renderRoute = (path) => render(<MemoryRouter initialEntries={[path]}><AuthProvider><AppRoutes /></AuthProvider></MemoryRouter>)

afterEach(() => vi.restoreAllMocks())

describe('Japan 47 routes', () => {
  it('shows loading and then renders API-backed home content', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(() => json({ latest_places: [], top_places: [], top_prefectures: [], top_regions: [], top_contributors: [] }))
    renderRoute('/')
    expect(screen.getByRole('status')).toHaveTextContent('Loading Japan 47')
    expect(await screen.findByRole('heading', { name: 'The latest places' })).toBeInTheDocument()
    expect(screen.getByText('No published places have been added yet.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Register' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /theme/i })).not.toBeInTheDocument()
  })

  it('renders a useful API error state', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(() => json({ error: { code: 'service_unavailable', message: 'Please try later.' } }, 503))
    renderRoute('/regions')
    expect(await screen.findByRole('alert')).toHaveTextContent('Please try later.')
  })

  it('submits login credentials and navigates to the requested protected page', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation((url) => {
      if (String(url).endsWith('/auth/login/')) return json({ access: 'access-token', refresh: 'refresh-token' })
      if (String(url).endsWith('/profile/')) return json({ id: 7, display_name: 'Sakura', profile_image_url: null, nickname: 'Sakura', email: 'sakura@example.com' })
      if (String(url).endsWith('/home/')) return json({ latest_places: [], top_places: [], top_prefectures: [], top_regions: [], top_contributors: [] })
      if (String(url).endsWith('/prefectures/')) return json([])
      if (String(url).endsWith('/health/')) return json({ status: 'ok' })
      return json({ status: 'ok' })
    })
    renderRoute('/login')
    await userEvent.type(screen.getByLabelText('Username'), 'sakura')
    await userEvent.type(screen.getByLabelText('Password'), 'StrongPass123!')
    await userEvent.click(screen.getByRole('button', { name: 'Login' }))
    await waitFor(() => expect(screen.getByText('Sakura')).toBeInTheDocument())
    expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/auth/login/'), expect.objectContaining({ method: 'POST' }))
  })

  it('keeps discovery filters in the URL-backed API request', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation((url) => {
      if (String(url).includes('/places/')) return json({ count: 0, page: 1, pages: 1, next: null, previous: null, results: [] })
      return json([])
    })
    renderRoute('/places?region=kanto&best_season=spring')
    expect(await screen.findByText('No places match')).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/places/?region=kanto&best_season=spring'), expect.any(Object))
  })
})
