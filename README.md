**Business Intelligent Agent**

*Build interactive dashboards and data slicers effortlessly.*

---

## Overview

The **Business Intelligent Agent** leverages Streamlit and the o4-mini LLM to generate dashboards and data slicers in seconds. Simply provide your requirements and CSV data, and the agent will create a polished, interactive UI for data exploration.

---

## Features

* **Rapid Prototyping**: Instantly visualize small to medium-sized datasets.
* **Transparent Workflow**: Generates Python code as an intermediary step, allowing you to review and customize before deployment.
* **Multi-File Support**: Can work with multiple CSV files to create combined dashboards.

---

## Installation

1. Ensure you have Python 3.7 or higher installed.
2. Install required packages:

   ```bash
   pip install streamlit pandas openai
   ```
3. Clone this repository and navigate to the project folder.
4. Run the application:

   ```bash
   streamlit run 1_🤖_Home.py
   ```

---

## Configuration

* **OpenAI API Key**:
  Add your OpenAI API key in the sidebar of the home page. This is required for the o4-mini model to generate code and UI components.

---

## Usage

1. Launch the app with `streamlit run 1_🤖_Home.py`.
2. In the sidebar, enter your OpenAI API key.
3. Upload one or more CSV files containing your data.
4. Specify your dashboard requirements (e.g., fields to plot, filters to add).
5. The agent will generate a Streamlit UI, including code snippets, within seconds.
6. Review and modify the generated Python code as needed.

---

## Advantages

* **Speed**: Quickly creates interactive visualizations without manual coding.
* **Transparency**: Python code is displayed, making it easy to audit and adjust.
* **Flexibility**: Supports multiple data files and a variety of chart types (e.g., line, bar, scatter).

---

## Limitations

* **Inconsistent Plotting**: Some chart types or edge-case datasets may not render exactly as expected.
* **Fragile Code Generation**: The generated Python code might require additional prompt tuning for complex data or advanced customizations.

---

## Contributing

Contributions and feature requests are welcome! Please open an issue or submit a pull request with your suggestions.

---

## License

This project is licensed under the MIT License.
Feel free to modify and distribute as needed.

