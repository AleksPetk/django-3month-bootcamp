import { Link, useParams } from 'react-router-dom'
import { PlaceCard, PrefectureCard } from '../components/Cards'
import { ErrorState, LoadingState } from '../components/AsyncState'
import MediaImage from '../components/MediaImage'
import Rating from '../components/Rating'
import { useApi } from '../hooks/useApi'

export default function RegionDetailPage() {
  const { name } = useParams()
  const { data, loading, error } = useApi(`/regions/${encodeURIComponent(name)}/`)
  if (loading) return <LoadingState />
  if (error) return <ErrorState error={error} />
  return <article className="detail page"><Link className="back" to="/regions">← Back to all regions</Link><header className="detail-hero"><div><p className="eyebrow">Region of Japan</p><h1>{data.label}</h1><Rating value={data.average_rating} large /><div className="prose">{data.description}</div></div><MediaImage src={data.image_url} alt={`${data.label} region`} mark="日" priority /></header>
    {data.top_prefecture && <aside className="featured-callout"><p className="eyebrow">Highest rated prefecture</p><h2>{data.top_prefecture.name}</h2><Rating value={data.top_prefecture.average_rating} /></aside>}
    <section className="feature"><header className="section-header"><div><p className="eyebrow">Where to go</p><h2>Prefectures in {data.label}</h2></div></header><div className="grid grid--3">{data.prefectures.map((item) => <PrefectureCard key={item.id} prefecture={item} />)}</div></section>
    {data.popular_places?.length > 0 && <section className="feature"><header className="section-header"><div><p className="eyebrow">Community favorites</p><h2>Most popular places</h2></div></header><div className="grid grid--3">{data.popular_places.map((place) => <PlaceCard key={place.id} place={place} />)}</div></section>}
  </article>
}
