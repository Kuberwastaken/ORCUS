![Orcus_Banner](static/images/readme-images/Orcus-Banner-Github.png)

<h1 align="center">
  Observational Recognition of Content with Unnatural Speech
</h1>

<p align="center">
<img src="https://img.shields.io/static/v1?label=Kuberwastaken&message=ORCUS&color=e53935&logo=github" alt="Kuberwastaken - TREAT">
<img src="https://img.shields.io/badge/version-Alpha-e53935" alt="Version 2.0">
<img src="https://img.shields.io/badge/License-Apache_2.0-e53935" alt="License Apache 2.0">
</p>

Named after the Roman god of the underworld and the punisher of broken oaths, ORCUS is dedicated to upholding integrity and authenticity in the digital realm. 

## Mission
ORCUS' mission is to address the growing issue of AI-generated content, particularly on platforms like LinkedIn, where AI generated comments fill up the discussion without adding significantly to the original post or conversation.

These automated responses often overshadow genuine human engagement, contributing to a superficial online environment that diminishes the quality of discourse.

ORCUS strives to foster a cultural shift. By encouraging digital literacy and active participation, the project aims to reshape online spaces, restore trust, and ensure that social media remains a platform for thoughtful, original interactions where human creativity and insight are celebrated over automated, generic outputs, without much thought to it.

## Features
- **AI Detection Algorithms**: ORCUS uses the highly advanced and Open Soruce Roberta-Base-OpenAI-Detector Model from Hugging Face

- **Interactive Interface**: A user-friendly interface allows users to input text and analyze its authenticity.
- **Real-Time Feedback**: Provides almost immediate insights and suggestions for creating more authentic and engaging content.

- **Community-Driven**: Encourages a community of users committed to promoting originality and discouraging the overuse of AI for trivial purposes.

## Installation Instructions
### Prerequisites
 - Star the Repository to Show Your Support :P
 - Clone the Repository to Your Local Machine:

    ```bash
   git clone https://github.com/Kuberwastaken/ORCUS.git
    ```

### Hugging Face Instructions

1. **Login to Hugging Face in Your Environment:**

    Run the following command in your terminal:

    ```bash
    huggingface-cli login
    ```

    Enter your Hugging Face access token when prompted.

2. **Download the Roberta-Base-Openai-Detector Model:**

   The model will be downloaded automatically when running the script analysis for the first time, provided you have received access.

### Environment Setup
To set up the development environment, you will need to create a virtual environment and install the necessary dependencies.

1. Create a Virtual Environment:

   ```bash
   python3 -m venv orcus
   ```

2. Activate the Virtual Environment:

   ```bash
   source treat-env/bin/activate   # On Unix or MacOS
   treat-env\Scripts\activate      # On Windows
   ```

3. Install Dependencies:

   Navigate to the project directory and run:

   ```bash
   pip install -r requirements.txt
   ```

## Project Usage
1. **Start the Flask Server:**

   ```bash
   python app.py
   ```

2. **Open Your Browser:** 

   Navigate to `http://127.0.0.1:5000` to access the ORCUS web interface.

3. **Analyze Scripts:**

   You can manually enter a comment or text in the provided text area and click "Analyze Script."

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript

- **Backend**: Node.js

- **Machine Learning**: TensorFlow.js


## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/Kuberwastaken/ORCUS/blob/main/LICENSE) file for details.

## Contribution
Contributions are welcome and highly encouraged! Please fork the repository and submit a pull request for review!
