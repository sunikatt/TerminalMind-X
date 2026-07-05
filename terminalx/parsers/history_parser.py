import os

def parse_bash_history(file_path: str) -> list[str]:
    """
    Reads bash or zsh history and extracts valid commands.
    Uses an explicit loop for clear data flow and filtering.
    """
    parsed_commands = []
    
    # Expand ~ to full path
    full_path = os.path.expanduser(file_path)
    
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"History file not found: {full_path}")
        
    with open(full_path, 'r', encoding='utf-8', errors='ignore') as history_file:
        for line in history_file:
            clean_line = line.strip()
            
            # Skip empty lines, comments, or timestamp markers (like in zsh)
            if not clean_line or clean_line.startswith('#') or clean_line.startswith(':'):
                continue
                
            # Filter out basic noise commands
            if clean_line in ['ls', 'pwd', 'cd', 'clear', 'exit']:
                continue
                
            # Keep only the actual command text for Cognee ingestion
            parsed_commands.append(clean_line)
            
    return parsed_commands