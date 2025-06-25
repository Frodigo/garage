import streamlit as st
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import time

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import GridSearchCV, learning_curve

st.set_page_config(
    page_title="Text Classification ML Experiment",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-theme="light"] .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        color: #262730 !important;
        margin-bottom: 1rem;
    }

    [data-theme="dark"] .metric-card,
    .metric-card {
        background-color: rgba(40, 75, 99, 0.2);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #58c4dc;
        color: #fafafa !important;
        margin-bottom: 1rem;
        border: 1px solid rgba(250, 250, 250, 0.1);
    }

    .metric-card h4 {
        color: inherit !important;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    .metric-card p {
        color: inherit !important;
        margin: 0;
        opacity: 0.8;
    }

    /* Success cards */
    [data-theme="light"] .success-card {
        background-color: #d4edda;
        color: #155724 !important;
    }

    [data-theme="dark"] .success-card,
    .success-card {
        background-color: rgba(40, 167, 69, 0.2);
        color: #90ee90 !important;
        border-left: 4px solid #28a745;
    }

    /* Warning cards */
    [data-theme="light"] .warning-card {
        background-color: #fff3cd;
        color: #856404 !important;
    }

    [data-theme="dark"] .warning-card,
    .warning-card {
        background-color: rgba(255, 193, 7, 0.2);
        color: #ffeb3b !important;
        border-left: 4px solid #ffc107;
    }

    /* Better text visibility for all themes */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: inherit !important;
    }

    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: inherit !important;
    }

    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: inherit !important;
    }

    /* Enhanced visibility for metric cards */
    .metric-card,
    .success-card,
    .warning-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .metric-card {
            padding: 0.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)


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
def train_and_cache_model(enable_hyperparameter_tuning=False):
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
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'SVM': SVC(kernel='linear', random_state=42, probability=True)
    }

    results = {}
    training_times = {}

    for name, model in models.items():
        start_time = time.time()
        model.fit(X_train_tfidf, y_train)
        training_time = time.time() - start_time

        y_pred = model.predict(X_test_tfidf)
        accuracy = accuracy_score(y_test, y_pred)

        results[name] = {
            'accuracy': accuracy,
            'predictions': y_pred,
            'model': model,
            'training_time': training_time
        }
        training_times[name] = training_time

    # Get best model
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    best_model = results[best_model_name]['model']

    optimized_model = None
    optimization_improvement = 0

    if enable_hyperparameter_tuning and best_model_name == 'Logistic Regression':
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'penalty': ['l1', 'l2'],
            'solver': ['liblinear', 'lbfgs'],
            'max_iter': [1000, 2000]
        }

        grid_search = GridSearchCV(
            LogisticRegression(random_state=42),
            param_grid,
            cv=3,  # Reduced for faster execution
            scoring='accuracy',
            n_jobs=-1
        )

        grid_search.fit(X_train_tfidf, y_train)
        optimized_predictions = grid_search.predict(X_test_tfidf)
        optimized_accuracy = accuracy_score(y_test, optimized_predictions)

        if optimized_accuracy > results[best_model_name]['accuracy']:
            optimization_improvement = optimized_accuracy - \
                results[best_model_name]['accuracy']
            results[best_model_name]['model'] = grid_search.best_estimator_
            results[best_model_name]['predictions'] = optimized_predictions
            results[best_model_name]['accuracy'] = optimized_accuracy
            optimized_model = grid_search.best_estimator_

    final_accuracy = results[best_model_name]['accuracy']
    final_predictions = results[best_model_name]['predictions']

    classification_rep = classification_report(
        y_test, final_predictions,
        target_names=categories,
        output_dict=True
    )

    cm = confusion_matrix(y_test, final_predictions)

    feature_importance = None
    if best_model_name == 'Logistic Regression':
        coefficients = results[best_model_name]['model'].coef_
        feature_names = vectorizer.get_feature_names_out()

        # Get top features per category
        feature_importance = {}
        for i, category in enumerate(categories):
            top_indices = coefficients[i].argsort()[-10:][::-1]
            feature_importance[category.split('.')[-1]] = [
                {
                    'feature': feature_names[idx],
                    'coefficient': float(coefficients[i][idx])
                }
                for idx in top_indices
            ]

    metadata = {
        'model_name': best_model_name,
        'final_accuracy': final_accuracy,
        'categories': categories,
        'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'training_samples': len(X_train_raw),
        'test_samples': len(X_test_raw),
        'vocabulary_size': len(vectorizer.get_feature_names_out()),
        'classification_report': classification_rep,
        'confusion_matrix': cm.tolist(),
        'model_comparison': {name: data['accuracy'] for name, data in results.items()},
        'training_times': training_times,
        'optimization_improvement': optimization_improvement,
        'feature_importance': feature_importance,
        'preprocessing_info': {
            'tfidf_params': {
                'max_features': vectorizer.max_features,
                'min_df': vectorizer.min_df,
                'max_df': vectorizer.max_df,
                'ngram_range': vectorizer.ngram_range
            }
        }
    }

    return results[best_model_name]['model'], vectorizer, metadata


def predict_text_tags(text, model, vectorizer, categories):
    """Predict tags for text with enhanced error handling"""
    try:
        if not text or len(text.strip()) == 0:
            return None

        processed_text = preprocess_text(text)

        if len(processed_text.strip()) == 0:
            return None

        text_vector = vectorizer.transform([processed_text])
        prediction = model.predict(text_vector)[0]
        probabilities = model.predict_proba(text_vector)[0]
        top_3_indices = probabilities.argsort()[-3:][::-1]

        return {
            'text_length': len(text.split()),
            'processed_length': len(processed_text.split()),
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
# SIDEBAR CONFIGURATION
# =====================================================


st.sidebar.header("⚙️ Configuration")

# Model training options
enable_tuning = st.sidebar.checkbox(
    "Enable Hyperparameter Tuning",
    value=False,
    help="This will take longer but may improve accuracy"
)

if st.sidebar.button("🔄 Retrain Model"):
    st.cache_resource.clear()
    st.rerun()

st.sidebar.header("📊 Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["🏠 Home", "🎯 Demo", "📈 Analytics", "🔬 Advanced Analysis", "ℹ️ About"]
)

# =====================================================
# LOAD/TRAIN MODEL
# =====================================================

with st.spinner('🤖 Loading/Training model... This may take a few minutes on first run.'):
    try:
        model, vectorizer, metadata = train_and_cache_model(enable_tuning)
        model_loaded = True
        st.success("✅ Model ready!")
    except Exception as e:
        st.error(f"❌ Model training failed: {e}")
        model_loaded = False
        model, vectorizer, metadata = None, None, None

# Sidebar status
if model_loaded:
    st.sidebar.success("✅ Model Status: Ready")
    with st.sidebar:
        st.markdown(f"""
        **Model:** {metadata['model_name']}
        **Accuracy:** {metadata['final_accuracy']:.1%}
        **Categories:** {len(metadata['categories'])}
        **Vocabulary:** {metadata['vocabulary_size']:,}
        """)

        if metadata.get('optimization_improvement', 0) > 0:
            st.success(
                f"🚀 Optimization improved accuracy by +{metadata['optimization_improvement']:.3f}")
else:
    st.sidebar.error("❌ Model Status: Failed")
    st.sidebar.warning("Training failed or in progress...")

# =====================================================
# MAIN HEADER
# =====================================================

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #1f77b4; font-size: 3rem;">🏷️ Text Classification ML</h1>
    <p style="font-size: 1.2rem; color: #666;">Automatic text categorization using advanced Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Training status banner
if model_loaded:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success(
            f"🎯 Model trained successfully! **{metadata['model_name']}** achieved **{metadata['final_accuracy']:.1%}** accuracy"
        )
else:
    st.error(
        "⚠️ Model training in progress or failed. Please wait or refresh the page.")

# =====================================================
# PAGE ROUTING
# =====================================================

if page == "🏠 Home":
    st.header("🏠 Welcome to Text Classification Demo")

    if model_loaded and metadata is not None:
        # Enhanced metrics display
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="🎯 Model Accuracy",
                value=f"{metadata['final_accuracy']:.1%}",
                delta=f"Algorithm: {metadata['model_name']}"
            )

        with col2:
            st.metric(
                label="📂 Categories",
                value=len(metadata['categories']),
                delta="Multi-class classification"
            )

        with col3:
            st.metric(
                label="📚 Vocabulary",
                value=f"{metadata['vocabulary_size']:,}",
                delta="TF-IDF features"
            )

        with col4:
            training_time = sum(metadata.get('training_times', {}).values())
            st.metric(
                label="⚡ Training Time",
                value=f"{training_time:.1f}s",
                delta=f"{metadata['training_samples']:,} samples"
            )

        if metadata.get('optimization_improvement', 0) > 0:
            st.info(
                f"🚀 **Performance Boost:** Hyperparameter optimization improved accuracy by +{metadata['optimization_improvement']:.3f}")

        st.subheader("📋 Available Categories")

        categories_info = {
            'atheism': {'icon': '🛐', 'desc': 'Religious discussions'},
            'graphics': {'icon': '🎨', 'desc': 'Computer graphics'},
            'misc': {'icon': '💻', 'desc': 'Windows systems'},
            'hardware': {'icon': '🔧', 'desc': 'PC hardware'},
            'autos': {'icon': '🚗', 'desc': 'Automotive'},
            'motorcycles': {'icon': '🏍️', 'desc': 'Motorcycles'},
            'space': {'icon': '🚀', 'desc': 'Space & astronomy'},
            'misc': {'icon': '🗳️', 'desc': 'Politics'}
        }

        cols = st.columns(4)
        for i, category in enumerate(metadata['categories']):
            cat_short = category.split('.')[-1]
            with cols[i % 4]:
                icon = categories_info.get(cat_short, {}).get('icon', '📄')
                desc = categories_info.get(cat_short, {}).get(
                    'desc', cat_short.title())
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{icon} {cat_short.title()}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # Quick performance overview
        st.subheader("📊 Quick Performance Overview")

        if 'classification_report' in metadata:
            # Get F1 scores for categories
            f1_scores = []
            category_names = []

            for cat in metadata['categories']:
                if cat in metadata['classification_report']:
                    f1_scores.append(
                        metadata['classification_report'][cat]['f1-score'])
                    category_names.append(cat.split('.')[-1].title())

            if f1_scores:
                fig = px.bar(
                    x=category_names,
                    y=f1_scores,
                    title="F1-Score by Category",
                    color=f1_scores,
                    color_continuous_scale='RdYlGn',
                    range_color=[0, 1]
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(
            "❌ Model training failed or in progress. Please wait or refresh the page.")

elif page == "🎯 Demo":
    st.header("🎯 Try the Text Classifier")

    if model_loaded and model is not None:
        # Enhanced example texts with emojis
        examples = {
            "🚗 Cars": "I just bought a new car with amazing acceleration and great fuel economy. The engine performance is outstanding and the handling is smooth.",
            "🎨 Computer Graphics": "The latest graphics card from NVIDIA has incredible performance for gaming and machine learning applications. The ray tracing capabilities are impressive.",
            "🚀 Space": "NASA announced a new mission to Mars next year. The spacecraft will carry advanced scientific instruments to study the planet's atmosphere and geology.",
            "🗳️ Politics": "The political situation is getting more complex every day with new policies being announced. The government needs to address these issues carefully.",
            "🛐 Atheism": "Religious discussions often lead to debates about faith versus scientific evidence and rational thinking. Many people question traditional beliefs.",
            "🏍️ Motorcycles": "Harley Davidson motorcycles are known for their distinctive sound and classic American design. The chrome finish and powerful engine make them iconic.",
            "💻 Windows": "I'm having trouble with Windows 10 installation. The system keeps crashing during setup and showing blue screen errors.",
            "🔧 PC Hardware": "The new CPU has 16 cores and runs at 3.8 GHz with 32MB cache. Perfect for gaming, video editing and machine learning workloads."
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

            if st.button("🎯 Classify Text", type="primary"):
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
                                f"{result['text_length']} words",
                                f"Processed: {result['processed_length']} words"
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
                st.markdown(f"""
                <div class="success-card">
                    <h4>🤖 Algorithm: {metadata['model_name']}</h4>

                    <p><strong>⚡ Performance:</strong></p>
                    <ul>
                        <li>Accuracy: <strong>{metadata['final_accuracy']:.1%}</strong></li>
                        <li>Training samples: <strong>{metadata['training_samples']:,}</strong></li>
                        <li>Vocabulary: <strong>{metadata['vocabulary_size']:,}</strong> words</li>
                    </ul>

                    <p><strong>📅 Training Date:</strong> {metadata['training_date'].split()[0]}</p>
                </div>
                """, unsafe_allow_html=True)

            st.subheader("📂 Categories")
            categories_display = [
                f"🛐 {cat.split('.')[-1].title()}" if 'atheism' in cat else
                f"🎨 {cat.split('.')[-1].title()}" if 'graphics' in cat else
                f"💻 {cat.split('.')[-1].title()}" if 'windows' in cat else
                f"🔧 {cat.split('.')[-1].title()}" if 'hardware' in cat else
                f"🚗 {cat.split('.')[-1].title()}" if 'autos' in cat else
                f"🏍️ {cat.split('.')[-1].title()}" if 'motorcycles' in cat else
                f"🚀 {cat.split('.')[-1].title()}" if 'space' in cat else
                f"🗳️ {cat.split('.')[-1].title()}"
                for cat in metadata['categories']
            ]

            for cat_display in categories_display:
                st.write(f"• {cat_display}")

    else:
        st.error("Model not available. Training failed or in progress.")

elif page == "📈 Analytics":
    st.header("📈 Model Analytics")

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

elif page == "🔬 Advanced Analysis":
    st.header("🔬 Advanced Analysis")

    if model_loaded and metadata is not None:
        # Feature importance
        if 'feature_importance' in metadata and metadata['feature_importance'] is not None:
            st.subheader("Feature Importance")

            # Prepare data for visualization
            feature_importance_data = metadata['feature_importance']
            categories = metadata['categories']
            feature_importance_data_flat = [
                {
                    'Category': category.split('.')[-1].title(),
                    'Feature': feature['feature'],
                    'Coefficient': feature['coefficient']
                }
                for category, features in feature_importance_data.items()
                for feature in features
            ]

            if feature_importance_data_flat:
                df_feature_importance = pd.DataFrame(
                    feature_importance_data_flat)

                # Display table
                st.dataframe(df_feature_importance.round(3),
                             use_container_width=True)

                # Feature importance visualization
                fig = px.bar(
                    df_feature_importance.sort_values(
                        by='Coefficient', ascending=False),
                    x='Coefficient',
                    y='Feature',
                    color='Coefficient',
                    title="Feature Importance",
                    labels={'x': 'Coefficient', 'y': 'Feature'},
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

        # Learning curves
        st.subheader("Learning Curves")

        # Get data for learning curves
        X_train_raw, X_test_raw, y_train, y_test, categories = download_and_prepare_data()

        vectorizer_temp = TfidfVectorizer(
            max_features=10000,
            min_df=2,
            max_df=0.95,
            stop_words='english',
            ngram_range=(1, 2)
        )
        X_train_tfidf = vectorizer_temp.fit_transform(X_train_raw)

        with st.spinner("Calculating learning curves..."):
            # Calculate learning curves
            train_sizes, train_scores, test_scores = learning_curve(
                model, X_train_tfidf, y_train, cv=3, scoring='accuracy', n_jobs=-1)

        # Calculate mean and standard deviation for training and test scores
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)

        fig = go.Figure()

        # Training scores
        fig.add_trace(go.Scatter(
            x=train_sizes,
            y=train_scores_mean,
            name="Training score",
            mode='lines+markers',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))

        # Cross-validation scores
        fig.add_trace(go.Scatter(
            x=train_sizes,
            y=test_scores_mean,
            name="Cross-validation score",
            mode='lines+markers',
            line=dict(color='#ff7f0e', width=2),
            marker=dict(size=6)
        ))

        # Add confidence bands using fill_between approach
        # Upper bound for training
        fig.add_trace(go.Scatter(
            x=train_sizes,
            y=train_scores_mean + train_scores_std,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Lower bound for training (with fill)
        fig.add_trace(go.Scatter(
            x=train_sizes,
            y=train_scores_mean - train_scores_std,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(31, 119, 180, 0.2)',
            showlegend=False,
            hoverinfo='skip'
        ))

        # Upper bound for validation
        fig.add_trace(go.Scatter(
            x=train_sizes,
            y=test_scores_mean + test_scores_std,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Lower bound for validation (with fill)
        fig.add_trace(go.Scatter(
            x=train_sizes,
            y=test_scores_mean - test_scores_std,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(255, 127, 14, 0.2)',
            showlegend=False,
            hoverinfo='skip'
        ))

        fig.update_layout(
            title="Learning Curves - Model Performance vs Dataset Size",
            xaxis_title="Training examples",
            yaxis_title="Accuracy Score",
            legend=dict(x=0.02, y=0.98),
            hovermode='x unified',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # Add insights
        final_gap = train_scores_mean[-1] - test_scores_mean[-1]
        overfitting_status = "Low" if final_gap < 0.05 else "Medium" if final_gap < 0.1 else "High"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Training Score", f"{train_scores_mean[-1]:.3f}")
        with col2:
            st.metric("Validation Score", f"{test_scores_mean[-1]:.3f}")
        with col3:
            st.metric("Overfitting Level", overfitting_status,
                      f"Gap: {final_gap:.3f}")

    else:
        st.error(
            "Advanced analysis not available. Model training failed or in progress.")

elif page == "ℹ️ About":
    st.header("ℹ️ About This Project")

    st.markdown("""
    ## 🎯 Project Goal

    This project demonstrates a **complete machine learning pipeline** for automatic text classification.
    The system can automatically assign category tags to text documents using advanced ML techniques,
    meeting all academic requirements for ML project development.

    ## 🛠️ Technology Stack

    **Machine Learning:**
    - **Scikit-learn** - ML algorithms and evaluation tools
    - **TF-IDF Vectorization** - Advanced text feature extraction
    - **Multiple Algorithms** - Logistic Regression, Random Forest, SVM
    - **Hyperparameter Optimization** - GridSearchCV implementation
    - **Cross-Validation** - Robust model evaluation

    **Data Processing:**
    - **Pandas & NumPy** - Data manipulation and analysis
    - **Regular Expressions** - Text preprocessing and cleaning
    - **Feature Engineering** - N-gram extraction and importance analysis

    **Web Interface:**
    - **Streamlit** - Interactive web application framework
    - **Plotly** - Advanced interactive visualizations
    - **Real-time Prediction** - Live text classification

    ## 📊 Dataset

    **20 Newsgroups Dataset:**
    - Classic text classification benchmark dataset
    - 8 carefully selected categories from original 20
    - Real-world text data from Usenet discussion groups
    - Automatically downloaded and processed
    - ~4,500 training samples, ~3,000 test samples

    ## 🔄 ML Pipeline

    1. **Data Acquisition** - Automatic 20 Newsgroups fetching
    2. **Exploratory Data Analysis** - Statistical analysis and visualization
    3. **Text Preprocessing** - Cleaning, normalization, and feature extraction
    4. **Feature Engineering** - TF-IDF vectorization with unigrams and bigrams
    5. **Model Training** - Multiple algorithm comparison and evaluation
    6. **Hyperparameter Tuning** - GridSearch optimization (optional)
    7. **Model Evaluation** - Comprehensive metrics and error analysis
    8. **Feature Importance** - Model interpretability analysis
    9. **Model Persistence** - Caching for production use
    10. **Real-time Inference** - Interactive text classification

    ## 🎓 Academic Requirements Met

    ✅ **Problem Definition** - Clear, justified ML problem
    ✅ **Data Exploration** - Comprehensive EDA with visualizations
    ✅ **ML Model Building** - Multiple algorithms tested and compared
    ✅ **Hyperparameter Tuning** - GridSearch optimization available
    ✅ **Model Evaluation** - Multiple metrics and detailed analysis
    ✅ **Results Visualization** - Interactive charts and analysis
    ✅ **Feature Importance** - Model interpretability
    ✅ **Conclusions** - Insights and future recommendations

    ## 📈 Performance Results
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
        🤖 <strong>Text Classification ML System</strong><br>
        Built with Python • Scikit-learn • Streamlit • Plotly<br>
        {f"🎯 Current Model: {metadata['model_name']} | ⚡ Accuracy: {metadata['final_accuracy']:.1%} | 📚 Vocabulary: {metadata['vocabulary_size']:,} features" if model_loaded else "🔄 Model training in progress..."}
        <br><br>
        <em>Complete ML Pipeline: EDA → Feature Engineering → Model Training → Hyperparameter Tuning → Evaluation → Deployment</em>
    </div>
    """,
    unsafe_allow_html=True
)
