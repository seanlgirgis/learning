"""Lab 33 — Memory (bite by bite — you type each step).

Mirror: sean_langchain_lab.ipynb — Memory + Exercise 5.

Why memory?
  LLMs are stateless. Each call only sees what you send in that call.
  Memory = store past turns and attach them to the next prompt.

Two levels in this lab:
  A. ChatMessageHistory     — manual list (you add each message)
  B. ConversationBufferMemory + ConversationChain — automatic (chain handles it)

Run set_env.ps1 before python.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\33.memory.py

Bites (do in order; run after each bite to check):
  1. Imports
  2. LLM — chat = make_watsonx_llm()
  3. ChatMessageHistory — seed hi + France question
  4. Print history.messages
  5. chat.invoke(history.messages) → add_ai_message
  6. ConversationChain + ConversationBufferMemory (verbose=True)
  7. Little-cat demo — 3 invokes, last asks "Who am I?"
  8. Exercise 5 — Alice history + memory wired into chain
  9. chat_simulation(test_inputs) — color / hiking / recall
  10. Print conversation.memory.buffer
  11. (Bonus) ConversationSummaryMemory — compare buffer sizes
"""

# --- Bite 1: imports ---
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_classic.chains import ConversationChain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from watson_llm import make_watsonx_llm

# --- Bite 2: LLM ---
parameters = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.2,
}
chat = make_watsonx_llm(parameters)
print("LLM ready:", type(chat).__name__)


# --- Bite 3: manual history (notebook: Chat message history) ---
history = ChatMessageHistory()
history.add_ai_message("hi!")
history.add_user_message("what is the capital of France?")
print("Messages stored:", len(history.messages))

# --- Bite 4: inspect ---
print("\n--- Chat history ---")
for message in history.messages:
    sender = "Human" if isinstance(message, HumanMessage) else "AI"
    print(f"{sender}: {message.content}")

# --- Bite 5: LLM sees full thread ---
print("\n--- LLM reply ---")
ai_response = chat.invoke(history.messages)
print(ai_response)

history.add_ai_message(ai_response)
print("Messages after reply:", len(history.messages))

# --- Bite 6: automatic memory (notebook: Conversation buffer) ---
print("\n--- ConversationChain (auto memory) ---")
conversation = ConversationChain(
    llm=chat,
    verbose=True,
    memory=ConversationBufferMemory(),
)
print("Chain ready")

# --- Bite 7: little cat ---
print("\n--- Little cat demo ---")

r1 = conversation.invoke(input="Hello, I am a little cat. Who are you?")
print("Turn 1:", r1["response"])

r2 = conversation.invoke(input="What can you do?")
print("Turn 2:", r2["response"])

r3 = conversation.invoke(input="Who am I?")
print("Turn 3:", r3["response"])

# --- Bite 8: Exercise 5 setup ---
print("\n--- Exercise 5: Alice ---")

alice_history = ChatMessageHistory()
alice_history.add_user_message("Hello, my name is Alice.")
alice_history.add_ai_message(
    "Hello Alice! It's nice to meet you. How can I help you today?"
)

alice_memory = ConversationBufferMemory(chat_memory=alice_history)
alice_conversation = ConversationChain(
    llm=chat,
    memory=alice_memory,
    verbose=False,
)
print("Alice chain ready — seeded with 2 messages")

# --- Bite 9: chat_simulation ---
def chat_simulation(chain, inputs):
    print("\n=== Beginning Chat Simulation ===")
    for i, user_input in enumerate(inputs):
        print(f"\n--- Turn {i + 1} ---")
        print(f"Human: {user_input}")
        response = chain.invoke(input=user_input)
        print(f"AI: {response['response']}")
    print("\n=== End of Chat Simulation ===")


test_inputs = [
    "My favorite color is blue.",
    "I enjoy hiking in the mountains.",
    "What activities would you recommend for me?",
    "What was my favorite color again?",
    "Can you remember both my name and my favorite color?",
]

chat_simulation(alice_conversation, test_inputs)

# --- Bite 10: peek inside buffer memory ---
print("\n--- Final memory buffer ---")
print(alice_conversation.memory.buffer)
print("Buffer size (chars):", len(alice_conversation.memory.buffer))

# --- Bite 11 (bonus): summary memory ---
from langchain_classic.memory import ConversationSummaryMemory

print("\n--- Bite 11: Summary memory ---")

summary_memory = ConversationSummaryMemory(llm=chat)
summary_memory.save_context(
    {"input": "Hello, my name is Alice."},
    {"output": "Hello Alice! It's nice to meet you. How can I help you today?"},
)

summary_conversation = ConversationChain(
    llm=chat,
    memory=summary_memory,
    verbose=False,
)

print("Summary chain ready")
print("Initial summary buffer:")
print(summary_memory.buffer)

# 11b

chat_simulation(summary_conversation, test_inputs)

print("\n=== Memory comparison ===")
print(f"Buffer memory size: {len(alice_conversation.memory.buffer)} chars")
print(f"Summary memory size: {len(summary_memory.buffer)} chars")
print("\nFinal summary buffer:")
print(summary_memory.buffer)