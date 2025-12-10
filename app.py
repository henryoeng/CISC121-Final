import gradio as gr
import time

# ---------- HTML + CSS BOX RENDERING WITH SMOOTH ANIMATION ----------
def render_boxes(arr, highlight=None, swap=False):
    """
    arr: list of numbers to display
    highlight: tuple (i, j) showing which indices are being compared
    swap: True when a swap just occurred -> boxes flash green
    """

    html = """
    <style>
      .container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 20px;
      }

      .box {
        width: 70px;
        height: 70px;
        background-color: #ddd;
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 28px;
        font-weight: bold;

        /* Smooth fade + slide */
        transition: all 0.55s ease-in-out;
        opacity: 1;
        transform: translateY(0px);
      }

      .compare {
        background-color: #4aa3f7 !important; /* blue */
        transform: translateY(-10px); /* slight lift */
      }

      .swap {
        background-color: #5ad65a !important; /* green */
        opacity: 0.4;
      }

      .legend {
        text-align: center;
        font-size: 16px;
        margin-top: 10px;
      }
    </style>

    <div class="container">
    """

    for idx, value in enumerate(arr):
        css_class = "box"

        if highlight and idx in highlight:
            css_class += " compare"
        if swap and idx in highlight:
            css_class += " swap"

        html += f'<div class="{css_class}">{value}</div>'

    html += "</div>"

    html += """
    <div class="legend">
        🔵 Blue = comparison &nbsp;&nbsp; 🟢 Green = swapped &nbsp;&nbsp; ⚪ Grey = idle
    </div>
    """

    return html


# ---------- SORTING STATE ----------
class BubbleSortVisualizer:
    def __init__(self, numbers):
        self.arr = numbers[:]
        self.i = 0
        self.j = 0
        self.n = len(numbers)
        self.steps_done = False

    def next_step(self):
        if self.steps_done:
            return render_boxes(self.arr), "Sorting is already complete."

        # Done?
        if self.i >= self.n - 1:
            self.steps_done = True
            return render_boxes(self.arr), "Sorting complete!"

        # comparing indices
        a, b = self.j, self.j + 1

        # Show comparison state
        compare_frame = render_boxes(self.arr, highlight=(a, b))
        time.sleep(0.25)

        # Swap?
        if self.arr[a] > self.arr[b]:
            self.arr[a], self.arr[b] = self.arr[b], self.arr[a]
            swap_frame = render_boxes(self.arr, highlight=(a, b), swap=True)
            frame_html = swap_frame
            message = f"Swapped {self.arr[b]} and {self.arr[a]}"
        else:
            frame_html = compare_frame
            message = f"No swap needed between {self.arr[a]} and {self.arr[b]}"

        # Step forward
        self.j += 1
        if self.j >= self.n - self.i - 1:
            self.j = 0
            self.i += 1

        return frame_html, message


# ---------- GRADIO UI ----------
visualizer = None

def start_sort(input_text):
    global visualizer
    try:
        nums = [int(x.strip()) for x in input_text.split(",")]
    except:
        return gr.update(), "❌ Error: Enter numbers like: 5, 3, 8, 1, 4"

    visualizer = BubbleSortVisualizer(nums)
    return render_boxes(nums), "Sorting started! Click NEXT STEP."


def next_step():
    if visualizer is None:
        return gr.update(), "❌ Start the sort first."

    return visualizer.next_step()


with gr.Blocks(css="body {text-align: center;}") as demo:
    gr.Markdown("""
    # 🔢 Bubble Sort Visualizer  
    Enter numbers like **5, 3, 8, 1, 4**  
    Then press **Start** → **Next Step** to animate the sorting.
    """)

    user_input = gr.Textbox(label="Enter numbers separated by commas", placeholder="Example: 5, 3, 8, 1, 4")

    start_btn = gr.Button("Start Sorting")
    next_btn = gr.Button("Next Step")

    output_html = gr.HTML()
    message_box = gr.Textbox(label="Message")

    start_btn.click(start_sort, inputs=user_input, outputs=[output_html, message_box])
    next_btn.click(next_step, outputs=[output_html, message_box])

demo.launch()