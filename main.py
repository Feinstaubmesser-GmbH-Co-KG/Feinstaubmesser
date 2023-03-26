from database import Configuration as configuration


def start():
    print("Starting program...")
    # . . . . . . . . .
    # . program logic .
    # . . . . . . . . .
    # Start Tkinter GUI here...
    # Fetch required data for "Start menu"???
    # continue in button logic descriptor for further database calls...
    print(configuration.execute("SELECT * FROM sensor_3660"))
    print("Exiting...")
