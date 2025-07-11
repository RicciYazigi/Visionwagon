import os
import yaml

class BaseAgent:
    """
    Base class for all agents in the Vision Wagon X system.
    Provides common functionalities like configuration loading and API key access.
    """
    def __init__(self, agent_name, config=None, api_keys=None):
        self.agent_name = agent_name
        self.config = config if config else self._load_global_config()
        self.api_keys = api_keys if api_keys else self._load_api_keys()

        if not self.config:
            print(f"Warning: Agent '{self.agent_name}' initialized without global configuration.")
        if not self.api_keys:
            print(f"Warning: Agent '{self.agent_name}' initialized without API keys.")

    def _load_global_config(self):
        """Loads the global configuration."""
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config_multi.yaml')
        try:
            with open(config_path, 'r') as f:
                full_config = yaml.safe_load(f)
            env = os.getenv('ENV', 'dev')
            return full_config.get(env, full_config.get('default', {}))
        except Exception as e:
            print(f"Error loading global config for agent {self.agent_name}: {e}")
            return {}

    def _load_api_keys(self):
        """Loads API keys from environment variables or config."""
        keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "elevenlabs": os.getenv("ELEVENLABS_API_KEY"),
            "stable_diffusion": os.getenv("STABLE_DIFFUSION_API_KEY")
        }
        # Fallback to config if environment variables are not set
        if self.config and self.config.get('api_keys'):
            for key_name, env_var_value in keys.items():
                if not env_var_value: # If env var is not set
                    keys[key_name] = self.config['api_keys'].get(key_name)
        return keys

    def get_api_key(self, service_name):
        """
        Retrieves a specific API key.
        :param service_name: Name of the service (e.g., 'openai', 'elevenlabs').
        :return: The API key string or None if not found.
        """
        key = self.api_keys.get(service_name)
        if not key:
            print(f"Warning: API key for '{service_name}' not found for agent '{self.agent_name}'.")
        return key

    def execute(self, data, context=None):
        """
        Main execution method for the agent.
        This method should be overridden by subclasses.

        :param data: Input data for the agent.
        :param context: Optional context or state information.
        :return: Output data from the agent.
        """
        print(f"Agent '{self.agent_name}' received data: {data}")
        raise NotImplementedError("Subclasses must implement the 'execute' method.")

    def __str__(self):
        return f"<BaseAgent: {self.agent_name}>"

if __name__ == '__main__':
    # Example usage (for testing purposes)
    print("Testing BaseAgent...")
    agent = BaseAgent(agent_name="TestBaseAgent")
    print(f"Agent initialized: {agent}")
    print(f"Config loaded: {agent.config}")
    print(f"OpenAI Key: {agent.get_api_key('openai')}")

    try:
        agent.execute({"test_input": "hello"})
    except NotImplementedError as e:
        print(f"Caught expected error: {e}")
    print("BaseAgent test complete.")
