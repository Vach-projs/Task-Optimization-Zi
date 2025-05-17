This project is an AI-powered employee wellbeing and productivity monitoring system built using Django, integrating machine learning models for multimodal sentiment detection and task management. The system identifies employees' emotional states from audio, video, and text, tracks performance trends, and dynamically suggests alternate tasks during periods of emotional distress. It also notifies HR in real-time when an employee shows signs of stress, ensuring mental health support and workflow optimization.

Project Objectives
-To detect employee emotions using ML models trained on facial expressions (FER2013), audio tones, video features, and HDF5 prediction files.
-To classify and label emotional states (e.g., happy, sad, stressed, neutral).
-To identify stress-prone states and suggest alternate work tasks accordingly.
-To log and graph employee performance trends based on emotional tracking.
-To automatically alert HR when recurring stress signals are detected.
-To maintain two user portals: one for employees and one for HR representatives.

Datasets used:
-FER2013 for facial expressions
-RAVDESS for audio 
-Glassdoor company reviews for the textual sentiment analysis

The emotions mapped are happy, neutral, sad and stressed. As mentioned before the stress-related states are internally flagged and recorded for historical data for a given employee. When an employee is flagged as “stressed,” the system fetches less cognitively demanding alternate tasks. Tasks are suggested based on department, skill set, and previously completed work. A database-level trigger or Django signal is used to notify HR in real-time. Only HR has access to historical emotional logs of employees. The database used is the Django's in-built dbsqlite3 database management system.

 Tech Stack
-Backend: Django (Python)
-Frontend: Django Templates (HTML, CSS, Bootstrap)
-ML Models: TensorFlow/Keras models integrated via .h5 files
-Database: SQLite (default), can be upgraded to PostgreSQL
-Visualization: Matplotlib / Plotly for performance graphs

Employee emotional logs are only visible to HR. No raw audio/video/image data is stored—only emotion labels and timestamps. 
