import time
import pyautogui
from pynput import keyboard

class SnapchatBot:
    def __init__(self):
        self.running = True
        self.delay = 0.3
        self.first_time = True
        self.recipients = []

    def wait_for_key(self, target_key='f'):
        print(f"Press '{target_key.upper()}' to continue...")

        def on_press(key):
            try:
                if key.char == target_key:
                    listener.stop()
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def get_positions(self):
        print("Move mouse to the FIRST CAMERA ICON (for opening cam only once).")
        self.wait_for_key()
        self.open_camera = pyautogui.position()

        print("Move mouse to the SHUTTER BUTTON (to take the snap).")
        self.wait_for_key()
        self.camera_shutter = pyautogui.position()

        print("Move mouse to the SEND TO button.")
        self.wait_for_key()
        self.send_to = pyautogui.position()

        print("Now select your RECIPIENTS.")
        print("Move to each one and press 'F'. When you're done, press 'ENTER'.")
        def record_recipients():
            def on_press(key):
                if key == keyboard.Key.enter:
                    return False
                try:
                    if key.char == 'f':
                        pos = pyautogui.position()
                        self.recipients.append(pos)
                        print(f"✅ Added person at {pos}")
                except AttributeError:
                    pass
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        record_recipients()

        print("Move mouse to the SEND button.")
        self.wait_for_key()
        self.send_button = pyautogui.position()

    def send_snap(self):
        if self.first_time:
            pyautogui.moveTo(self.open_camera)
            pyautogui.click()
            time.sleep(self.delay)
            self.first_time = False

        pyautogui.moveTo(self.camera_shutter)
        pyautogui.click()
        time.sleep(self.delay)

        pyautogui.moveTo(self.send_to)
        pyautogui.click()
        time.sleep(self.delay)

        for person in self.recipients:
            pyautogui.moveTo(person)
            pyautogui.click()
            time.sleep(self.delay)

        pyautogui.moveTo(self.send_button)
        pyautogui.click()
        pyautogui.press('enter')
        print("✅ Snap sent!")
        time.sleep(self.delay)

    def stop_listener(self):
        def on_press(key):
            if key == keyboard.Key.esc:
                print("❌ Stopping...")
                self.running = False
                return False
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    def main(self):
        self.get_positions()
        print("Ready to send snaps. Press 'F' to begin. Press 'ESC' to stop.")
        self.wait_for_key()
        self.stop_listener()

        while self.running:
            self.send_snap()

if __name__ == "__main__":
    bot = SnapchatBot()
    bot.main()
