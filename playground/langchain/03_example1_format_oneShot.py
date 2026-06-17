"""Minimal example: import llm_model from another playground file."""

from watson_llm import llm_model

if __name__ == "__main__":
# 1. One-shot prompt for formal email writing
    formal_email_prompt = """
    Here is an example of a formal email requesting information:

    Subject: Inquiry Regarding Product Specifications for Model XYZ-100

    Dear Customer Support Team,

    I hope this email finds you well. I am writing to request detailed specifications for your product Model XYZ-100. Specifically, I am interested in learning about its dimensions, power requirements, and compatibility with third-party accessories.

    Could you please provide this information at your earliest convenience? Additionally, I would appreciate any available documentation or user manuals that you could share.

    Thank you for your assistance in this matter.

    Sincerely,
    John Smith

    ---

    Now, please write a formal email to a university admissions office requesting information about their application deadline and required documents for the Master's program in Computer Science:

    """
    # 2. One-shot prompt for simplifying technical concepts
    technical_concept_prompt = """
    Here is an example of explaining a technical concept in simple terms:

    Technical Concept: Blockchain
    Simple Explanation: A blockchain is like a digital notebook that many people have copies of. When someone writes a new entry in this notebook, everyone's copy gets updated. Once something is written, it can't be erased or changed, and everyone can see who wrote what. This makes it useful for recording important information that needs to be secure and trusted by everyone.

    ---

    Now, please explain the following technical concept in simple terms:

    Technical Concept: Machine Learning
    Simple Explanation:
    """
    # 3. One-shot prompt for keyword extraction
    keyword_extraction_prompt = """
    Here is an example of extracting keywords from a sentence:

    Sentence: "Cloud computing offers businesses flexibility, scalability, and cost-efficiency for their IT infrastructure needs."
    Keywords: cloud computing, flexibility, scalability, cost-efficiency, IT infrastructure

    ---

    Now, please extract the main keywords from the following sentence:

    Sentence: "Sustainable agriculture practices focus on biodiversity, soil health, water conservation, and reducing chemical inputs."
    Keywords:
    """
    responses = {}
    responses["formal_email"] = llm_model(formal_email_prompt)
    responses["technical_concept"] = llm_model(technical_concept_prompt)
    responses["keyword_extraction"] = llm_model(keyword_extraction_prompt)

    for prompt_type, response in responses.items():
        print('-' * 150)
        print(f"=== {prompt_type.upper()} RESPONSE ===")
        print(response)
        print()