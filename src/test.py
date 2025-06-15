import gradio as gr
import random

questions = [
    ["I can play the guitar", "I’ve met the president", "I’ve never used a smartphone,I’ve never used a smartphone,I’ve never used a smartphone,I’ve never used a smartphone"],
    ["I have been skydiving", "I am allergic to water", "I have eaten bugs"],
    ["I speak five languages", "I’ve been to space", "I love spicy food"],
    ["I have a pet snake", "I hate chocolate", "I sleep only 2 hours a day"],
    ["I broke my arm as a kid", "I hate ice cream", "I’ve never watched TV"],
    ["I’ve met a Bollywood star", "I’m afraid of balloons", "I can hold my breath for 10 minutes"],
    ["I ran a marathon", "I hate music", "I’ve never seen snow"],
    ["I’ve swum with sharks", "I’ve never eaten pizza", "I love broccoli"],
    ["I’ve gone viral on Instagram", "I dislike colors", "I can’t ride a bike"],
    ["I’ve been in a movie", "I don’t have a phone", "I’ve never lied"]
]

images = ["image.png"] * 10  # Replace with real images or URLs if available

game_state = {
    "current_index": 0,
    "audience_score": 0,
    "ai_score": 0,
    "ai_guess": "",
    "game_over": False
}

def get_question():
    index = game_state["current_index"]
    if index >= len(questions):
        return "", "", "", "🎉 Game Over!", None
    q = questions[index]
    question_number = f"📍 Question {index + 1} of {len(questions)}"
    return q[0], q[1], q[2], question_number, images[index]

def ask_ai(choice1, choice2, choice3):
    if game_state["game_over"]:
        return "Game has ended!"
    guess = random.choice([choice1, choice2, choice3])
    game_state["ai_guess"] = guess
    return f"🤖 AI guesses the lie is: “{guess}”"

def submit_winner(winner):
    if game_state["game_over"]:
        return get_leaderboard()

    if winner == "Audience":
        game_state["audience_score"] += 1
    elif winner == "AI":
        game_state["ai_score"] += 1

    is_last = game_state["current_index"] >= len(questions) - 1
    leaderboard = get_leaderboard()

    if is_last:
        game_state["game_over"] = True
        leaderboard += f"\n\n🎉 Game Over! {determine_winner()}"

    return leaderboard

def get_leaderboard():
    return f"🏆 Leaderboard: Audience 🧍‍♀️ {game_state['audience_score']} — 🤖 AI {game_state['ai_score']}"

def determine_winner():
    if game_state["audience_score"] > game_state["ai_score"]:
        return "🎊 Audience Wins!"
    elif game_state["ai_score"] > game_state["audience_score"]:
        return "🤖 AI Wins!"
    else:
        return "It’s a tie! 👯"

def next_question():
    if game_state["game_over"]:
        return "🎮 Game Over!", "", "", "", "", None
    game_state["current_index"] += 1
    if game_state["current_index"] >= len(questions):
        return "🎮 Game Over!", "", "", "", "", None
    return get_question() + ("",)  # add blank AI guess

def reset_game():
    game_state.update({
        "current_index": 0,
        "audience_score": 0,
        "ai_score": 0,
        "ai_guess": "",
        "game_over": False
    })
    return get_question() + ("", "")  # blank AI + leaderboard

with gr.Blocks() as demo:
    gr.Markdown("# 🎭 Two Truths and a Lie - Game Night!")

    question_number = gr.Markdown("📍 Question 1 of 10")
    image_box = gr.Image(height=500, width=500, show_label=False, show_download_button=False, label="🧑 Person Playing")

    with gr.Row():
        choice1 = gr.Textbox(label="Statement 1", interactive=False)
        choice2 = gr.Textbox(label="Statement 2", interactive=False)
        choice3 = gr.Textbox(label="Statement 3", interactive=False)

    ai_response = gr.Textbox(label="🤖 AI's Guess", interactive=False)

    with gr.Row():
        ask_btn = gr.Button("🧠 Ask AI")
        audience_btn = gr.Button("✅ Audience Wins")
        ai_btn = gr.Button("✅ AI Wins")

    leaderboard = gr.Textbox(label="🏆 Leaderboard", interactive=False)

    with gr.Row():
        next_btn = gr.Button("➡️ Next Question")
        reset_btn = gr.Button("🔄 Restart Game")

    # Bind UI events
    ask_btn.click(ask_ai, inputs=[choice1, choice2, choice3], outputs=ai_response)
    audience_btn.click(lambda: submit_winner("Audience"), outputs=leaderboard)
    ai_btn.click(lambda: submit_winner("AI"), outputs=leaderboard)
    next_btn.click(next_question, outputs=[choice1, choice2, choice3, question_number, image_box, ai_response])
    reset_btn.click(reset_game, outputs=[choice1, choice2, choice3, question_number, image_box, ai_response, leaderboard])

    # Force init on page load
    demo.load(
        fn=lambda: get_question() + ("",),
        inputs=[],
        outputs=[choice1, choice2, choice3, question_number, image_box, ai_response]
    )

demo.launch(server_name="0.0.0.0", server_port=8080)
