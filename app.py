
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------
# 1. PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="CSV Data Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CSV Data Analyzer")
st.write("Upload your CSV file and explore your dataset easily.")

# ----------------------------------
# 2. FILE UPLOAD
# ----------------------------------

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        st.success("CSV file uploaded successfully!")

        # ----------------------------------
        # 3. DATASET OVERVIEW
        # ----------------------------------

        st.header("1. Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Rows", df.shape[0])

        with col2:
            st.metric("Total Columns", df.shape[1])

        with col3:
            st.metric("Missing Values", int(df.isnull().sum().sum()))

        # Display dataset
        st.subheader("Dataset Preview")

        st.dataframe(df.head(10), use_container_width=True)

        # ----------------------------------
        # 4. DATASET INFORMATION
        # ----------------------------------

        st.subheader("Dataset Information")

        info_df = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Non-Null Count": df.notnull().sum().values,
            "Missing Count": df.isnull().sum().values
        })

        st.dataframe(info_df, use_container_width=True)

        # ----------------------------------
        # 5. MISSING VALUE ANALYSIS
        # ----------------------------------

        st.header("2. Missing Value Analysis")

        missing_df = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isnull().sum().values,
            "Missing Percentage": (
                df.isnull().mean().values * 100
            ).round(2)
        })

        missing_df = missing_df.sort_values(
            by="Missing Values",
            ascending=False
        )

        st.dataframe(missing_df, use_container_width=True)

        # Missing value chart
        if df.isnull().sum().sum() > 0:

            st.subheader("Missing Values Chart")

            fig, ax = plt.subplots(figsize=(10, 4))

            df.isnull().sum().plot(
                kind="bar",
                ax=ax
            )

            ax.set_title("Missing Values by Column")
            ax.set_xlabel("Columns")
            ax.set_ylabel("Missing Count")

            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

        else:
            st.success("No missing values found!")

        # ----------------------------------
        # 6. AUTOMATIC DATA VISUALIZATION
        # ----------------------------------

        st.header("3. Data Visualization")

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        # Histogram
        st.subheader("Numerical Data Distribution")

        if numeric_columns:

            selected_column = st.selectbox(
                "Select a numerical column",
                numeric_columns
            )

            fig, ax = plt.subplots(figsize=(9, 4))

            sns.histplot(
                data=df,
                x=selected_column,
                kde=True,
                ax=ax
            )

            ax.set_title(
                f"Distribution of {selected_column}"
            )

            st.pyplot(fig)
            plt.close(fig)

        else:
            st.info("No numerical columns available.")

        # Bar Chart
        st.subheader("Categorical Data Analysis")

        if categorical_columns:

            selected_category = st.selectbox(
                "Select a categorical column",
                categorical_columns
            )

            category_counts = (
                df[selected_category]
                .value_counts()
                .head(15)
            )

            fig, ax = plt.subplots(figsize=(9, 4))

            category_counts.plot(
                kind="bar",
                ax=ax
            )

            ax.set_title(
                f"Top Categories in {selected_category}"
            )

            ax.set_xlabel(selected_category)
            ax.set_ylabel("Count")

            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

        else:
            st.info("No categorical columns available.")

        # Correlation Heatmap
        st.subheader("Correlation Heatmap")

        if len(numeric_columns) >= 2:

            fig, ax = plt.subplots(figsize=(10, 6))

            correlation = df[numeric_columns].corr()

            sns.heatmap(
                correlation,
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                ax=ax
            )

            ax.set_title("Correlation Between Numerical Columns")

            st.pyplot(fig)
            plt.close(fig)

        else:
            st.info(
                "At least two numerical columns are required "
                "for a correlation heatmap."
            )

        # ----------------------------------
        # 7. DOWNLOAD REPORT
        # ----------------------------------

        st.header("4. Download Report")

        csv_data = missing_df.to_csv(index=False)

        st.download_button(
            label="Download Missing Values Report",
            data=csv_data,
            file_name="missing_values_report.csv",
            mime="text/csv"
        )

        st.success("Data analysis completed!")

    except Exception as e:

        st.error(f"Error reading or analyzing CSV file: {e}")

else:

    st.info("Please upload a CSV file to begin analysis.")

    st.write("Supported format: CSV")