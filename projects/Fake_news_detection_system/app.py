# Interactive Fake News Detection Interface
# Optimized for Google Colab with Web UI

# ============================================================================
# INSTALLATION AND IMPORTS
# ============================================================================

# Install required packages
!pip install gradio wordcloud seaborn plotly

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Text processing
import re
import string
import nltk

# Download NLTK data with proper error handling
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except:
    print("NLTK packages not available, using basic preprocessing")
    NLTK_AVAILABLE = False

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import pickle
import gradio as gr

# Set style
plt.style.use('default')
print("All packages imported successfully!")

# ============================================================================
# DATA PREPARATION
# ============================================================================

def create_enhanced_dataset():
    """Create a more comprehensive fake news dataset"""
    
    fake_news_samples = [
        "BREAKING: Scientists discover that drinking water daily can be deadly according to secret government study!",
        "SHOCKING: Local man grows third arm after eating vegetables, doctors baffled by transformation!",
        "Government secretly controls weather using mind control satellites hidden in plain sight!",
        "URGENT: Celebrity X dies in horrific car crash, family confirms tragic news (completely fabricated story)!",
        "New groundbreaking study shows breathing air causes rapid aging - medical experts absolutely shocked!",
        "CONFIRMED: Aliens spotted landing in downtown area, mayor personally confirms alien invasion beginning!",
        "MIRACLE CURE: This one amazing fruit prevents ALL diseases, pharmaceutical companies hate this discovery!",
        "URGENT WARNING: All banks will close forever next Tuesday, withdraw your money immediately or lose everything!",
        "BREAKING NEWS: Internet to be permanently shut down next month by global conspiracy!",
        "Scientists finally prove the earth is actually cube-shaped, not round as previously believed!",
        "EXPOSED: Vaccines contain microchips that control your thoughts, leaked documents reveal shocking truth!",
        "ALERT: 5G towers cause instant death within 100 meters, government covers up massive casualties!",
        "DISCOVERED: Time travel machine built by teenager in garage, changes history forever!",
        "CONFIRMED: Moon landing was filmed in Hollywood studio, astronaut finally admits truth!",
        "SHOCKING: Pizza causes immediate weight loss of 50 pounds, nutritionists can't explain phenomenon!"
    ]
    
    real_news_samples = [
        "Stock market reaches new quarterly high amid positive economic recovery indicators and investor confidence.",
        "Local university receives significant federal grant for innovative climate change research program.",
        "City council unanimously approves comprehensive infrastructure development plan for downtown area renovation.",
        "National weather service forecasts moderate rainfall expected throughout the weekend across region.",
        "Major technology company announces opening of new regional headquarters in business district.",
        "Public health officials recommend annual flu vaccinations as part of preventive healthcare measures.",
        "Transportation authority announces schedule modifications for public transit during upcoming holiday period.",
        "New educational literacy program launches to provide additional support for elementary school students.",
        "Environmental protection agency releases quarterly report showing improvements in local air quality.",
        "Regional hospital expands cardiac care services and announces new specialized treatment programs.",
        "Scientists publish peer-reviewed research on renewable energy efficiency in leading academic journal.",
        "Local government implements new recycling initiative to reduce environmental waste in community.",
        "University researchers collaborate with international team on advanced medical treatment development.",
        "Economic analysts report steady growth in employment rates across multiple industry sectors.",
        "Public library system introduces digital literacy programs for senior citizens and community members."
    ]
    
    # Create balanced dataset
    data = []
    for text in fake_news_samples:
        data.append({'text': text, 'label': 1, 'category': 'Fake News'})
    for text in real_news_samples:
        data.append({'text': text, 'label': 0, 'category': 'Real News'})
    
    df = pd.DataFrame(data)
    return df

# ============================================================================
# TEXT PREPROCESSING
# ============================================================================

def preprocess_text_basic(text):
    """Basic text preprocessing without NLTK dependencies"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove user mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Basic stopwords removal (common English stopwords)
    basic_stopwords = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
        'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
        'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
        'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
        'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
        'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'further', 'then', 'once'
    }
    
    words = text.split()
    text = ' '.join([word for word in words if word not in basic_stopwords and len(word) > 2])
    
    return text

def preprocess_text_nltk(text):
    """Advanced text preprocessing with NLTK"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove user mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove stopwords using NLTK
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    text = ' '.join([word for word in word_tokens if word not in stop_words and len(word) > 2])
    
    return text

# Choose preprocessing function based on NLTK availability
preprocess_text = preprocess_text_nltk if NLTK_AVAILABLE else preprocess_text_basic

# ============================================================================
# MACHINE LEARNING MODEL
# ============================================================================

class FakeNewsDetector:
    """Streamlined fake news detection system"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def train_model(self, df):
        """Train the fake news detection model"""
        print("Training fake news detection model...")
        
        # Preprocess text
        df['cleaned_text'] = df['text'].apply(preprocess_text)
        
        # Prepare data
        X = df['cleaned_text']
        y = df['label']
        
        # Create and train pipeline
        self.model = Pipeline([
            ('vectorizer', TfidfVectorizer(
                max_features=5000, 
                ngram_range=(1, 2), 
                stop_words='english'
            )),
            ('classifier', LogisticRegression(random_state=42, max_iter=1000))
        ])
        
        # Train model
        self.model.fit(X, y)
        self.is_trained = True
        
        # Calculate accuracy on training data (for demo purposes)
        train_accuracy = self.model.score(X, y)
        print(f"Model trained successfully! Training accuracy: {train_accuracy:.3f}")
        
        return train_accuracy
    
    def predict(self, text):
        """Predict if text is fake news or real news"""
        if not self.is_trained:
            return "Error: Model not trained yet!"
        
        # Preprocess text
        cleaned_text = preprocess_text(text)
        
        # Make prediction
        prediction = self.model.predict([cleaned_text])[0]
        probabilities = self.model.predict_proba([cleaned_text])[0]
        
        # Format results
        label = "🚨 FAKE NEWS" if prediction == 1 else "✅ REAL NEWS"
        confidence = max(probabilities) * 100
        fake_prob = probabilities[1] * 100
        real_prob = probabilities[0] * 100
        
        return {
            'label': label,
            'confidence': confidence,
            'fake_probability': fake_prob,
            'real_probability': real_prob
        }

# Initialize and train the model
print("Initializing fake news detection system...")
detector = FakeNewsDetector()
df = create_enhanced_dataset()
training_accuracy = detector.train_model(df)

# ============================================================================
# GRADIO INTERFACE
# ============================================================================

def predict_fake_news(text):
    """Main prediction function for Gradio interface"""
    if not text.strip():
        return "Please enter some text to analyze.", 0, 0, 0
    
    if len(text.strip()) < 10:
        return "Please enter a longer text (at least 10 characters) for better analysis.", 0, 0, 0
    
    # Get prediction
    result = detector.predict(text)
    
    # Format output
    prediction_text = f"""
    ## Prediction: {result['label']}
    
    **Overall Confidence:** {result['confidence']:.1f}%
    
    ### Detailed Probabilities:
    - **Fake News Probability:** {result['fake_probability']:.1f}%
    - **Real News Probability:** {result['real_probability']:.1f}%
    
    ### Analysis Notes:
    - Higher fake probability suggests sensational language, extraordinary claims, or suspicious patterns
    - Higher real probability suggests factual reporting style and credible content structure
    - Confidence indicates how certain the model is about its prediction
    """
    
    return (
        prediction_text,
        result['confidence'],
        result['fake_probability'],
        result['real_probability']
    )

# Create example texts for testing
example_texts = [
    "Scientists at Stanford University published a peer-reviewed study on climate change impacts in the Journal of Environmental Science.",
    "SHOCKING: This one weird trick will make you lose 50 pounds overnight! Doctors hate this secret method!",
    "The stock market closed higher today following positive economic indicators and strong quarterly earnings reports.",
    "BREAKING: Government secretly controlling your mind through 5G towers, leaked documents reveal conspiracy!",
    "Local university receives federal grant to expand research programs in renewable energy technology."
]

# Create Gradio interface
def create_interface():
    """Create the main Gradio interface"""
    
    with gr.Blocks(
        title="Fake News Detection System",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1000px !important;
        }
        .prediction-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🔍 Fake News Detection System
        
        This AI-powered system analyzes text content to determine whether it's likely to be fake news or legitimate news.
        The model was trained on various news articles and can identify patterns commonly associated with misinformation.
        
        **How to use:**
        1. Enter or paste news text in the box below
        2. Click "Analyze Text" to get the prediction
        3. Review the confidence scores and probabilities
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                text_input = gr.Textbox(
                    label="📝 Enter News Text to Analyze",
                    placeholder="Paste your news article or headline here...",
                    lines=8,
                    max_lines=15
                )
                
                analyze_btn = gr.Button(
                    "🔍 Analyze Text", 
                    variant="primary",
                    size="lg"
                )
                
                gr.Markdown("### 📋 Example Texts to Try:")
                example_buttons = []
                for i, example in enumerate(example_texts):
                    btn = gr.Button(f"Example {i+1}: {example[:50]}...", size="sm")
                    btn.click(lambda x=example: x, outputs=text_input)
            
            with gr.Column(scale=2):
                prediction_output = gr.Markdown(
                    label="🎯 Prediction Results",
                    value="Enter text and click 'Analyze Text' to see results."
                )
                
                confidence_gauge = gr.Number(
                    label="📊 Overall Confidence (%)",
                    value=0,
                    interactive=False
                )
                
                with gr.Row():
                    fake_prob = gr.Number(
                        label="🚨 Fake News Probability (%)",
                        value=0,
                        interactive=False
                    )
                    real_prob = gr.Number(
                        label="✅ Real News Probability (%)",
                        value=0,
                        interactive=False
                    )
        
        # Connect the analyze button
        analyze_btn.click(
            predict_fake_news,
            inputs=text_input,
            outputs=[prediction_output, confidence_gauge, fake_prob, real_prob]
        )
        
        gr.Markdown("""
        ---
        ### ⚠️ Important Notes:
        - This is a demonstration model trained on limited data
        - Results should be used as guidance, not absolute truth
        - Always verify information from multiple reliable sources
        - The model may have biases based on its training data
        
        ### 🔧 Technical Details:
        - **Algorithm:** Logistic Regression with TF-IDF features
        - **Training Accuracy:** {:.1f}%
        - **Features:** Text preprocessing, N-gram analysis, Statistical modeling
        """.format(training_accuracy * 100))
    
    return interface

# Launch the interface
print("Creating interactive interface...")
interface = create_interface()

# Launch with public sharing enabled for Colab
print("Launching Fake News Detection Interface...")
interface.launch(
    share=True,  # Creates public link for Colab
    server_name="0.0.0.0",
    server_port=7860,
    show_error=True
)

# ============================================================================
# COMMAND LINE TESTING (Optional)
# ============================================================================

def test_command_line():
    """Test the model via command line interface"""
    print("\n" + "="*70)
    print("COMMAND LINE TESTING MODE")
    print("="*70)
    
    test_cases = [
        "Breaking news: Local mayor announces new community center opening next month.",
        "SHOCKING: This miracle pill will make you immortal! Buy now before it's banned!",
        "Weather forecast shows sunny skies expected throughout the weekend.",
        "URGENT: Aliens have landed and are demanding our pizza recipes!"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Text: {test_text}")
        result = detector.predict(test_text)
        print(f"Prediction: {result['label']}")
        print(f"Confidence: {result['confidence']:.1f}%")
        print("-" * 50)

# Uncomment to run command line tests
# test_command_line()

print("\n🚀 Fake News Detection System is ready!")
print("📱 Use the web interface above to analyze news text")
print("🔗 The interface should be accessible via the public link generated")
