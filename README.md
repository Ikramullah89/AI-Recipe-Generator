AI Recipe Generator
A Streamlit-based web application powered by Gemini AI to create personalized recipes tailored to your preferences, dietary needs, and available ingredients.
Overview
The AI Recipe Generator is an innovative tool designed for home cooks, food enthusiasts, and anyone looking to explore new recipes. Whether you want a recipe for a specific dish, need to use ingredients you have on hand, or prefer dishes that align with dietary restrictions or regional cuisines, this app delivers. With a sleek, modern interface, it offers interactive cooking steps, visual aids, shopping lists, and curated recipe suggestions based on seasons and cuisines.
Features

Recipe Generation: Create detailed recipes by entering a dish name (e.g., Chocolate Cake) or listing ingredients (e.g., flour, sugar, eggs).
Dietary Preferences: Customize recipes for diets like Vegan, Vegetarian, Gluten-Free, Dairy-Free, Keto, or Low-Carb.
Allergen Exclusions: Exclude allergens such as peanuts, shellfish, milk, or wheat with a simple comma-separated input.
Seasonal Ingredients: Choose recipes using ingredients in season for Spring, Summer, Autumn, or Winter.
Regional Cuisines: Select from cuisines including Italian, Mexican, Indian, Japanese, Mediterranean, American, Pakistani, Thai, Chinese, French, and Brazilian.
Interactive Cooking Steps: Follow step-by-step instructions with estimated times, visual aids, and interactive timers.
Shopping List Generation: Automatically generate a downloadable shopping list for your recipe.
Grocery Delivery Integration: Link to services like Instacart for convenient ingredient ordering.
Recipe Suggestions: Discover three curated recipes based on your selected season, cuisine, and dietary preferences.

Installation
To set up the AI Recipe Generator locally, follow these steps:

Obtain a Gemini API Key:

Sign up for a free API key at Google AI Studio.


Clone the Repository:
git clone https://github.com/Ikramullah89/AI-Recipe-Generator.git


Navigate to the Project Directory:
cd AI-Recipe-Generator


Install Dependencies:

Ensure you have Python 3.8 or higher installed.
Install the required libraries using the provided requirements.txt:pip install -r requirements.txt


The requirements.txt includes:streamlit==1.31.0
google-generativeai==0.8.3
python-dotenv==1.0.1
nest_asyncio==1.6.0




Set Up Environment Variables:

Create a .env file in the project directory.
Add your Gemini API key:GEMINI_API_KEY=your_api_key_here


Replace your_api_key_here with your actual API key.



Usage

Run the Application:

Start the Streamlit app:streamlit run app.py


This will open the app in your default web browser.


Explore the App:

Generate Recipe:
Select "Generate Recipe" from the sidebar.
Choose to generate by dish name or ingredients.
Specify dietary preferences, allergens to exclude, season, and regional cuisine.
Click "Generate Recipe" to view your recipe, complete with ingredients, nutritional information, and interactive cooking steps.


Seasonal/Regional Suggestions:
Select "Seasonal/Regional Suggestions" from the sidebar.
Choose a season and cuisine, and optionally add dietary preferences or allergens.
Click "Discover Recipes" to get three curated recipe suggestions.




Interact with Features:

Use the timer buttons for each cooking step to track preparation time.
Download the shopping list as a text file or follow the grocery delivery link to order ingredients.



Project Structure



File/Folder
Description



app.py
Main application script for the Streamlit app.


.gitignore
Excludes unnecessary files (e.g., .env, venv/).


requirements.txt
Lists Python dependencies for the project.


README.md
This file, providing project documentation.


Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch for your changes:git checkout -b feature/your-feature-name


Make your changes and commit them:git commit -m "Add your feature description"


Push to your fork:git push origin feature/your-feature-name


Open a pull request on GitHub.

Please ensure your code follows the project's coding style and includes appropriate documentation.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions, feedback, or collaboration opportunities, reach out to me:

GitHub: Ikramullah89
Email: your_email@example.com

Happy cooking! 🍽️
