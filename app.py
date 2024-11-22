import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from sklearn.preprocessing import LabelEncoder

# Set up Gemini API key
gemini_api_key = 'AIzaSyCyZMPQFH_4KFA2Yont0aWOMcPtoNwFUFE'

def query_gemini_api(query):
    """Query the Gemini API with a custom query."""
    url = "https://api.gemini.com/v1/query"
    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def generate_visualizations(df):
    """Automatically generate key visualizations based on the dataset."""
    st.header("Generated Visualizations")

    # Detect numerical and categorical columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    # Visualization 1: Correlation heatmap for numerical columns
    if len(num_cols) > 1:
        st.subheader("Correlation Heatmap")
        plt.figure(figsize=(10, 6))
        sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
        st.pyplot(plt)

    # Visualization 2: Countplot for categorical columns
    for col in cat_cols:
        st.subheader(f"Countplot for {col}")
        plt.figure(figsize=(8, 4))
        sns.countplot(data=df, x=col)
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # Visualization 3: Boxplots for numerical vs categorical columns
    for num_col in num_cols:
        for cat_col in cat_cols:
            st.subheader(f"Boxplot: {num_col} vs {cat_col}")
            plt.figure(figsize=(8, 4))
            sns.boxplot(data=df, x=cat_col, y=num_col)
            plt.xticks(rotation=45)
            st.pyplot(plt)

    # Visualization 4: Histogram for numerical columns
    for col in num_cols:
        st.subheader(f"Histogram for {col}")
        plt.figure(figsize=(8, 4))
        sns.histplot(data=df, x=col, kde=True)
        st.pyplot(plt)

    # Visualization 5: Pairplot for numerical columns
    if len(num_cols) > 1:
        st.subheader("Pairplot for Numerical Columns")
        plt.figure(figsize=(10, 6))
        sns.pairplot(df[num_cols])
        st.pyplot(plt)

    # Visualization 6: Barplot for categorical columns
    for col in cat_cols:
        st.subheader(f"Barplot for {col}")
        plt.figure(figsize=(8, 4))
        sns.barplot(data=df, x=col, y=num_cols[0])
        plt.xticks(rotation=45)
        st.pyplot(plt)

def generate_custom_visualization(df, query):
    """Generate custom visualizations based on the query."""
    query = query.lower()
    col = query.split("for")[-1].strip()
    col = col.lower()

    # Convert dataframe columns to lowercase for comparison
    df.columns = df.columns.str.lower()

    if "pie chart" in query:
        if col in df.columns:
            st.subheader(f"Pie Chart for {col}")
            plt.figure(figsize=(8, 8))
            df[col].value_counts().plot.pie(autopct='%1.1f%%')
            st.pyplot(plt)
        else:
            st.write(f"Column '{col}' not found in the dataset.")
    elif "bar chart" in query or "bar plot" in query:
        if col in df.columns:
            st.subheader(f"Bar Chart for {col}")
            plt.figure(figsize=(8, 4))
            sns.barplot(x=df[col].value_counts().index, y=df[col].value_counts().values)
            plt.xticks(rotation=45)
            st.pyplot(plt)
        else:
            st.write(f"Column '{col}' not found in the dataset.")
    elif "count plot" in query or "countplot" in query:
        if col in df.columns:
            st.subheader(f"Count Plot for {col}")
            plt.figure(figsize=(8, 4))
            sns.countplot(data=df, x=col)
            plt.xticks(rotation=45)
            st.pyplot(plt)
        else:
            st.write(f"Column '{col}' not found in the dataset.")
    elif "box plot" in query or "boxplot" in query:
        cols = query.split("for")[-1].strip().split("vs")
        if len(cols) == 2:
            cat_col, num_col = cols[0].strip(), cols[1].strip()
            cat_col, num_col = cat_col.lower(), num_col.lower()
            if cat_col in df.columns and num_col in df.columns:
                st.subheader(f"Box Plot: {num_col} vs {cat_col}")
                plt.figure(figsize=(8, 4))
                sns.boxplot(data=df, x=cat_col, y=num_col)
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.write(f"Columns '{cat_col}' or '{num_col}' not found in the dataset.")
        else:
            st.write("Please specify the columns in the format 'box plot for <categorical_column> vs <numerical_column>'.")
    else:
        st.write("Could not process query. Please try rephrasing.")

def main():
    st.title("Automated Data Visualization System")

    uploaded_file = st.file_uploader("Upload your dataset (CSV)", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Preview of the Dataset")
        st.write(df.head())

        # Generate automated visualizations
        generate_visualizations(df)

        # Allow user to enter natural language queries
        st.header("Natural Language Query")
        query = st.text_input("Ask something about the dataset:")

        if st.button("Generate Visualization"):
            generate_custom_visualization(df, query)

if __name__ == "__main__":
    main()
    
    
    
    #AIzaSyCyZMPQFH_4KFA2Yont0aWOMcPtoNwFUFE