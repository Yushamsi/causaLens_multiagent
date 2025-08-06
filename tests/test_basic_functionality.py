# test_basic_functionality.py - Basic functionality tests without MCP servers
import asyncio
import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class BasicFunctionalityTester:
    """
    Test basic functionality without MCP servers.
    """
    
    def __init__(self):
        self.test_results = {}
    
    async def test_import_crewai(self):
        """
        Test that CrewAI can be imported and basic classes work.
        """
        print("🔧 Testing CrewAI Import...")
        
        try:
            from crewai import Agent, Task, Crew, Process, LLM
            from crewai_tools import MCPServerAdapter
            
            print("✅ CrewAI imports successful")
            self.test_results['crewai_import'] = {
                'status': 'PASS',
                'message': 'All CrewAI classes imported successfully'
            }
            return True
            
        except Exception as e:
            print(f"❌ CrewAI Import Failed: {e}")
            self.test_results['crewai_import'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_agent_creation(self):
        """
        Test that agents can be created without MCP tools.
        """
        print("\n🤖 Testing Agent Creation...")
        
        try:
            from crewai import Agent, LLM
            
            # Test LLM creation
            llm = LLM(
                model="ollama/qwen3:8b",
                base_url="http://localhost:11434"
            )
            
            # Test agent creation
            agent = Agent(
                role="Test Agent",
                goal="Test the agent creation functionality",
                backstory="A simple test agent",
                verbose=True,
                llm=llm
            )
            
            print("✅ Agent creation successful")
            self.test_results['agent_creation'] = {
                'status': 'PASS',
                'agent_role': agent.role,
                'agent_goal': agent.goal
            }
            return True
            
        except Exception as e:
            print(f"❌ Agent Creation Failed: {e}")
            self.test_results['agent_creation'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_task_creation(self):
        """
        Test that tasks can be created.
        """
        print("\n📋 Testing Task Creation...")
        
        try:
            from crewai import Task, Agent, LLM
            
            # Create a simple agent and task
            llm = LLM(
                model="ollama/qwen3:8b",
                base_url="http://localhost:11434"
            )
            
            agent = Agent(
                role="Test Agent",
                goal="Test task creation",
                backstory="A test agent",
                verbose=True,
                llm=llm
            )
            
            task = Task(
                description="Test task description",
                expected_output="Test output",
                agent=agent,
                verbose=True
            )
            
            print("✅ Task creation successful")
            self.test_results['task_creation'] = {
                'status': 'PASS',
                'task_description': task.description,
                'expected_output': task.expected_output
            }
            return True
            
        except Exception as e:
            print(f"❌ Task Creation Failed: {e}")
            self.test_results['task_creation'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_crew_creation(self):
        """
        Test that crews can be created.
        """
        print("\n👥 Testing Crew Creation...")
        
        try:
            from crewai import Crew, Agent, Task, LLM
            
            # Create agents and tasks
            llm = LLM(
                model="ollama/qwen3:8b",
                base_url="http://localhost:11434"
            )
            
            agent1 = Agent(
                role="Agent 1",
                goal="Test agent 1",
                backstory="Test agent 1",
                verbose=True,
                llm=llm
            )
            
            agent2 = Agent(
                role="Agent 2", 
                goal="Test agent 2",
                backstory="Test agent 2",
                verbose=True,
                llm=llm
            )
            
            task1 = Task(
                description="Test task 1",
                expected_output="Test output 1",
                agent=agent1,
                verbose=True
            )
            
            task2 = Task(
                description="Test task 2",
                expected_output="Test output 2",
                agent=agent2,
                verbose=True
            )
            
            crew = Crew(
                agents=[agent1, agent2],
                tasks=[task1, task2],
                process="sequential",
                verbose=True
            )
            
            print("✅ Crew creation successful")
            self.test_results['crew_creation'] = {
                'status': 'PASS',
                'num_agents': len(crew.agents),
                'num_tasks': len(crew.tasks),
                'process': str(crew.process)
            }
            return True
            
        except Exception as e:
            print(f"❌ Crew Creation Failed: {e}")
            self.test_results['crew_creation'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_ollama_connection(self):
        """
        Test connection to Ollama LLM.
        """
        print("\n🤖 Testing Ollama Connection...")
        
        try:
            import requests
            
            # Test if Ollama is running
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            
            if response.status_code == 200:
                print("✅ Ollama connection successful")
                self.test_results['ollama_connection'] = {
                    'status': 'PASS',
                    'message': 'Ollama server is running'
                }
                return True
            else:
                print(f"❌ Ollama connection failed: {response.status_code}")
                self.test_results['ollama_connection'] = {
                    'status': 'FAIL',
                    'error': f'Ollama server returned status {response.status_code}'
                }
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Ollama connection failed: Server not running")
            self.test_results['ollama_connection'] = {
                'status': 'FAIL',
                'error': 'Ollama server is not running'
            }
            return False
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            self.test_results['ollama_connection'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    def print_summary(self):
        """
        Print a summary of all test results.
        """
        print("\n" + "="*60)
        print("📊 BASIC FUNCTIONALITY TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result.get('status') == 'PASS')
        failed_tests = sum(1 for result in self.test_results.values() if result.get('status') == 'FAIL')
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print()
        
        for test_name, result in self.test_results.items():
            status = result.get('status', 'UNKNOWN')
            status_icon = {
                'PASS': '✅',
                'FAIL': '❌'
            }.get(status, '❓')
            
            print(f"{status_icon} {test_name.replace('_', ' ').title()}: {status}")
            
            if 'error' in result:
                print(f"   Error: {result['error']}")
            elif 'message' in result:
                print(f"   Message: {result['message']}")
        
        print("\n" + "="*60)
        
        # Save results to file
        results_file = os.path.join(os.path.dirname(__file__), 'basic_functionality_results.json')
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"📄 Test results saved to '{results_file}'")
    
    async def run_all_tests(self):
        """
        Run all basic functionality tests.
        """
        print("🚀 Starting Basic Functionality Tests")
        print("="*60)
        
        # Run tests
        await self.test_import_crewai()
        await self.test_agent_creation()
        await self.test_task_creation()
        await self.test_crew_creation()
        await self.test_ollama_connection()
        
        # Print summary
        self.print_summary()

async def main():
    """
    Main function to run the basic functionality tests.
    """
    tester = BasicFunctionalityTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 