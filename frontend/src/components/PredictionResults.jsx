import { useEffect } from 'react'
import BokehChart from './BokehChart'

function PredictionResults({ data }) {
    if (!data || !data.success) {
        return null
    }

    const { analysis, target_date, last_data_date, prediction_horizon } = data

    // Format currency
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(value)
    }

    // Format date
    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('id-ID', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        })
    }

    const trendDirection = analysis.trend_direction
    const trendPercentage = Math.abs(analysis.trend_percentage).toFixed(2)
    const isUpTrend = trendDirection === 'NAIK'

    return (
        <div className="results-container">
            {/* Statistics Cards */}
            <div className="card">
                <h2 className="card-title">
                    <span className="card-icon">📊</span>
                    Hasil Prediksi
                </h2>

                <div className="results-grid">
                    <div className="stat-card">
                        <div className="stat-label">Harga Terakhir</div>
                        <div className="stat-value">
                            {formatCurrency(analysis.last_price)}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.5rem' }}>
                            Per {formatDate(last_data_date)}
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-label">Prediksi Harga</div>
                        <div className={`stat-value ${isUpTrend ? 'success' : 'danger'}`}>
                            {formatCurrency(analysis.predicted_price)}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.5rem' }}>
                            Target {formatDate(target_date)}
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-label">Perubahan</div>
                        <div className={`stat-value ${isUpTrend ? 'success' : 'danger'}`}>
                            {isUpTrend ? '↑' : '↓'} {trendPercentage}%
                        </div>
                        <div className={`trend-badge ${isUpTrend ? 'up' : 'down'}`}>
                            {isUpTrend ? '📈 Tren Naik' : '📉 Tren Turun'}
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-label">Rentang Prediksi</div>
                        <div className="stat-value" style={{ fontSize: '1rem' }}>
                            {formatCurrency(analysis.confidence_range.lower)}
                            <br />
                            <span style={{ fontSize: '0.75rem', color: '#6b7280' }}>sampai</span>
                            <br />
                            {formatCurrency(analysis.confidence_range.upper)}
                        </div>
                    </div>
                </div>
            </div>

            {/* Analysis Panel */}
            <div className="analysis-panel">
                <h3 className="analysis-title">
                    💡 Analisis Prediksi
                </h3>
                <p className="analysis-text">
                    Berdasarkan model Temporal Fusion Transformer, harga saham BBRI diprediksi akan{' '}
                    <strong>{trendDirection}</strong> sebesar <strong>{trendPercentage}%</strong> dalam{' '}
                    <strong>{prediction_horizon} hari</strong> ke depan (dari {formatCurrency(analysis.last_price)} menjadi{' '}
                    {formatCurrency(analysis.predicted_price)}).
                </p>
                <p className="analysis-text" style={{ marginTop: '1rem' }}>
                    Area berwarna biru pada grafik menunjukkan <strong>rentang ketidakpastian</strong> prediksi.
                    Harga aktual kemungkinan besar akan berada di antara{' '}
                    <strong>{formatCurrency(analysis.confidence_range.lower)}</strong> dan{' '}
                    <strong>{formatCurrency(analysis.confidence_range.upper)}</strong>.
                </p>
            </div>

            {/* Bokeh Chart */}
            <div className="card">
                <h2 className="card-title">
                    <span className="card-icon">📈</span>
                    Visualisasi Prediksi
                </h2>

                <div className="info-box">
                    <div className="info-box-title">📖 Cara Membaca Grafik</div>
                    <div className="info-box-text">
                        <ul style={{ marginLeft: '1.5rem', marginTop: '0.5rem' }}>
                            <li><strong>Garis Gelap:</strong> Data historis harga saham BBRI (90 hari terakhir)</li>
                            <li><strong>Garis Merah:</strong> Prediksi harga (nilai median)</li>
                            <li><strong>Area Biru Transparan:</strong> Rentang kemungkinan harga (confidence interval 10%-90%)</li>
                            <li><strong>Hover:</strong> Arahkan kursor ke grafik untuk melihat detail harga dan tanggal</li>
                        </ul>
                    </div>
                </div>

                <BokehChart plotData={data.bokeh_plot} />
            </div>

            {/* Disclaimer */}
            <div className="card" style={{ background: '#fef3c7', border: '2px solid #fbbf24' }}>
                <h3 style={{ color: '#92400e', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    ⚠️ Disclaimer
                </h3>
                <p style={{ color: '#78350f', lineHeight: '1.6' }}>
                    Prediksi ini dibuat menggunakan model machine learning dan <strong>bukan merupakan saran investasi</strong>.
                    Harga saham dipengaruhi oleh banyak faktor yang tidak dapat sepenuhnya diprediksi.
                    Selalu lakukan riset mendalam dan konsultasi dengan ahli keuangan sebelum membuat keputusan investasi.
                </p>
            </div>
        </div>
    )
}

export default PredictionResults
