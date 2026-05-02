import styles from './Header.module.css'

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        Lex<span>Brief</span>
      </div>
      <div className={styles.badge}>AI Legal Summarizer</div>
    </header>
  )
}
