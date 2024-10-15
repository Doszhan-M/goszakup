import time

def main():
    print("Hello from main.py! Running...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Shutting down gracefully.")

if __name__ == "__main__":
    main()
