# Module for generating monthly reports

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import json

class ReportGenerator:
    def __init__(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_report(self, analysis_results, user_id):
        """Generate a monthly report from analysis results."""
        timestamp = datetime.now().strftime("%Y%m_%B")  # YYYYMM_MonthName
        
        # Create report directory for the month if it doesn't exist
        month_dir = os.path.join(self.reports_dir, timestamp)
        os.makedirs(month_dir, exist_ok=True)
        
        # Convert boolean values to integers for JSON serialization
        serializable_results = {
            'risk_score': analysis_results['risk_score'],
            'risk_factors': {k: int(v) for k, v in analysis_results['risk_factors'].items()},
            'recommendations': analysis_results['recommendations']
        }
        
        # Prepare report data
        report_data = {
            'user_id': user_id,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'analysis_results': serializable_results
        }
        
        # Save raw data as JSON
        json_path = os.path.join(month_dir, f"report_data_{user_id}.json")
        with open(json_path, 'w') as f:
            json.dump(report_data, f, indent=4)
            
        # Generate visualizations
        self._generate_visualizations(analysis_results, month_dir, user_id)
        
        # Generate HTML report
        html_report = self._generate_html_report(report_data, month_dir, user_id)
        
        return html_report
        
    def _generate_visualizations(self, analysis_results, report_dir, user_id):
        """Generate visualizations for the report."""
        # Plot risk factors
        plt.figure(figsize=(10, 6))
        risk_factors = analysis_results['risk_factors']
        plt.bar(range(len(risk_factors)), 
                [1 if v else 0 for v in risk_factors.values()],
                tick_label=list(risk_factors.keys()))
        plt.title('Risk Factors Analysis')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(report_dir, f"risk_factors_{user_id}.png"))
        plt.close()
        
    def _generate_html_report(self, report_data, report_dir, user_id):
        """Generate an HTML report."""
        html_content = f"""
        <html>
        <head>
            <title>Speech Analysis Report - {report_data['date']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .risk-score {{ font-size: 24px; margin: 20px 0; }}
                .recommendations {{ margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Speech Analysis Report</h1>
                <p>User ID: {report_data['user_id']}</p>
                <p>Date: {report_data['date']}</p>
            </div>
            
            <div class="risk-score">
                Overall Risk Score: {report_data['analysis_results']['risk_score']:.2f}
            </div>
            
            <div class="recommendations">
                <h2>Recommendations:</h2>
                <ul>
                    {''.join(f'<li>{rec}</li>' for rec in report_data['analysis_results']['recommendations'])}
                </ul>
            </div>
            
            <div class="visualizations">
                <h2>Risk Factors Analysis</h2>
                <img src="risk_factors_{user_id}.png" alt="Risk Factors Graph">
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        html_path = os.path.join(report_dir, f"report_{user_id}.html")
        with open(html_path, 'w') as f:
            f.write(html_content)
            
        return html_path
