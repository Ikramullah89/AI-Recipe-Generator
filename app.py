import os
import asyncio
import streamlit as st
import nest_asyncio
from dotenv import load_dotenv
import google.generativeai as genai
import time
import re
import io

# Handle asyncio loop for Streamlit
nest_asyncio.apply()

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Function definitions
async def get_recipe(prompt):
    generation_config = {
        "max_output_tokens": 1200,
        "temperature": 0.7,
    }
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro-001",
        generation_config=generation_config
    )
    response = await model.generate_content_async(prompt)
    return response.text

def get_placeholder_image(step_text):
    step_text = step_text.lower()
    if "preheat" in step_text or "oven" in step_text:
        return "https://images.unsplash.com/photo-1600585154340-be6161a56a0c"
    elif "mix" in step_text or "stir" in step_text or "blend" in step_text:
        return "https://images.unsplash.com/photo-1600585154526-990dced4db0d"
    elif "chop" in step_text or "cut" in step_text or "slice" in step_text:
        return "https://images.unsplash.com/photo-1586201375761-83865001e31c"
    elif "cook" in step_text or "fry" in step_text or "sauté" in step_text:
        return "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"
    elif "bake" in step_text:
        return "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd"
    else:
        return "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"

def extract_steps_and_times(recipe_text):
    steps = []
    step_pattern = r"Step \d+:.*?(\([^)]+\))"
    matches = re.finditer(step_pattern, recipe_text, re.DOTALL)
    for match in matches:
        step_text = match.group(0)
        time_text = match.group(1).strip("()")
        minutes = 0
        if "minute" in time_text.lower():
            num = re.search(r"\d+", time_text)
            if num:
                minutes = int(num.group())
        elif "second" in time_text.lower():
            num = re.search(r"\d+", time_text)
            if num:
                minutes = int(num.group()) / 60
        image_url = get_placeholder_image(step_text)
        steps.append({"text": step_text, "time_minutes": minutes, "image_url": image_url})
    return steps

def extract_ingredients(recipe_text):
    ingredients = []
    ingredients_pattern = r"Ingredients:.*?(?=(?:Step \d+|Nutritional Information|$))"
    match = re.search(ingredients_pattern, recipe_text, re.DOTALL)
    if match:
        ingredients_text = match.group(0)
        items = re.split(r",\s*|\n", ingredients_text)
        for item in items:
            item = item.strip()
            if item and not item.lower().startswith("ingredients:"):
                ingredients.append(item)
    return ingredients

def generate_shopping_list(ingredients):
    shopping_list = "Shopping List\n\n"
    for item in ingredients:
        shopping_list += f"- {item}\n"
    return shopping_list

def display_timer(step_text, minutes):
    if minutes > 0:
        if st.button(f"<i class='fas fa-clock accent-icon'></i> Start Timer for {step_text[:30]}... ({minutes} min)", key=step_text, help="Start a timer for this step"):
            placeholder = st.empty()
            seconds = int(minutes * 60)
            for i in range(seconds, -1, -1):
                mins = i // 60
                secs = i % 60
                placeholder.markdown(f"<i class='fas fa-stopwatch accent-icon'></i> Timer: {mins:02d}:{secs:02d}", unsafe_allow_html=True)
                time.sleep(1)
            placeholder.markdown("<i class='fas fa-check-circle accent-icon'></i> Timer finished!", unsafe_allow_html=True)

# Streamlit UI setup
st.set_page_config(page_title="AI Recipe Generator", page_icon="🍽️", layout="wide")

# Custom CSS for a modern, fancy, and professional UI
custom_css = """
<style>
    /* General styling */
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #F3F4F6; /* Light Gray */
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        padding: 30px;
    }
    h1, h2, h3 {
        color: #111827; /* Dark Slate */
        font-weight: 700;
    }
    h1 {
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #10B981, #059669); /* Emerald Green gradient */
        color: #F9FAFB; /* Almost White */
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stMultiSelect>div>div>select {
        border: 2px solid #4F46E5; /* Indigo */
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        background-color: #F9FAFB; /* Almost White */
        color: #111827; /* Dark Slate */
    }
    .stMarkdown {
        line-height: 1.8;
        color: #111827; /* Dark Slate */
    }
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: #161D27; /* Darker Charcoal Gray */
        color: #F9FAFB; /* Almost White */
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .sidebar .sidebar-content h2 {
        color: #F9FAFB; /* Almost White */
        font-size: 1.8em;
        margin-bottom: 20px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    .sidebar .sidebar-content .stSelectbox>label, .sidebar .sidebar-content .stMarkdown {
        color: #F9FAFB !important; /* Almost White */
        font-weight: 500;
        font-size: 16px;
    }
    .sidebar .sidebar-content .stSelectbox>div>div>select {
        background-color: #374151; /* Slightly lighter gray for contrast */
        color: #F9FAFB; /* Almost White */
        border: 2px solid #4F46E5; /* Indigo */
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .sidebar .sidebar-content .stSelectbox>div>div>select:hover {
        background-color: #4F46E5; /* Indigo */
        color: #F9FAFB; /* Almost White */
    }
    .stExpander {
        border: 1px solid #d1d8e0;
        border-radius: 8px;
        margin-bottom: 15px;
        background-color: #F9FAFB; /* Almost White */
    }
    .stExpander summary {
        background: linear-gradient(90deg, #F3F4F6, #E5E7EB); /* Light Gray gradient */
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        color: #111827; /* Dark Slate */
    }
    .stSpinner {
        color: #4F46E5; /* Indigo */
    }
    .section-header {
        background: linear-gradient(90deg, #10B981, #059669); /* Emerald Green gradient */
        color: #F9FAFB; /* Almost White */
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 25px;
        font-size: 22px;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    .step-container {
        background-color: #F9FAFB; /* Almost White */
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .step-container:hover {
        transform: translateY(-3px);
    }
    .shopping-list {
        background-color: #E5E7EB; /* Slightly darker gray */
        padding: 20px;
        border-radius: 8px;
        margin-top: 25px;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
    }
    .accent-icon {
        color: #F59E0B; /* Amber */
        margin-right: 8px;
    }
    .download-link {
        color: #F59E0B; /* Amber */
        font-weight: 500;
        text-decoration: none;
    }
    .download-link:hover {
        text-decoration: underline;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Title with icon
st.markdown("<h1><i class='fas fa-utensils accent-icon'></i> AI Recipe Generator</h1>", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.markdown("<h2><i class='fas fa-compass accent-icon'></i> Navigation</h2>", unsafe_allow_html=True)
    page = st.selectbox(
        "Choose an action:", 
        ["Generate Recipe", "Seasonal/Regional Suggestions"], 
        format_func=lambda x: f"{'Recipe Creation' if x == 'Generate Recipe' else 'Seasonal Ideas'} {x}",
        key="nav"
    )

if page == "Generate Recipe":
    with st.container():
        st.markdown("<div class='section-header'><i class='fas fa-cog accent-icon'></i> Recipe Configuration</div>", unsafe_allow_html=True)
        
        # Choose generation type
        st.markdown("<p><i class='fas fa-list accent-icon'></i> Choose recipe generation method:</p>", unsafe_allow_html=True)
        mode = st.radio(
            "",
            ("By Dish Name", "By Ingredients"),
            format_func=lambda x: f"{'Dish Name' if x == 'By Dish Name' else 'Ingredients'} {x}",
            horizontal=True
        )

        # Get user input
        if mode == "By Dish Name":
            st.markdown("<p><i class='fas fa-tag accent-icon'></i> Enter the dish name (e.g., Chocolate Cake, Apple Pie):</p>", unsafe_allow_html=True)
            user_input = st.text_input(
                "",
                placeholder="Type dish name here..."
            )
        else:
            st.markdown("<p><i class='fas fa-seedling accent-icon'></i> Enter the ingredients you have (comma-separated):</p>", unsafe_allow_html=True)
            user_input = st.text_input(
                "",
                placeholder="e.g., flour, sugar, eggs..."
            )

        # Dietary preferences and allergen exclusions
        st.markdown("<div class='section-header'><i class='fas fa-heart accent-icon'></i> Dietary Preferences & Allergens</div>", unsafe_allow_html=True)
        st.markdown("<p><i class='fas fa-leaf accent-icon'></i> Select dietary preferences (optional):</p>", unsafe_allow_html=True)
        dietary_options = st.multiselect(
            "",
            ["Vegan", "Vegetarian", "Gluten-Free", "Dairy-Free", "Keto", "Low-Carb"],
            help="Choose preferences to tailor your recipe."
        )
        st.markdown("<p><i class='fas fa-ban accent-icon'></i> Enter allergens to exclude (comma-separated):</p>", unsafe_allow_html=True)
        allergen_exclusions = st.text_input(
            "",
            placeholder="e.g., peanuts, shellfish"
        )
        st.markdown("<small>Common allergens: peanuts, tree nuts, milk, eggs, fish, shellfish, soy, wheat, sesame</small>", unsafe_allow_html=True)

        # Seasonal and regional preferences
        st.markdown("<div class='section-header'><i class='fas fa-globe accent-icon'></i> Seasonal & Regional Preferences</div>", unsafe_allow_html=True)
        st.markdown("<p><i class='fas fa-sun accent-icon'></i> Select season (optional):</p>", unsafe_allow_html=True)
        season = st.selectbox(
            "",
            ["None", "Spring", "Summer", "Autumn", "Winter"],
            help="Choose a season for seasonal ingredients."
        )
        st.markdown("<p><i class='fas fa-map-marker-alt accent-icon'></i> Select regional cuisine (optional):</p>", unsafe_allow_html=True)
        region = st.selectbox(
            "",
            ["None", "Italian", "Mexican", "Indian", "Japanese", "Mediterranean", "American", "Pakistani", "Thai", "Chinese", "French", "Brazilian"],
            help="Choose a region for authentic cuisine."
        )

        # Construct the prompt based on mode and preferences
        if mode == "By Dish Name":
            prompt = f"Provide a detailed recipe for {user_input}."
        else:
            prompt = f"Create a detailed recipe using the following ingredients: {user_input}."

        # Add dietary, allergen, seasonal, regional, and step-by-step constraints to the prompt
        if dietary_options:
            prompt += f" The recipe must adhere to the following dietary preferences: {', '.join(dietary_options)}."
        if allergen_exclusions:
            prompt += f" Exclude the following allergens: {allergen_exclusions}."
        if season != "None":
            prompt += f" Use ingredients that are in season during {season}."
        if region != "None":
            prompt += f" The recipe should reflect the cuisine of {region}."
        prompt += " Include dish name, a clearly labeled ingredients list with quantities (e.g., 'Ingredients: 2 cups flour, 1 tsp salt'), detailed nutritional information (calories, macronutrients, and micronutrients per serving), and clear, sequential step-by-step cooking instructions with estimated time for each step (e.g., 'Step 1: Preheat oven to 350°F (2 minutes)')."

        # Generate button
        st.markdown("<p><i class='fas fa-magic accent-icon'></i> Generate your recipe:</p>", unsafe_allow_html=True)
        if st.button("Generate Recipe", key="generate"):
            if not user_input.strip():
                st.warning("<i class='fas fa-exclamation-triangle accent-icon'></i> Please enter some input first.", icon="⚠️")
            else:
                with st.spinner("Generating recipe..."):
                    try:
                        start_time = time.time()
                        recipe = asyncio.run(get_recipe(prompt))
                        with st.expander("🍲 Your Recipe", expanded=True):
                            st.markdown(recipe)

                        # Extract and display steps with timers and images
                        steps = extract_steps_and_times(recipe)
                        if steps:
                            st.markdown("<div class='section-header'><i class='fas fa-list-ol accent-icon'></i> Interactive Cooking Steps</div>", unsafe_allow_html=True)
                            for step in steps:
                                with st.container():
                                    st.markdown("<div class='step-container'>", unsafe_allow_html=True)
                                    col1, col2 = st.columns([1, 3])
                                    with col1:
                                        st.image(step['image_url'], caption="Step Visual", width=150)
                                    with col2:
                                        st.markdown(f"**{step['text']}**")
                                        display_timer(step['text'], step['time_minutes'])
                                    st.markdown("</div>", unsafe_allow_html=True)

                        # Generate and display shopping list
                        ingredients = extract_ingredients(recipe)
                        if ingredients:
                            st.markdown("<div class='section-header'><i class='fas fa-shopping-cart accent-icon'></i> Shopping List</div>", unsafe_allow_html=True)
                            with st.container():
                                st.markdown("<div class='shopping-list'>", unsafe_allow_html=True)
                                shopping_list = generate_shopping_list(ingredients)
                                st.markdown(shopping_list)
                                buffer = io.StringIO(shopping_list)
                                shopping_list_bytes = buffer.getvalue().encode()
                                st.download_button(
                                    label="<i class='fas fa-download accent-icon'></i> Download Shopping List",
                                    data=shopping_list_bytes,
                                    file_name="shopping_list.txt",
                                    mime="text/plain",
                                    key="download_shopping"
                                )
                                st.markdown(
                                    "<a href='https://www.instacart.com' target='_blank' class='download-link'><i class='fas fa-truck accent-icon'></i> Order Ingredients via Grocery Delivery</a> "
                                    "(Note: Manually add items to your cart on the service)",
                                    unsafe_allow_html=True
                                )
                                st.markdown("</div>", unsafe_allow_html=True)

                        end_time = time.time()
                        st.success(f"<i class='fas fa-check-circle accent-icon'></i> Recipe generated in {end_time - start_time:.2f} seconds!", icon="✅")
                        st.balloons()

                    except Exception as e:
                        st.error(f"<i class='fas fa-exclamation-circle accent-icon'></i> Error generating recipe: {e}", icon="❌")

elif page == "Seasonal/Regional Suggestions":
    with st.container():
        st.markdown("<div class='section-header'><i class='fas fa-leaf accent-icon'></i> Seasonal & Regional Recipe Suggestions</div>", unsafe_allow_html=True)
        st.markdown("<p><i class='fas fa-sun accent-icon'></i> Select season:</p>", unsafe_allow_html=True)
        season = st.selectbox(
            "",
            ["Spring", "Summer", "Autumn", "Winter"],
            help="Choose a season for seasonal ingredients."
        )
        st.markdown("<p><i class='fas fa-map-marker-alt accent-icon'></i> Select regional cuisine:</p>", unsafe_allow_html=True)
        region = st.selectbox(
            "",
            ["Italian", "Mexican", "Indian", "Japanese", "Mediterranean", "American", "Pakistani", "Thai", "Chinese", "French", "Brazilian"],
            help="Choose a region for authentic cuisine."
        )
        st.markdown("<p><i class='fas fa-leaf accent-icon'></i> Select dietary preferences (optional):</p>", unsafe_allow_html=True)
        dietary_options = st.multiselect(
            "",
            ["Vegan", "Vegetarian", "Gluten-Free", "Dairy-Free", "Keto", "Low-Carb"],
            help="Choose preferences to tailor your suggestions."
        )
        st.markdown("<p><i class='fas fa-ban accent-icon'></i> Enter allergens to exclude (comma-separated):</p>", unsafe_allow_html=True)
        allergen_exclusions = st.text_input(
            "",
            placeholder="e.g., peanuts, shellfish"
        )
        st.markdown("<small>Common allergens: peanuts, tree nuts, milk, eggs, fish, shellfish, soy, wheat, sesame</small>", unsafe_allow_html=True)

        # Construct prompt for suggestions
        suggestion_prompt = f"Suggest 3 recipes that use ingredients in season during {season} and reflect the cuisine of {region}."
        if dietary_options:
            suggestion_prompt += f" The recipes must adhere to the following dietary preferences: {', '.join(dietary_options)}."
        if allergen_exclusions:
            suggestion_prompt += f" Exclude the following allergens: {allergen_exclusions}."
        suggestion_prompt += " For each recipe, include dish name, a brief description, and a short list of key seasonal ingredients."

        st.markdown("<p><i class='fas fa-lightbulb accent-icon'></i> Discover recipes:</p>", unsafe_allow_html=True)
        if st.button("Discover Recipes", key="suggestions"):
            with st.spinner("Generating suggestions..."):
                try:
                    suggestions = asyncio.run(get_recipe(suggestion_prompt))
                    with st.expander("📜 Recipe Suggestions", expanded=True):
                        st.markdown(suggestions)
                except Exception as e:
                    st.error(f"<i class='fas fa-exclamation-circle accent-icon'></i> Error generating suggestions: {e}", icon="❌")