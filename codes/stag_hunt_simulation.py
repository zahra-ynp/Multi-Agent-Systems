import re
import time
import autogen
import json
import os

# Setup LLM Configuration
config_list = [
    {
        "model": "gemini-3.1-flash-lite",
        "api_key": os.environ.get("GEMINI_API_KEY"),
        "api_type": 'google',
    }
]

system_msg_base = """You are playing the Stag Hunt game. 
Your goal is to maximize your total payoff over multiple rounds. 
Payoffs:
- Both choose Stag: 3 points each.
- You choose Stag, opponent chooses Hare: You get 0, opponent gets 2.
- You choose Hare, opponent chooses Stag: You get 2, opponent gets 0.
- Both choose Hare: 1 point each.
"""

decision_prompt = """Based on the game, make your final decision for this round. 
Output ONLY a JSON object in this exact format: {"choice": "Stag"} or {"choice": "Hare"}."""

# Initialize Agents
agent_a = autogen.ConversableAgent(
    name="Agent_A",
    system_message=system_msg_base,
    llm_config={"config_list": config_list},
    human_input_mode="NEVER"
)

agent_b = autogen.ConversableAgent(
    name="Agent_B",
    system_message=system_msg_base,
    llm_config={"config_list": config_list},
    human_input_mode="NEVER"
)

def simulate_game(iterations=5, allow_communication=False):
    # Initialize separate histories for simultaneous decision making
    history_a = [{"role": "system", "content": system_msg_base}]
    history_b = [{"role": "system", "content": system_msg_base}]
    
    for i in range(iterations):
        print(f"\n--- Round {i+1} ---")
        
        #  Communication Phase
        if allow_communication:
            print("Agents are communicating...")
            
            # Agent A initiates the discussion
            msg_from_a = agent_a.generate_reply(messages=history_a + [{"role": "user", "content": "Send a short message to your opponent to coordinate your next move."}])
            history_a.append({"role": "assistant", "content": msg_from_a})
            history_b.append({"role": "user", "content": f"Opponent says: {msg_from_a}"})
            
            # Agent B replies
            msg_from_b = agent_b.generate_reply(messages=history_b + [{"role": "user", "content": "Reply to your opponent to coordinate."}])
            history_b.append({"role": "assistant", "content": msg_from_b})
            history_a.append({"role": "user", "content": f"Opponent replies: {msg_from_b}"})
            
            print(f"Agent A: {msg_from_a}")
            print(f"Agent B: {msg_from_b}")
            
        # Decision Phase
        choice_a_raw = agent_a.generate_reply(messages=history_a + [{"role": "user", "content": decision_prompt}])
        choice_b_raw = agent_b.generate_reply(messages=history_b + [{"role": "user", "content": decision_prompt}])
        
        # Robust parsing function to handle both strings and dictionaries
        def parse_choice(raw_output):
            # If AutoGen already converted it to a dictionary
            if isinstance(raw_output, dict):
                if "choice" in raw_output:
                    return raw_output.get("choice")
                # Sometimes AutoGen wraps the string in a "content" key
                raw_output = raw_output.get("content", str(raw_output))
            
            # Make absolutely sure we are working with a string
            if not isinstance(raw_output, str):
                raw_output = str(raw_output)
                
            # Run Regex to find the JSON
            match = re.search(r'\{.*?\}', raw_output, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0)).get("choice", "Error")
                except json.JSONDecodeError:
                    return "Error"
            return "Error"
        
        choice_a = parse_choice(choice_a_raw)
        choice_b = parse_choice(choice_b_raw)
        
        print(f"Result -> Agent A chose: {choice_a} | Agent B chose: {choice_b}")
        
        # Update histories with the outcome to simulate a repeated game
        history_a.append({"role": "user", "content": f"Round {i+1} result: You chose {choice_a}, Opponent chose {choice_b}."})
        history_b.append({"role": "user", "content": f"Round {i+1} result: You chose {choice_b}, Opponent chose {choice_a}."})

        time.sleep(20) # Protects free tier rate limits


# print("=== SETTING 1: NO COMMUNICATION ===")
# no_communication_results = simulate_game(iterations=5, allow_communication=False)
# with open("../results/first_game_no_communication.json", "w") as f:
#     json.dump(no_communication_results, f, indent=4)
# print("\n[SUCCESS] All data successfully saved to 'first_game_no_communication.json'!")

print("\n=== SETTING 2: WITH COMMUNICATION ===")
with_communication_results = simulate_game(iterations=5, allow_communication=True)
with open("../results/first_game_with_communication.json", "w") as f:
    json.dump(with_communication_results, f, indent=4)
print("\n[SUCCESS] All data successfully saved to 'first_game_with_communication.json'!")