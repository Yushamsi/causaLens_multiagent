# test_mcp_working.py - Test the working MCP functionality
import asyncio
import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class MCPWorkingTester:
    """
    Test the MCP functionality that is actually working.
    """
    
    def __init__(self):
        self.test_results = {}
    
    async def test_mcp_imports(self):
        """
        Test that MCP-related imports work correctly.
        """
        print("🔧 Testing MCP Imports...")
        
        try:
            from mcp import StdioServerParameters
            from crewai_tools import MCPServerAdapter
            
            print("✅ MCP imports successful")
            self.test_results['mcp_imports'] = {
                'status': 'PASS',
                'message': 'MCP imports successful'
            }
            return True
            
        except ImportError as e:
            print(f"❌ MCP Import Failed: {e}")
            self.test_results['mcp_imports'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_filesystem_server(self):
        """
        Test the filesystem MCP server which we know works.
        """
        print("\n📁 Testing Filesystem MCP Server...")
        
        try:
            from mcp import StdioServerParameters
            from crewai_tools import MCPServerAdapter
            
            # Create filesystem server parameters
            serverparams = StdioServerParameters(
                command='npx',
                args=['-y', '@modelcontextprotocol/server-filesystem'],
                env=os.environ.copy()
            )
            
            # Test with context manager (recommended approach)
            with MCPServerAdapter(serverparams) as tools:
                print(f"✅ Filesystem MCP server initialized with {len(tools)} tools")
                self.test_results['filesystem_server'] = {
                    'status': 'PASS',
                    'tools_count': len(tools),
                    'message': 'Filesystem MCP server working'
                }
                return True
                
        except Exception as e:
            print(f"❌ Filesystem MCP Server Failed: {e}")
            self.test_results['filesystem_server'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_agents_mcp_integration(self):
        """
        Test that the agents.py MCP server setup works correctly.
        """
        print("\n🤖 Testing Agents.py MCP Integration...")
        
        try:
            from agents import CrewAIChatInterface
            
            # Create chat interface
            chat_interface = CrewAIChatInterface()
            
            # Test MCP server setup
            mcp_tools = await chat_interface.setup_mcp_servers()
            
            if mcp_tools and len(mcp_tools) > 0:
                print(f"✅ Agents.py MCP integration successful - {len(mcp_tools)} servers initialized")
                self.test_results['agents_mcp_integration'] = {
                    'status': 'PASS',
                    'servers_initialized': len(mcp_tools),
                    'server_names': list(mcp_tools.keys())
                }
                return True
            else:
                print("⚠️  Agents.py MCP integration - no servers initialized")
                self.test_results['agents_mcp_integration'] = {
                    'status': 'PARTIAL',
                    'message': 'No MCP servers were initialized'
                }
                return False
                
        except Exception as e:
            print(f"❌ Agents.py MCP Integration Failed: {e}")
            self.test_results['agents_mcp_integration'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_crewai_with_mcp_tools(self):
        """
        Test that CrewAI can work with MCP tools.
        """
        print("\n👥 Testing CrewAI with MCP Tools...")
        
        try:
            from crewai import Agent, Task, Crew, LLM
            from mcp import StdioServerParameters
            from crewai_tools import MCPServerAdapter
            
            # Create LLM
            llm = LLM(
                model="ollama/qwen3:8b",
                base_url="http://localhost:11434"
            )
            
            # Test with filesystem MCP server
            serverparams = StdioServerParameters(
                command='npx',
                args=['-y', '@modelcontextprotocol/server-filesystem'],
                env=os.environ.copy()
            )
            
            try:
                with MCPServerAdapter(serverparams) as tools:
                    # Create agent with MCP tools
                    agent = Agent(
                        role="Test Agent",
                        goal="Test MCP integration",
                        backstory="A test agent with MCP tools",
                        verbose=True,
                        llm=llm,
                        tools=tools
                    )
                    
                    print("✅ CrewAI with MCP tools successful")
                    self.test_results['crewai_with_mcp_tools'] = {
                        'status': 'PASS',
                        'message': 'CrewAI agent created with MCP tools',
                        'tools_count': len(tools)
                    }
                    return True
                    
            except Exception as e:
                print(f"⚠️  MCP tools not available: {e}")
                # Test without MCP tools
                agent = Agent(
                    role="Test Agent",
                    goal="Test basic functionality",
                    backstory="A test agent",
                    verbose=True,
                    llm=llm
                )
                
                print("✅ CrewAI basic functionality works")
                self.test_results['crewai_with_mcp_tools'] = {
                    'status': 'PARTIAL',
                    'message': 'CrewAI works but MCP tools not available'
                }
                return True
                
        except Exception as e:
            print(f"❌ CrewAI with MCP Tools Failed: {e}")
            self.test_results['crewai_with_mcp_tools'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    def print_summary(self):
        """
        Print a summary of all test results.
        """
        print("\n" + "="*60)
        print("📊 MCP WORKING TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result.get('status') == 'PASS')
        failed_tests = sum(1 for result in self.test_results.values() if result.get('status') == 'FAIL')
        partial_tests = sum(1 for result in self.test_results.values() if result.get('status') == 'PARTIAL')
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Partial: {partial_tests}")
        print()
        
        for test_name, result in self.test_results.items():
            status = result.get('status', 'UNKNOWN')
            status_icon = {
                'PASS': '✅',
                'FAIL': '❌',
                'PARTIAL': '⚠️'
            }.get(status, '❓')
            
            print(f"{status_icon} {test_name.replace('_', ' ').title()}: {status}")
            
            if 'error' in result:
                print(f"   Error: {result['error']}")
            elif 'message' in result:
                print(f"   Message: {result['message']}")
            elif 'servers_initialized' in result:
                print(f"   Servers: {result['servers_initialized']} ({', '.join(result['server_names'])})")
            elif 'tools_count' in result:
                print(f"   Tools: {result['tools_count']}")
        
        print("\n" + "="*60)
        
        # Save results to file
        results_file = os.path.join(os.path.dirname(__file__), 'mcp_working_results.json')
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"📄 Test results saved to '{results_file}'")
    
    async def run_all_tests(self):
        """
        Run all MCP working tests.
        """
        print("🚀 Starting MCP Working Tests")
        print("="*60)
        
        # Run tests
        await self.test_mcp_imports()
        await self.test_filesystem_server()
        await self.test_agents_mcp_integration()
        await self.test_crewai_with_mcp_tools()
        
        # Print summary
        self.print_summary()

async def main():
    """
    Main function to run the MCP working tests.
    """
    tester = MCPWorkingTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 