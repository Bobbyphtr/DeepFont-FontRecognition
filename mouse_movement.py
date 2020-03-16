from pynput.mouse import Button, Controller
from pynput import keyboard
import time

mouse = Controller()

tick = 0

def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        global exit_flag
        exit_flag = True
        print("SET EXIT TO {}".format(exit_flag))
        return False


exit_flag = False

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:

    while not exit_flag: 
        mouse.position = (1308, 189)
        mouse.click(Button.left, 1)
        tick += 1
        time.sleep(30)

    listener.join()