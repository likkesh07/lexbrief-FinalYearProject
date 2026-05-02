import styles from './Hero.module.css'

export default function Hero() {
  return (
    <section className={styles.hero}>
      <div className={styles.content}>
        <h1>
          Understand any legal document <em>instantly</em>
        </h1>
        <p>
          Paste contracts, NDAs, leases, or any legal text — LexBrief extracts
          key clauses, obligations, risks, and plain-language summaries powered
          by Claude AI.
        </p>
      </div>
      <div className={styles.glyph} aria-hidden="true">§</div>
    </section>
  )
}
