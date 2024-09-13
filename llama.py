import subprocess

chat_history = []

def create_model():
    """Create the nutritionist model using the Modelfile."""
    create_model_cmd = ["ollama", "create", "nutritionist", "-f", "./Modelfile"]
    
    try:
        subprocess.run(create_model_cmd, check=True, encoding="utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Error creating the model: {e}")

def run_ollama_model():
    """Run the nutritionist model and maintain chat history."""
    global chat_history
    run_model_cmd = ["ollama", "run", "nutritionist"]

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["goodbye", "bye"]:
            break

        chat_history.append(f"User: {user_input}")

        prompt = "\n".join(chat_history)

        try:
            process = subprocess.Popen(
                run_model_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            process.stdin.write(prompt)
            process.stdin.close()

            print("Nutritionist: ", end="", flush=True)
            
            while True:
                output = process.stdout.read(1) 
                if output == "" and process.poll() is not None:
                    break
                if output:
                    print(output, end="", flush=True)

            process.wait()
            model_response = process.stdout.read().strip()

            chat_history.append(f"Nutritionist: {model_response}")
        except subprocess.CalledProcessError as e:
            print(f"Error running the model: {e}")

if __name__ == "__main__":
    create_model()
    run_ollama_model()

