from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime, timedelta
import os
from voice_recorder import VoiceRecorder
from speech_analysis import SpeechAnalyzer
from holistic_health import HolisticHealthManager, SleepMetrics, ExerciseActivity, NutritionLog
from health_visualizer import HealthVisualizer

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Temporary user storage (replace with database in production)
users = {}

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.recorder = VoiceRecorder()
        self.analyzer = SpeechAnalyzer()
        self.health_manager = HolisticHealthManager(user_id)
        self.visualizer = HealthVisualizer(user_id)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        users[user_id] = User(user_id)
    return users[user_id]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # For demo purposes, accept any username/password
        user_id = form.username.data
        user = load_user(user_id)
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard'))
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.username.data
        user = User(user_id)
        users[user_id] = user
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    sleep_quality = 75  # Example data
    exercise_progress = 60
    mood_level = 80
    
    upcoming_activities = [
        {"name": "Morning Exercise", "time": "9:00 AM"},
        {"name": "Speech Practice", "time": "11:00 AM"},
        {"name": "Relaxation Session", "time": "3:00 PM"}
    ]
    
    # Example progress data
    speech_data = {
        "dates": ["2025-01-25", "2025-01-26", "2025-01-27", "2025-01-28"],
        "scores": [85, 87, 82, 88]
    }
    
    sleep_data = {
        "dates": ["2025-01-25", "2025-01-26", "2025-01-27", "2025-01-28"],
        "quality": [70, 75, 80, 75]
    }
    
    recommendations = {
        "Exercise": [
            "Take a 20-minute walk",
            "Do gentle stretching exercises",
            "Practice balance exercises"
        ],
        "Speech": [
            "Practice vocal exercises",
            "Record and analyze speech",
            "Do breathing exercises"
        ],
        "Wellness": [
            "Take medications as prescribed",
            "Stay hydrated",
            "Practice stress-relief techniques"
        ]
    }
    
    return render_template('dashboard.html',
                         sleep_quality=sleep_quality,
                         exercise_progress=exercise_progress,
                         mood_level=mood_level,
                         upcoming_activities=upcoming_activities,
                         speech_data=speech_data,
                         sleep_data=sleep_data,
                         recommendations=recommendations)

@app.route('/speech')
@login_required
def speech():
    return render_template('speech.html')

@app.route('/speech/record', methods=['POST'])
@login_required
def record_speech():
    try:
        # Record audio
        recording_path = current_user.recorder.record_voice(10)
        # Save the recording
        audio_file = current_user.recorder.save_recording()
        
        # Extract features and analyze
        features = current_user.analyzer.extract_features(audio_file)
        if features is None:
            raise ValueError("Failed to extract features from audio")
            
        # Initialize model if needed
        if current_user.analyzer.ml_model.model is None:
            current_user.analyzer.ml_model.train_model()
            
        analysis = current_user.analyzer.analyze_parkinsons_indicators()
        
        return jsonify({
            'status': 'success',
            'recording_path': audio_file,
            'analysis': {
                'risk_score': analysis['risk_score'],
                'patterns': [
                    f"Tremor detected: {'Yes' if analysis['risk_factors']['high_tremor'] else 'No'}",
                    f"Speech irregularity: {'High' if analysis['risk_factors']['irregular_speech'] else 'Low'}",
                    f"Voice stability: {'Unstable' if analysis['risk_factors']['voice_instability'] else 'Stable'}"
                ],
                'recommendations': [
                    "Practice speech exercises regularly",
                    "Focus on breath control during speech",
                    "Consider speech therapy sessions"
                ] if analysis['risk_score'] > 0.5 else [
                    "Continue monitoring speech patterns",
                    "Maintain regular voice exercises",
                    "Record speech samples periodically"
                ]
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/sleep')
@login_required
def sleep():
    return render_template('sleep.html')

@app.route('/sleep/log', methods=['GET', 'POST'])
@login_required
def log_sleep():
    if request.method == 'POST':
        try:
            metrics = SleepMetrics(
                sleep_duration=float(request.form['duration']),
                sleep_quality=int(request.form['quality']),
                time_to_bed=datetime.strptime(request.form['bedtime'], '%H:%M').time(),
                time_woke_up=datetime.strptime(request.form['wake_time'], '%H:%M').time(),
                disturbances=request.form.getlist('disturbances')
            )
            recommendations = current_user.health_manager.log_sleep(metrics)
            flash('Sleep data logged successfully!', 'success')
            return jsonify({
                'status': 'success',
                'recommendations': recommendations
            })
        except Exception as e:
            flash(f'Error logging sleep data: {str(e)}', 'error')
            return jsonify({'status': 'error', 'message': str(e)})
    return render_template('sleep.html')

@app.route('/exercise')
@login_required
def exercise():
    return render_template('exercise.html')

@app.route('/exercise/start', methods=['POST'])
@login_required
def start_exercise():
    try:
        mobility_level = request.form['mobility_level']
        energy_level = int(request.form['energy_level'])
        plan = current_user.health_manager.suggest_exercise_plan(mobility_level, energy_level)
        return jsonify({
            'status': 'success',
            'plan': plan
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/nutrition')
@login_required
def nutrition():
    return render_template('nutrition.html')

@app.route('/nutrition/log', methods=['POST'])
@login_required
def log_nutrition():
    try:
        meal_type = request.form['meal_type']
        food_items = request.form.getlist('food_items[]')
        portions = request.form.getlist('portions[]')
        difficulties = request.form.getlist('difficulties[]')
        notes = request.form.get('notes', '')
        
        # Process the nutrition data
        foods = [{'item': item, 'portions': float(portion)} 
                for item, portion in zip(food_items, portions)]
        
        nutrition_log = NutritionLog(
            meal_type=meal_type,
            foods=foods,
            difficulties=difficulties,
            notes=notes
        )
        
        summary = current_user.health_manager.log_nutrition(nutrition_log)
        recommendations = current_user.health_manager.get_nutrition_recommendations()
        
        return jsonify({
            'status': 'success',
            'summary': summary,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/mental-health')
@login_required
def mental_health():
    return render_template('mental_health.html')

@app.route('/mental-health/check', methods=['POST'])
@login_required
def mental_health_check():
    try:
        mood = int(request.form['mood'])
        stress = int(request.form['stress'])
        anxiety = int(request.form['anxiety'])
        factors = request.form.getlist('factors[]')
        notes = request.form.get('notes', '')
        
        support = current_user.health_manager.get_behavioral_health_support(
            mood=mood,
            stress=stress,
            anxiety=anxiety,
            factors=factors,
            notes=notes
        )
        
        return jsonify({
            'status': 'success',
            'support': support
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# @app.route('/progress')
# @login_required
# def progress():
#     try:
#         # Get progress data for each category
#         speech_progress = current_user.analyzer.get_progress_data()
#         sleep_progress = current_user.health_manager.get_sleep_progress()
#         exercise_progress = current_user.health_manager.get_exercise_progress()
#         nutrition_progress = current_user.health_manager.get_nutrition_progress()
#         mental_health_progress = current_user.health_manager.get_mental_health_progress()
        
#         # Generate visualizations
#         visualizations = current_user.visualizer.generate_progress_dashboard(
#             speech_data=speech_progress,
#             sleep_data=sleep_progress,
#             exercise_data=exercise_progress,
#             nutrition_data=nutrition_progress,
#             mental_health_data=mental_health_progress
#         )
        
#         return render_template('progress.html', 
#                              visualizations=visualizations,
#                              speech_progress=speech_progress,
#                              sleep_progress=sleep_progress,
#                              exercise_progress=exercise_progress,
#                              nutrition_progress=nutrition_progress,
#                              mental_health_progress=mental_health_progress)
#     except Exception as e:
#         flash(f'Error generating progress dashboard: {str(e)}', 'error')
#         return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
