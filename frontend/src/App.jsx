import { useState } from 'react'
import PredictionForm from './components/PredictionForm'
import PredictionResults from './components/PredictionResults'

function App() {
    const [predictionData, setPredictionData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handlePrediction = (data) => {
        setPredictionData(data)
        setError(null)
    }

    const handleError = (errorMessage) => {
        setError(errorMessage)
        setPredictionData(null)
    }

    const handleLoading = (isLoading) => {
        setLoading(isLoading)
    }

    return (
        <div className="app-container">
            <header className="app-header">
                <h1 className="app-title">📈 Prediksi Saham BBRI</h1>
                <p className="app-subtitle">
                    Prediksi Harga Saham Bank Rakyat Indonesia menggunakan AI
                </p>
                <span className="app-badge">
                    Powered by Temporal Fusion Transformer
                </span>
            </header>

            <main className="main-content">
                <PredictionForm
                    onPrediction={handlePrediction}
                    onError={handleError}
                    onLoading={handleLoading}
                    loading={loading}
                />

                {error && (
                    <div className="card">
                        <div className="error-message">
                            <strong>❌ Terjadi Kesalahan:</strong> {error}
                        </div>
                    </div>
                )}

                {predictionData && (
                    <PredictionResults data={predictionData} />
                )}
            </main>

            <footer style={{
                textAlign: 'center',
                color: 'white',
                marginTop: '3rem',
                opacity: 0.8,
                fontSize: '0.875rem'
            }}>
                <p>© 2025 BBRI Stock Prediction System | Developed with ❤️ using Django & React</p>
            </footer>
        </div>
    )
}

export default App
