import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Optional
import numpy as np

class HealthVisualizer:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.data_dir = "health_data"
        self.plots_dir = "health_plots"
        os.makedirs(self.plots_dir, exist_ok=True)
        
    def _load_data(self, category: str) -> pd.DataFrame:
        """Load data from JSON files into a pandas DataFrame."""
        file_path = os.path.join(self.data_dir, f"{self.user_id}_{category}.json")
        if not os.path.exists(file_path):
            return pd.DataFrame()
            
        data = []
        with open(file_path, 'r') as f:
            for line in f:
                data.append(json.loads(line.strip()))
        
        df = pd.DataFrame(data)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df

    def plot_sleep_trends(self, days: int = 30) -> str:
        """Generate sleep trends visualization."""
        df = self._load_data("sleep")
        if df.empty:
            return "No sleep data available"
            
        # Create figure with secondary y-axis
        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()
        
        # Plot sleep duration
        df['metrics'].apply(pd.Series)['duration'].plot(
            ax=ax1, marker='o', linestyle='-', color='blue', label='Duration (hours)'
        )
        
        # Plot sleep quality
        df['metrics'].apply(pd.Series)['quality'].plot(
            ax=ax2, marker='s', linestyle='--', color='green', label='Quality (1-10)'
        )
        
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Sleep Duration (hours)', color='blue')
        ax2.set_ylabel('Sleep Quality', color='green')
        
        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        plt.title('Sleep Trends Over Time')
        
        # Save plot
        plot_path = os.path.join(self.plots_dir, f'sleep_trends_{self.user_id}.png')
        plt.savefig(plot_path)
        plt.close()
        
        return plot_path

    def create_exercise_heatmap(self) -> str:
        """Generate exercise activity heatmap."""
        activities_data = self._load_data("exercise")
        if activities_data.empty:
            return "No exercise data available"
            
        # Prepare data for heatmap
        activity_matrix = pd.pivot_table(
            activities_data,
            values='duration',
            index=pd.to_datetime(activities_data['date']).dt.strftime('%A'),
            columns='activity_type',
            aggfunc='mean'
        ).fillna(0)
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(activity_matrix, annot=True, fmt='.0f', cmap='YlOrRd')
        plt.title('Weekly Exercise Activity Patterns')
        plt.xlabel('Activity Type')
        plt.ylabel('Day of Week')
        
        plot_path = os.path.join(self.plots_dir, f'exercise_heatmap_{self.user_id}.png')
        plt.savefig(plot_path)
        plt.close()
        
        return plot_path

    def plot_nutrition_radar(self) -> str:
        """Generate nutrition radar chart using plotly."""
        nutrition_data = self._load_data("nutrition")
        if nutrition_data.empty:
            return "No nutrition data available"
            
        # Calculate average nutritional metrics
        metrics = {
            'Water Intake': nutrition_data['water_intake'].mean(),
            'Diet Adherence': nutrition_data['diet_adherence'].mean(),
            'Meal Variety': len(set(str(m) for m in nutrition_data['meals'])),
            'Supplement Usage': len(set(str(s) for s in nutrition_data['supplements']))
        }
        
        # Create radar chart
        fig = go.Figure(data=go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill='toself'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(metrics.values())]
                )),
            showlegend=False,
            title='Nutrition Overview'
        )
        
        plot_path = os.path.join(self.plots_dir, f'nutrition_radar_{self.user_id}.html')
        fig.write_html(plot_path)
        
        return plot_path

    def create_mental_health_timeline(self) -> str:
        """Generate mental health timeline visualization."""
        mental_health_data = self._load_data("mental_health")
        if mental_health_data.empty:
            return "No mental health data available"
            
        # Create line plot for mood, stress, and anxiety levels
        plt.figure(figsize=(12, 6))
        
        metrics = ['mood', 'stress', 'anxiety']
        colors = ['green', 'red', 'blue']
        
        for metric, color in zip(metrics, colors):
            plt.plot(
                mental_health_data['date'],
                mental_health_data[metric],
                marker='o',
                linestyle='-',
                color=color,
                label=metric.capitalize()
            )
        
        plt.title('Mental Health Metrics Over Time')
        plt.xlabel('Date')
        plt.ylabel('Level (1-10)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plot_path = os.path.join(self.plots_dir, f'mental_health_timeline_{self.user_id}.png')
        plt.savefig(plot_path)
        plt.close()
        
        return plot_path

    def generate_progress_dashboard(self) -> Dict[str, str]:
        """Generate a comprehensive progress dashboard with all visualizations."""
        plots = {
            'sleep': self.plot_sleep_trends(),
            'exercise': self.create_exercise_heatmap(),
            'nutrition': self.plot_nutrition_radar(),
            'mental_health': self.create_mental_health_timeline()
        }
        
        # Create an HTML dashboard
        dashboard_html = """
        <html>
        <head>
            <title>Health Progress Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                .section { margin-bottom: 30px; }
                h1, h2 { color: #333; }
                .plot-container { margin: 20px 0; }
                img { max-width: 100%; border: 1px solid #ddd; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Health Progress Dashboard - {user_id}</h1>
        """.format(user_id=self.user_id)
        
        sections = {
            'sleep': 'Sleep Patterns',
            'exercise': 'Exercise Activity',
            'nutrition': 'Nutrition Overview',
            'mental_health': 'Mental Health Tracking'
        }
        
        for key, title in sections.items():
            if plots[key] != f"No {key} data available":
                dashboard_html += f"""
                <div class="section">
                    <h2>{title}</h2>
                    <div class="plot-container">
                """
                if key == 'nutrition':
                    dashboard_html += f'<iframe src="{plots[key]}" width="100%" height="600px" frameborder="0"></iframe>'
                else:
                    dashboard_html += f'<img src="{plots[key]}" alt="{title}">'
                dashboard_html += """
                    </div>
                </div>
                """
        
        dashboard_html += """
            </div>
        </body>
        </html>
        """
        
        dashboard_path = os.path.join(self.plots_dir, f'dashboard_{self.user_id}.html')
        with open(dashboard_path, 'w') as f:
            f.write(dashboard_html)
            
        return {
            'dashboard': dashboard_path,
            'plots': plots
        }
