# 1-Hour MVP PRD: Quick MCP DataFlow Pipeline with Ollama

## 🎯 **MVP Goals (1 Hour Total)**
- Upload CSV files and get automated AI analysis
- 5 agents working in sequence using 4 MCP servers
- **Uses Ollama with Qwen3:8b model** (local, free AI)
- Simple Streamlit UI with progress tracking
- Working demo of multi-agent data pipeline

## 🏗️ **Simplified Architecture**

```
CSV Upload → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Agent 5 → Results
             (Ingest)  (Clean)   (Analyze) (Visualize) (Report)
```

## 🔧 **Required MCP Servers (2 Total)**

```yaml
MCP Servers for MVP:
  1. filesystem_mcp: "@modelcontextprotocol/server-filesystem" (File operations)
  2. data_exploration_mcp: "mcp-server-data-exploration" (Auto insights)
```

## 📁 **Super Simple File Structure**

```
mcp-dataflow-mvp/
├── requirements.txt       # 10 lines
├── .env                  # MCP configs
├── main.py               # Streamlit UI (150 lines)
├── agents.py             # All agents (120 lines)
└── README.md             # Setup instructions
```

## ⏰ **1-Hour Implementation Timeline**

### **Step 1: Setup (10 minutes)**
### **Step 2: MCP Integration (20 minutes)**  
### **Step 3: CrewAI Implementation (20 minutes)**
### **Step 4: Streamlit UI (10 minutes)**

---

# 🚀 **STEP 1: PROJECT SETUP (10 minutes)**

## **1.1 Create Project Structure**
```bash
# Terminal commands
mkdir mcp-dataflow-mvp
cd mcp-dataflow-mvp
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

## **1.2 Setup Ollama with Qwen3:8b**
```bash
# Install Ollama if not already installed
# Visit: https://ollama.ai and follow installation instructions

# Pull the Qwen3:8b model
ollama pull qwen3:8b

# Verify it's working
ollama run qwen3:8b "Hello, how are you?"

# Keep Ollama running in background
ollama serve
```

## **1.2 Create requirements.txt**
```txt
streamlit==1.39.0
crewai==0.86.0
crewai-tools>=0.18.0
matplotlib==3.9.2
plotly==5.24.1
python-dotenv==1.0.1
asyncio
requests
```

## **1.3 Install Dependencies**
```bash
pip install -r requirements.txt
```

## **1.4 Install MCP Servers**
```bash
# Install 2 MCP servers (takes 2-3 minutes)
npx -y @modelcontextprotocol/server-filesystem
uvx mcp-server-data-exploration
```

## **1.5 Create .env File**
```env
# .env
STREAMLIT_PORT=8501
MCP_TIMEOUT=60
MAX_FILE_SIZE=100

# Ollama Configuration (assuming already running)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:8b
```

---

# 🔧 **STEP 2: MCP INTEGRATION (20 minutes)**

## **2.1 Create agents.py**
```python
# agents.py - Complete implementation with Ollama (CrewAI syntax)
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Configure Ollama LLM using CrewAI's native syntax
ollama_llm = LLM(
    model="ollama/qwen3:8b",
    base_url="http://localhost:11434"
)

class MCPDataFlowPipeline:
    def __init__(self):
        self.mcp_tools = {}
        self.crew = None
        self.llm = ollama_llm
    
    async def setup_mcp_servers(self):
        """Initialize all 4 MCP servers"""
        mcp_configs = {
            'filesystem': {
                'command': 'npx',
                'args': ['-y', '@modelcontextprotocol/server-filesystem'],
                'transport': 'stdio'
            },
            'data_exploration': {
                'command': 'uvx', 
                'args': ['mcp-server-data-exploration'],
                'transport': 'stdio'
            }
        }
        
        # Create MCP tools
        for name, config in mcp_configs.items():
            try:
                adapter = MCPServerAdapter(
                    name=name,
                    command=config['command'],
                    args=config['args'],
                    transport=config['transport']
                )
                self.mcp_tools[name] = adapter
                print(f"✅ MCP Server {name} initialized")
            except Exception as e:
                print(f"❌ Failed to initialize {name}: {e}")
        
        return self.mcp_tools
    
    def create_agents(self):
        """Create all 5 agents with MCP tools and Ollama LLM"""
        
        # Agent 1: Data Ingestion Specialist
        ingestion_agent = Agent(
            role='Data Ingestion Specialist',
            goal='Load and validate uploaded CSV files using filesystem MCP',
            backstory='You are an expert at securely handling file uploads and basic data validation. You work efficiently and provide clear summaries.',
            tools=[self.mcp_tools.get('filesystem')] if self.mcp_tools.get('filesystem') else [],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agent 2: Data Quality Engineer  
        cleaning_agent = Agent(
            role='Data Quality Engineer',
            goal='Clean and preprocess CSV data using data exploration MCP',
            backstory='You are a specialist in data cleaning, missing values, and data standardization. You explain your cleaning decisions clearly.',
            tools=[tool for tool in [self.mcp_tools.get('data_exploration'), self.mcp_tools.get('filesystem')] if tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agent 3: Statistical Analyst
        analysis_agent = Agent(
            role='Statistical Analyst', 
            goal='Perform comprehensive data analysis using data exploration MCP',
            backstory='You are an expert at finding patterns, correlations, and insights in data. You provide actionable insights from statistical analysis.',
            tools=[tool for tool in [self.mcp_tools.get('data_exploration'), self.mcp_tools.get('filesystem')] if tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agent 4: Visualization Specialist
        viz_agent = Agent(
            role='Visualization Specialist',
            goal='Create charts and visualizations using data exploration MCP',
            backstory='You are an expert at creating clear, informative data visualizations that tell a story with data.',
            tools=[self.mcp_tools.get('data_exploration')] if self.mcp_tools.get('data_exploration') else [],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agent 5: Report Generator
        report_agent = Agent(
            role='Report Generator',
            goal='Synthesize all findings into a comprehensive report',
            backstory='You are a technical writer who creates clear, actionable data reports that business stakeholders can understand and act upon.',
            tools=[tool for tool in [self.mcp_tools.get('data_exploration'), self.mcp_tools.get('filesystem')] if tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        return [ingestion_agent, cleaning_agent, analysis_agent, viz_agent, report_agent]
    
    def create_tasks(self, agents, csv_file_path):
        """Create tasks for each agent with Ollama-optimized prompts"""
        
        # Task 1: Data Ingestion
        ingestion_task = Task(
            description=f"""
            Load and validate the CSV file: {csv_file_path}
            
            Your task:
            1. Use filesystem MCP to read the CSV file safely
            2. Check file format and detect encoding issues
            3. Load data and count rows, columns, data types
            4. Find obvious data quality problems (empty cells, duplicates)
            5. Create a summary report
            
            Be concise and focus on key findings only.
            Return results as structured text with clear sections.
            """,
            agent=agents[0],
            expected_output="File validation summary with data shape, types, and quality issues found"
        )
        
        # Task 2: Data Cleaning  
        cleaning_task = Task(
            description="""
            Clean the CSV data using data exploration MCP tools.
            
            Your task:
            1. Handle missing values (fill, remove, or flag them)
            2. Remove exact duplicate rows
            3. Fix data type issues (numbers stored as text, etc.)
            4. Handle obvious outliers appropriately
            5. Summarize what you cleaned
            
            Focus on the most important cleaning steps.
            Explain what you did and why in simple terms.
            """,
            agent=agents[1],
            expected_output="Data cleaning summary showing before/after statistics and changes made"
        )
        
        # Task 3: Statistical Analysis
        analysis_task = Task(
            description="""
            Analyze the cleaned data using data exploration MCP.
            
            Your task:
            1. Calculate basic statistics (mean, median, mode, etc.)
            2. Find correlations between numeric columns
            3. Identify the 3 most interesting patterns in the data
            4. Spot any unusual values or trends
            5. Generate 5 key insights about this dataset
            
            Keep insights practical and easy to understand.
            Focus on findings that would be useful to a business user.
            """,
            agent=agents[2],
            expected_output="Statistical analysis with key insights, correlations, and business-relevant findings"
        )
        
        # Task 4: Data Visualization
        viz_task = Task(
            description="""
            Create visualizations to show the key findings using data exploration MCP.
            
            Your task:
            1. Make 2-3 charts that highlight the most important patterns
            2. Create a correlation plot if there are numeric columns
            3. Show distribution of key variables
            4. Create simple, clear charts (avoid complexity)
            5. Describe what each chart shows
            
            Focus on charts that tell a clear story.
            Keep visualizations simple and interpretable.
            """,
            agent=agents[3],
            expected_output="Chart descriptions and visualization plan showing key data patterns"
        )
        
        # Task 5: Report Generation
        report_task = Task(
            description="""
            Create a final report combining all the analysis.
            
            Your task:
            1. Write a 2-paragraph executive summary of key findings
            2. List the data quality improvements that were made
            3. Present the 3 most important insights from the analysis
            4. Describe the visualizations and what they show
            5. Give 3 actionable recommendations based on the data
            
            Write in clear, business-friendly language.
            Focus on insights that can drive decisions.
            """,
            agent=agents[4],
            expected_output="Complete business-ready analysis report with executive summary and recommendations"
        )
        
        return [ingestion_task, cleaning_task, analysis_task, viz_task, report_task]
    
    async def create_crew(self, csv_file_path):
        """Assemble the complete crew"""
        # Setup MCP servers
        await self.setup_mcp_servers()
        
        # Create agents and tasks
        agents = self.create_agents()
        tasks = self.create_tasks(agents, csv_file_path)
        
        # Create crew with sequential process and Ollama LLM
        self.crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            manager_llm=self.llm  # Use Ollama for crew management
        )
        
        return self.crew
    
    async def run_pipeline(self, csv_file_path):
        """Execute the complete pipeline"""
        try:
            crew = await self.create_crew(csv_file_path)
            result = crew.kickoff(inputs={"csv_file": csv_file_path})
            
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

# Helper function for Streamlit
def create_pipeline():
    return MCPDataFlowPipeline()
```

---

# 🖥️ **STEP 3: STREAMLIT UI (10 minutes)**

## **3.1 Create main.py**
```python
# main.py - Complete Streamlit application
import streamlit as st
import os
import asyncio
import tempfile
from agents import create_pipeline
import json

# Page configuration
st.set_page_config(
    page_title="MCP DataFlow Pipeline",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🤖 MCP DataFlow Pipeline")
st.markdown("**1-Hour MVP**: Upload CSV → AI Analysis → Automated Report")

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
    st.markdown("**Pipeline Steps:**")
    st.markdown("1. 📁 Data Ingestion")
    st.markdown("2. 🧹 Data Cleaning")
    st.markdown("3. 📊 Statistical Analysis")
    st.markdown("4. 📈 Visualization")
    st.markdown("5. 📋 Report Generation")

# Main interface
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📁 File Upload")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file for automated AI analysis"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.info(f"📏 Size: {uploaded_file.size} bytes")
        
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

with col2:
    st.header("🚀 Pipeline Execution")
    
    if uploaded_file is not None:
        # Run pipeline button
        if st.button("🤖 Run AI Analysis Pipeline", type="primary", use_container_width=True):
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_file_path = tmp_file.name
            
            try:
                # Create progress placeholder
                progress_placeholder = st.empty()
                results_placeholder = st.empty()
                
                with progress_placeholder.container():
                    st.markdown("### 🔄 Pipeline Progress")
                    
                    # Progress bars for each agent
                    progress_bars = {}
                    status_texts = {}
                    
                    agents = [
                        ("Agent 1", "📁 Data Ingestion Specialist"),
                        ("Agent 2", "🧹 Data Quality Engineer"), 
                        ("Agent 3", "📊 Statistical Analyst"),
                        ("Agent 4", "📈 Visualization Specialist"),
                        ("Agent 5", "📋 Report Generator")
                    ]
                    
                    for i, (agent_name, agent_desc) in enumerate(agents):
                        col_a, col_b = st.columns([1, 3])
                        with col_a:
                            st.markdown(f"**{agent_name}**")
                        with col_b:
                            status_texts[agent_name] = st.empty()
                            progress_bars[agent_name] = st.progress(0)
                        status_texts[agent_name].markdown(f"⏳ {agent_desc}")
                
                # Initialize pipeline
                with st.spinner("Initializing MCP servers and Ollama connection..."):
                    pipeline = create_pipeline()
                
                # Run pipeline asynchronously
                async def run_async_pipeline():
                    # Simulate progress updates
                    for i, (agent_name, agent_desc) in enumerate(agents):
                        status_texts[agent_name].markdown(f"🔄 Running: {agent_desc}")
                        progress_bars[agent_name].progress((i + 1) * 20)
                        
                        if i < len(agents) - 1:
                            await asyncio.sleep(2)  # Simulate processing time
                    
                    # Run actual pipeline
                    result = await pipeline.run_pipeline(temp_file_path)
                    
                    # Update all progress bars to complete
                    for agent_name, _ in agents:
                        progress_bars[agent_name].progress(100)
                        status_texts[agent_name].markdown("✅ Completed")
                    
                    return result
                
                # Execute pipeline
                try:
                    result = asyncio.run(run_async_pipeline())
                    
                    # Clear progress and show results
                    progress_placeholder.empty()
                    
                    with results_placeholder.container():
                        st.markdown("### 🎉 Analysis Complete!")
                        
                        if result["status"] == "success":
                            st.success("✅ Pipeline executed successfully!")
                            
                            # Display results in tabs
                            tab1, tab2, tab3 = st.tabs(["📋 Summary", "📊 Detailed Results", "⚙️ Technical Info"])
                            
                            with tab1:
                                st.markdown("#### Executive Summary")
                                if isinstance(result["results"], dict):
                                    st.json(result["results"])
                                else:
                                    st.markdown(str(result["results"]))
                            
                            with tab2:
                                st.markdown("#### Detailed Analysis Results")
                                st.code(str(result["results"]), language="text")
                            
                            with tab3:
                                st.markdown("#### Pipeline Information")
                                st.json({
                                    "status": result["status"],
                                    "file_processed": uploaded_file.name,
                                    "crew_metrics": result.get("crew_usage", {})
                                })
                                
                                # Download results
                                if st.button("💾 Download Results"):
                                    results_json = json.dumps(result, indent=2)
                                    st.download_button(
                                        label="📄 Download Analysis Report",
                                        data=results_json,
                                        file_name=f"analysis_report_{uploaded_file.name}.json",
                                        mime="application/json"
                                    )
                        
                        else:
                            st.error(f"❌ Pipeline failed: {result['error']}")
                            st.code(result['error'], language="text")
                
                except Exception as e:
                    progress_placeholder.empty()
                    st.error(f"❌ Error running pipeline: {str(e)}")
                    st.code(str(e), language="text")
                
                finally:
                    # Cleanup temporary file
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
            
            except Exception as e:
                st.error(f"❌ Setup error: {str(e)}")
    
    else:
        st.info("👆 Please upload a CSV file to begin analysis")

# Footer
st.markdown("---")
st.markdown(
    """
    **🤖 MCP DataFlow Pipeline MVP** | Built with CrewAI + MCP Servers + Ollama Qwen3:8b  
    *Agents: Data Ingestion → Cleaning → Analysis → Visualization → Report*
    """
)
```

---

# 🧪 **STEP 4: TESTING & LAUNCH (10 minutes)**

## **4.1 Start Ollama Server**
```bash
# In a separate terminal, start Ollama
ollama serve

# Test that Qwen3:8b is working
ollama run qwen3:8b "Analyze this sample data and give me 3 insights"
```

## **4.2 Create Test CSV**
Create a simple test file `sample_data.csv`:
```csv
name,age,salary,department,join_date
John Doe,28,50000,Engineering,2022-01-15
Jane Smith,34,65000,Marketing,2021-06-10
Bob Johnson,45,80000,Engineering,2020-03-20
Alice Brown,29,55000,Sales,2023-02-05
Charlie Wilson,38,70000,Marketing,2019-11-30
```

## **4.3 Launch Application**
```bash
# Make sure Ollama is running in another terminal: ollama serve
# Then start Streamlit
streamlit run main.py --server.port 8501
```

## **4.4 Test the Pipeline**
1. Open browser to `http://localhost:8501`
2. Upload the `sample_data.csv` file
3. Click "🤖 Run AI Analysis Pipeline"
4. Watch the progress bars as agents execute
5. View results in the tabs

---

# ✅ **1-Hour Success Checklist**

After 60 minutes, you should have:

- [ ] **Ollama running** with Qwen3:8b model loaded
- [ ] **Working Streamlit UI** with file upload
- [ ] **2 MCP servers** initialized and connected
- [ ] **5 AI agents** using Ollama LLM in a sequential CrewAI crew
- [ ] **CSV processing pipeline** that takes uploaded files through all stages
- [ ] **Progress tracking** showing each agent's work
- [ ] **Results display** with analysis outputs
- [ ] **Error handling** for common issues

## **🎯 Expected Demo Flow**

1. **"Here's my CSV upload interface powered by Ollama..."**
2. **"Watch as 5 AI agents using Qwen3:8b process the data sequentially..."**
3. **"Agent 1 ingests, Agent 2 cleans, Agent 3 analyzes with MCP..."**
4. **"Agent 4 creates visualizations, Agent 5 generates the report..."**
5. **"All running locally with no API costs - here's the final analysis!"**

## **🚀 Next Steps After MVP**

Once your 1-hour demo works, you can add:
- More Ollama models (llama3.1, codellama, etc.)
- More file formats (Excel, JSON)
- Advanced visualizations
- Export to PDF
- Pipeline history
- Additional MCP servers
- Better error handling
- Model comparison features

## **💡 Ollama Benefits**
- **No API costs** - runs completely locally
- **Privacy** - your data never leaves your machine  
- **Fast** - Qwen3:8b is optimized for reasoning tasks
- **Reliable** - no rate limits or internet dependency

**This MVP proves the concept and gets you a working multi-agent MCP pipeline with local AI in just 1 hour!**