import { useState } from 'react'
import axios from 'axios'
import { format, addDays } from 'date-fns'

function PredictionForm({ onPrediction, onError, onLoading, loading }) {
    const today = new Date()
    const defaultDate = addDays(today, 7) // Default to 7 days from now

    const [day, setDay] = useState(defaultDate.getDate())
    const [month, setMonth] = useState(defaultDate.getMonth() + 1)
    const [year, setYear] = useState(defaultDate.getFullYear())

    const handleSubmit = async (e) => {
        e.preventDefault()

        // Validate inputs
        if (!day || !month || !year) {
            onError('Mohon isi semua field tanggal')
            return
        }

        // Create date string
        const targetDate = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`

        // Validate date
        const selectedDate = new Date(targetDate)
        if (isNaN(selectedDate.getTime())) {
            onError('Tanggal tidak valid')
            return
        }

        if (selectedDate <= today) {
            onError('Tanggal target harus di masa depan')
            return
        }

        // Check if date is within 30 days
        const maxDate = addDays(today, 30)
        if (selectedDate > maxDate) {
            const maxDateStr = format(maxDate, 'dd MMMM yyyy', { locale: require('date-fns/locale/id') })
            onError(`Prediksi maksimal 30 hari dari sekarang. Pilih tanggal sebelum ${maxDateStr}`)
            return
        }

        // Call API
        onLoading(true)
        try {
            const response = await axios.post('/api/predict/', {
                target_date: targetDate
            })

            onPrediction(response.data)
        } catch (err) {
            const errorMessage = err.response?.data?.error || 'Gagal melakukan prediksi. Silakan coba lagi.'
            onError(errorMessage)
        } finally {
            onLoading(false)
        }
    }

    // Generate day options
    const days = Array.from({ length: 31 }, (_, i) => i + 1)

    // Generate month options
    const months = [
        { value: 1, label: 'Januari' },
        { value: 2, label: 'Februari' },
        { value: 3, label: 'Maret' },
        { value: 4, label: 'April' },
        { value: 5, label: 'Mei' },
        { value: 6, label: 'Juni' },
        { value: 7, label: 'Juli' },
        { value: 8, label: 'Agustus' },
        { value: 9, label: 'September' },
        { value: 10, label: 'Oktober' },
        { value: 11, label: 'November' },
        { value: 12, label: 'Desember' }
    ]

    // Generate year options (current year + 1)
    const currentYear = today.getFullYear()
    const years = [currentYear, currentYear + 1]

    return (
        <div className="card">
            <h2 className="card-title">
                <span className="card-icon">📅</span>
                Pilih Tanggal Target Prediksi
            </h2>

            <div className="info-box">
                <div className="info-box-title">ℹ️ Cara Menggunakan</div>
                <div className="info-box-text">
                    Pilih tanggal di masa depan untuk melihat prediksi harga saham BBRI.
                    <br /><br />
                    <strong>⚠️ Batasan:</strong> Maksimal <strong>30 hari</strong> dari hari ini.
                    <br />
                    <strong>✅ Contoh tanggal valid:</strong>
                    <ul style={{ marginLeft: '1.5rem', marginTop: '0.5rem' }}>
                        <li>23 Desember 2025 (7 hari dari sekarang)</li>
                        <li>31 Desember 2025 (15 hari dari sekarang)</li>
                        <li>15 Januari 2026 (30 hari dari sekarang)</li>
                    </ul>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="prediction-form">
                <div className="date-inputs">
                    <div className="form-group">
                        <label className="form-label" htmlFor="day">Hari</label>
                        <select
                            id="day"
                            className="form-input"
                            value={day}
                            onChange={(e) => setDay(parseInt(e.target.value))}
                            disabled={loading}
                        >
                            {days.map(d => (
                                <option key={d} value={d}>{d}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="month">Bulan</label>
                        <select
                            id="month"
                            className="form-input"
                            value={month}
                            onChange={(e) => setMonth(parseInt(e.target.value))}
                            disabled={loading}
                        >
                            {months.map(m => (
                                <option key={m.value} value={m.value}>{m.label}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="year">Tahun</label>
                        <select
                            id="year"
                            className="form-input"
                            value={year}
                            onChange={(e) => setYear(parseInt(e.target.value))}
                            disabled={loading}
                        >
                            {years.map(y => (
                                <option key={y} value={y}>{y}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading}
                >
                    {loading ? (
                        <>
                            <span className="spinner"></span>
                            Memproses Prediksi...
                        </>
                    ) : (
                        <>
                            🔮 Prediksi Sekarang
                        </>
                    )}
                </button>
            </form>
        </div>
    )
}

export default PredictionForm
