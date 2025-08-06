# agents.py - Simplified CrewAI implementation with Manager Agent (Hierarchical Process)
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
            'pandas': {
                'command': 'uvx',
                'args': ['pandas-mcp-server'],
                'transport': 'stdio'
            },
            'data_exploration': {
                'command': 'uvx', 
                'args': ['mcp-server-data-exploration'],
                'transport': 'stdio'
            },
            'sqlite': {
                'command': 'npx',
                'args': ['-y', '@modelcontextprotocol/server-sqlite'],
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
    
    def create_manager_agent(self):
        """Create the central manager agent that coordinates everything"""
        return Agent(
            role="Project Manager",
            goal="Efficiently manage the crew and ensure high-quality task completion",
            backstory="""You're an experienced project manager, skilled in overseeing complex projects 
            and guiding teams to success. Your role is to coordinate the efforts of the crew members, 
            ensuring that each task is completed on time and to the highest standard. You can delegate 
            tasks to specialists based on their expertise and manage the overall workflow.""",
            allow_delegation=True,  # 🔑 Key: Manager can delegate to specialists
            verbose=True,
            llm=self.llm
        )
    
    def create_specialist_agents(self):
        """Create specialist agents that the manager can delegate to"""
        agents = {}
        
        # Data Ingestion Specialist
        ingestion_agent = Agent(
            role="Data Ingestion Specialist",
            goal="Efficiently load and prepare data for analysis",
            backstory="""You're an expert in data ingestion and preprocessing. You specialize in 
            loading data from various sources, cleaning it, and preparing it for analysis. You work 
            with CSV files, databases, and other data formats to ensure data quality and consistency.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm
        )
        
        # Data Quality Engineer
        cleaning_agent = Agent(
            role="Data Quality Engineer",
            goal="Clean and preprocess data to ensure quality",
            backstory="""You're a specialist in data cleaning, missing values, and data standardization. 
            You explain your cleaning decisions clearly and ensure data quality for downstream analysis.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm
        )
        
        # Data Analysis Specialist
        analysis_agent = Agent(
            role="Data Analysis Specialist", 
            goal="Analyze data patterns and extract insights",
            backstory="""You're a skilled data analyst with expertise in statistical analysis, 
            pattern recognition, and data visualization. You can identify trends, correlations, and 
            insights from complex datasets to support decision-making.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm
        )
        
        # Visualization Specialist
        viz_agent = Agent(
            role="Data Visualization Specialist",
            goal="Create compelling and informative data visualizations",
            backstory="""You're an expert in data visualization who can transform complex data into 
            clear, engaging visual representations. You understand how to choose the right chart types, 
            color schemes, and layouts to effectively communicate data insights.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm
        )
        
        # Report Generator
        report_agent = Agent(
            role="Report Generator",
            goal="Synthesize findings into comprehensive reports",
            backstory="""You're a technical writer who creates clear, actionable data reports that 
            business stakeholders can understand and act upon. You can compile insights from various 
            specialists into cohesive, professional reports.""",
            allow_delegation=False,  # Specialist focuses on core expertise
            verbose=True,
            llm=self.llm
        )
        
        return [ingestion_agent, cleaning_agent, analysis_agent, viz_agent, report_agent]
    
    def create_main_task(self, csv_file_path):
        """Create the main task that the manager will delegate"""
        return Task(
            description=f"""Analyze the data in {csv_file_path} and create comprehensive insights.
            
            Your responsibilities include:
            1. Load and examine the data file
            2. Clean and preprocess the data for quality
            3. Perform thorough data analysis to identify patterns and trends
            4. Create visualizations to illustrate key findings
            5. Generate a comprehensive report with actionable insights
            
            Delegate specific tasks to your team members based on their expertise:
            - Data Ingestion Specialist: Handle data loading and initial preprocessing
            - Data Quality Engineer: Clean data, handle missing values, and ensure data quality
            - Data Analysis Specialist: Perform statistical analysis and pattern recognition  
            - Data Visualization Specialist: Create charts and visual representations
            - Report Generator: Compile all findings into a comprehensive final report
            
            Coordinate the workflow and ensure all components come together into a cohesive final report.""",
            expected_output="""A comprehensive data analysis report including:
            - Data overview and quality assessment
            - Data cleaning summary and improvements made
            - Key statistical findings and patterns
            - Visualizations (charts, graphs)
            - Actionable insights and recommendations
            - Technical appendix with methodology""",
            agent=self.create_manager_agent(),  # 🔑 Key: Manager handles the task
            verbose=True
        )
    
    async def create_crew(self, csv_file_path):
        """Create a hierarchical crew with manager agent"""
        print("🔄 Creating hierarchical crew with manager agent...")
        
        # Create manager and specialist agents
        manager = self.create_manager_agent()
        specialists = self.create_specialist_agents()
        
        # Create the main task for the manager
        main_task = self.create_main_task(csv_file_path)
        
        # Create hierarchical crew
        self.crew = Crew(
            agents=[manager] + specialists,  # Manager + all specialists
            tasks=[main_task],  # Single task managed by manager
            process=Process.hierarchical,  # 🔑 Key: Hierarchical process
            manager_llm=self.llm,  # Manager uses the same LLM
            verbose=True
        )
        
        print("✅ Hierarchical crew created successfully")
        print(f"   - Manager Agent: {manager.role}")
        print(f"   - Specialist Agents: {[agent.role for agent in specialists]}")
        print(f"   - Process: Hierarchical with delegation")
        
        return self.crew
    
    async def run_pipeline(self, csv_file_path, **kwargs):
        """Run the complete data analysis pipeline"""
        try:
            # Setup MCP servers
            await self.setup_mcp_servers()
            
            # Create and run the crew
            crew = await self.create_crew(csv_file_path)
            result = crew.kickoff()
            
            print("🎉 Pipeline completed successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            raise

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        pipeline = MCPDataFlowPipeline()
        result = await pipeline.run_pipeline('sample_data.csv')
        print(f"Result: {result}")
    
    asyncio.run(main()) 