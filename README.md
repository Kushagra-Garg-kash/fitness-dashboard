# 🏋️ Lifestyle Fitness Dashboard

This project is a dynamic and interactive fitness dashboard built with **Streamlit** that allows users to visualize and analyze their health and fitness data. It provides quick stats, detailed graphs, trend analysis, and AI-powered insights to help you understand your activity patterns and stay on track with your wellness goals.

---

## 🚀 Features

* **Interactive Dashboard:** Explore your data with a user-friendly and responsive interface.
* **Quick Stats (KPI Cards):** Get a snapshot of your key metrics for a selected month, including total steps, average sleep, and total calories burned.
* **Correlation Heatmap:** Visualize the relationships between different fitness metrics to see which factors are most connected in your life.
* **Weekly Activity Breakdown:** Analyze how your activity levels evolve over time with an area chart.
* **AI-Powered Insights:** Get automatic insights and trend detections, such as an increase or decrease in metrics over time or the detection of unusual values.
* **Calendar Heatmap:** Discover daily and monthly activity patterns, revealing your most and least active days of the week.
* **7-Day Rolling Averages:** Smooth out daily fluctuations to identify underlying trends in your data.
* **Custom Data Upload:** Upload your own fitness data in a CSV format to analyze your personal health journey.
* **Theme Toggle:** Switch between light and dark themes for a customized viewing experience.

---

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```
2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

**Note:** The `requirements.txt` file should include the following libraries: `streamlit`, `pandas`, `numpy`, `plotly`, `matplotlib`, `seaborn`.

---

## 🏃 Usage

1.  **Run the Streamlit application:**
    ```bash
    streamlit run your_app_name.py
    ```
    (Replace `your_app_name.py` with the name of your Python script.)
2.  The application will automatically open in your default web browser.
3.  **Explore the dashboard:**
    * Use the **sidebar filters** to select a month and choose which metrics you want to display.
    * Navigate between the **tabs** to view different sections: "Graphs," "Insights," "Trends," and "Upload Data."
    * In the "Upload Data" tab, you can upload your own CSV file. The file must contain the following columns: **`Date`**, **`Steps`**, **`Calories`**, **`WorkoutMinutes`**, **`SleepHours`**, **`WaterIntake(L)`**, and **`HeartRate`**.

---

## 📂 File Structure

* `app.py`: The main Streamlit application script containing all the code.
* `fitness_dashboard_data.csv`: A sample dataset to run the dashboard out of the box.
* `requirements.txt`: Lists all the necessary Python libraries.
* `README.md`: This file.

---

## 🤝 Contribution

Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.