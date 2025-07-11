from .base_agent import BaseAgent

class AdultComplianceAgent(BaseAgent):
    """
    Agent responsible for checking content against adult content policies,
    age verification guidelines, or other compliance requirements.
    This is a placeholder and would need real policy logic or API integration.
    """
    def __init__(self, config=None, api_keys=None):
        super().__init__(agent_name="AdultComplianceAgent", config=config, api_keys=api_keys)
        # Potentially load rule sets or connect to a compliance service here
        self.compliance_rules = self.config.get("compliance_rules", {})
        print("AdultComplianceAgent initialized.")
        if not self.compliance_rules:
            print("Warning: AdultComplianceAgent has no specific compliance rules loaded from config.")

    def execute(self, data, context=None):
        """
        Checks the provided content for compliance.

        :param data: Dictionary containing content to be checked,
                     e.g., {"text_content": "...", "image_description": "..."}
        :param context: Optional context.
        :return: Dictionary with 'compliance_status' ('approved', 'rejected', 'needs_review')
                 and 'issues' (list of identified problems).
        """
        super().execute(data, context) # Logs and raises NotImplementedError

        text_content = data.get("text_content", "")
        image_description = data.get("image_description", "") # Or actual image data in a real scenario

        print(f"AdultComplianceAgent received content for review. Text length: {len(text_content)}, Image desc: '{image_description}'")

        # --- Placeholder Logic ---
        # In a real implementation, this would involve:
        # - Checking text against keyword lists (e.g., self.compliance_rules.get('forbidden_keywords'))
        # - Using an image moderation API for image_data
        # - Applying more complex rule-based logic

        issues = []
        compliance_status = "approved" # Default to approved for placeholder

        # Example placeholder check:
        if "illegal_activity_simulation" in text_content.lower(): # A very basic rule
            issues.append("Text contains potentially problematic simulated content.")
            compliance_status = "rejected"

        if self.compliance_rules.get("enforce_age_appropriateness"):
            if "underage_looking_character" in image_description.lower():
                issues.append("Image description suggests potentially non-compliant depiction.")
                compliance_status = "needs_review"

        if not text_content and not image_description:
            issues.append("No content provided for compliance check.")
            compliance_status = "rejected"

        result = {
            "compliance_status": compliance_status,
            "issues": issues,
            "checked_items": {"text": bool(text_content), "image_description": bool(image_description)}
        }

        print(f"AdultComplianceAgent completed review. Status: {result['compliance_status']}, Issues: {len(result['issues'])}")

        return result

if __name__ == '__main__':
    print("Testing AdultComplianceAgent...")
    # Example config that might be loaded
    mock_config = {
        "env": "dev",
        "compliance_rules": {
            "forbidden_keywords": ["bad_word1", "bad_word2"],
            "enforce_age_appropriateness": True
        }
    }
    agent = AdultComplianceAgent(config=mock_config)

    test_data_approved = {
        "text_content": "A romantic story between consenting adults.",
        "image_description": "Two adults sharing a sunset view."
    }
    result_approved = agent.execute(test_data_approved)
    print(f"Approved Test - Status: {result_approved['compliance_status']}, Issues: {result_approved['issues']}")

    test_data_rejected = {
        "text_content": "This story involves illegal_activity_simulation which is not allowed.",
        "image_description": "A generic scene."
    }
    result_rejected = agent.execute(test_data_rejected)
    print(f"Rejected Test - Status: {result_rejected['compliance_status']}, Issues: {result_rejected['issues']}")

    test_data_review = {
        "text_content": "A fantasy story.",
        "image_description": "Character described as an underage_looking_character in a neutral context."
    }
    result_review = agent.execute(test_data_review)
    print(f"Needs Review Test - Status: {result_review['compliance_status']}, Issues: {result_review['issues']}")

    print("AdultComplianceAgent test complete.")
