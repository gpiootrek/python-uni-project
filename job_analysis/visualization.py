import pandas as pd
import streamlit as st 
import altair as alt

class Visualization:
    @staticmethod
    def display_salary_statistics(salary_stats):
        """Display salary statistics in a DataFrame format."""
        if salary_stats:
            lower_stats = salary_stats.get("lower_range_stats", {})
            upper_stats = salary_stats.get("upper_range_stats", {})

            # Extract all statistics into a unified DataFrame
            salary_df = pd.DataFrame({
                "Statistic": ["Min", "Max", "Mean", "Median", "Standard Deviation", "Count"],
                "Lower Range": [
                    lower_stats.get("min"),
                    lower_stats.get("max"),
                    lower_stats.get("mean"),
                    lower_stats.get("median"),
                    lower_stats.get("std_dev"),
                    lower_stats.get("count"),
                ],
                "Upper Range": [
                    upper_stats.get("min"),
                    upper_stats.get("max"),
                    upper_stats.get("mean"),
                    upper_stats.get("median"),
                    upper_stats.get("std_dev"),
                    upper_stats.get("count"),
                ],
            })

            # Display the DataFrame in Streamlit
            st.write("### Salary Statistics")
            st.dataframe(salary_df, use_container_width=True)
        else:
            st.write("No salary data available.")
            
    @staticmethod
    def plot_skill_frequency(skill_counter, title="Top 5 most frequently required primary skills", n_skills=5):
        """Plot the skill frequency as a bar chart."""
        
        # Create a DataFrame from the skill counter and sort it by frequency
        df = pd.DataFrame(skill_counter.items(), columns=["Skill", "Frequency"]).sort_values(by="Frequency", ascending=False).head(n_skills)
        
        # Reset the index for the DataFrame
        df = df.reset_index(drop=True)
        
        # Display the title
        st.write(title)
        
        # Altair bar chart
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Skill', sort='-y'),  
            y='Frequency',
            color='Skill',  
            tooltip=['Skill', 'Frequency'] 
        )
        
        # Display the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)
        
        # Display the DataFrame as a table for better context
        st.write(df)

    @staticmethod
    def display_skill_frequency_table(analysis_results):
        """Display the primary and secondary skill frequencies as tables."""
        primary_skill_frequency = analysis_results["skill_frequency"]["primary"]
        secondary_skill_frequency = analysis_results["skill_frequency"]["secondary"]

        # Convert to Pandas DataFrame
        primary_df = pd.DataFrame(primary_skill_frequency.items(), columns=["Skill", "Frequency"]).sort_values(by="Frequency", ascending=False)
        secondary_df = pd.DataFrame(secondary_skill_frequency.items(), columns=["Skill", "Frequency"]).sort_values(by="Frequency", ascending=False)

        # Display the tables in Streamlit
        st.write("Primary Skill Frequency:")
        st.dataframe(primary_df[["Skill", "Frequency"]].reset_index(drop=True), use_container_width=True)

        st.write("Secondary Skill Frequency:")
        st.dataframe(secondary_df[["Skill", "Frequency"]].reset_index(drop=True), use_container_width=True)
