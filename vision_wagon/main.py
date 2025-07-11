# Main application entry point for Vision Wagon X
import os
import yaml
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    """Loads configuration from config_multi.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config_multi.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        env = os.getenv('ENV', 'dev')
        return config.get(env, config.get('default', {}))
    except FileNotFoundError:
        print(f"Warning: Configuration file not found at {config_path}")
        return {}
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}

def main():
    """Main function to run the application."""
    print("🚀 Wagon X Initializing...")

    config = load_config()

    print(f"Environment: {config.get('env', 'Not set')}")
    print(f"OpenAI Key Loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    print(f"ElevenLabs Key Loaded: {'Yes' if os.getenv('ELEVENLABS_API_KEY') else 'No'}")
    print(f"Stable Diffusion Key Loaded: {'Yes' if os.getenv('STABLE_DIFFUSION_API_KEY') else 'No'}")

    print("Checking for workflow file...")
    workflow_path = os.path.join(os.path.dirname(__file__), 'workflows', 'example_workflow_eros.yaml')
    if os.path.exists(workflow_path):
        print(f"Found example workflow: {workflow_path}")
        try:
            with open(workflow_path, 'r') as wf_file:
                workflow_data = yaml.safe_load(wf_file)
            print("Successfully parsed example_workflow_eros.yaml")
            # Here you would typically initialize and run the workflow
            # For now, just print a message
            print(f"Workflow '{workflow_data.get('name', 'Unnamed Workflow')}' would run here.")
        except Exception as e:
            print(f"Error parsing workflow file: {e}")
    else:
        print(f"Workflow file not found: {workflow_path}")

    print("Wagon X application placeholder started.")
    print("This script will keep running to simulate a service...")

    # Keep the script running (e.g., for Docker)
    try:
        while True:
            time.sleep(60)
            print("Wagon X is running...")
    except KeyboardInterrupt:
        print("Wagon X stopping.")

if __name__ == "__main__":
    main()
