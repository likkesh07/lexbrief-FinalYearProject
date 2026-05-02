import styles from './Loader.module.css'

export default function Loader({ message, progress }) {
  return (
    <div className={styles.wrap}>
      {progress > 0 && progress < 100 && (
        <div className={styles.progressBar}>
          <div className={styles.progressFill} style={{ width: `${progress}%` }} />
        </div>
      )}
      <div className={styles.row}>
        <div className={styles.spinner} aria-hidden="true" />
        <span className={styles.message} aria-live="polite">{message}</span>
      </div>
    </div>
  )
}
