#!/usr/bin/env python3
"""
Simple Manager Agent Demo
Shows how the manager agent automatically handles delegation and task assignment
"""

import asyncio
import os
from agents import MCPDataFlowPipeline

async def demo_manager_agent():
    """Demo: Manager agent handles everything automatically"""
    print("🚀 Manager Agent Demo")
    print("=" * 50)
    print("The manager agent will automatically:")
    print("1. Analyze the user request")
    print("2. Decide which specialists to involve")
    print("3. Delegate tasks to appropriate specialists")
    print("4. Coordinate the workflow")
    print("5. Compile the final report")
    print("=" * 50)
    
    pipeline = MCPDataFlowPipeline()
    
    try:
        # The manager agent handles everything - no complex selection needed!
        result = await pipeline.run_pipeline('sample_data.csv')
        
        print("\n✅ Demo completed successfully!")
        print("The manager agent automatically:")
        print("   - Analyzed the data file")
        print("   - Delegated to Data Ingestion Specialist")
        print("   - Delegated to Data Analysis Specialist") 
        print("   - Delegated to Data Visualization Specialist")
        print("   - Coordinated all results into final report")
        
        return result
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(demo_manager_agent()) 