import gradio as gr
import assistant_model

gr.ChatInterface(assistant_model.augmented_llm, title = "📉🫠 Fantasy Stonks Assistant 💸💸", examples = 
                 ["Should I invest in Nvidia?", "Which stocks in my portfolio should I sell?", "Recommend some trending stocks."], 
                 theme="freddyaboulton/test-blue", submit_btn = None, stop_btn = None, retry_btn = None, 
                 undo_btn = None, clear_btn = None).launch()

