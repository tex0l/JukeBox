import thread
import threading

def raw_input_with_timeout(prompt, timeout=30.0):
    print prompt,    
    timer = threading.Timer(timeout, thread.interrupt_main)
    result = None
    try:
        timer.start()
        result = raw_input(prompt)
    except KeyboardInterrupt:
        pass
    timer.cancel()
    return result