from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Dict, Optional
import json
import os

@dataclass
class SleepMetrics:
    sleep_duration: float  # in hours
    sleep_quality: int     # 1-10 scale
    time_to_bed: time
    time_woke_up: time
    disturbances: List[str]
    
@dataclass
class ExerciseActivity:
    activity_type: str
    duration: int      # in minutes
    intensity: str    # 'low', 'moderate', 'high'
    completed: bool
    notes: str

@dataclass
class NutritionLog:
    meals: List[Dict]
    water_intake: float  # in liters
    supplements: List[str]
    diet_adherence: int  # 1-10 scale

class HolisticHealthManager:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.data_dir = "health_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def _get_user_file(self, category: str) -> str:
        return os.path.join(self.data_dir, f"{self.user_id}_{category}.json")
        
    def log_sleep(self, metrics: SleepMetrics) -> Dict:
        """Log sleep metrics and get personalized recommendations."""
        recommendations = []
        
        # Analyze sleep duration
        if metrics.sleep_duration < 6:
            recommendations.append(
                "Your sleep duration is below recommended levels. Consider: \n"
                "- Establishing a consistent sleep schedule\n"
                "- Creating a relaxing bedtime routine\n"
                "- Avoiding screens 1 hour before bed"
            )
        
        # Analyze sleep quality
        if metrics.sleep_quality < 7:
            recommendations.append(
                "To improve sleep quality, try: \n"
                "- Creating a dark, quiet, and cool sleeping environment\n"
                "- Practicing relaxation techniques before bed\n"
                "- Limiting caffeine and alcohol intake"
            )
        
        # Analyze sleep disturbances
        if metrics.disturbances:
            recommendations.append(
                "To address sleep disturbances: \n"
                "- Consider using a white noise machine\n"
                "- Practice gentle stretching before bed\n"
                "- Discuss medication timing with your healthcare provider"
            )
        
        # Save sleep data
        data = {
            "date": datetime.now().isoformat(),
            "metrics": {
                "duration": metrics.sleep_duration,
                "quality": metrics.sleep_quality,
                "bed_time": metrics.time_to_bed.isoformat(),
                "wake_time": metrics.time_woke_up.isoformat(),
                "disturbances": metrics.disturbances
            }
        }
        
        with open(self._get_user_file("sleep"), 'a') as f:
            f.write(json.dumps(data) + '\n')
            
        return {"recommendations": recommendations}
    
    def suggest_exercise_plan(self, mobility_level: str, energy_level: int) -> List[ExerciseActivity]:
        """Generate personalized exercise recommendations."""
        exercise_plans = {
            "high": [
                ExerciseActivity("Walking", 30, "moderate", False, "Focus on maintaining good posture"),
                ExerciseActivity("Tai Chi", 20, "low", False, "Helps with balance and flexibility"),
                ExerciseActivity("Resistance Training", 20, "moderate", False, "Use light weights or resistance bands")
            ],
            "moderate": [
                ExerciseActivity("Gentle Walking", 20, "low", False, "Take breaks as needed"),
                ExerciseActivity("Chair Yoga", 15, "low", False, "Focus on breathing and stretching"),
                ExerciseActivity("Balance Exercises", 10, "low", False, "Hold onto a chair for support")
            ],
            "limited": [
                ExerciseActivity("Seated Exercises", 15, "low", False, "Focus on range of motion"),
                ExerciseActivity("Breathing Exercises", 10, "low", False, "Practice deep breathing"),
                ExerciseActivity("Gentle Stretching", 10, "low", False, "Stay within comfortable range")
            ]
        }
        
        # Adjust plan based on energy level (1-10)
        if energy_level < 5:
            mobility_level = "limited" if mobility_level != "limited" else mobility_level
            
        return exercise_plans.get(mobility_level, exercise_plans["moderate"])
    
    def get_nutrition_recommendations(self, current_diet: NutritionLog) -> Dict:
        """Provide personalized nutrition recommendations."""
        recommendations = {
            "general": [
                "Maintain a balanced diet rich in whole grains, lean proteins, and vegetables",
                "Stay hydrated with at least 2 liters of water daily",
                "Consider incorporating anti-inflammatory foods"
            ],
            "supplements": [
                "Discuss vitamin D supplementation with your healthcare provider",
                "Consider CoQ10 supplementation under medical supervision",
                "Ensure adequate calcium intake"
            ],
            "specific_improvements": []
        }
        
        # Analyze water intake
        if current_diet.water_intake < 2.0:
            recommendations["specific_improvements"].append(
                "Increase water intake to at least 2 liters daily"
            )
            
        # Analyze diet adherence
        if current_diet.diet_adherence < 7:
            recommendations["specific_improvements"].extend([
                "Try meal planning to improve diet adherence",
                "Keep healthy snacks readily available",
                "Consider working with a nutritionist"
            ])
            
        return recommendations
    
    def get_behavioral_health_support(self, mood: int, stress_level: int, 
                                    anxiety_level: int) -> Dict[str, List[str]]:
        """Provide CBT-based coping strategies and recommendations."""
        strategies = {
            "relaxation": [
                "Practice progressive muscle relaxation",
                "Try guided meditation or mindfulness exercises",
                "Use deep breathing techniques"
            ],
            "cognitive": [
                "Challenge negative thoughts with evidence",
                "Practice gratitude journaling",
                "Set realistic daily goals"
            ],
            "behavioral": [
                "Engage in enjoyable activities",
                "Maintain social connections",
                "Establish daily routines"
            ]
        }
        
        # Customize recommendations based on reported levels
        recommendations = []
        
        if mood < 5:  # Scale 1-10
            recommendations.extend([
                "Consider scheduling an appointment with a mental health professional",
                "Engage in mood-lifting activities",
                "Maintain social connections with family and friends"
            ])
            
        if stress_level > 7:  # Scale 1-10
            recommendations.extend([
                "Practice stress-reduction techniques regularly",
                "Take regular breaks during the day",
                "Consider stress-management counseling"
            ])
            
        if anxiety_level > 7:  # Scale 1-10
            recommendations.extend([
                "Use grounding techniques when feeling anxious",
                "Practice regular relaxation exercises",
                "Consider discussing anxiety management with your healthcare provider"
            ])
            
        return {
            "coping_strategies": strategies,
            "personalized_recommendations": recommendations
        }
    def get_exercise_progress(self) -> Dict:
        """Get exercise tracking progress data."""
        try:
            exercise_file = self._get_user_file("exercise")
            if not os.path.exists(exercise_file):
                return {
                    "dates": [],
                    "duration": [],
                    "intensity": []
                }

            exercise_data = {
                "dates": [],
                "duration": [],
                "intensity": []
            }

            with open(exercise_file, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    exercise_data["dates"].append(entry["date"])
                    exercise_data["duration"].append(entry["duration"])
                    exercise_data["intensity"].append(entry["intensity"])

            return exercise_data
        except Exception as e:
            print(f"Error reading exercise progress: {str(e)}")
            return {
                "dates": [],
                "duration": [],
                "intensity": []
            }

    def get_mental_health_progress(self) -> Dict:
        """Get mental health tracking progress data."""
        try:
            mental_health_file = self._get_user_file("mental_health")
            if not os.path.exists(mental_health_file):
                return {
                    "dates": [],
                    "mood": [],
                    "stress": [],
                    "anxiety": []
                }

            mental_health_data = {
                "dates": [],
                "mood": [],
                "stress": [],
                "anxiety": []
            }

            with open(mental_health_file, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    mental_health_data["dates"].append(entry["date"])
                    mental_health_data["mood"].append(entry["mood"])
                    mental_health_data["stress"].append(entry["stress"])
                    mental_health_data["anxiety"].append(entry["anxiety"])

            return mental_health_data
        except Exception as e:
            print(f"Error reading mental health progress: {str(e)}")
            return {
                "dates": [],
                "mood": [],
                "stress": [],
                "anxiety": []
            }

    def get_nutrition_progress(self) -> Dict:
        """Get nutrition tracking progress data."""
        try:
            nutrition_file = self._get_user_file("nutrition")
            if not os.path.exists(nutrition_file):
                return {
                    "dates": [],
                    "water_intake": [],
                    "diet_adherence": []
                }

            nutrition_data = {
                "dates": [],
                "water_intake": [],
                "diet_adherence": []
            }

            with open(nutrition_file, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    nutrition_data["dates"].append(entry["date"])
                    nutrition_data["water_intake"].append(entry["water_intake"])
                    nutrition_data["diet_adherence"].append(entry["diet_adherence"])

            return nutrition_data
        except Exception as e:
            print(f"Error reading nutrition progress: {str(e)}")
            return {
                "dates": [],
                "water_intake": [],
                "diet_adherence": []
    
    
        }
