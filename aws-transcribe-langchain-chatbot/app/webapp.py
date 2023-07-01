import gradio as gr
import logging
from utils import get_prompt_results

logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    logger.debug("Launching Gradio App")
    with gr.Blocks(css="footer {visibility: hidden}") as demo:
        gr.Markdown("# 👩‍💻 Pastor Poju Oyemade virtual assistant (parody)")
        gr.Markdown("### Powered by [Covenant Nation messages](https://elibrary.insightsforliving.org/) and [Amazon Transribe](https://aws.amazon.com/transcribe/) for context,  and [ChatGPT](https://platform.openai.com/docs/api-reference), [LangChain](https://python.langchain.com/docs/get_started/introduction.html) Generative AI. App is hosted on AWS")
        gr.Markdown("This chatbot does not represent the Pastor Poju in anyway.")
        with gr.Column():
            chatbot = gr.Chatbot()
            with gr.Row():
                with gr.Column():
                    message = gr.Textbox(label="Chat with Pastor Poju bot", placeholder="Ask me a question and I will consult the Pastor Poju's sermons on Covenant Nation e-library website to answer...", show_label=False)
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
            print(prompt)

            # send request to endpoint
            llm_response = get_prompt_results(message)

            # remove prompt from response
            chat_history.append((message, llm_response))
            return "", chat_history


        submit.click(respond, [message, chatbot], [message, chatbot], queue=False)
        clear.click(lambda: None, None, chatbot, queue=False)

    demo.launch(share=False, server_port=8080, server_name="0.0.0.0", show_error=True, debug=True)
