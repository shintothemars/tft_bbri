"""
Django REST Framework views for stock prediction
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from bokeh.plotting import figure
from bokeh.models import HoverTool, Range1d, Band, ColumnDataSource
from bokeh.embed import json_item
import pandas as pd
import numpy as np

from .model import get_predictor


class HealthCheckView(APIView):
    """Health check endpoint"""
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'BBRI Stock Prediction API',
            'version': '1.0.0'
        })


class PredictStockView(APIView):
    """
    API endpoint for stock prediction
    
    POST /api/predict/
    Body: {
        "target_date": "2025-12-31"  // Format: YYYY-MM-DD
    }
    """
    
    def post(self, request):
        try:
            # Get target date from request
            target_date_str = request.data.get('target_date')
            
            if not target_date_str:
                return Response({
                    'error': 'Parameter target_date diperlukan (format: YYYY-MM-DD)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate date format
            try:
                target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
            except ValueError:
                return Response({
                    'error': 'Format tanggal tidak valid. Gunakan format: YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get predictor and make prediction
            predictor = get_predictor()
            result = predictor.predict(target_date)
            
            # Create Bokeh visualization
            bokeh_plot = self._create_bokeh_plot(result)
            
            # Add bokeh plot to result
            result['bokeh_plot'] = bokeh_plot
            
            return Response(result, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': f'Terjadi kesalahan: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _create_bokeh_plot(self, prediction_data):
        """
        Create interactive Bokeh plot with confidence intervals
        
        Args:
            prediction_data: Dictionary containing prediction results
            
        Returns:
            JSON representation of Bokeh plot
        """
        try:
            # Extract data
            hist_dates = pd.to_datetime(prediction_data['historical']['dates'])
            hist_prices = prediction_data['historical']['close']
            
            pred_dates = pd.to_datetime(prediction_data['predictions']['dates'])
            pred_median = prediction_data['predictions']['median']
            pred_lower = prediction_data['predictions']['lower_bound']
            pred_upper = prediction_data['predictions']['upper_bound']
            
            # Create figure
            p = figure(
                title="Prediksi Harga Saham BBRI",
                x_axis_type='datetime',
                width=1000,
                height=500,
                tools="pan,wheel_zoom,box_zoom,reset,save",
                toolbar_location="above",
                sizing_mode="stretch_width"
            )
            
            # Historical data line
            p.line(
                hist_dates, 
                hist_prices,
                legend_label="Data Historis",
                line_width=2.5,
                color='#2C3E50',
                alpha=0.8
            )
            
            # Historical data circles for hover
            hist_source = ColumnDataSource(data=dict(
                date=hist_dates,
                price=hist_prices,
                date_formatted=[d.strftime('%d %b %Y') for d in hist_dates],
                price_formatted=[f"Rp {p:,.0f}" for p in hist_prices]
            ))
            
            hist_circles = p.circle(
                'date',
                'price',
                source=hist_source,
                size=5,
                color='#2C3E50',
                alpha=0.6
            )
            
            # Prediction median line
            p.line(
                pred_dates,
                pred_median,
                legend_label="Prediksi (Median)",
                line_width=3,
                color='#E74C3C',
                alpha=0.9
            )
            
            # Prediction circles for hover
            pred_source = ColumnDataSource(data=dict(
                date=pred_dates,
                median=pred_median,
                lower=pred_lower,
                upper=pred_upper,
                date_formatted=[d.strftime('%d %b %Y') for d in pred_dates],
                median_formatted=[f"Rp {p:,.0f}" for p in pred_median],
                lower_formatted=[f"Rp {p:,.0f}" for p in pred_lower],
                upper_formatted=[f"Rp {p:,.0f}" for p in pred_upper]
            ))
            
            pred_circles = p.circle(
                'date',
                'median',
                source=pred_source,
                size=6,
                color='#E74C3C',
                alpha=0.8
            )
            
            # Confidence interval (shaded area)
            band_source = ColumnDataSource(data=dict(
                date=pred_dates,
                lower=pred_lower,
                upper=pred_upper
            ))
            
            band = Band(
                base='date',
                lower='lower',
                upper='upper',
                source=band_source,
                level='underlay',
                fill_alpha=0.3,
                fill_color='#3498DB',
                line_width=1,
                line_color='#3498DB',
                line_dash='dashed',
                line_alpha=0.5
            )
            p.add_layout(band)
            
            # Add hover tools
            hist_hover = HoverTool(
                renderers=[hist_circles],
                tooltips=[
                    ("Tanggal", "@date_formatted"),
                    ("Harga", "@price_formatted"),
                ],
                mode='mouse'
            )
            
            pred_hover = HoverTool(
                renderers=[pred_circles],
                tooltips=[
                    ("Tanggal", "@date_formatted"),
                    ("Prediksi", "@median_formatted"),
                    ("Rentang Bawah (10%)", "@lower_formatted"),
                    ("Rentang Atas (90%)", "@upper_formatted"),
                ],
                mode='mouse'
            )
            
            p.add_tools(hist_hover, pred_hover)
            
            # Styling
            p.title.text_font_size = "16pt"
            p.title.text_color = "#2C3E50"
            p.title.align = "center"
            
            p.xaxis.axis_label = "Tanggal"
            p.xaxis.axis_label_text_font_size = "12pt"
            p.xaxis.major_label_text_font_size = "10pt"
            
            p.yaxis.axis_label = "Harga (IDR)"
            p.yaxis.axis_label_text_font_size = "12pt"
            p.yaxis.major_label_text_font_size = "10pt"
            p.yaxis.formatter.use_scientific = False
            
            # Format y-axis to show currency
            from bokeh.models import NumeralTickFormatter
            p.yaxis.formatter = NumeralTickFormatter(format="0,0")
            
            # Legend styling
            p.legend.location = "top_left"
            p.legend.click_policy = "hide"
            p.legend.label_text_font_size = "10pt"
            p.legend.background_fill_alpha = 0.8
            
            # Grid styling
            p.grid.grid_line_alpha = 0.3
            
            # Background
            p.background_fill_color = "#FAFAFA"
            p.border_fill_color = "#FFFFFF"
            
            # Convert to JSON for embedding in React
            return json_item(p, "bbri_prediction_plot")
            
        except Exception as e:
            print(f"❌ Error creating Bokeh plot: {str(e)}")
            raise
