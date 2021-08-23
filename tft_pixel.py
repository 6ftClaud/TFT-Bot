from time import sleep

import pyautogui
import win32gui

pyautogui.FAILSAFE = False


class AutoLoL:

    hwnd = None
    screenshot = None
    rect = None
    x = None
    y = None
    w = None
    h = None

    def __init__(self):
        self.hwnd = win32gui.FindWindow(None, "League of Legends")
        if self.hwnd == 0:
            raise Exception("You must run League of Legends first.")
        self.WindowInfo()

    # Gets client position and size
    def WindowInfo(self):
        try:
            rect = win32gui.GetWindowRect(self.hwnd)
            self.x = rect[0]
            self.y = rect[1]
            self.w = rect[2] - self.x
            self.h = rect[3] - self.y
        except:
            self.hwnd = win32gui.FindWindow(None, "League of Legends")
        finally:
            if self.hwnd == 0:
                self.hwnd = win32gui.FindWindow(None, "League of Legends (TM) Client")

    def SetButtonPositions(self):
        pass

    # Adds client offset to given coordinates
    def ClickInClient(self, clickpos, time=0):
        sleep(time)
        self.WindowInfo()
        try:
            pyautogui.moveTo(clickpos[0] + self.x, clickpos[1] + self.y)
            pyautogui.mouseDown()
            sleep(0.15)
            pyautogui.mouseUp()
        except pyautogui.FailSafeException:
            pyautogui.moveTo(clickpos[0] + self.x, clickpos[1] + self.y)
            pyautogui.mouseDown()
            sleep(0.15)
            pyautogui.mouseUp()

    # Checks color of given pixel in client
    def CheckColor(self, pos):
        self.WindowInfo()
        x = pos[0] + self.x
        y = pos[1] + self.y
        try:
            rgb = pyautogui.pixel(x, y)
            return rgb
        except OSError:
            print(f"Failed to find RGB value of {pos}")

    def UpdateHwnd(self, name):
        self.hwnd = win32gui.FindWindow(None, name)
        sleep(1)


def main():
    autolol = AutoLoL()
    gameCount = 1

    # Positions and Colors in 1280x720 Client
    if autolol.w == 1280 and autolol.h == 720:
        print("Setting button positions for 1280x720 client")
        # Positions
        startButton = (545, 680)
        acceptButton = (696, 556)
        OKButton = (640, 684)
        playAgainButton = (600, 685)
        # Colors
        # startButtonColor = (30, 35, 40)
        acceptButtonColor = (30, 37, 42)
        playAgainButtonColor = (30, 35, 40)

    # Positions and Colors in 1600x900 Client
    elif autolol.w == 1600 and autolol.h == 900:
        print("Setting button positions for 1600x900 client")
        # Positions
        startButton = (743, 847) 
        acceptButton = (866, 694)
        OKButton = (800, 855)
        playAgainButton = (744, 856)
        # Colors
        # startButtonColor = (23, 49, 62)
        acceptButtonColor = (30, 37, 42)
        playAgainButtonColor = (23, 49, 62)
    else:
        raise Exception(f"Invalid client size ({autolol.w}x{autolol.h})")

    # Positions and Colors in 1920x1080 Game
    # Positions
    XPButton = (398, 952)
    refreshButton = (395, 1022)
    championCard = (582, 992)
    exitNowButton = (900, 550)
    continueButton = (963, 643)
    # Colors
    refreshButtonColor = (71, 65, 44)
    exitNowButtonColor = (8, 81, 99)
    continueButtonColor = (132, 19, 16)

    while True:
        # Count no of games
        print(f"Match count: {gameCount}")
        # Update Client position
        autolol.WindowInfo()
        # Start queue
        sleep(3)
        print("Starting queue")
        for i in range(0, 3):
            autolol.ClickInClient(startButton, 1)

        # Accept queue
        while win32gui.FindWindow(None, "League of Legends (TM) Client") == 0:
            if autolol.CheckColor(acceptButton) == acceptButtonColor:
                autolol.ClickInClient(acceptButton)
                pyautogui.moveTo(
                        ((autolol.x + autolol.w / 2), (autolol.y + autolol.h / 2))
                )
                sleep(1)
        print("Accepted match")

        # Switch to game
        print("Waiting for game to launch")
        sleep(60)
        print("Updating window handle to Game")
        autolol.UpdateHwnd("League of Legends (TM) Client")

        while True:
            # Click Exit Now if it exists
            if autolol.CheckColor(exitNowButton) == exitNowButtonColor:
                autolol.ClickInClient(exitNowButton)
                print("Game finished")
                break
            # Click Continue if it exists
            elif autolol.CheckColor(continueButton) == continueButtonColor:
                autolol.ClickInClient(continueButton)
                print("Game finished")
                break
            # If refresh champion cards button exists, level up and buy champions
            else:
                if autolol.CheckColor(refreshButton) == refreshButtonColor:
                    # Iterate over all champion cards
                    for champion in range(580, 1510, 200):
                        print("Buying champion")
                        autolol.ClickInClient((champion, championCard[1]))
                    print("Buying XP")
                    autolol.ClickInClient(XPButton)
                    pyautogui.moveTo(
                        ((autolol.x + autolol.w / 2), (autolol.y + autolol.h / 2 - 150))
                    )
                
        # Wait for Client to load
        sleep(15)
        print("Updating window handle to Client")
        autolol.UpdateHwnd("League of Legends")

        # Press OKButton button if it exists
        autolol.WindowInfo()
        while autolol.CheckColor(playAgainButton) != playAgainButtonColor:
            autolol.ClickInClient(OKButton, 2)
        # Press Play Again
        autolol.ClickInClient(playAgainButton, 3)

        gameCount += 1


if __name__ == "__main__":
    main()
