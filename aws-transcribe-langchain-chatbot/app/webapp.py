import gradio as gr


# hyperparameters for llm
parameters = {
    "do_sample": True,
    "top_p": 0.7,
    "temperature": 0.7,
    "top_k": 50,
    "max_new_tokens": 256,
    "repetition_penalty": 1.03,
    "stop": ["<|endoftext|>"]
  }

with gr.Blocks() as demo:
    gr.Markdown("## Chat with Pastor Poju bot")
    with gr.Column():
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column():
                message = gr.Textbox(label="Chat Message Box", placeholder="Chat Message Box", show_label=False)
            with gr.Column():
                with gr.Row():
                    submit = gr.Button("Submit")
                    clear = gr.Button("Clear")

    def respond(message, chat_history):
        # convert chat history to prompt
        converted_chat_history = ""
        if len(chat_history) > 0:
          for c in chat_history:
            converted_chat_history += f"<|prompter|>{c[0]}<|endoftext|><|assistant|>{c[1]}<|endoftext|>"
        prompt = f"{converted_chat_history}<|prompter|>{message}<|endoftext|><|assistant|>"

        # send request to endpoint
        llm_response = llm.predict({"inputs": prompt, "parameters": parameters})

        # remove prompt from response
        parsed_response = llm_response[0]["generated_text"][len(prompt):]
        chat_history.append((message, parsed_response))
        return "", chat_history

    submit.click(respond, [message, chatbot], [message, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(share=True)
