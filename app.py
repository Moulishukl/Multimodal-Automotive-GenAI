import streamlit as st
from PIL import Image
import io
import requests
import google.generativeai as genai
from datetime import datetime
import uuid
import time
import numpy as np
from sentence_transformers import SentenceTransformer

# ============================================
# CONFIGURATION
# ============================================

GEMINI_API_KEY = "your-gemini-api-key-here"  # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# ============================================
# SIMPLE VECTOR DATABASE (No FAISS needed)
# ============================================

class SimpleVectorDB:
    """Simple vector database using numpy - no extra packages needed"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = []
        self.metadata = []
        self.ids = []
    
    def add(self, design_id, text, metadata):
        """Add a design to the database"""
        embedding = self.model.encode([text])[0]
        self.embeddings.append(embedding)
        self.metadata.append(metadata)
        self.ids.append(design_id)
    
    def search(self, query_text, n_results=3):
        """Search for similar designs using cosine similarity"""
        if len(self.embeddings) == 0:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query_text])[0]
        
        # Calculate cosine similarity
        similarities = []
        for i, emb in enumerate(self.embeddings):
            # Cosine similarity
            similarity = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
            similarities.append(similarity)
        
        # Get top n results
        indices = np.argsort(similarities)[::-1][:n_results]
        
        results = []
        for idx in indices:
            results.append({
                'id': self.ids[idx],
                'metadata': self.metadata[idx],
                'similarity': float(similarities[idx])
            })
        
        return results
    
    def count(self):
        return len(self.embeddings)

# Initialize vector database
@st.cache_resource
def init_vector_db():
    return SimpleVectorDB()

# ============================================
# CORE FUNCTION: Generate Complete Car Design
# ============================================

def generate_complete_car_design(user_input):
    """Use Gemini to design a complete car with detailed features"""
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are a senior automotive design engineer at a major car manufacturer.
    
    Based on the user's request: "{user_input}"
    
    Design a complete car with the following DETAILED specifications.
    Output in this exact format:

    === CAR DESIGN SPECIFICATION ===
    
    **Car Name:** [Creative name for this model]
    
    **Category:** [e.g., Hypercar, SUV, Sedan, Electric Sports Car, Luxury GT]
    
    **Exterior Design:**
    - Body Style: [Detailed description]
    - Dimensions: [Length, width, height characteristics]
    - Color & Finish: [Specific color, paint type]
    - Key Design Elements: [Grille, headlights, taillights, spoiler]
    - Aerodynamics: [Special features]
    
    **Interior Design:**
    - Seating: [Configuration, materials]
    - Dashboard & Controls: [Screen size, buttons, steering wheel]
    - Technology Features: [Infotainment, displays]
    - Comfort Features: [Climate control, sound system]
    - Materials: [Leather, Alcantara, carbon fiber]
    
    **Performance Specifications:**
    - Powertrain: [Engine type, electric motors]
    - Horsepower: [Estimated power output]
    - Acceleration: [0-60 mph time]
    - Top Speed: [Estimated top speed]
    - Range/Fuel Economy: [EV range or MPG]
    - Drivetrain: [AWD, RWD, FWD]
    
    **Unique Features:**
    - [Feature 1]
    - [Feature 2]
    - [Feature 3]
    
    **Target Audience:** [Who would buy this car]
    
    **Price Range:** [Estimated cost]
    
    === IMAGE GENERATION PROMPT ===
    [Write a detailed 2-3 sentence prompt for generating an image of this exact car design]
    """
    
    response = model.generate_content(prompt)
    return response.text

def extract_image_prompt(full_design):
    """Extract the image generation prompt from the full design"""
    if "=== IMAGE GENERATION PROMPT ===" in full_design:
        parts = full_design.split("=== IMAGE GENERATION PROMPT ===")
        if len(parts) > 1:
            lines = parts[1].strip().split('\n')
            for line in lines:
                if line.strip() and not line.startswith('-'):
                    return line.strip()
    return "A futuristic car design, photorealistic, 4k quality"

# ============================================
# IMAGE GENERATION
# ============================================

def generate_car_image(prompt):
    """Generate image based on the detailed design prompt"""
    
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
    params = {"width": 1024, "height": 768, "nologo": "true", "model": "flux"}
    
    try:
        response = requests.get(url, params=params, timeout=60)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except Exception as e:
        st.warning(f"Image generation attempt failed: {str(e)[:50]}")
    
    # Create placeholder with text
    placeholder = Image.new('RGB', (1024, 768), color=(30, 30, 50))
    return placeholder

# ============================================
# STREAMLIT UI
# ============================================

st.set_page_config(page_title="Automotive Design Studio", layout="wide")

# Initialize vector DB
vector_db = init_vector_db()

st.title("🚗 AI Automotive Design Studio")
st.caption("Describe any car - Get a COMPLETE design with specifications + High-quality visualization")

# Sidebar
with st.sidebar:
    st.markdown("### 🔍 Search Design Library")
    search_query = st.text_input("Find similar designs:", placeholder="e.g., electric sports car")
    
    if st.button("Search"):
        if search_query:
            with st.spinner("Searching..."):
                results = vector_db.search(search_query, n_results=5)
                if results:
                    st.session_state['search_results'] = results
                    st.session_state['show_search'] = True
                    st.success(f"Found {len(results)} similar designs!")
                else:
                    st.info("No similar designs found yet. Generate some designs first!")
    
    if st.button("Clear Search Results"):
        st.session_state['show_search'] = False
        st.session_state['search_results'] = []
    
    st.markdown("---")
    st.markdown(f"### 📊 Design Library")
    st.markdown(f"**Total designs:** {vector_db.count()}")
    
    st.markdown("---")
    st.markdown("### 📝 Example Prompts")
    st.markdown("""
    **Try these:**
    - "Futuristic electric hypercar for billionaires"
    - "Luxury electric SUV for families with 3 rows"
    - "Affordable compact car for city driving"
    - "Track-focused sports car with hybrid engine"
    - "Luxury sedan targeting business executives"
    - "Vintage muscle car restomod with electric powertrain"
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Be specific about features
    - Mention target audience
    - Include performance expectations
    - Describe the interior and exterior
    """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎨 Describe Your Dream Car")
    
    user_prompt = st.text_area(
        "What kind of car do you want to design?",
        value="A futuristic electric hypercar with gullwing doors, active aerodynamics, 2000+ horsepower, and a luxurious carbon fiber interior. Target audience is billionaires who want the ultimate status symbol.",
        height=150
    )
    
    if st.button("🔨 DESIGN THIS CAR", type="primary", use_container_width=True):
        if user_prompt:
            with st.spinner("🏗️ Designing your car from scratch (this may take 10-15 seconds)..."):
                full_design = generate_complete_car_design(user_prompt)
                st.session_state['full_design'] = full_design
                
                # Extract image prompt
                image_prompt = extract_image_prompt(full_design)
                st.session_state['image_prompt'] = image_prompt
            
            with st.spinner("🎨 Rendering the car design..."):
                img = generate_car_image(image_prompt)
                if img:
                    st.session_state['generated_img'] = img
                    st.session_state['success'] = True
                    
                    # Save to vector database
                    design_id = str(uuid.uuid4())[:8]
                    vector_db.add(
                        design_id=design_id,
                        text=f"User: {user_prompt}\nDesign: {full_design[:1500]}",
                        metadata={
                            "user_prompt": user_prompt,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "design_id": design_id,
                            "car_name": full_design.split("**Car Name:**")[1].split("\n")[0].strip() if "**Car Name:**" in full_design else "Unknown"
                        }
                    )
                    st.session_state['design_id'] = design_id
                    st.success(f"✅ Design saved to library! ID: {design_id}")

with col2:
    st.subheader("📋 Generated Car Design")
    
    if st.session_state.get('success') and st.session_state.get('generated_img'):
        # Show the image
        st.image(st.session_state['generated_img'], use_container_width=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Save Image"):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.session_state['generated_img'].save(f"car_design_{timestamp}.png")
                st.success("Image saved!")
        
        with col_b:
            if st.button("🔍 Find Similar Designs"):
                if st.session_state.get('full_design'):
                    results = vector_db.search(st.session_state['full_design'][:500], n_results=3)
                    if results:
                        st.session_state['search_results'] = results
                        st.session_state['show_search'] = True
                        st.rerun()
        
        # Show the complete design specification
        if st.session_state.get('full_design'):
            with st.expander("📝 View Complete Car Design Specification", expanded=True):
                st.markdown(st.session_state['full_design'])
    
    elif st.session_state.get('show_search') and st.session_state.get('search_results'):
        st.markdown("### 🔍 Similar Designs Found")
        for i, result in enumerate(st.session_state['search_results']):
            with st.expander(f"Design {i+1} (Match: {result['similarity']*100:.1f}%)"):
                st.markdown(f"**User asked:** {result['metadata'].get('user_prompt', 'Unknown')[:200]}...")
                st.markdown(f"**Date:** {result['metadata'].get('timestamp', 'Unknown')}")
                st.markdown(f"**ID:** {result['metadata'].get('design_id', 'Unknown')}")
                if result['metadata'].get('car_name'):
                    st.markdown(f"**Car Name:** {result['metadata']['car_name']}")
    else:
        st.info("✨ No design generated yet. Describe your dream car and click 'DESIGN THIS CAR'!")

# Footer
st.markdown("---")
st.markdown("🎓 *Multimodal GenAI Project - Complete Automotive Design Studio with Vector Search*")