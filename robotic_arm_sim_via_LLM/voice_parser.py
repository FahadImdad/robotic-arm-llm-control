import speech_recognition as sr
import pyttsx3
import json
from openai import OpenAI

# === Set your OpenAI API key ===
client = OpenAI(api_key="Add API key here")  # Replace with your real API key

# === Text-to-speech engine ===
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("🗣️ Speaking:", text)
    engine.say(text)
    engine.runAndWait()

def listen(max_attempts=3):
    recognizer = sr.Recognizer()

    for attempt in range(max_attempts):
        with sr.Microphone() as source:
            print("🎧 Listening... You have up to 8 seconds to speak.")
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # better noise filtering
                print("🕒 Speak now...")

                # Increased listening window
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)

                # Try recognizing
                text = recognizer.recognize_google(audio)
                print("📝 Heard:", text)
                return text

            except sr.UnknownValueError:
                print("🤷 Sorry, I didn't catch that. Please try again.")

            except sr.WaitTimeoutError:
                print("⏰ Timeout. You didn’t speak in time.")

            except Exception as e:
                print("❌ Recognition error:", e)

    print("❌ Max attempts reached. Returning None.")
    return None


def gpt_parse_command(prompt):
    try:
        print("🧠 Sending to GPT:", prompt)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a robotic arm controller. Convert the user's voice command into a JSON object "
                        "with the following fields: task, direction, distance_cm, and action. Use null for any field "
                        "you cannot determine."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "parse_movement_command",
                        "description": "Parse robotic arm instruction.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task": {"type": "string"},
                                "direction": {
                                    "type": "string",
                                    "enum": ["left", "right", "up", "down", "forward", "backward"]
                                },
                                "distance_cm": {"type": "number"},
                                "action": {"type": "string"}
                            },
                            "required": ["task", "direction", "distance_cm", "action"]
                        }
                    }
                }
            ],
            tool_choice={"type": "function", "function": {"name": "parse_movement_command"}}
        )

        # Extract and parse tool arguments
        tool_call = response.choices[0].message.tool_calls[0]
        arguments_str = tool_call.function.arguments
        print("📦 Raw tool arguments:", arguments_str)

        parsed = json.loads(arguments_str)
        print("✅ Parsed JSON:", parsed)
        return parsed

    except Exception as e:
        print("❌ GPT Function Call Error:", e)
        return None
