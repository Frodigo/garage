import streamlit as st
import re
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import GridSearchCV

st.set_page_config(
    page_title="Text Classification ML Experiment",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


@st.cache_data
def download_and_prepare_data():
    """Download and prepare 20 newsgroups data"""

    categories = [
        'alt.atheism',
        'comp.graphics',
        'comp.os.ms-windows.misc',
        'comp.sys.ibm.pc.hardware',
        'rec.autos',
        'rec.motorcycles',
        'sci.space',
        'talk.politics.misc'
    ]

    newsgroups_train = fetch_20newsgroups(
        subset='train',
        categories=categories,
        shuffle=True,
        random_state=42,
        remove=('headers', 'footers', 'quotes')
    )

    newsgroups_test = fetch_20newsgroups(
        subset='test',
        categories=categories,
        shuffle=True,
        random_state=42,
        remove=('headers', 'footers', 'quotes')
    )

    # Preprocessing
    X_train_raw = [preprocess_text(text) for text in newsgroups_train.data]
    X_test_raw = [preprocess_text(text) for text in newsgroups_test.data]
    y_train = newsgroups_train.target
    y_test = newsgroups_test.target

    return X_train_raw, X_test_raw, y_train, y_test, newsgroups_test.target_names


@st.cache_resource
def train_and_cache_model():
    """Train model and cache it (runs only once)"""

    X_train_raw, X_test_raw, y_train, y_test, categories = download_and_prepare_data()

    vectorizer = TfidfVectorizer(
        max_features=10000,
        min_df=2,
        max_df=0.95,
        stop_words='english',
        ngram_range=(1, 2)
    )

    X_train_tfidf = vectorizer.fit_transform(X_train_raw)
    X_test_tfidf = vectorizer.transform(X_test_raw)

    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='linear', random_state=42, probability=True)
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = {
            'accuracy': accuracy,
            'predictions': y_pred,
            'model': model
        }

    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    best_model = results[best_model_name]['model']
    final_accuracy = results[best_model_name]['accuracy']

    final_predictions = results[best_model_name]['predictions']
    classification_rep = classification_report(
        y_test, final_predictions,
        target_names=categories,
        output_dict=True
    )

    metadata = {
        'model_name': best_model_name,
        'final_accuracy': final_accuracy,
        'categories': categories,
        'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'training_samples': len(X_train_raw),
        'test_samples': len(X_test_raw),
        'vocabulary_size': len(vectorizer.get_feature_names_out()),
        'classification_report': classification_rep,
        'model_comparison': {name: data['accuracy'] for name, data in results.items()},
        'preprocessing_info': {
            'tfidf_params': {
                'max_features': vectorizer.max_features,
                'min_df': vectorizer.min_df,
                'max_df': vectorizer.max_df,
                'ngram_range': vectorizer.ngram_range
            }
        }
    }

    return best_model, vectorizer, metadata


def predict_text_tags(text, model, vectorizer, categories):
    """Predict tags for text"""
    try:
        processed_text = preprocess_text(text)

        text_vector = vectorizer.transform([processed_text])

        prediction = model.predict(text_vector)[0]
        probabilities = model.predict_proba(text_vector)[0]

        top_3_indices = probabilities.argsort()[-3:][::-1]

        return {
            'main_tag': categories[prediction],
            'main_tag_short': categories[prediction].split('.')[-1],
            'confidence': float(probabilities[prediction]),
            'top_3_tags': [
                {
                    'tag': categories[idx],
                    'tag_short': categories[idx].split('.')[-1],
                    'probability': float(probabilities[idx])
                }
                for idx in top_3_indices
            ]
        }
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

# =====================================================
# LOAD/TRAIN MODEL
# =====================================================


with st.spinner('Loading/Training model... This may take a few minutes on first run.'):
    try:
        model, vectorizer, metadata = train_and_cache_model()
        model_loaded = True
        st.success("Model ready!")
    except Exception as e:
        st.error(f"Model training failed: {e}")
        model_loaded = False
        model, vectorizer, metadata = None, None, None

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "Demo", "Analytics", "About"]
)

if model_loaded:
    st.sidebar.success("Model loaded successfully!")
    st.sidebar.info(f"**Model:** {metadata['model_name']}")
    st.sidebar.info(f"**Accuracy:** {metadata['final_accuracy']:.1%}")
    st.sidebar.info(f"**Categories:** {len(metadata['categories'])}")
else:
    st.sidebar.error("Model not loaded!")
    st.sidebar.warning("Training failed or in progress...")

# =====================================================
# MAIN HEADER
# =====================================================

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #1f77b4; font-size: 3rem;">Text Classification ML</h1>
    <p style="font-size: 1.2rem; color: #666;">Automatic text tagging using Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Add training info banner
if model_loaded:
    st.info(
        f"Model trained successfully! Algorithm: **{metadata['model_name']}** | Accuracy: **{metadata['final_accuracy']:.1%}**")
else:
    st.warning(
        "Model training in progress or failed. Please wait or refresh the page.")

# =====================================================
# PAGE: HOME
# =====================================================

if page == "Home":
    st.header("Welcome to Text Classification Demo")

    if model_loaded and metadata is not None:
        # Model statistics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Model Accuracy",
                value=f"{metadata['final_accuracy']:.1%}",
                delta=f"{metadata['model_name']}"
            )

        with col2:
            st.metric(
                label="Categories",
                value=len(metadata['categories']),
                delta="Multi-class"
            )

        with col3:
            st.metric(
                label="Vocabulary",
                value=f"{metadata['vocabulary_size']:,}",
                delta="TF-IDF features"
            )

        with col4:
            st.metric(
                label="Training Texts",
                value=f"{metadata['training_samples']:,}",
                delta="20 Newsgroups"
            )

        # Available categories
        st.subheader("Available Categories")
        categories_display = [cat.split('.')[-1].title()
                              for cat in metadata['categories']]

        cols = st.columns(4)
        for i, category in enumerate(categories_display):
            with cols[i % 4]:
                st.info(f"**{category}**")

    else:
        st.error(
            "Model training failed or in progress. Please wait or refresh the page.")

# =====================================================
# PAGE: DEMO
# =====================================================

elif page == "Demo":
    st.header("Try the Text Classifier")

    if model_loaded and model is not None:
        # Example texts
        examples = {
            "Cars": "I just bought a new car with amazing acceleration and great fuel economy. The engine performance is outstanding.",
            "Computer Graphics": "The latest graphics card from NVIDIA has incredible performance for gaming and machine learning applications.",
            "Space": "NASA announced a new mission to Mars next year. The spacecraft will carry advanced scientific instruments.",
            "Politics": "The political situation is getting more complex every day with new policies being announced.",
            "Atheism": "Religious discussions often lead to debates about faith versus scientific evidence and rational thinking.",
            "Motorcycles": "Harley Davidson motorcycles are known for their distinctive sound and classic American design.",
            "Windows": "I'm having trouble with Windows 10 installation. The system keeps crashing during setup.",
            "PC Hardware": "The new CPU has 16 cores and runs at 3.8 GHz. Perfect for gaming and video editing."
        }

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Enter text to classify:")

            # Example selector
            selected_example = st.selectbox(
                "Or choose an example:",
                [""] + list(examples.keys())
            )

            if selected_example:
                default_text = examples[selected_example]
            else:
                default_text = ""

            user_text = st.text_area(
                "Text to classify:",
                value=default_text,
                height=150,
                placeholder="Enter your text here..."
            )

            if st.button("Classify Text", type="primary"):
                if user_text.strip():
                    with st.spinner('Analyzing text...'):
                        result = predict_text_tags(
                            user_text,
                            model,
                            vectorizer,
                            metadata['categories']
                        )

                    if result:
                        # Main prediction
                        st.success("Classification completed!")

                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric(
                                "Predicted Category",
                                result['main_tag_short'].title(),
                                f"Confidence: {result['confidence']:.1%}"
                            )

                        with col_b:
                            st.metric(
                                "Text Length",
                                f"{len(user_text.split())} words",
                                f"Processed: {len(preprocess_text(user_text).split())} words"
                            )

                        # Top 3 predictions
                        st.subheader("Top 3 Predictions:")

                        for i, tag_info in enumerate(result['top_3_tags']):
                            prob = tag_info['probability']
                            tag_name = tag_info['tag_short'].title()

                            rank = f"#{i+1}" if i < 3 else ""

                            # Progress bar
                            st.write(f"{rank} **{tag_name}** - {prob:.1%}")
                            st.progress(prob)

                        # Visualization
                        if len(result['top_3_tags']) > 1:
                            fig = px.bar(
                                x=[tag['tag_short'].title()
                                   for tag in result['top_3_tags']],
                                y=[tag['probability']
                                    for tag in result['top_3_tags']],
                                title="Prediction Probabilities",
                                labels={'x': 'Category', 'y': 'Probability'},
                                color=[tag['probability']
                                       for tag in result['top_3_tags']],
                                color_continuous_scale='viridis'
                            )
                            fig.update_layout(showlegend=False, height=400)
                            st.plotly_chart(fig, use_container_width=True)

                    else:
                        st.error("Error during prediction")
                else:
                    st.warning("Please enter some text to classify")

        with col2:
            st.subheader("Model Info")

            if metadata:
                st.info(f"""
                **Algorithm:** {metadata['model_name']}

                **Performance:**
                - Accuracy: {metadata['final_accuracy']:.1%}
                - Training samples: {metadata['training_samples']:,}
                - Vocabulary: {metadata['vocabulary_size']:,} words

                **Training Date:** {metadata['training_date'].split()[0]}
                """)

            st.subheader("Categories")
            for cat in metadata['categories']:
                st.write(f"• {cat.split('.')[-1].title()}")

    else:
        st.error("Model not available. Training failed or in progress.")

# =====================================================
# PAGE: ANALYTICS
# =====================================================

elif page == "Analytics":
    st.header("Model Analytics")

    if model_loaded and metadata is not None:
        # Model overview
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Algorithm", metadata['model_name'])
        with col2:
            st.metric("Accuracy", f"{metadata['final_accuracy']:.3f}")
        with col3:
            st.metric("Training Date", metadata['training_date'].split()[0])

        # Classification report
        if 'classification_report' in metadata:
            st.subheader("Classification Report")

            # Prepare data for visualization
            categories = metadata['categories']
            metrics_data = []

            for cat in categories:
                if cat in metadata['classification_report']:
                    cat_report = metadata['classification_report'][cat]
                    metrics_data.append({
                        'Category': cat.split('.')[-1].title(),
                        'Precision': cat_report['precision'],
                        'Recall': cat_report['recall'],
                        'F1-Score': cat_report['f1-score'],
                        'Support': cat_report['support']
                    })

            if metrics_data:
                df_metrics = pd.DataFrame(metrics_data)

                # Display table
                st.dataframe(df_metrics.round(3), use_container_width=True)

                # Metrics visualization
                fig = px.bar(
                    df_metrics.melt(id_vars=['Category'],
                                    value_vars=['Precision', 'Recall', 'F1-Score']),
                    x='Category',
                    y='value',
                    color='variable',
                    title="Classification Metrics per Category",
                    barmode='group'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

        # Model comparison
        if 'model_comparison' in metadata:
            st.subheader("Model Comparison")

            comparison_data = metadata['model_comparison']
            models = list(comparison_data.keys())
            accuracies = list(comparison_data.values())

            fig = px.bar(
                x=models,
                y=accuracies,
                title="Model Accuracy Comparison",
                labels={'x': 'Models', 'y': 'Accuracy'},
                color=accuracies,
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Technical details
        st.subheader("Technical Details")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"""
            **Data Statistics:**
            - Training samples: {metadata['training_samples']:,}
            - Test samples: {metadata['test_samples']:,}
            - Categories: {len(metadata['categories'])}
            - Vocabulary size: {metadata['vocabulary_size']:,}
            """)

        with col2:
            if 'preprocessing_info' in metadata:
                tfidf_params = metadata['preprocessing_info']['tfidf_params']
                st.info(f"""
                **TF-IDF Parameters:**
                - Max features: {tfidf_params['max_features']:,}
                - Min document frequency: {tfidf_params['min_df']}
                - Max document frequency: {tfidf_params['max_df']}
                - N-gram range: {tfidf_params['ngram_range']}
                """)

    else:
        st.error("Analytics not available. Model training failed or in progress.")

# =====================================================
# PAGE: ABOUT
# =====================================================

elif page == "About":
    st.header("About This Project")

    st.markdown("""
    ## Project Goal

    This project demonstrates a **complete machine learning pipeline** for automatic text classification.
    The system can automatically assign category tags to text documents using advanced ML techniques.

    ## Technology Stack

    **Machine Learning:**
    - **Scikit-learn** - ML algorithms and tools
    - **TF-IDF Vectorization** - Text feature extraction
    - **Logistic Regression** - Classification algorithm

    **Data Processing:**
    - **Pandas & NumPy** - Data manipulation
    - **Regular Expressions** - Text preprocessing

    **Web Interface:**
    - **Streamlit** - Interactive web application
    - **Plotly** - Interactive visualizations

    ## Dataset

    **20 Newsgroups Dataset:**
    - Classic text classification benchmark
    - 8 selected categories from original 20
    - Real-world text data from online forums
    - Automatically downloaded and processed

    ## ML Pipeline

    1. **Data Download** - Automatic 20 Newsgroups fetching
    2. **Text Preprocessing** - Cleaning and normalization
    3. **Feature Extraction** - TF-IDF vectorization with n-grams
    4. **Model Training** - Multiple algorithm comparison
    5. **Model Selection** - Best performer selection
    6. **Caching** - Model stored in Streamlit cache
    7. **Inference** - Real-time text classification

    ## Results
    """)

    if model_loaded and metadata:
        st.success(f"""
        **Current Model Performance:**
        - **Algorithm:** {metadata['model_name']}
        - **Test Accuracy:** {metadata['final_accuracy']:.1%}
        - **Training Completed:** {metadata['training_date']}
        - **Categories:** {len(metadata['categories'])} classes
        - **Vocabulary:** {metadata['vocabulary_size']:,} features
        """)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: #666; padding: 1rem;">
        Machine Learning Project | Text Classification System<br>
        Made using Python, Scikit-learn & Streamlit Cloud<br>
        {f"Model: {metadata['model_name']} | Accuracy: {metadata['final_accuracy']:.1%}" if model_loaded else "Model training in progress..."}
    </div>
    """,
    unsafe_allow_html=True
)
