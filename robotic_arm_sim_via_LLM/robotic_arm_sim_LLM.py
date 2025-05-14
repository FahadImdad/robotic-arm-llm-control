import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from mpl_toolkits.mplot3d import Axes3D
import threading
import time
import json
from voice_parser import listen, speak, gpt_parse_command

L1, L2 = 50, 30  # Arm segment lengths scaled for large display

def forward_kinematics(theta1, theta2, elevation=np.radians(0)):
    x0, y0, z0 = 0, 0, 0

    x1 = L1 * np.cos(theta1) * np.cos(elevation)
    y1 = L1 * np.sin(theta1) * np.cos(elevation)
    z1 = L1 * np.sin(elevation)

    x2 = x1 + L2 * np.cos(theta1 + theta2) * np.cos(elevation)
    y2 = y1 + L2 * np.sin(theta1 + theta2) * np.cos(elevation)
    z2 = z1 + L2 * np.sin(elevation)

    return [(x0, y0, z0), (x1, y1, z1), (x2, y2, z2)]

def command_to_angles(parsed):
    direction = parsed.get("direction", "").lower()
    print("🎯 Direction from GPT:", direction)

    if direction == "right":
        return np.radians(30), np.radians(30), np.radians(0)
    elif direction == "left":
        return np.radians(150), np.radians(-60), np.radians(0)
    elif direction == "up":
        return np.radians(90), np.radians(0), np.radians(35)
    elif direction == "down":
        return np.radians(90), np.radians(0), np.radians(-35)
    else:
        raise ValueError("Unknown direction")

class RoboticArmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robotic Arm Control via LLMs")
        self.root.geometry("1300x1000")

        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.view_init(elev=30, azim=45)
        self.canvas = tkagg.FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.status = tk.Label(root, text="🎙️ Listening for commands...", font=("Arial", 28), fg="blue")
        self.status.pack(pady=10)

        self.text_box = tk.Text(root, height=10, font=("Courier", 24))
        self.text_box.pack(padx=10, pady=10)

        self.current_joints = forward_kinematics(0, 0, 0)
        self.draw_arm(self.current_joints)

        threading.Thread(target=self.voice_loop, daemon=True).start()

    def draw_arm(self, joints):
        self.ax.clear()
        self.ax.view_init(elev=30, azim=45)

        x_vals = [p[0] for p in joints]
        y_vals = [p[1] for p in joints]
        z_vals = [p[2] for p in joints]

        # Plot arm
        self.ax.plot(x_vals, y_vals, z_vals, 'o-', linewidth=8, markersize=14,
                    markerfacecolor='gray', markeredgecolor='black', color='silver')
        self.ax.scatter(*joints[2], color='green', s=160)

        # Plot floor plane
        x_plane = np.array([[-100, -100], [100, 100]])
        y_plane = np.array([[-100, 100], [-100, 100]])
        z_plane = np.zeros_like(x_plane)
        self.ax.plot_surface(x_plane, y_plane, z_plane, color='lightgray', alpha=0.2)

        # Add directional arrows with labels
        arrow_len = 60
        self.ax.quiver(0, 0, 0, arrow_len, 0, 0, color='blue', linewidth=3)
        self.ax.text(arrow_len, 0, 0, '→ Right', fontsize=14, fontweight='bold', color='blue')

        self.ax.quiver(0, 0, 0, -arrow_len, 0, 0, color='blue', linewidth=3)
        self.ax.text(-arrow_len, 0, 0, '← Left', fontsize=14, fontweight='bold', color='blue')

        self.ax.quiver(0, 0, 0, 0, arrow_len, 0, color='green', linewidth=3)
        self.ax.text(0, arrow_len, 0, '↑ Forward', fontsize=14, fontweight='bold', color='green')

        self.ax.quiver(0, 0, 0, 0, -arrow_len, 0, color='green', linewidth=3)
        self.ax.text(0, -arrow_len, 0, '↓ Backward', fontsize=14, fontweight='bold', color='green')

        self.ax.quiver(0, 0, 0, 0, 0, arrow_len, color='purple', linewidth=3)
        self.ax.text(0, 0, arrow_len, '⬆ Up', fontsize=14, fontweight='bold', color='purple')

        self.ax.quiver(0, 0, 0, 0, 0, -arrow_len, color='purple', linewidth=3)
        self.ax.text(0, 0, -arrow_len, '⬇ Down', fontsize=14, fontweight='bold', color='purple')

        # Axis settings
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)
        self.ax.set_zlim(-100, 100)
        self.ax.set_xlabel("X Axis (Left-Right)", fontsize=18, labelpad=20, fontweight='bold')
        self.ax.set_ylabel("Y Axis (Forward-Back)", fontsize=18, labelpad=20, fontweight='bold')
        self.ax.set_zlabel("Z Axis (Up-Down)", fontsize=18, labelpad=20, fontweight='bold')
        self.ax.tick_params(axis='both', labelsize=14)
        self.ax.grid(True)
        self.canvas.draw()



    def animate_arm(self, target_joints, steps=10, delay=0.01):
        for i in range(1, steps + 1):
            intermediate = [
                (c[0] + (t[0] - c[0]) * i / steps,
                 c[1] + (t[1] - c[1]) * i / steps,
                 c[2] + (t[2] - c[2]) * i / steps)
                for c, t in zip(self.current_joints, target_joints)
            ]
            self.draw_arm(intermediate)
            self.root.update()
            time.sleep(delay)
        self.current_joints = target_joints

    def execute(self, heard, parsed):
        print("🔍 Received parsed command:", parsed)
        try:
            theta1, theta2, elevation = command_to_angles(parsed)
            joints = forward_kinematics(theta1, theta2, elevation)
            self.animate_arm(joints)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, f"Heard: {heard}\n\nParsed:\n{json.dumps(parsed, indent=4)}")
            self.status.config(text=f"✅ Executed: {parsed['direction'].capitalize()}")
            speak(f"Moving {parsed['direction']}")
        except Exception as e:
            print("❌ Error in execute():", e)
            speak("Sorry, I couldn't move.")
            if self.status.winfo_exists():
                self.status.config(text=f"Error: {str(e)}")

    def update_status_safe(self, text):
        if self.status.winfo_exists():
            self.status.config(text=text)

    def voice_loop(self):
        time.sleep(20)
        while True:
            heard = listen()
            if heard:
                self.root.after(0, self.update_status_safe, f"Heard: {heard}")
                parsed = gpt_parse_command(heard)
                if parsed:
                    self.root.after(0, self.execute, heard, parsed)
                else:
                    self.root.after(0, self.update_status_safe, "❌ GPT didn't return valid output.")
                    speak("Sorry, I didn't understand.")

if __name__ == "__main__":
    print("🚀 Launching Robotic Arm App...")
    root = tk.Tk()
    app = RoboticArmApp(root)
    root.mainloop()
