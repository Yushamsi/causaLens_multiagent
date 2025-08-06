# agents.py - CrewAI Chat Interface with Manager Agent Delegation
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

class CrewAIChatInterface:
    """
    A chat interface powered by CrewAI with a manager agent that can delegate tasks to specialists.
    
    Primary Use Case: Chat-based interaction where users can ask questions, provide data,
    and request analysis/visualizations. The manager agent automatically delegates to specialists.
    """
    
    def __init__(self):
        """
        Initialize the chat interface with LLM and MCP tools.
        """
        self.llm = ollama_llm
        self.mcp_tools = {}
        self.crew = None
    
    async def setup_mcp_servers(self):
        """
        Initialize MCP servers for enhanced data processing capabilities.
        
        Returns:
            dict: Dictionary of initialized MCP server adapters.
        """
        try:
            from mcp import StdioServerParameters
            
            mcp_configs = {
                'filesystem': StdioServerParameters(
                    command='npx',
                    args=['-y', '@modelcontextprotocol/server-filesystem'],
                    env=os.environ.copy()
                ),
                'data_exploration': StdioServerParameters(
                    command='uvx', 
                    args=['mcp-server-data-exploration'],
                    env=os.environ.copy()
                )
            }
            
            # Create MCP tools
            for name, serverparams in mcp_configs.items():
                try:
                    adapter = MCPServerAdapter(serverparams)
                    self.mcp_tools[name] = adapter
                    print(f"✅ MCP Server {name} initialized")
                except Exception as e:
                    print(f"❌ Failed to initialize {name}: {e}")
            
            return self.mcp_tools
            
        except ImportError as e:
            print(f"⚠️  MCP package not available: {e}")
            print("   Install with: pip install crewai-tools[mcp]")
            return self.mcp_tools
    
    def create_manager_agent(self):
        """
        Create the manager agent that coordinates the chat interface.
        
        Returns:
            Agent: A manager agent configured for chat-based task delegation.
        """
        manager = Agent(
            role="Senior Project Manager & Technical Coordinator",
            goal="Orchestrate chat-based workflows and delegate tasks to specialists",
            backstory="""You're a seasoned project manager with deep technical expertise. Your role is to:
            
            1. **Chat Coordination**: Handle user messages and determine appropriate responses
            2. **Task Delegation**: Match user requests to the most qualified specialists
            3. **Quality Assurance**: Review and validate outputs from team members
            4. **Communication**: Ensure clear responses to user queries
            
            You excel at:
            - Understanding user intent and requirements
            - Coordinating multiple specialists effectively
            - Providing helpful, informative responses
            - Adapting strategies based on user input""",
            allow_delegation=True,  # 🔑 Key: Manager can delegate to specialists
            verbose=True,
            llm=self.llm,
            # Enhanced capabilities for better coordination
            max_iter=15,  # Allow more iterations for complex coordination
            respect_context_window=True,  # Handle large conversation contexts
            reasoning=True,  # Enable strategic reasoning
            max_reasoning_attempts=3  # Limit reasoning attempts for efficiency
        )
        return manager
    
    def create_specialist_agents(self):
        """
        Create specialist agents that the manager can delegate to.
        
        Returns:
            list: List of specialist agents configured for specific domains.
        """
        # Data Ingestion Specialist
        ingestion_agent = Agent(
            role="Data Ingestion Specialist",
            goal="Efficiently load, validate, and prepare data for analysis",
            backstory="""You're an expert in data ingestion and preprocessing with deep knowledge of:
            - Various data formats (CSV, JSON, XML, databases)
            - Data validation and quality assessment
            - Initial data exploration and profiling
            - Handling missing data and outliers
            - Data format conversion and standardization
            
            You work closely with the Data Quality Engineer to ensure seamless data flow.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm,
            tools=[self.mcp_tools.get('filesystem', None)] if self.mcp_tools else None
        )
        
        # Data Quality Engineer
        cleaning_agent = Agent(
            role="Data Quality Engineer",
            goal="Clean, preprocess, and ensure data quality for downstream analysis",
            backstory="""You're a specialist in data cleaning and quality assurance with expertise in:
            - Missing value imputation strategies
            - Outlier detection and treatment
            - Data type conversion and validation
            - Duplicate detection and removal
            - Data standardization and normalization
            - Quality metrics and reporting
            
            You provide detailed documentation of all cleaning decisions and their rationale.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm,
            tools=[self.mcp_tools.get('data_exploration', None)] if self.mcp_tools else None
        )
        
        # Data Analysis Specialist
        analysis_agent = Agent(
            role="Data Analysis Specialist", 
            goal="Perform comprehensive statistical analysis and extract actionable insights",
            backstory="""You're a skilled data analyst with expertise in:
            - Descriptive and inferential statistics
            - Correlation and regression analysis
            - Time series analysis and forecasting
            - Pattern recognition and trend identification
            - Statistical significance testing
            - Data-driven hypothesis testing
            
            You excel at translating complex statistical findings into business insights.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm,
            tools=[self.mcp_tools.get('data_exploration', None)] if self.mcp_tools else None
        )
        
        # Visualization Specialist
        viz_agent = Agent(
            role="Data Visualization Specialist",
            goal="Create compelling, informative, and accessible data visualizations",
            backstory="""You're an expert in data visualization who understands:
            - Chart type selection for different data types
            - Color theory and accessibility
            - Interactive visualization techniques
            - Storytelling through data
            - Dashboard design principles
            - Export formats for various platforms
            
            You create visualizations that effectively communicate insights to stakeholders.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm,
            tools=[self.mcp_tools.get('data_exploration', None)] if self.mcp_tools else None
        )
        
        # Report Generator
        report_agent = Agent(
            role="Technical Report Writer",
            goal="Synthesize findings into comprehensive, actionable reports",
            backstory="""You're a technical writer who specializes in:
            - Executive summaries for business stakeholders
            - Technical documentation for developers
            - Methodology and process documentation
            - Recommendations and action items
            - Risk assessment and mitigation strategies
            - Multi-format report generation (PDF, HTML, Markdown)
            
            You excel at making complex technical findings accessible to diverse audiences.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm
        )
        
        specialists = [ingestion_agent, cleaning_agent, analysis_agent, viz_agent, report_agent]
        return specialists
    
    def create_chat_task(self, user_message):
        """
        Create a dynamic task based on user input for chat interaction.
        
        Args:
            user_message (str): The user's message or request.
            
        Returns:
            Task: A task configured for chat-based delegation.
        """
        task = Task(
            description=f"""User request: {user_message}
            
            **Your Role**: You are the manager of a team of specialists. Respond to the user's request appropriately.
            
            **Available Team Members**:
            - Data Ingestion Specialist: Handle data loading and validation
            - Data Quality Engineer: Clean and preprocess data
            - Data Analysis Specialist: Perform statistical analysis
            - Data Visualization Specialist: Create charts and graphs
            - Technical Report Writer: Compile findings into reports
            
            **Instructions**:
            1. If the user asks general questions about your purpose or capabilities, answer directly
            2. If the user provides data (tables, CSV content, etc.), delegate to appropriate specialists
            3. If the user asks for analysis, visualization, or reports, coordinate with relevant team members
            4. Always provide helpful, informative responses
            5. When delegating, ensure the task is completed and results are compiled
            
            **Examples**:
            - "What is your purpose?" → Answer directly about your role as a project manager
            - "Analyze this table: [data]" → Delegate to Data Analysis Specialist
            - "Create a visualization" → Delegate to Data Visualization Specialist
            - "Generate a report" → Delegate to Technical Report Writer
            
            Respond appropriately to the user's request.""",
            expected_output="A helpful response addressing the user's request, either directly or through coordinated team effort.",
            agent=self.create_manager_agent(),
            verbose=True
        )
        return task
    
    async def create_chat_crew(self):
        """
        Create a crew configured for chat-based interactions.
        
        Returns:
            Crew: A hierarchical crew configured for chat-based task delegation.
        """
        print("🔄 Creating chat-enabled crew...")
        
        # Create manager and specialist agents
        manager = self.create_manager_agent()
        specialists = self.create_specialist_agents()
        
        # Create hierarchical crew for chat
        self.crew = Crew(
            agents=[manager] + specialists,  # Manager + all specialists
            tasks=[],  # Tasks will be created dynamically for each chat
            process=Process.hierarchical,  # 🔑 Key: Hierarchical process
            manager_llm=self.llm,  # Manager uses the same LLM
            verbose=True,
            # Enhanced crew configuration
            planning=True,  # Enable strategic planning
            max_rpm=10,  # Rate limiting for API calls
            memory=True  # Enable memory for better context retention
        )
        
        print("✅ Chat-enabled crew created successfully")
        print(f"   - Manager Agent: {manager.role}")
        print(f"   - Specialist Agents: {[agent.role for agent in specialists]}")
        print(f"   - Process: Hierarchical with chat-based delegation")
        print(f"   - Features: Planning enabled, Memory enabled, Rate limiting active")
        
        return self.crew
    
    async def chat(self, user_message, **kwargs):
        """
        Chat with the crew through the manager agent.
        
        Args:
            user_message (str): The user's message or request.
            **kwargs: Additional keyword arguments for chat configuration.
            
        Returns:
            str: Response from the crew via the manager agent.
        """
        try:
            # Setup MCP servers if not already done
            if not self.mcp_tools:
                await self.setup_mcp_servers()
            
            # Create crew if not already created
            if not self.crew:
                await self.create_chat_crew()
            
            # Create a dynamic task based on user input
            chat_task = self.create_chat_task(user_message)
            
            # Add the task to the crew and execute
            self.crew.tasks = [chat_task]
            result = self.crew.kickoff()
            
            return result.raw if hasattr(result, 'raw') else str(result)
            
        except Exception as e:
            print(f"❌ Chat failed: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    # ============================================================================
    # PIPELINE FUNCTIONALITY (Secondary Use Case)
    # ============================================================================
    
    def create_pipeline_task(self, csv_file_path):
        """
        Create a task for traditional pipeline processing.
        
        Args:
            csv_file_path (str): Path to the CSV file to analyze.
            
        Returns:
            Task: A task configured for pipeline processing.
        """
        task = Task(
            description=f"""Conduct a comprehensive data analysis project on {csv_file_path}.
            
            **Project Overview:**
            This is a complex data analysis project requiring coordination across multiple specialists.
            Your role is to orchestrate the entire workflow and ensure high-quality deliverables.
            
            **Your Responsibilities:**
            1. **Project Planning**: Break down the analysis into logical phases
            2. **Task Delegation**: Assign specific tasks to the most qualified team members
            3. **Progress Monitoring**: Track task completion and quality
            4. **Quality Assurance**: Review outputs and request improvements if needed
            5. **Final Integration**: Compile all findings into a cohesive report
            
            **Team Member Expertise:**
            - **Data Ingestion Specialist**: Handle data loading, validation, and initial exploration
            - **Data Quality Engineer**: Clean data, handle missing values, ensure data quality
            - **Data Analysis Specialist**: Perform statistical analysis and pattern recognition
            - **Data Visualization Specialist**: Create charts, graphs, and interactive visualizations
            - **Technical Report Writer**: Compile findings into comprehensive reports
            
            **Expected Workflow:**
            1. Start with data ingestion and initial assessment
            2. Delegate data cleaning and quality assurance
            3. Coordinate statistical analysis and insight generation
            4. Oversee visualization creation
            5. Manage final report compilation
            
            **Quality Standards:**
            - All data cleaning decisions must be documented
            - Statistical findings must include confidence intervals
            - Visualizations must be accessible and well-labeled
            - Final report must include executive summary and technical details
            
            Coordinate the workflow efficiently and ensure all deliverables meet quality standards.""",
            expected_output="""A comprehensive data analysis package including:
            - **Executive Summary**: Key findings and recommendations for business stakeholders
            - **Technical Report**: Detailed methodology, analysis, and statistical findings
            - **Data Quality Report**: Documentation of cleaning decisions and data improvements
            - **Visualizations**: Charts, graphs, and interactive elements
            - **Technical Appendix**: Code, methodology, and detailed statistical results
            - **Action Items**: Specific recommendations for next steps""",
            agent=self.create_manager_agent(),
            verbose=True
        )
        return task
    
    async def run_pipeline(self, csv_file_path, **kwargs):
        """
        Run the traditional data analysis pipeline (secondary use case).
        
        Args:
            csv_file_path (str): Path to the CSV file to analyze.
            **kwargs: Additional keyword arguments for pipeline configuration.
            
        Returns:
            dict: Results from the data analysis pipeline.
            
        Raises:
            Exception: If the pipeline fails to execute.
        """
        try:
            # Setup MCP servers if not already done
            if not self.mcp_tools:
                await self.setup_mcp_servers()
            
            # Create crew if not already created
            if not self.crew:
                await self.create_chat_crew()
            
            # Create pipeline task
            pipeline_task = self.create_pipeline_task(csv_file_path)
            
            # Execute pipeline
            self.crew.tasks = [pipeline_task]
            result = self.crew.kickoff()
            
            print("🎉 Pipeline completed successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            raise

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Initialize the chat interface
        chat_interface = CrewAIChatInterface()
        
        # Example 1: Chat functionality (Primary Use Case)
        print("=== Chat Interface Examples ===")
        
        # General question
        response1 = await chat_interface.chat("What is your purpose?")
        print(f"Q: What is your purpose?\nA: {response1}\n")
        
        # Data analysis request
        response2 = await chat_interface.chat("Can you analyze this table: Sales,2023,1000; Sales,2024,1200; Marketing,2023,500; Marketing,2024,800")
        print(f"Q: Can you analyze this table?\nA: {response2}\n")
        
        # Visualization request
        response3 = await chat_interface.chat("Create a visualization of the sales data")
        print(f"Q: Create a visualization\nA: {response3}\n")
        
        # Example 2: Pipeline functionality (Secondary Use Case)
        print("=== Pipeline Example ===")
        pipeline_result = await chat_interface.run_pipeline('sample_data.csv')
        print(f"Pipeline Result: {pipeline_result}")
    
    asyncio.run(main()) 