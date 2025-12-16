import { useEffect, useRef } from 'react'

function BokehChart({ plotData }) {
    const chartRef = useRef(null)

    useEffect(() => {
        if (!plotData || !window.Bokeh) {
            console.error('Bokeh or plot data not available')
            return
        }

        try {
            // Clear previous chart
            if (chartRef.current) {
                chartRef.current.innerHTML = ''
            }

            // Embed Bokeh plot
            window.Bokeh.embed.embed_item(plotData, 'bokeh-plot')
        } catch (error) {
            console.error('Error embedding Bokeh plot:', error)
        }
    }, [plotData])

    return (
        <div className="chart-container">
            <div id="bokeh-plot" ref={chartRef}></div>
        </div>
    )
}

export default BokehChart
