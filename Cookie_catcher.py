from tkinter import *
import random

# Define the window configuration.
def configure_window():
    window.geometry("1280x720")
    window.configure(bg='black')
    window.title("Cookie Catcher")

window = Tk()
configure_window()

# Main game loop
def game_loop():
    destroy_start()
    default_keys()
    game.itemconfig(catcher, state= 'normal') # Make catcher visible
    game.coords(catcher, CATCHER_X_COORD, 650) # Update catcher position
    create_enemies()
    create_cookies()
    falling_objects()
    check_catcher()

# Allow the catcher to move left or right with restrictive range
def move_catcher(event):
    global CATCHER_X_COORD
    if GAMEOVER is False:
        leftborder = CATCHER_X_COORD > 0
        rightborder = CATCHER_X_COORD < CANVAS_WIDTH - CATCHER_IMAGE_SIZE
        if event.keysym == MOVE_LEFT_KEY and leftborder:
            CATCHER_X_COORD -= 20
            game.move(catcher, -20, 0)
        if event.keysym == MOVE_RIGHT_KEY and rightborder:
            CATCHER_X_COORD += 20
            game.move(catcher, 20, 0)

# Repeatedly create enemies after certain amount of time
def create_enemies():
    if GAMEOVER is False:
        x_coord = random.randrange(30, CANVAS_WIDTH - ENEMIES_IMAGE_SIZE, 20)
        y_coord = 0
        enemies = game.create_image(x_coord, y_coord, image = enemies_image)
        enemies_list.append(enemies)
        game.after(ENEMIES_CREATE_TIME, create_enemies)

# Repeatedly create cookies after certain amount of time
def create_cookies():
    if GAMEOVER is False:
        x_coord = random.randrange(30, CANVAS_WIDTH - COOKIE_IMAGE_SIZE, 20)
        y_coord = 0
        cookies = game.create_image(x_coord, y_coord, image = cookie_image)
        cookies_list.append(cookies)
        game.after(COOKIE_CREATE_TIME, create_cookies)

# Set the enemies to fall down from the top
def falling_objects():
    if GAMEOVER is False:
        for enemies in enemies_list:
            game.move(enemies, 0, 5)
        for cookies in cookies_list:
            game.move(cookies, 0, 5)
        game.after(FALL_SPEED, falling_objects)

# Get points if cookie in catcher and lose if enemies in catcher
def check_catcher():
    for cookies in cookies_list:
        (cookies_x_coord, cookies_y_coord) = game.coords(cookies)
        # Check whether the cookie coordinates is within the catcher
        if CATCHER_X_COORD < cookies_x_coord < (CATCHER_X_COORD + CATCHER_IMAGE_SIZE) and 670 <= cookies_y_coord <= 700:
            cookies_list.remove(cookies)
            game.delete(cookies)
            record_score()

    for enemies in enemies_list:
        enemies_x_coord, enemies_y_coord = game.coords(enemies)
        # Check whether the enemy coordinates is within the catcher
        if CATCHER_X_COORD < enemies_x_coord < (CATCHER_X_COORD + ENEMIES_IMAGE_SIZE) and 670 <= enemies_y_coord <= 700:
            enemies_list.remove(enemies)
            game.delete(enemies)
            if CHEAT is True:
                record_score()
            # If CHEAT code is not on and player catch a enemy,
            # they lose the game and get shown the leaderboard
            # while having the option to record their SCORE in the leaderboard.
            else:
                global GAMEOVER
                GAMEOVER = True
                leaderboard_window()
                enter_name()

    game.after(50, check_catcher)

# Record the current SCORE and increase difficulty for every 50 points the user get.
def record_score():
    global SCORE
    SCORE += 10
    SCORELabel.config(text = "SCORE: " + str(SCORE))
    inc_diff()

# Increase the difficulty of the game.
# As the player SCORE increases, the fall speed of the objects are gonna become faster,
# less cookies will be generated and more enemies will be generated.
def inc_diff():
    global FALL_SPEED, COOKIE_CREATE_TIME, ENEMIES_CREATE_TIME
    if FALL_SPEED > 10:
        FALL_SPEED -= 2
    COOKIE_CREATE_TIME += 20
    if ENEMIES_CREATE_TIME > 200:
        ENEMIES_CREATE_TIME -= 20

# Window to allow user to input their name and save it alongside the SCORE to leaderboard.txt
def enter_name():
    name = Toplevel(window)
    name.title("Enter name for leaderboard")

    user_input = Text(name, width= 40, height= 1)
    user_input.pack()

    # Save username to leaderboard.txt with their SCORE once they click Save
    # If user does not input any name, they will be save as Guest instead.
    def save_leaderboard():
        username = user_input.get(1.0, "end-1c")
        if username == "" or username.isspace() is True:
            username = "Guest"
        with open("leaderboard.txt", "a") as file:
            file.write(str(username) + " " + str(SCORE) + "\n")
        window.quit()

    save_name_button = Button(name, text = "Save", highlightbackground = "white", command = save_leaderboard)
    save_name_button.pack()

# Opens a new window that display the leaderboard in a table.
def leaderboard_window():
    leaderboard = Toplevel(window)
    leaderboard.title("Leaderboard")

    with open("leaderboard.txt", "r") as file:
        data = file.readlines()

    # Split the data in the text file into [Name, Points] list and store them in tmp2
    tmp2 = []

    # Add actual username and points to the list
    for i in range(len(data)):
        tmp = data[i]
        tmp = tmp.split()
        tmp[1] = int(tmp[1])
        tmp2.append(list(tmp))

    # Sort the points in descending order
    tmp2 = sorted(tmp2, key=lambda x: x[1], reverse = True)

    # Create a entry widget and input the details from the text file.
    rows = len(tmp2)
    columns = len(tmp2[0])
    for i in range(rows):
        for j in range (columns):
            table = Entry(leaderboard)
            Name = Label(leaderboard, text = "Name", font=("Comic-Sans", 30), bg = "blue", fg = "white")
            Points = Label(leaderboard, text = "Points", font=("Comic-Sans", 30), bg = "blue", fg = "white")
            Name.grid(row= 0, column= 0)
            Points.grid(row= 0, column = 1)
            table.grid(row=i + 1, column=j)
            table.insert(END, tmp2[i][j])

# CHEAT code where player can eat both good and bad cookie and still gain points.
# This CHEAT code basically grants player invulnerability
def cheat_code(event):
    global CHEAT
    if CHEAT is False:
        CHEAT = True
        print("CHEAT ON")
    else:
        CHEAT = False
        print("CHEAT OFF")

# Pause the game by pressing Shift-P
def pause_game(event):
    global GAMEOVER
    global game_pause_img
    if GAMEOVER is False:
        GAMEOVER = True
        print("Game Paused")
        game_pause_img = game.create_image(640, 360, image = pause_image)
    else:
        GAMEOVER = False
        game.delete(game_pause_img)
        print("Game Resumed")
        create_enemies()
        create_cookies()
        falling_objects()

# Open a new window that mimic a working screen
def boss_window(event):
    global BOSS
    global WORK_SCREEN
    pause_game(event)
    if BOSS is False:
        BOSS = True
        print("Opened BOSS window")
        WORK_SCREEN = Toplevel(window)
        WORK_SCREEN.title("Word.doc")

        fake_screen = Canvas(WORK_SCREEN, width= 1920, height= 1080)
        fake_screen.pack(fill= "both", expand = True)
        fake_screen.create_image(0, 0, image = fake_work_image, anchor = "nw")
        WORK_SCREEN.bind("<Shift-B>", boss_window)
    else:
        BOSS = False
        print("Close BOSS window")
        WORK_SCREEN.destroy()

# Save the game and store the data into a text file called save.txt and then close the game.
def save_game(event):
    with open("save.txt", "w") as file:
        temp = [SCORE, COOKIE_CREATE_TIME, ENEMIES_CREATE_TIME, FALL_SPEED]
        for data in temp:
            file.write("%s\n" % data)
        print("Game saved")
        window.quit()

# Load the last saved game data into the game and run it
def load_data():
    with open("save.txt", "r") as file:
        data = file.read()
        game_data = data.split("\n")
        print("Load last saved game data")
        global SCORE, COOKIE_CREATE_TIME, ENEMIES_CREATE_TIME, FALL_SPEED
        SCORE = int(game_data[0])
        COOKIE_CREATE_TIME = int(game_data[1])
        ENEMIES_CREATE_TIME = int(game_data[2])
        FALL_SPEED = int(game_data[3])
        SCORELabel.config(text = "SCORE: " + str(SCORE))
        game_loop()

# Clear all the start_screen buttons and labels
def destroy_start():
    instrucions.destroy()
    instrucions1.destroy()
    instrucions2.destroy()
    instrucions3.destroy()
    start_button.destroy()
    option_button.destroy()
    leaderboard_button.destroy()
    load_button.destroy()

# Default keys of the game and only activate them when the game start
def default_keys():
    window.bind("<KeyPress>", move_catcher)
    window.bind("<Shift-C>", cheat_code)
    window.bind("<Shift-P>", pause_game)
    window.bind("<Shift-S>", save_game)
    window.bind("<Shift-B>", boss_window)

# Open the options window allowing user to perform some customization and display controls
def controls_window():
    controls_screen = Toplevel(window)
    controls_screen.title("Controls")
    controls_screen.geometry("800x500")

    # Set testing to change moving left key for change_key() function
    def change_left_key():
        global CHANGING_LEFT
        CHANGING_LEFT = True
        set_key()

    # Set testing to change moving right key for change_key() function
    def change_right_key():
        global CHANGING_RIGHT
        CHANGING_RIGHT = True
        set_key()

    # Open a new window asking user to choose a key they want
    def set_key():
        global input_change
        input_change = Toplevel(controls_screen)
        input_change.title("Input key change")
        input_change.geometry("280x25")

        blank_label = Label(input_change, text = "Please press the key you want to set it to: ")
        blank_label.grid(row = 0, column = 0, sticky=N+S+E+W)
        input_change.bind("<KeyPress>", change_key)

    # Change the default keys according to user input
    # Once receive user input, overwrite the original button with the new
    # button with the new user inputted value.
    def change_key(event):
        global MOVE_LEFT_KEY
        global MOVE_RIGHT_KEY
        global CHANGING_LEFT
        global CHANGING_RIGHT
        tmp = event.keysym

        if CHANGING_LEFT is True:
            MOVE_LEFT_KEY = event.keysym
            CHANGING_LEFT = False
            move_left_button = Button(controls_screen, text = MOVE_LEFT_KEY, command = change_left_key)
            move_left_button.grid(row = 3, column = 1, sticky=N+S+E+W)
            input_change.destroy()

        if CHANGING_RIGHT is True:
            MOVE_RIGHT_KEY = event.keysym
            CHANGING_RIGHT = False
            move_right_button = Button(controls_screen, text = MOVE_RIGHT_KEY, command = change_right_key)
            move_right_button.grid(row = 4, column = 1, sticky=N+S+E+W)
            input_change.destroy()

    # Dynamically resize the grid
    for x in range(10):
        controls_screen.columnconfigure(x, weight = 1)
        controls_screen.rowconfigure(x, weight = 1)

    home_button = Button(controls_screen, text = "Back to home screen", command = controls_screen.destroy)
    home_button.grid(row = 0, column = 0, sticky=NW)

    explanation = Label(controls_screen, text = "You can change 'Move left' and 'Move right'", font=("Arial", 30), bg= "black", fg= "white")
    explanation.grid(row = 1, columnspan = 2, sticky = N+S+E+W)

    explanation1 = Label(controls_screen, text = "by clicking on the button", font=("Arial", 30), bg= "black", fg="white")
    explanation1.grid(row = 2, columnspan = 2, sticky = N+S+E+W)

    move_left_label = Label(controls_screen, text = "Move left", font=("Arial", 20), bg= "black", fg="white")
    move_left_label.grid(row = 3, column = 0, sticky = W)

    move_left_button = Button(controls_screen, text = MOVE_LEFT_KEY, command = change_left_key)
    move_left_button.grid(row = 3, column = 1, sticky=N+S+E+W)

    move_right_label = Label(controls_screen, text = "Move right", font=("Arial", 20), bg= "black", fg="white")
    move_right_label.grid(row = 4, column = 0, sticky = W)

    move_right_button = Button(controls_screen, text = MOVE_RIGHT_KEY, command = change_right_key)
    move_right_button.grid(row = 4, column = 1, sticky=N+S+E+W)

    cheat_label = Label(controls_screen, text = "Cheat mode", font=("Arial", 20), bg= "black", fg="white")
    cheat_label.grid(row = 5, column = 0, sticky = W)

    cheat_button = Button(controls_screen, text = "Shift + C", command = None)
    cheat_button.grid(row = 5, column = 1, sticky=N+S+E+W)

    pause_label = Label(controls_screen, text = "Pause the game", font=("Arial", 20), bg= "black", fg="white")
    pause_label.grid(row = 6, column = 0, sticky = W)

    pause_button = Button(controls_screen, text = "Shift + P", command = None)
    pause_button.grid(row = 6, column = 1, sticky=N+S+E+W)

    save_label = Label(controls_screen, text = "Save the game", font=("Arial", 20), bg= "black", fg="white")
    save_label.grid(row = 7, column = 0, sticky = W)

    save_button = Button(controls_screen, text = "Shift + S", command = None)
    save_button.grid(row = 7, column = 1, sticky=N+S+E+W)

    boss_label = Label(controls_screen, text = "Boss key", font=("Arial", 20), bg= "black", fg="white")
    boss_label.grid(row = 8, column = 0, sticky = W)

    boss_button = Button(controls_screen, text = "Shift + B", command = None)
    boss_button.grid(row = 8, column = 1, sticky=N+S+E+W)


# Global variables and images use for characters/background
bg_image = PhotoImage(file="images/gamebg.png")
catcher_image = PhotoImage(file="images/catcher.png")
enemies_image = PhotoImage(file="images/enemies.png")
cookie_image = PhotoImage(file="images/cookie.png")
fake_work_image = PhotoImage(file="images/busy.png")
pause_image = PhotoImage(file="images/pause.png")

enemies_list = []
cookies_list = []
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
CATCHER_X_COORD = CANVAS_WIDTH / 2
CATCHER_IMAGE_SIZE = 60
COOKIE_IMAGE_SIZE= 50
ENEMIES_IMAGE_SIZE = 50
ENEMIES_COOKIES_Y_COORD = 0
GAMEOVER = False
CHEAT = False
BOSS = False
SCORE = 0
MOVE_LEFT_KEY = "a"
MOVE_RIGHT_KEY = "d"
CHANGING_LEFT = False
CHANGING_RIGHT = False

# The lower the value, the faster cookies and enemies are created
COOKIE_CREATE_TIME = 2000
ENEMIES_CREATE_TIME = 1000

# The higher the value, the slower the cookies and enemies fall
FALL_SPEED = 50

# Create the canvas for the main gameplay page
game = Canvas(window, width= CANVAS_WIDTH, height= CANVAS_HEIGHT)
game.pack(fill= "both", expand = True)
game.create_image(0, 0, image = bg_image, anchor = "nw")

# Create the catcher and hide at the start
catcher = game.create_image(0, 0, image = catcher_image, anchor = "nw")
game.itemconfig(catcher, state= 'hidden')

# Create the SCORE tab and place it in the canvas
SCORELabel = Label(game, text = "SCORE: " + str(SCORE))
SCORELabel.place(x = 0, y = 0)

# Label and buttons at the start of the game
instrucions = Label(game, text = "Collect the normal cookies to earn points.", font=("Comic-Sans", 30), bg = "brown", fg = "white")
instrucions.place(x = 250, y = 120)

instrucions1 = Label(game, text = "DO NOT CATCH the bad cookie. You have 1 LIFE.", font=("Comic-Sans", 30), bg = "brown", fg = "white")
instrucions1.place(x = 170, y = 180)

instrucions2 = Label(game, text = "Use 'a' and 'd' to move left and right", font=("Comic-Sans", 30), bg = "red", fg = "white")
instrucions2.place(x = 300, y = 240)

instrucions3 = Label(game, text = "GOOD LUCK!", font=("Comic-Sans", 30), bg = "brown", fg = "white")
instrucions3.place(x = 500, y = 300)

start_button = Button(game, text = "Start the Game", highlightbackground = "white", command = game_loop)
start_button.place(x = 570, y = 360)

option_button = Button(game, text = "Options", highlightbackground = "white", command = controls_window)
option_button.place(x = 570, y = 400)

leaderboard_button = Button(game, text = "View Leaderboard", highlightbackground = "white", command = leaderboard_window)
leaderboard_button.place(x = 570, y = 440)

load_button = Button(game, text = "Load last saved game", highlightbackground = "white", command = load_data)
load_button.place(x = 570, y = 480)

window.mainloop()
