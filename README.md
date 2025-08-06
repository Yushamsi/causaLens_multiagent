# 🤖 MCP DataFlow Chat

**Dynamic AI Analysis**: Chat with your data using intelligent agents that adapt to your requests

## 🎯 **What This Does**

- **Upload CSV files** and chat naturally with your data
- **5 intelligent agents** that dynamically select based on your requests
- **Uses Ollama with Qwen3:8b model** (local, free AI)
- **Streamlit Chat UI** with conversation history
- **Dynamic agent selection** - only uses the agents you need

## 🏗️ **Dynamic Architecture**

```
CSV Upload → Chat Interface → Agent Selection → Targeted Analysis → Results
             (User Input)    (Smart Routing)   (Flexible Crew)   (Conversational)
```

## 🔧 **Required MCP Servers (4 Total)**

```yaml
MCP Servers for MVP:
  1. filesystem_mcp: "@modelcontextprotocol/server-filesystem" (File operations)
  2. pandas_mcp: "pandas-mcp-server" (Data processing) 
  3. data_exploration_mcp: "mcp-server-data-exploration" (Auto insights)
  4. sqlite_mcp: "@modelcontextprotocol/server-sqlite" (Optional storage)
```

## 🚀 **Quick Setup (1 Hour)**

### **Step 1: Install Ollama**
```bash
# Visit: https://ollama.ai and follow installation instructions
# Then pull the Qwen3:8b model
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

**⚠️ Important:** Please use Python 3.12 or below, as some dependencies are not compatible with Python 3.13 and above.

### **Step 3: Install MCP Servers**
```bash
# Install 4 MCP servers (takes 3-5 minutes)
npx -y @modelcontextprotocol/server-filesystem
uvx pandas-mcp-server
uvx mcp-server-data-exploration  
npx -y @modelcontextprotocol/server-sqlite
```

### **Step 4: Launch Application**
```bash
# Make sure Ollama is running in another terminal: ollama serve
# Then start Streamlit
streamlit run main.py --server.port 8501
```

### **Step 5: Test the Chat Interface**
1. Open browser to `http://localhost:8501`
2. Upload the `sample_data.csv` file
3. Start chatting with your data using natural language
4. Try different types of requests and watch the agents adapt

## 📁 **File Structure**

```
mcp-dataflow-chat/
├── requirements.txt       # Dependencies
├── main.py               # Streamlit Chat UI (250 lines)
├── agents.py             # Dynamic agents with MCP (300 lines)
├── sample_data.csv       # Test data
└── README.md             # This file
```

## 🤖 **The 5 Intelligent Agents**

1. **📁 Data Ingestion Specialist** - Loads and validates CSV files using filesystem MCP
2. **🧹 Data Quality Engineer** - Cleans and preprocesses data using pandas MCP
3. **📊 Statistical Analyst** - Performs analysis using data exploration MCP
4. **📈 Visualization Specialist** - Creates charts using pandas MCP
5. **📋 Report Generator** - Synthesizes findings into comprehensive report

## 💬 **Chat Examples**

**Try these natural language requests:**

- *"Upload and analyze this data"* → Uses all 5 agents
- *"Clean the dataset and find insights"* → Uses cleaning + analysis agents
- *"Create visualizations for key patterns"* → Uses visualization agent
- *"Generate a comprehensive report"* → Uses report generator
- *"What are the main trends in this data?"* → Uses analysis + visualization agents
- *"Check the data quality"* → Uses ingestion + cleaning agents

## 🧠 **Smart Agent Selection**

The system automatically selects the right agents based on your request:

- **Keywords like "clean", "quality"** → Data Quality Engineer
- **Keywords like "analyze", "insights"** → Statistical Analyst  
- **Keywords like "visualize", "chart"** → Visualization Specialist
- **Keywords like "report", "summary"** → Report Generator
- **Keywords like "upload", "validate"** → Data Ingestion Specialist

## 💡 **Ollama Benefits**
- **No API costs** - runs completely locally
- **Privacy** - your data never leaves your machine  
- **Fast** - Qwen3:8b is optimized for reasoning tasks
- **Reliable** - no rate limits or internet dependency

## ✅ **1-Hour Success Checklist**

After 60 minutes, you should have:

- [ ] **Ollama running** with Qwen3:8b model loaded
- [ ] **Working Streamlit Chat UI** with file upload
- [ ] **4 MCP servers** initialized and connected
- [ ] **5 AI agents** that dynamically select based on requests
- [ ] **Natural language processing** that routes to appropriate agents
- [ ] **Conversation history** with chat interface
- [ ] **Dynamic responses** that adapt to user requests
- [ ] **Error handling** for common issues

## 🎯 **Expected Demo Flow**

1. **"Here's my chat interface for data analysis..."**
2. **"Upload a CSV file and start chatting naturally..."**
3. **"Ask 'clean the data' and watch the Data Quality Engineer work..."**
4. **"Ask 'find insights' and the Statistical Analyst takes over..."**
5. **"The system intelligently selects only the agents you need!"**

## 🚀 **Next Steps After MVP**

Once your 1-hour demo works, you can add:
- More Ollama models (llama3.1, codellama, etc.)
- More file formats (Excel, JSON)
- Advanced visualizations
- Export to PDF
- Conversation memory
- Additional MCP servers
- Better error handling
- Model comparison features
- Multi-turn conversations

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
uvx pandas-mcp-server --help
```

### **Python Dependencies**
```bash
# Reinstall if needed
pip install -r requirements.txt --force-reinstall
```

## 📊 **Sample Chat Session**

```
User: "Upload and analyze this data"
Assistant: "I'll help you analyze this data! Let me start by validating the file..."

User: "What are the main trends?"
Assistant: "Based on the analysis, here are the key trends I found..."

User: "Create some visualizations"
Assistant: "I'll create charts to show the patterns. Here are the visualizations..."
```

**This MVP proves the concept and gets you a working dynamic chat interface with intelligent agent selection in just 1 hour!** 