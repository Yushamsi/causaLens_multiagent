# 🤖 MCP DataFlow Chat

**Dynamic AI Analysis Platform**: A sophisticated chat-based data analysis system powered by CrewAI, MCP servers, and Ollama

## 🎯 **Repository Overview**

This repository contains a **dynamic AI-powered data analysis platform** that allows users to upload CSV files and chat naturally with their data. The system uses intelligent agents that automatically select the most appropriate analysis tools based on user requests.

### **Key Features**
- **📁 CSV File Upload & Processing** - Secure file handling with validation
- **🤖 5 Intelligent AI Agents** - Specialized agents for different analysis tasks
- **💬 Natural Language Chat Interface** - Conversational data analysis
- **🔧 MCP Server Integration** - Model Context Protocol for enhanced capabilities
- **🆓 Local AI Processing** - Uses Ollama with Qwen3:8b (no API costs)
- **📊 Dynamic Agent Selection** - Only uses the agents you need for each request

## 🏗️ **Architecture**

```
User Upload → Streamlit UI → Agent Router → Specialized Agents → MCP Servers → Results
     ↓              ↓              ↓              ↓              ↓           ↓
  CSV File    Chat Interface   Smart Logic    CrewAI Agents   File/Data   Insights
```

### **Technology Stack**
- **Frontend**: Streamlit (Python web framework)
- **AI Framework**: CrewAI (multi-agent orchestration)
- **Local AI**: Ollama with Qwen3:8b model
- **Data Processing**: MCP (Model Context Protocol) servers
- **Language**: Python 3.12 (required for compatibility)

## 🔧 **Current MCP Server Configuration**

The system currently uses **2 MCP servers** for enhanced data processing:

```yaml
Active MCP Servers:
  1. filesystem_mcp: "@modelcontextprotocol/server-filesystem" 
     - Purpose: File operations, CSV reading, data validation
     - Status: ✅ Working
     - Tools: 14 filesystem-related tools
  
  2. data_exploration_mcp: "mcp-server-data-exploration"
     - Purpose: Automated data analysis and insights
     - Status: ⚠️ Requires installation
     - Tools: Statistical analysis, pattern recognition
```

## 🤖 **The 5 Intelligent Agents**

Each agent is specialized for specific data analysis tasks:

1. **📁 Data Ingestion Specialist**
   - **Purpose**: Loads and validates CSV files
   - **MCP Access**: filesystem MCP
   - **Capabilities**: File validation, data type detection, quality assessment

2. **🧹 Data Quality Engineer**
   - **Purpose**: Cleans and preprocesses data
   - **MCP Access**: data_exploration MCP
   - **Capabilities**: Missing value handling, outlier detection, data standardization

3. **📊 Statistical Analyst**
   - **Purpose**: Performs comprehensive statistical analysis
   - **MCP Access**: data_exploration MCP
   - **Capabilities**: Correlation analysis, trend identification, statistical testing

4. **📈 Visualization Specialist**
   - **Purpose**: Creates compelling data visualizations
   - **MCP Access**: data_exploration MCP
   - **Capabilities**: Chart creation, interactive visualizations, storytelling

5. **📋 Report Generator**
   - **Purpose**: Synthesizes findings into comprehensive reports
   - **MCP Access**: None (focuses on report writing)
   - **Capabilities**: Executive summaries, technical documentation, recommendations

## 🚀 **Quick Setup Guide**

### **Prerequisites**
- **Python 3.12 or below** (⚠️ Python 3.13+ not compatible with dependencies)
- **Ollama** installed and running
- **Node.js** (for MCP servers)

### **Step 1: Install Ollama**
```bash
# Visit: https://ollama.ai and follow installation instructions
# Pull the Qwen3:8b model
ollama pull qwen3:8b

# Verify it's working
ollama run qwen3:8b "Hello, how are you?"

# Keep Ollama running in background
ollama serve
```

### **Step 2: Setup Python Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

**⚠️ Critical**: Use Python 3.12 or below. Python 3.13+ causes dependency conflicts.

### **Step 3: Install MCP Servers**
```bash
# Install required MCP servers
npx -y @modelcontextprotocol/server-filesystem
uvx mcp-server-data-exploration
```

### **Step 4: Launch Application**
```bash
# Make sure Ollama is running in another terminal: ollama serve
# Then start Streamlit
streamlit run main.py --server.port 8501
```

### **Step 5: Test the System**
1. Open browser to `http://localhost:8501`
2. Upload the `sample_data.csv` file
3. Start chatting with your data using natural language
4. Try different types of requests and watch the agents adapt

## 📁 **Repository Structure**

```
mcp-dataflow-chat/
├── main.py                    # Streamlit Chat UI (250 lines)
├── agents.py                  # Dynamic agents with MCP (300 lines)
├── requirements.txt           # Python dependencies
├── sample_data.csv           # Test data file
├── README.md                 # This comprehensive guide
├── PRD.md                    # Product Requirements Document
├── tests/                    # Test suite
│   ├── test_basic_functionality.py
│   ├── test_mcp_connections.py
│   ├── test_mcp_working.py
│   ├── MCP_TEST_RESULTS.md
│   └── README.md
└── venv/                     # Virtual environment (created during setup)
```

## 💬 **Chat Interface Examples**

The system understands natural language requests and routes them to appropriate agents:

### **Data Analysis Requests**
- *"Upload and analyze this data"* → Uses all 5 agents sequentially
- *"Clean the dataset and find insights"* → Uses cleaning + analysis agents
- *"What are the main trends in this data?"* → Uses analysis + visualization agents

### **Specific Task Requests**
- *"Create visualizations for key patterns"* → Uses visualization agent
- *"Generate a comprehensive report"* → Uses report generator
- *"Check the data quality"* → Uses ingestion + cleaning agents

### **Smart Agent Selection**
The system automatically selects agents based on keywords:
- **"clean", "quality"** → Data Quality Engineer
- **"analyze", "insights"** → Statistical Analyst  
- **"visualize", "chart"** → Visualization Specialist
- **"report", "summary"** → Report Generator
- **"upload", "validate"** → Data Ingestion Specialist

## 🧠 **How It Works**

1. **File Upload**: User uploads CSV file through Streamlit interface
2. **Agent Selection**: System analyzes user request and selects appropriate agents
3. **MCP Integration**: Selected agents use MCP servers for enhanced data processing
4. **Analysis Execution**: CrewAI orchestrates agent collaboration
5. **Results Delivery**: Conversational response with insights and recommendations

## 💡 **Key Benefits**

### **Local Processing**
- **No API costs** - runs completely locally with Ollama
- **Privacy** - your data never leaves your machine  
- **Fast** - Qwen3:8b is optimized for reasoning tasks
- **Reliable** - no rate limits or internet dependency

### **Intelligent Routing**
- **Dynamic agent selection** - only uses the agents you need
- **Conversational interface** - natural language processing
- **Adaptive responses** - learns from user interactions
- **Error handling** - graceful failure recovery

## ✅ **Success Checklist**

After setup, you should have:

- [ ] **Ollama running** with Qwen3:8b model loaded
- [ ] **Working Streamlit Chat UI** with file upload
- [ ] **2 MCP servers** initialized and connected
- [ ] **5 AI agents** that dynamically select based on requests
- [ ] **Natural language processing** that routes to appropriate agents
- [ ] **Conversation history** with chat interface
- [ ] **Dynamic responses** that adapt to user requests
- [ ] **Error handling** for common issues

## 🔧 **Troubleshooting**

### **Ollama Issues**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### **MCP Server Issues**
```bash
# Test individual MCP servers
npx -y @modelcontextprotocol/server-filesystem --help
uvx mcp-server-data-exploration --help
```

### **Python Dependencies**
```bash
# Reinstall if needed
pip install -r requirements.txt --force-reinstall
```

### **Common Issues**
- **Python 3.13+**: Downgrade to Python 3.12 or below
- **MCP Server Timeouts**: Check if servers are properly installed
- **Ollama Connection**: Ensure Ollama is running on port 11434

## 📊 **Sample Chat Session**

```
User: "Upload and analyze this data"
Assistant: "I'll help you analyze this data! Let me start by validating the file..."

User: "What are the main trends?"
Assistant: "Based on the analysis, here are the key trends I found..."

User: "Create some visualizations"
Assistant: "I'll create charts to show the patterns. Here are the visualizations..."
```

## 🚀 **Current Status**

### **✅ Working Components**
- Core CrewAI integration
- Streamlit chat interface
- Filesystem MCP server (14 tools available)
- Agent orchestration and delegation
- File upload and validation
- Natural language processing

### **⚠️ Known Issues**
- Data exploration MCP server requires separate installation
- Python 3.13+ compatibility issues
- Some MCP servers not available in package registry

### **🎯 Next Development Phase**
See `FUTURE.md` for planned enhancements including:
- Local MCP service installation
- Multiple chat sessions
- Database integration
- Docker containerization

## 📚 **Documentation**

- **`PRD.md`**: Detailed Product Requirements Document
- **`tests/`**: Comprehensive test suite and results
- **`FUTURE.md`**: Planned enhancements and roadmap

---

**This repository provides a working foundation for dynamic AI-powered data analysis with intelligent agent selection and local processing capabilities.** 