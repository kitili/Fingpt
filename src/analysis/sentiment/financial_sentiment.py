"""
Financial Sentiment Analysis
===========================

This module demonstrates how CS concepts like NLP, machine learning,
and data processing can be applied to analyze financial sentiment.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import re
import logging
from dataclasses import dataclass
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import nltk
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Data class for sentiment analysis results"""
    text: str
    polarity: float  # -1 to 1
    subjectivity: float  # 0 to 1
    compound_score: float  # -1 to 1
    sentiment_label: str  # 'positive', 'negative', 'neutral'
    confidence: float  # 0 to 1

class FinancialSentimentAnalyzer:
    """
    Financial Sentiment Analyzer using multiple NLP techniques
    Demonstrates: NLP, machine learning, text processing, API integration
    """
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.model = None
        self.financial_lexicon = self._load_financial_lexicon()
        
    def _load_financial_lexicon(self) -> Dict[str, float]:
        """
        Load financial-specific sentiment lexicon
        Demonstrates: Domain-specific knowledge integration
        """
        return {
            # Positive financial terms
            'bullish': 0.8, 'surge': 0.7, 'rally': 0.7, 'gain': 0.6,
            'profit': 0.7, 'growth': 0.6, 'strong': 0.5, 'beat': 0.6,
            'exceed': 0.6, 'outperform': 0.7, 'breakthrough': 0.8,
            'milestone': 0.6, 'record': 0.5, 'high': 0.4,
            
            # Negative financial terms
            'bearish': -0.8, 'crash': -0.9, 'plunge': -0.8, 'loss': -0.7,
            'decline': -0.6, 'weak': -0.5, 'miss': -0.6, 'disappoint': -0.7,
            'concern': -0.4, 'risk': -0.3, 'volatile': -0.4, 'uncertain': -0.5,
            'downturn': -0.7, 'recession': -0.8, 'crisis': -0.9
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess financial text
        Demonstrates: Text cleaning, regex, data preprocessing
        """
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove special characters but keep financial symbols
        text = re.sub(r'[^a-zA-Z0-9\s$%]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def analyze_sentiment_textblob(self, text: str) -> Tuple[float, float]:
        """
        Analyze sentiment using TextBlob
        Demonstrates: Library integration, sentiment analysis
        """
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity, blob.sentiment.subjectivity
        except Exception as e:
            logger.error(f"TextBlob analysis error: {str(e)}")
            return 0.0, 0.0
    
    def analyze_sentiment_vader(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using VADER
        Demonstrates: Advanced sentiment analysis, compound scoring
        """
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            return scores
        except Exception as e:
            logger.error(f"VADER analysis error: {str(e)}")
            return {'pos': 0.0, 'neu': 1.0, 'neg': 0.0, 'compound': 0.0}
    
    def analyze_financial_sentiment(self, text: str) -> SentimentResult:
        """
        Comprehensive financial sentiment analysis
        Demonstrates: Multi-method analysis, ensemble techniques
        """
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        if not processed_text:
            return SentimentResult(
                text=text, polarity=0.0, subjectivity=0.0,
                compound_score=0.0, sentiment_label='neutral', confidence=0.0
            )
        
        # TextBlob analysis
        polarity, subjectivity = self.analyze_sentiment_textblob(processed_text)
        
        # VADER analysis
        vader_scores = self.analyze_sentiment_vader(processed_text)
        
        # Financial lexicon analysis
        financial_score = self._analyze_financial_lexicon(processed_text)
        
        # Combine scores (weighted average)
        combined_polarity = (polarity * 0.3 + vader_scores['compound'] * 0.5 + financial_score * 0.2)
        
        # Determine sentiment label
        if combined_polarity > 0.1:
            sentiment_label = 'positive'
        elif combined_polarity < -0.1:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'
        
        # Calculate confidence based on agreement between methods
        confidence = self._calculate_confidence(polarity, vader_scores['compound'], financial_score)
        
        return SentimentResult(
            text=text,
            polarity=combined_polarity,
            subjectivity=subjectivity,
            compound_score=vader_scores['compound'],
            sentiment_label=sentiment_label,
            confidence=confidence
        )
    
    def _analyze_financial_lexicon(self, text: str) -> float:
        """
        Analyze using financial-specific lexicon
        Demonstrates: Domain-specific analysis, lexicon-based scoring
        """
        words = text.split()
        total_score = 0.0
        word_count = 0
        
        for word in words:
            if word in self.financial_lexicon:
                total_score += self.financial_lexicon[word]
                word_count += 1
        
        return total_score / word_count if word_count > 0 else 0.0
    
    def _calculate_confidence(self, polarity: float, vader_compound: float, financial_score: float) -> float:
        """
        Calculate confidence based on agreement between methods
        Demonstrates: Statistical analysis, confidence scoring
        """
        scores = [polarity, vader_compound, financial_score]
        
        # Calculate variance (lower variance = higher confidence)
        mean_score = np.mean(scores)
        variance = np.var(scores)
        
        # Convert variance to confidence (inverse relationship)
        confidence = max(0.0, min(1.0, 1.0 - variance))
        
        return confidence
    
    def analyze_batch(self, texts: List[str]) -> List[SentimentResult]:
        """
        Analyze multiple texts efficiently
        Demonstrates: Batch processing, list comprehensions
        """
        return [self.analyze_financial_sentiment(text) for text in texts]
    
    def get_sentiment_summary(self, results: List[SentimentResult]) -> Dict[str, float]:
        """
        Generate summary statistics for sentiment results
        Demonstrates: Statistical analysis, data aggregation
        """
        if not results:
            return {}
        
        polarities = [r.polarity for r in results]
        confidences = [r.confidence for r in results]
        
        # Count sentiment labels
        label_counts = {}
        for result in results:
            label = result.sentiment_label
            label_counts[label] = label_counts.get(label, 0) + 1
        
        total = len(results)
        
        return {
            'avg_polarity': np.mean(polarities),
            'std_polarity': np.std(polarities),
            'avg_confidence': np.mean(confidences),
            'positive_ratio': label_counts.get('positive', 0) / total,
            'negative_ratio': label_counts.get('negative', 0) / total,
            'neutral_ratio': label_counts.get('neutral', 0) / total,
            'total_analyzed': total
        }
    
    def fetch_financial_news(self, symbol: str, num_articles: int = 10) -> List[str]:
        """
        Fetch financial news for a symbol (mock implementation)
        Demonstrates: Web scraping concepts, API integration
        """
        # This is a simplified mock - in practice, you'd use real news APIs
        mock_news = [
            f"{symbol} shows strong quarterly performance with record revenue",
            f"Analysts are bullish on {symbol} following recent earnings beat",
            f"{symbol} faces headwinds in the current market environment",
            f"Investors remain optimistic about {symbol}'s long-term prospects",
            f"{symbol} stock price volatility concerns some market participants"
        ]
        
        return mock_news[:num_articles]
    
    def train_custom_model(self, training_data: List[Tuple[str, str]]) -> None:
        """
        Train a custom sentiment model
        Demonstrates: Machine learning, model training, feature engineering
        """
        if not training_data:
            logger.warning("No training data provided")
            return
        
        texts, labels = zip(*training_data)
        
        # Preprocess texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Convert labels to numeric
        label_map = {'positive': 1, 'negative': -1, 'neutral': 0}
        numeric_labels = [label_map.get(label, 0) for label in labels]
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(processed_texts)
        y = np.array(numeric_labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Custom model trained with accuracy: {accuracy:.3f}")
        print(f"Model Accuracy: {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=['negative', 'neutral', 'positive']))

# Example usage and testing
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = FinancialSentimentAnalyzer()
    
    # Sample financial texts
    sample_texts = [
        "Apple's quarterly earnings exceeded expectations with strong iPhone sales",
        "The market crash has investors worried about tech stocks",
        "Tesla's stock price remains volatile amid production concerns",
        "Microsoft's cloud revenue growth shows promising signs",
        "The Federal Reserve's interest rate decision is uncertain"
    ]
    
    print("Analyzing financial sentiment...")
    
    # Analyze individual texts
    for text in sample_texts:
        result = analyzer.analyze_financial_sentiment(text)
        print(f"\nText: {text}")
        print(f"Sentiment: {result.sentiment_label} (polarity: {result.polarity:.3f})")
        print(f"Confidence: {result.confidence:.3f}")
    
    # Batch analysis
    print("\n" + "="*50)
    print("BATCH ANALYSIS")
    print("="*50)
    
    results = analyzer.analyze_batch(sample_texts)
    summary = analyzer.get_sentiment_summary(results)
    
    print(f"Average Polarity: {summary['avg_polarity']:.3f}")
    print(f"Positive Ratio: {summary['positive_ratio']:.3f}")
    print(f"Negative Ratio: {summary['negative_ratio']:.3f}")
    print(f"Neutral Ratio: {summary['neutral_ratio']:.3f}")
    print(f"Average Confidence: {summary['avg_confidence']:.3f}")
    
    # Train custom model (with sample data)
    print("\n" + "="*50)
    print("CUSTOM MODEL TRAINING")
    print("="*50)
    
    training_data = [
        ("Stock prices are rising", "positive"),
        ("Market is crashing", "negative"),
        ("Earnings report is neutral", "neutral"),
        ("Great quarterly results", "positive"),
        ("Poor performance this quarter", "negative")
    ]
    
    analyzer.train_custom_model(training_data)
