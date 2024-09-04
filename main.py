from tkinter import *
from PIL import ImageTk, Image

root = Tk() 
root.attributes('-topmost', True)
root.attributes('-transparentcolor', 'gray')
root.configure(bg='gray')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

def load(path: str) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(Image.open(path))

images = {
    "right": {
        "up": [load("assets/upright1.png"), load("assets/upright2.png")],
        "down": [load("assets/downright1.png"), load("assets/downright2.png")],
        "right": [load("assets/right1.png"), load("assets/right2.png")]
    },
    "left": {
        "up": [load("assets/upleft1.png"), load("assets/upleft2.png")],
        "down": [load("assets/downleft1.png"), load("assets/downleft2.png")],
        "left": [load("assets/left1.png"), load("assets/left2.png")]
    },
    "up": [load("assets/up1.png"), load("assets/up2.png")],
    "down": [load("assets/down1.png"), load("assets/down2.png")],
    "awake": load("assets/awake.png"),
    "sleep": [load("assets/sleep1.png"), load("assets/sleep2.png")],
    "yawn": [load("assets/yawn1.png"), load("assets/yawn2.png")]
}

pet_x: float = 0
pet_y: float = 0
pet_vel_x: float = 0
pet_vel_y: float = 0
pet_width: int = 32
pet_height: int = 32

pet_is_following = True

follow_radius = 32

def toggle_follow():
    global pet_is_following
    pet_is_following = not pet_is_following

def create_context_menu(event) -> Menu:
    menu = Menu(root, tearoff=0)
    
    menu.add_command(label="Stop Following" if pet_is_following else "Start Following", command=toggle_follow)
    menu.add_command(label="Quit", command=root.destroy)

    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

panel = Label(root, image = images["awake"], bg="gray")
panel.pack()

panel.bind("<Button-3>", create_context_menu)

ticks = 0
last_state = "awake"
ticks_awake = 0

sleep_timer = (10 * 10)

def move_to(x: float, y: float):
    root.geometry(f"{pet_width}x{pet_height}+{int(x)}+{int(y)}")

def tick():
    global pet_x
    global pet_y

    global pet_vel_x
    global pet_vel_y
    
    global ticks_awake
    global last_state

    global ticks

    mouse_x = root.winfo_pointerx()
    mouse_y = root.winfo_pointery()

    pet_center_x = pet_x + (pet_width / 2)
    pet_center_y = pet_y + (pet_height / 2)

    distance_to_mouse_x = abs(mouse_x - pet_center_x)
    distance_to_mouse_y = abs(mouse_y - pet_center_y)

    speed = pet_width / 4

    sprite = images["awake"]
    horizontal_direction = "none"
    vertical_direction = "none"

    if pet_is_following:
        if distance_to_mouse_x > follow_radius:
            horizontal_direction = "right" if mouse_x > pet_center_x else "left"
        
        if distance_to_mouse_y > follow_radius:
            vertical_direction = "up" if mouse_y < pet_center_y else "down"

    frame = 0 if ticks % 2 == 0 else 1
    
    if horizontal_direction == "right":
        pet_x += speed
        if vertical_direction == "up":
            sprite = images["right"]["up"][frame]
            pet_y -= speed
        elif vertical_direction == "down":
            sprite = images["right"]["down"][frame]
            pet_y += speed
        else:
            sprite = images["right"]["right"][frame]

    elif horizontal_direction == "left":
        pet_x -= speed
        if vertical_direction == "up":
            sprite = images["left"]["up"][frame]
            pet_y -= speed
        elif vertical_direction == "down":
            sprite = images["left"]["down"][frame]
            pet_y += speed
        else:
            sprite = images["left"]["left"][frame]

    if horizontal_direction == "none":
        if vertical_direction == "up":
            sprite = images["up"][frame]
            pet_y -= speed
        if vertical_direction == "down":
            sprite = images["down"][frame]
            pet_y += speed

    if horizontal_direction == "none" and vertical_direction == "none":
        if last_state == "awake":
            ticks_awake += 1
        
        if ticks_awake > sleep_timer - 10:
            sprite = images["yawn"][(0 if (ticks_awake - 1) % 10 > 4 else 1)]

        if ticks_awake >= sleep_timer:
            last_state = "sleep"
            sprite = images["sleep"][0 if ticks % 8 > 3 else 1]
        else:
            last_state = "awake"
    else:
        last_state = "moving"
        ticks_awake = 0

    panel.configure(image=sprite)

    if pet_y > screen_height - pet_height:
        pet_y = screen_height - pet_height

    if pet_y < 0:
        pet_y = 0

    ticks += 1

    move_to(pet_x, pet_y)
    panel.after(int(1000 / 10), tick)

tick()

root.overrideredirect(True)
root.mainloop()