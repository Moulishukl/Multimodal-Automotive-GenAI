#  AutoGenX – Multimodal Automotive Generative

##  Overview

AutoGenX is a final-year project focused on exploring how **Generative AI can be applied in the automotive domain**. The core idea behind this project is to allow users to generate creative and futuristic car designs simply by providing text prompts.

Instead of relying on traditional design tools, this system leverages **multimodal AI capabilities** to transform human imagination into visual outputs. The application is built with a simple and interactive interface so that even non-technical users can experiment with AI-generated automotive designs.

This project reflects the practical implementation of **GenAI, API integration, and real-time UI systems**, making it a strong example of applied AI in a real-world use case.

---

##  Objective

The main objectives of this project are:

* To demonstrate the use of **Generative AI in design automation**
* To build a system that can convert **text prompts into automotive visuals**
* To explore **multimodal AI systems** (text + image generation)
* To develop an **interactive web-based application** for AI-driven creativity

---

##  How the System Works

The workflow of the system is simple yet powerful:

1. The user enters a text prompt (e.g., *"A futuristic electric sports car with neon lights"*)
2. The prompt is sent to a **Generative AI API** (such as Gemini or other image generation APIs)
3. The AI model processes the input and generates an image
4. The generated image is displayed on the **Streamlit interface**

This pipeline connects **user input → AI processing → visual output** in real time.

---

## Technologies Used

This project combines multiple technologies to achieve its functionality:

### Programming Language

* Python

### Frontend / UI

* Streamlit (for building an interactive web interface)

### AI & APIs

* Google Gemini API (for generative capabilities)
* External image generation APIs (if configured)

### Libraries

* `requests` – for API communication
* `Pillow (PIL)` – for image processing
* `python-dotenv` – for managing environment variables

---

## Project Structure

The project is organized in a simple and understandable way:

* `app.py` → Main application file (Streamlit UI + logic)
* `app_gemini.py` → Alternative implementation using Gemini API
* `requirements.txt` → Contains all dependencies required to run the project
* `car_design.png` → Sample generated output
* `README.md` → Project documentation

---

## Getting Started

Follow these steps to run the project on your local system:

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AutoGenX-Multimodal-Automotive-AI.git
cd AutoGenX-Multimodal-Automotive-AI
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory and add your API key:

```
API_KEY=your_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## Sample Output

The system generates images based on user prompts. A sample output has been included in the repository:

`car_design.png`

This demonstrates how AI interprets textual descriptions into automotive designs.

---

## Use Cases

This project can be useful in multiple scenarios:

* Concept car design and prototyping
* AI-based creative exploration
* Educational demonstration of Generative AI
* Rapid visualization for automotive ideas

---

## Future Improvements

There are several ways this project can be enhanced further:

* Adding **customization options** (color, model type, features)
* Integrating a **vector database (Chroma)** for better prompt understanding
* Implementing **agentic AI workflows** for automated design suggestions
* Deploying the application on **cloud platforms**
* Adding **CI/CD pipelines using GitHub Actions (DevOps integration)**

---

## Important Notes

* The `.env` file should not be uploaded to GitHub as it contains sensitive API keys
* The `venv/` folder should also be excluded from version control
* Use a `.gitignore` file to prevent these from being uploaded

---

## Author

Mouli Shukla
B.Tech (Computer Science – AI/ML)
Final Year Project

---

## Conclusion

AutoGenX showcases how **Generative AI can simplify and enhance creative processes** in industries like automotive design. By combining AI models with an intuitive interface, the project demonstrates the potential of building intelligent systems that are both powerful and accessible.

---

## Acknowledgement

This project makes use of modern AI tools and frameworks including:

* Google Generative AI (Gemini)
* Streamlit
* Open-source Python libraries

---

*If you found this project interesting, feel free to explore, modify, and build upon it.*
