from pynput.keyboard import Key, Controller, Listener

#hkeyboard = Controller()


keyboard = Controller()

# The key combination to check
COMBINATION = {Key.left, Key.right}

# The currently active modifiers
current = set()

def on_press(key):
    if key == Key.left or key == Key.right:
        #print(key)
        current.add(key)
        if all(k in current for k in COMBINATION):
            keyboard.press(Key.tab)
            #print("pressed tab")

def on_release(key):
    if key == Key.left or key == Key.right:
        current.remove(key)
        if len(current) == 1:
            #print("should be released")
            keyboard.release(Key.tab)

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()