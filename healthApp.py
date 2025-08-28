# Provide developer contact details via environment variables when available
import os
from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
# configure secret key from env or generate a random hex fallback
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(24).hex())
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///healthApp    .db"
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

# def __repr__(self):
#     return f"User('{self.username}', '{self.email}')"


symptom_disease_dict = {
    # Flu & Colds
    "fever": ["Flu", "Malaria", "Dengue", "COVID-19"],
    "cough": ["Common Cold", "Flu", "COVID-19", "Bronchitis"],
    "sore throat": ["Strep Throat", "Flu", "Common Cold"],
    "runny nose": ["Common Cold", "Allergy", "Flu"],
    "body ache": ["Flu", "Dengue"],
    "chills": ["Flu", "Malaria"],
    # Digestive issues
    "nausea": ["Food Poisoning", "Gastroenteritis", "Pregnancy"],
    "vomiting": ["Food Poisoning", "Gastroenteritis", "Migraine"],
    "diarrhea": ["Gastroenteritis", "Food Poisoning"],
    "stomach pain": ["Gastritis", "Appendicitis", "Food Poisoning"],
    # Head & Neurological
    "headache": ["Migraine", "Flu", "COVID-19", "Dehydration"],
    "dizziness": ["Anemia", "Dehydration", "Vertigo"],
    "fatigue": ["Anemia", "Diabetes", "Flu"],
    "confusion": ["Meningitis", "Stroke", "Hypoglycemia"],
    # Skin & Allergy
    "rash": ["Allergy", "Measles", "Chickenpox"],
    "itching": ["Allergy", "Eczema"],
    "redness": ["Allergy", "Conjunctivitis"],
    # Respiratory
    "shortness of breath": ["Asthma", "Pneumonia", "COVID-19"],
    "wheezing": ["Asthma", "Bronchitis"],
    # Cardiovascular
    "chest pain": ["Heart Attack", "Angina", "Panic Attack"],
    "palpitations": ["Arrhythmia", "Anxiety", "Hyperthyroidism"],
    # Eye & Ear
    "red eyes": ["Conjunctivitis", "Allergy"],
    "ear pain": ["Ear Infection", "TMJ Disorder"],
    # Musculoskeletal
    "joint pain": ["Arthritis", "Gout", "Lupus"],
    "swelling": ["Arthritis", "Kidney Disease", "Injury"],
    # Endocrine/Metabolic
    "weight loss": ["Diabetes", "Hyperthyroidism", "Cancer"],
    "frequent urination": ["Diabetes", "Urinary Tract Infection"],
}


@app.route("/", methods=["GET", "POST"])
def home():
    diseases = None
    if request.method == "POST":
        # Get user input, split by commas, and normalize
        symptoms_input = request.form.get("symptoms", "")
        symptoms_list = [s.strip().lower() for s in symptoms_input.split(",")]

        # Collect all possible diseases
        diseases = []
        for symptom in symptoms_list:
            matched = symptom_disease_dict.get(symptom)
            if matched:
                for disease in matched:
                    if disease not in diseases:
                        diseases.append(disease)
    return render_template("home.html", diseases=diseases)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/health")
def health():
    # Simple health endpoint for load balancers / PaaS probes
    return "ok", 200


@app.context_processor
def inject_dev_info():
    """Inject developer contact placeholders into all templates.

    Set environment variables to show links (DEV_EMAIL, DEV_PHONE,
    DEV_LINKEDIN, DEV_GITHUB, DEV_INSTAGRAM). DEV_NAME defaults to your name.
    """
    return dict(
        dev_name=os.environ.get("DEV_NAME", "Takondwa Zulu"),
        dev_email=os.environ.get("DEV_EMAIL", "tkzulu44@gmail.com"),
        dev_phone=os.environ.get("DEV_PHONE", "+260764382988"),
        dev_linkedin=os.environ.get(
            "DEV_LINKEDIN",
            "www.linkedin.com/in/takondwa-zulu-aa3841379",
        ),
        dev_github=os.environ.get(
            "DEV_GITHUB",
            "https://github.com/Twixie101",
        ),
        dev_instagram=os.environ.get(
            "DEV_INSTAGRAM",
            " https://www.instagram.com/kha._.mari",
        ),
    )


if __name__ == "__main__":
    # Useful for local dev; Render will use Gunicorn (below)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
