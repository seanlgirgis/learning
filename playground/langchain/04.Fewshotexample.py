"""Minimal example: import llm_model from another playground file."""

from watson_llm import llm_model
if __name__ == "__main__":
# 1. One-shot prompt for formal email writing
    params = {
    "max_new_tokens": 10,
    }

    prompt = """Here are few examples of classifying emotions in statements:

                Statement: 'I just won my first marathon!'
                Emotion: Joy
                
                Statement: 'I can't believe I lost my keys again.'
                Emotion: Frustration
                
                Statement: 'My best friend is moving to another country.'
                Emotion: Sadness
                
                Now, classify the emotion in the following statement:
                Statement: 'That movie was so scary I had to cover my eyes.’
                

    """
    response = llm_model(prompt, params)
    print(f"prompt: {prompt}\n")
    print(f"response : {response}\n")