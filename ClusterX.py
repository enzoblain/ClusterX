from src.algorithm import algorithm

from dotenv import load_dotenv
import time

def main():
    frame_width = 50
    title = "ClusterX - Trading Algorithm"
    author = "Author: Enzo Blain"
    version = "Version: 0.0.1"

    # Informations
    print("+" + "-" * frame_width + "+")
    print("|" + title.center(frame_width) + "|")
    print("|" + author.center(frame_width) + "|")
    print("|" + version.center(frame_width) + "|")
    print("+" + "-" * frame_width + "+")

    try:
        load_dotenv() # Load environment variables
    except Exception as e: 
        print("Error loading environment variables : ", e)

    print("ClusterX is running...")
    while True:
        algorithm()

        time.sleep(60) # Execute the algorithm each minute

if __name__ == "__main__":
    main()