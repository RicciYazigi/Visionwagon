from .base_agent import BaseAgent

class AssemblyAgent(BaseAgent):
    """
    Agent responsible for assembling outputs from various other agents
    into a cohesive final product or an intermediate structured format.
    """
    def __init__(self, config=None, api_keys=None):
        super().__init__(agent_name="AssemblyAgent", config=config, api_keys=api_keys)
        print("AssemblyAgent initialized.")

    def execute(self, data, context=None):
        """
        Assembles data from different sources.

        :param data: Dictionary containing outputs from other agents,
                     e.g., {"narrative": "...", "image_prompt": "...", "voice_script": "..."}
        :param context: Optional context.
        :return: Dictionary with the assembled output.
        """
        super().execute(data, context) # Logs and raises NotImplementedError

        print(f"AssemblyAgent received data for assembly: {data.keys()}")

        # --- Placeholder Logic ---
        # This agent would combine various inputs.
        # For example, it might take a narrative, an image prompt, and a voice script
        # and structure them for final output or further processing.

        assembled_output = {
            "title": data.get("title", "Untitled Piece"),
            "story_elements": [],
            "errors": []
        }

        if "narrative_output" in data and isinstance(data["narrative_output"], dict):
            narrative_text = data["narrative_output"].get("narrative_text")
            if narrative_text:
                assembled_output["story_elements"].append({
                    "type": "narrative",
                    "content": narrative_text
                })
            elif data["narrative_output"].get("error"):
                 assembled_output["errors"].append(f"Narrative error: {data['narrative_output']['error']}")


        if "image_prompt_output" in data and isinstance(data["image_prompt_output"], dict):
            image_prompt = data["image_prompt_output"].get("image_prompt_text")
            if image_prompt:
                 assembled_output["story_elements"].append({
                    "type": "image_suggestion",
                    "prompt": image_prompt
                })
            elif data["image_prompt_output"].get("error"):
                assembled_output["errors"].append(f"Image prompt error: {data['image_prompt_output']['error']}")


        if "voice_script_output" in data and isinstance(data["voice_script_output"], dict):
            voice_script = data["voice_script_output"].get("voice_script_text")
            if voice_script:
                assembled_output["story_elements"].append({
                    "type": "voice_over_script",
                    "script": voice_script
                })
            elif data["voice_script_output"].get("error"):
                assembled_output["errors"].append(f"Voice script error: {data['voice_script_output']['error']}")

        # Example: create a simple combined text if all parts are present
        if not assembled_output["errors"] and len(assembled_output["story_elements"]) == 3:
             assembled_output["summary"] = f"Assembled story: [NARRATIVE] {assembled_output['story_elements'][0]['content'][:50]}... [IMAGE PROMPT] {assembled_output['story_elements'][1]['prompt'][:50]}... [VOICE SCRIPT] {assembled_output['story_elements'][2]['script'][:50]}..."
        else:
            assembled_output["summary"] = "Assembly incomplete or contains errors."

        print(f"AssemblyAgent produced output with keys: {assembled_output.keys()}")

        return {"assembled_content": assembled_output}

if __name__ == '__main__':
    print("Testing AssemblyAgent...")
    agent = AssemblyAgent()

    test_data = {
        "title": "Rainy Night Romance",
        "narrative_output": {"narrative_text": "The rain poured down, mirroring the tears she couldn't hold back..."},
        "image_prompt_output": {"image_prompt_text": "A dimly lit street, rain reflecting city lights, a lone figure with an umbrella."},
        "voice_script_output": {"voice_script_text": "She whispered his name, lost in the sound of the storm."}
    }
    result = agent.execute(test_data)

    if "error" in result.get("assembled_content", {}):
        print(f"Test Error: {result['assembled_content']['error']}")
    else:
        print(f"Test Assembled Summary: {result['assembled_content'].get('summary', 'No summary')}")
        # print(f"Full Assembled Output: {result['assembled_content']}")

    test_data_with_error = {
        "narrative_output": {"error": "LLM unavailable"},
    }
    result_error = agent.execute(test_data_with_error)
    print(f"Test Assembled Summary (with error): {result_error['assembled_content'].get('summary', 'No summary')}")
    print(f"Errors reported: {result_error['assembled_content'].get('errors')}")


    print("AssemblyAgent test complete.")
