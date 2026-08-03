export default function PageHero({ eyebrow, title, subtitle, children, home = false }) {
  return <header className={`page-hero${home ? ' page-hero--home' : ''}`}>
    <div className="page-hero__content">
      <p className="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p className="page-hero__subtitle">{subtitle}</p>
      {children && <div className="page-hero__actions">{children}</div>}
    </div>
  </header>
}
