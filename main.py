# main.py - Dynamic Chat Interface with CrewAI
import warnings
import streamlit as st
import os
import asyncio
import tempfile
from agents import create_pipeline
import json
import uuid

# Suppress Pydantic deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")

# Page configuration
st.set_page_config(
    page_title="MCP DataFlow Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "file_path" not in st.session_state:
    st.session_state.file_path = None
if "pipeline" not in st.session_state:
    st.session_state.pipeline = None

# Title and description
st.title("🤖 MCP DataFlow Chat")
st.markdown("**Dynamic AI Analysis**: Chat with your data using intelligent agents")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Ollama Status Check
    st.markdown("**🤖 Ollama Status:**")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            st.success("✅ Ollama Running (Qwen3:8b)")
        else:
            st.error("❌ Ollama Not Responding")
    except:
        st.error("❌ Ollama Not Running")
        st.info("Run: `ollama serve` in terminal")
    
    st.markdown("**MCP Servers Status:**")
    st.success("✅ Filesystem MCP")
    st.success("✅ Data Exploration MCP")
    
    st.markdown("---")
    st.markdown("**Available Agents:**")
    st.markdown("📁 Data Ingestion Specialist")
    st.markdown("🧹 Data Quality Engineer")
    st.markdown("📊 Statistical Analyst")
    st.markdown("📈 Visualization Specialist")
    st.markdown("📋 Report Generator")
    
    st.markdown("---")
    st.markdown("**💡 Try these prompts:**")
    st.markdown("• 'Upload and analyze this data'")
    st.markdown("• 'Clean the dataset and find insights'")
    st.markdown("• 'Create visualizations for key patterns'")
    st.markdown("• 'Generate a comprehensive report'")
    st.markdown("• 'What are the main trends in this data?'")

# File upload section
st.header("📁 Data Upload")
uploaded_file = st.file_uploader(
    "Choose a CSV file to analyze",
    type=['csv'],
    help="Upload a CSV file to start chatting with your data"
)

if uploaded_file is not None:
    # Save file if it's new
    if (st.session_state.uploaded_file is None or 
        st.session_state.uploaded_file.name != uploaded_file.name):
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            st.session_state.file_path = tmp_file.name
            st.session_state.uploaded_file = uploaded_file
        
        # Initialize pipeline
        with st.spinner("Initializing AI agents..."):
            st.session_state.pipeline = create_pipeline()
        
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Preview data
        try:
            # Read file content for preview
            file_content = uploaded_file.read()
            uploaded_file.seek(0)  # Reset file pointer
            
            # Show first few lines as preview
            lines = file_content.decode('utf-8').split('\n')[:5]
            preview_data = '\n'.join(lines)
            
            st.markdown("**Data Preview:**")
            st.code(preview_data, language='csv')
            st.caption(f"Showing first 5 lines of {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Chat interface
st.header("💬 Chat with Your Data")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your data..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check if file is uploaded
    if st.session_state.file_path is None:
        st.error("❌ Please upload a CSV file first!")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "I need a CSV file to analyze. Please upload one using the file uploader above."
        })
    else:
        # Display assistant message
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 Thinking...")
            
            try:
                # Create dynamic task based on user input
                dynamic_task = create_dynamic_task(prompt, st.session_state.file_path)
                
                # Run the task
                with st.spinner("🤖 Processing with AI agents..."):
                    result = asyncio.run(run_dynamic_task(
                        st.session_state.pipeline, 
                        dynamic_task
                    ))
                
                # Display result
                if result["status"] == "success":
                    message_placeholder.markdown(result["results"])
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result["results"]
                    })
                else:
                    error_msg = f"❌ Error: {result['error']}"
                    message_placeholder.markdown(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                    
            except Exception as e:
                error_msg = f"❌ Error processing request: {str(e)}"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

def create_dynamic_task(user_prompt, file_path):
    """Create a dynamic task based on user input"""
    
    # Analyze user intent and create appropriate task
    task_description = f"""
    User Request: {user_prompt}
    File: {file_path}
    
    Based on the user's request, determine which agents and tools are needed and execute the analysis.
    
    Common request types:
    - "Upload and analyze" → Use all agents in sequence
    - "Clean the data" → Use Data Quality Engineer
    - "Find insights" → Use Statistical Analyst
    - "Create visualizations" → Use Visualization Specialist
    - "Generate report" → Use Report Generator
    - "What are the trends?" → Use Statistical Analyst + Visualization Specialist
    
    Respond in a helpful, conversational manner. Explain what you're doing and provide actionable insights.
    """
    
    return {
        "description": task_description,
        "file_path": file_path,
        "user_prompt": user_prompt
    }

async def run_dynamic_task(pipeline, task):
    """Run a dynamic task using the appropriate agents"""
    try:
        # Create a flexible crew that can adapt to the task
        crew = await pipeline.create_flexible_crew(task)
        result = crew.kickoff(inputs={"task": task})
        
        return {
            "status": "success",
            "results": result,
            "crew_usage": crew.usage_metrics if hasattr(crew, 'usage_metrics') else {}
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": str(e),
            "results": None
        }

# Footer
st.markdown("---")
st.markdown(
    """
    **🤖 MCP DataFlow Chat** | Built with CrewAI + MCP Servers + Ollama Qwen3:8b  
    *Dynamic AI agents that adapt to your conversation*
    """
) 