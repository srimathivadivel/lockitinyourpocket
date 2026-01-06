from voice_recorder import VoiceRecorder
from speech_analysis import SpeechAnalyzer
from report_generator import ReportGenerator
from holistic_health import HolisticHealthManager, SleepMetrics, ExerciseActivity, NutritionLog
from health_visualizer import HealthVisualizer
from datetime import datetime, time
import os
import webbrowser

class ParkinsonsManagementApp:
    def __init__(self, user_id="test_user"):
        self.recorder = VoiceRecorder()
        self.analyzer = SpeechAnalyzer()
        self.report_generator = ReportGenerator()
        self.health_manager = HolisticHealthManager(user_id)
        self.visualizer = HealthVisualizer(user_id)
        self.user_id = user_id
        
    def record_session(self, duration=10):
        """Record a voice session."""
        print(f"Starting {duration} second recording session...")
        self.recorder.record_voice(duration)
        return self.recorder.save_recording()
        
    def analyze_recording(self, recording_path):
        """Analyze a recorded session."""
        print("Analyzing speech patterns...")
        features = self.analyzer.extract_features(recording_path)
        analysis = self.analyzer.analyze_parkinsons_indicators()
        return analysis
        
    def generate_report(self, analysis_results):
        """Generate a report from analysis results."""
        print("Generating report...")
        report_path = self.report_generator.generate_report(analysis_results, self.user_id)
        print(f"Report generated: {report_path}")
        return report_path
        
    def track_sleep(self, hours: float, quality: int, bed_time: str, wake_time: str, 
                   disturbances: list):
        """Track sleep metrics and get recommendations."""
        print("\nProcessing sleep data...")
        metrics = SleepMetrics(
            sleep_duration=hours,
            sleep_quality=quality,
            time_to_bed=datetime.strptime(bed_time, "%H:%M").time(),
            time_woke_up=datetime.strptime(wake_time, "%H:%M").time(),
            disturbances=disturbances
        )
        recommendations = self.health_manager.log_sleep(metrics)
        return recommendations
        
    def get_exercise_plan(self, mobility_level: str, energy_level: int):
        """Get personalized exercise recommendations."""
        print("\nGenerating exercise plan...")
        plan = self.health_manager.suggest_exercise_plan(mobility_level, energy_level)
        return plan
        
    def track_nutrition(self, meals: list, water_intake: float, supplements: list, 
                       diet_adherence: int):
        """Track nutrition and get recommendations."""
        print("\nProcessing nutrition data...")
        nutrition_log = NutritionLog(
            meals=meals,
            water_intake=water_intake,
            supplements=supplements,
            diet_adherence=diet_adherence
        )
        recommendations = self.health_manager.get_nutrition_recommendations(nutrition_log)
        return recommendations
        
    def get_mental_health_support(self, mood: int, stress: int, anxiety: int):
        """Get mental health support and recommendations."""
        print("\nGenerating mental health support recommendations...")
        support = self.health_manager.get_behavioral_health_support(mood, stress, anxiety)
        return support
        
    def generate_progress_visualizations(self):
        """Generate and display progress visualizations."""
        print("\nGenerating progress visualizations...")
        dashboard_info = self.visualizer.generate_progress_dashboard()
        
        # Open dashboard in default web browser
        dashboard_path = dashboard_info['dashboard']
        if os.path.exists(dashboard_path):
            print(f"\nDashboard generated: {dashboard_path}")
            print("Opening dashboard in your default web browser...")
            webbrowser.open('file://' + os.path.abspath(dashboard_path))
        
        return dashboard_info

def main():
    app = ParkinsonsManagementApp()
    
    try:
        # 1. Speech Analysis
        recording_path = app.record_session(duration=10)
        analysis_results = app.analyze_recording(recording_path)
        report_path = app.generate_report(analysis_results)
        
        print("\nSpeech Analysis Summary:")
        print(f"Risk Score: {analysis_results['risk_score']:.2f}")
        print("\nRecommendations:")
        for rec in analysis_results['recommendations']:
            print(f"- {rec}")
            
        # 2. Sleep Tracking Example
        sleep_recommendations = app.track_sleep(
            hours=6.5,
            quality=7,
            bed_time="23:00",
            wake_time="05:30",
            disturbances=["Restless legs", "Night sweats"]
        )
        print("\nSleep Recommendations:")
        for rec in sleep_recommendations['recommendations']:
            print(f"\n{rec}")
            
        # 3. Exercise Plan
        exercise_plan = app.get_exercise_plan(mobility_level="moderate", energy_level=6)
        print("\nRecommended Exercise Plan:")
        for activity in exercise_plan:
            print(f"- {activity.activity_type}: {activity.duration} minutes "
                  f"({activity.intensity} intensity)")
            print(f"  Note: {activity.notes}")
            
        # 4. Nutrition Tracking
        nutrition_recommendations = app.track_nutrition(
            meals=[
                {"breakfast": "Oatmeal with berries"},
                {"lunch": "Grilled chicken salad"},
                {"dinner": "Fish with vegetables"}
            ],
            water_intake=1.5,
            supplements=["Vitamin D", "CoQ10"],
            diet_adherence=8
        )
        print("\nNutrition Recommendations:")
        for category, recs in nutrition_recommendations.items():
            print(f"\n{category.replace('_', ' ').title()}:")
            for rec in recs:
                print(f"- {rec}")
                
        # 5. Mental Health Support
        mental_health_support = app.get_mental_health_support(
            mood=6,
            stress=7,
            anxiety=5
        )
        print("\nMental Health Support:")
        print("\nCoping Strategies:")
        for category, strategies in mental_health_support['coping_strategies'].items():
            print(f"\n{category.title()}:")
            for strategy in strategies:
                print(f"- {strategy}")
                
        if mental_health_support['personalized_recommendations']:
            print("\nPersonalized Recommendations:")
            for rec in mental_health_support['personalized_recommendations']:
                print(f"- {rec}")
                
        # Generate and display progress visualizations
        dashboard_info = app.generate_progress_visualizations()
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    print('Parkinsons Management App is running...')
    main()
