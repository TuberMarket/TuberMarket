import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob
import pandas as pd
from transformers import pipeline
def news_tab():
    # Load the summarization pipeline
    summarizer = pipeline("summarization")

    # Function to fetch top news headlines
    def fetch_news(query='stock market', language='en', page_size=10):
        newsapi = NewsApiClient(api_key='50fd4ed3f3bd4a2193cf69fd8f77a543')  # Replace YOUR_API_KEY_HERE with your actual News API key
        articles = newsapi.get_everything(q=query, language=language, page_size=page_size, sort_by="relevancy")
        return articles['articles']

    # Function to analyze sentiment of headlines
    def analyze_sentiment(headline):
        analysis = TextBlob(headline)
        return analysis.sentiment

    # Function to summarize an article
    def summarize_article(article_content):
        if article_content:
            summary_text = summarizer(article_content, max_length=130, min_length=25, do_sample=False)
            return summary_text[0]['summary_text']
        else:
            return "No content to summarize"

    # Streamlit app function
    def main():
        # Creating tabs
        tab1, tab2 = st.tabs(["News", "Another Tab"])
        
        with tab1:
            st.header("Stock Market News Analysis")
            
            # User inputs
            query = st.text_input("Enter search query:", value="stock market")
            page_size = st.slider("Number of articles to fetch:", min_value=1, max_value=20, value=10)
            
            if st.button("Fetch News"):
                with st.spinner("Fetching news articles..."):
                    articles = fetch_news(query=query, page_size=page_size)
                    
                    # List to store analyzed data
                    analyzed_data = []
                    
                    for article in articles:
                        headline = article['title']
                        description = article['description']
                        content = article['content']
                        
                        # Analyze sentiment
                        sentiment = analyze_sentiment(headline)
                        
                        # Summarize article content
                        summary = summarize_article(content if content else description)
                        
                        analyzed_data.append({'headline': headline, 'sentiment': sentiment.polarity, 'summary': summary})
                    
                    # Convert to DataFrame for display
                    df = pd.DataFrame(analyzed_data)
                    
                    # Displaying the DataFrame
                    st.dataframe(df)
                    
        with tab2:
            st.write("Content for another tab can go here.")

    if __name__ == "__main__":
        main()
