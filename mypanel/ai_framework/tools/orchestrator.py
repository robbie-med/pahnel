#!/usr/bin/env python3
"""
Hege Framework Agent Orchestrator
Inspired by nano-agent patterns for isolated, autonomous agent execution.

Implements three-layer architecture:
1. Framework Control Layer - Hege rules and coordination
2. Agent Execution Layer - Isolated agent spawning and management  
3. Tool Interface Layer - Standardized tool access

Author: Hege Framework
Version: 3.0
"""

import json
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import yaml

class HegeOrchestrator:
    """
    Three-layer orchestration pattern for agent management.
    Coordinates between framework rules, agent execution, and tool access.
    """
    
    def __init__(self, project_root: str = None):
        """Initialize orchestrator with project context."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.agents_dir = self.project_root / "project_dev" / "agents"
        self.state_dir = self.project_root / "project_dev" / "state"
        self.specs_dir = self.project_root / "project_dev" / "specs"
        
        # Layer components
        self.framework_control = FrameworkControlLayer(self.project_root)
        self.agent_execution = AgentExecutionLayer(self.agents_dir)
        self.tool_interface = ToolInterfaceLayer(self.project_root)
        
        # Current context
        self.current_agent = None
        self.current_mode = None
        self.current_task = None
        
    def process_message(self, message: str, context: Dict = None) -> Dict:
        """
        Main entry point for message processing.
        Handles @hege commands and agent activation.
        """
        context = context or {}
        
        # Layer 1: Framework Control - Check @hege commands first
        if message.strip().startswith("@hege"):
            return self.execute_hege_command(message, context)
        
        # Layer 1: Framework Control - Determine appropriate agent
        agent_decision = self.framework_control.determine_agent(message, context)
        
        # Layer 2: Agent Execution - Spawn isolated agent
        agent_result = self.agent_execution.spawn_isolated_agent(
            agent_type=agent_decision["agent"],
            context=agent_decision["context"],
            max_turns=agent_decision.get("max_turns", 20)
        )
        
        # Update current state
        self.current_agent = agent_decision["agent"]
        self.current_mode = agent_decision["mode"]
        self.current_task = agent_decision.get("task")
        
        return agent_result
    
    def execute_hege_command(self, command: str, context: Dict) -> Dict:
        """Execute @hege recovery commands."""
        parts = command.strip().split()
        cmd = parts[1] if len(parts) > 1 else "help"
        
        if cmd == "status":
            return self.report_current_state()
        elif cmd == "reset":
            return self.reset_to_framework_root()
        elif cmd == "agent":
            agent_name = parts[2] if len(parts) > 2 else None
            return self.switch_to_agent(agent_name, context)
        elif cmd == "mode":
            mode_name = parts[2] if len(parts) > 2 else None
            return self.switch_to_mode(mode_name, context)
        elif cmd == "resume":
            return self.load_checkpoint_and_continue()
        elif cmd == "validate":
            return self.run_framework_validation()
        elif cmd == "context":
            return self.display_current_context()
        else:
            return self.show_command_help()
    
    def report_current_state(self) -> Dict:
        """Report current agent, mode, task, and project state."""
        prd_status = self.framework_control.get_prd_status()
        active_stories = self.framework_control.get_active_stories()
        
        return {
            "header": f"[AGENT:primary|MODE:command_response|TASK:none]",
            "response": f"""@hege status response:
- Current Agent: {self.current_agent or 'primary'}
- Current Mode: {self.current_mode or 'coordination'}
- Current Task: {self.current_task or 'none'}
- PRD Status: {prd_status}
- Active Stories: {len(active_stories)}
- Last Activity: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- Framework Version: 3.0
""",
            "details": {
                "agent": self.current_agent,
                "mode": self.current_mode,
                "task": self.current_task,
                "prd_status": prd_status,
                "active_stories": active_stories
            }
        }
    
    def switch_to_agent(self, agent_name: str, context: Dict) -> Dict:
        """Force switch to specific agent."""
        if not agent_name:
            return {
                "header": "[AGENT:primary|MODE:error|TASK:none]",
                "response": "Error: Agent name required. Available: analyst, architect, pm, dev, qa, scrum, primary"
            }
        
        valid_agents = ["analyst", "architect", "pm", "dev", "qa", "scrum", "primary"]
        if agent_name not in valid_agents:
            return {
                "header": "[AGENT:primary|MODE:error|TASK:none]",
                "response": f"Error: Invalid agent '{agent_name}'. Available: {', '.join(valid_agents)}"
            }
        
        # Load agent and activate
        agent_context = self.framework_control.prepare_agent_context(agent_name, context)
        
        self.current_agent = agent_name
        self.current_mode = agent_context.get("default_mode", "active")
        
        return {
            "header": f"[AGENT:{agent_name}|MODE:{self.current_mode}|TASK:none]",
            "response": f"Switched to {agent_name} agent. Ready for {agent_context.get('primary_function', 'work')}.",
            "context": agent_context
        }

    def get_agent_header(self, agent: str = None, mode: str = None, task: str = None) -> str:
        """Generate proper agent header format."""
        agent = agent or self.current_agent or "primary"
        mode = mode or self.current_mode or "coordination"
        task = task or self.current_task or "none"
        return f"[AGENT:{agent}|MODE:{mode}|TASK:{task}]"


class FrameworkControlLayer:
    """
    Layer 1: Framework Control
    Implements Hege rules, workflow validation, and agent decision making.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.prd_file = project_root / "project_dev" / "PRD.md"
        self.state_dir = project_root / "project_dev" / "state"
    
    def determine_agent(self, message: str, context: Dict) -> Dict:
        """
        Determine which agent should handle the message based on framework rules.
        Implements the agent activation logic from the plan.
        """
        prd_status = self.get_prd_status()
        
        # PRD status-based decisions
        if prd_status in ["TEMPLATE", "BUILDING"]:
            return {
                "agent": "analyst",
                "mode": "prd_building",
                "context": self.prepare_prd_context(),
                "reason": f"PRD status is {prd_status}, analyst needed"
            }
        
        if prd_status == "MAINTAINED":
            if not self.specs_exist():
                return {
                    "agent": "architect",
                    "mode": "design",
                    "context": self.prepare_architecture_context(),
                    "reason": "PRD maintained but no specs exist"
                }
            
            if self.specs_exist() and not self.stories_exist():
                return {
                    "agent": "pm",
                    "mode": "planning",
                    "context": self.prepare_pm_context(),
                    "reason": "Specs exist but no stories generated"
                }
        
        # Message pattern-based decisions
        if "STORY-" in message:
            return {
                "agent": "dev",
                "mode": "implementation",
                "context": self.prepare_dev_context(message),
                "task": self.extract_story_id(message),
                "reason": "Story ID detected in message"
            }
        
        # Default coordination
        return {
            "agent": "primary",
            "mode": "coordination",
            "context": context,
            "reason": "Default coordination agent"
        }
    
    def get_prd_status(self) -> str:
        """Extract PRD status from PRD.md file."""
        if not self.prd_file.exists():
            return "MISSING"
        
        try:
            with open(self.prd_file, 'r') as f:
                first_line = f.readline().strip()
                if first_line.startswith("***PRD STATUS:"):
                    return first_line.split(":")[-1].strip().replace("***", "")
        except Exception:
            pass
        
        return "UNKNOWN"
    
    def specs_exist(self) -> bool:
        """Check if technical specifications exist."""
        specs_dir = self.project_root / "project_dev" / "specs"
        if not specs_dir.exists():
            return False
        
        # Check for actual spec files (not just README)
        spec_files = [f for f in specs_dir.rglob("*.md") if f.name != "README.md"]
        return len(spec_files) > 0
    
    def stories_exist(self) -> bool:
        """Check if stories/tasks exist."""
        stories_dir = self.project_root / "project_dev" / "stories"
        tasks_dir = self.project_root / "project_dev" / "tasks"
        
        # Check stories directory first, then fall back to tasks
        for directory in [stories_dir, tasks_dir]:
            if directory.exists():
                story_files = list(directory.rglob("*.md"))
                if len(story_files) > 0:
                    return True
        
        return False
    
    def get_active_stories(self) -> List[str]:
        """Get list of active stories/tasks."""
        active_dir = self.project_root / "project_dev" / "stories" / "active"
        if not active_dir.exists():
            # Fallback to tasks directory
            tasks_dir = self.project_root / "project_dev" / "tasks"
            if tasks_dir.exists():
                return [f.name for f in tasks_dir.glob("*.md")]
        else:
            return [f.name for f in active_dir.glob("*.md")]
        
        return []


class AgentExecutionLayer:
    """
    Layer 2: Agent Execution
    Handles isolated agent spawning and autonomous execution loops.
    """
    
    def __init__(self, agents_dir: Path):
        self.agents_dir = agents_dir
        self.definitions_dir = agents_dir / "definitions"
    
    def spawn_isolated_agent(self, agent_type: str, context: Dict, max_turns: int = 20) -> Dict:
        """
        Spawn an isolated agent with fresh context.
        Each agent runs autonomously within its own context bubble.
        """
        agent_id = str(uuid.uuid4())[:8]
        
        # Load agent definition
        agent_def = self.load_agent_definition(agent_type)
        if not agent_def:
            return {
                "error": f"Agent definition not found: {agent_type}",
                "header": "[AGENT:primary|MODE:error|TASK:none]"
            }
        
        # Create isolated context
        isolated_context = self.prepare_isolated_context(context, agent_def)
        
        # Execute autonomous loop
        execution_log = []
        for turn in range(max_turns):
            turn_result = self.execute_agent_turn(agent_def, isolated_context, turn)
            execution_log.append(turn_result)
            
            # Update context with turn results
            isolated_context.update(turn_result.get("context_updates", {}))
            
            # Check if agent goal is met
            if turn_result.get("goal_met", False):
                break
            
            # Check for handoff request
            if turn_result.get("handoff_requested"):
                break
        
        # Prepare handoff context
        return self.prepare_handoff_result(agent_def, isolated_context, execution_log)
    
    def load_agent_definition(self, agent_type: str) -> Optional[Dict]:
        """Load agent definition from YAML file."""
        definition_file = self.definitions_dir / f"{agent_type}.yaml"
        if not definition_file.exists():
            # Try with alternative naming
            alt_file = self.definitions_dir / f"{agent_type}-agent.yaml"
            if alt_file.exists():
                definition_file = alt_file
            else:
                return None
        
        try:
            with open(definition_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading agent definition: {e}")
            return None


class ToolInterfaceLayer:
    """
    Layer 3: Tool Interface
    Provides standardized tool access for all agents.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.available_tools = {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "search_codebase": self.search_codebase,
            "update_state": self.update_state,
            "validate_prd": self.validate_prd,
            "generate_spec": self.generate_spec,
            "create_story": self.create_story
        }
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict:
        """Execute a tool with given parameters."""
        if tool_name not in self.available_tools:
            return {"error": f"Tool not available: {tool_name}"}
        
        try:
            return self.available_tools[tool_name](**kwargs)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
    
    def read_file(self, file_path: str) -> Dict:
        """Read file content."""
        try:
            with open(file_path, 'r') as f:
                return {"content": f.read(), "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def write_file(self, file_path: str, content: str) -> Dict:
        """Write content to file."""
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            return {"success": True, "message": f"File written: {file_path}"}
        except Exception as e:
            return {"error": str(e), "success": False}


def create_orchestrator(project_root: str = None) -> HegeOrchestrator:
    """Factory function to create Hege orchestrator instance."""
    return HegeOrchestrator(project_root)


# Example usage
if __name__ == "__main__":
    orchestrator = create_orchestrator()
    
    # Test @hege status command
    result = orchestrator.process_message("@hege status")
    print(result["header"])
    print(result["response"])