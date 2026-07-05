import os
import asyncio
import cognee
from rich.console import Console

console = Console()

async def init_memory():
    """Initializes Cognee configurations with Google Gemini."""
    
    # 1. Tell Cognee to use Gemini (via its internal LiteLLM router)
    # Using gemini-1.5-flash as it is lightning fast for CLI responses
    cognee.config.llm_provider = "litellm" 
    cognee.config.llm_model = "gemini/gemini-1.5-flash" 
    
    # Ensure the API key is picked up from the environment
    if not os.getenv("GEMINI_API_KEY"):
        console.print("[red]Error: GEMINI_API_KEY not found in .env file![/red]")
        return False
        
    cognee.config.set_system_prompt(
        "You are TerminalX, a helpful local CLI assistant that remembers developer workflows. "
        "Answer concisely and provide shell commands when applicable."
    )
    console.print("[green]Memory engine initialized using Google Gemini.[/green]")
    return True
    
async def remember_data(data_list: list[str], dataset_name: str):
    """
    Adds a list of text data to Cognee and builds the knowledge graph.
    """
    try:
        # 1. Add data to Cognee
        # We explicitly loop through commands to add them as text snippets
        for item in data_list:
            await cognee.add(item, dataset_name=dataset_name)
            
        # 2. Cognify (This extracts entities, builds the graph, and creates vector embeddings)
        await cognee.cognify()
        
        return True
    except Exception as e:
        console.print(f"[bold red]Error remembering data:[/bold red] {e}")
        return False

async def ask_memory(question: str):
    """
    Searches the Cognee knowledge graph and returns an answer.
    """
    try:
        # Cognee's search handles the graph traversal and LLM generation
        results = await cognee.search(question)
        
        # Format results (assuming Cognee returns a list or string based on version)
        if isinstance(results, list):
            # Extracting just the text answers using an explicit loop
            answers = []
            for res in results:
                answers.append(str(res))
            return "\n".join(answers)
        return str(results)
        
    except Exception as e:
        console.print(f"[bold red]Error recalling data:[/bold red] {e}")
        return "I couldn't recall that information."