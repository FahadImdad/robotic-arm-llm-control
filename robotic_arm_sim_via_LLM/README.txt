# 🤖 Robotic Arm Control via LLMs

This project presents a **robotic arm simulation controlled via natural language**, utilizing a **Large Language Model (LLM)** to convert spoken commands into structured motion instructions. 🗣️🤖

Spoken phrases such as "move up by 10 centimeters" are parsed into executable **JSON commands**, enabling real-time 3D movement of a virtual robotic arm. The simulation integrates **speech recognition**, **natural language processing**, and **forward kinematics**, providing an intuitive interface for exploring **multimodal AI-based control systems**. 🌐✨

## Features 🌟:

* **🎙️ Voice Control**: Control the robotic arm with natural language commands.
* **🖥️ 3D Visualization**: Watch the robotic arm move in real-time using a 3D simulation.
* **🧠 LLM Integration**: Natural language commands are parsed by a large language model (LLM) to generate structured motion instructions.
* **🔧 Kinematics**: Forward kinematics are used to calculate and simulate the arm's movements accurately.

## 📺 Demo Video

Watch the robotic arm in action:

[![Robotic Arm Control via LLMs](https://img.youtube.com/vi/hi7t0NcHFU4/0.jpg)](https://youtu.be/hi7t0NcHFU4)


## Prerequisites 🛠️:

Before running the project, ensure you have the following:

* Python 3.x installed on your system.
* An active OpenAI API key for GPT integration.

## Installation 🔧:

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd robotic_arm_sim_via_LLM
   ```

2. **Set up the Virtual Environment**:

   * On Windows:

     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   * On macOS/Linux:

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   Install the necessary libraries by running:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the OpenAI API Key**:

   * Create an account on [OpenAI](https://beta.openai.com/signup/).
   * Copy your API key.
   * In the `voice_parser.py` file, replace `"Add API Key here"` with your API key:

     ```python
     openai.api_key = "Add API Key here"
     ```

## Usage 🚀:

1. **Activate the Virtual Environment** (if not already activated):

   * On Windows:

     ```bash
     .\.venv\Scripts\activate
     ```
   * On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

2. **Run the Simulation**:
   Start the robotic arm simulation:

   ```bash
   python robotic_arm_sim_LLM.py
   ```

   The program will begin listening for voice commands. Once you give a command (e.g., "move up by 10 centimeters"), the robotic arm will move accordingly in the simulation.

3. **Voice Commands**:
   You can say the following types of commands:

   * "Move \[direction] by \[distance]" (e.g., "move up by 10 centimeters")
   * "Rotate \[direction] by \[angle]" (e.g., "rotate left by 45 degrees")
   * "Extend" or "retract" for arm length adjustments.

   The system will interpret the command, parse it using GPT, and execute the corresponding arm movement.

## Project Structure 📁:

* **robotic\_arm\_sim\_LLM.py**: The main script that simulates the robotic arm and handles the visualization.
* **voice\_parser.py**: Responsible for voice recognition, command parsing using GPT, and text-to-speech output.
* **.venv/**: The virtual environment containing all necessary dependencies.
* ****pycache**/**: Python bytecode cache folder (automatically generated).
* **requirements.txt**: The list of dependencies required to run the project.
* **README.md**: This file.

## Dependencies 📚:

* `matplotlib`: For 3D plotting and arm visualization.
* `speech_recognition`: For recognizing voice commands.
* `pyttsx3`: For text-to-speech conversion.
* `openai`: For using the OpenAI GPT model.
* `numpy`: For mathematical computations.

To install all required dependencies, run:

```bash
pip install -r requirements.txt
```

## Contributing 🤝:

Feel free to contribute to the project! You can:

* 🐞 Report bugs.
* 💡 Suggest new features or improvements.
* 🍴 Fork the repository and create a pull request.

## License 📜:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

By Muhammad Fahad Imdad - [fahadimdad.com](http://fahadimdad.com)
