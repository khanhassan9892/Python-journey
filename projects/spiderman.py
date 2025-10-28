import turtle

# ----------------- CONFIGURATION -----------------
BG_COLOR = "red"
LINE_COLOR = "black"
EYE_COLOR = "white"
BLUE_COLOR = "blue"
MAIN_PEN_SIZE = 16
DETAIL_PEN_SIZE = 4

# ----------------- HELPER FUNCTION -----------------
def go_to(t, x, y):
    """Moves the turtle to a specific coordinate without drawing."""
    t.penup()
    t.goto(x, y)
    t.pendown()

# ----------------- DRAWING FUNCTIONS -----------------

def draw_body_and_limbs(t):
    """Draws the main stick-figure body and limbs."""
    t.color(LINE_COLOR)
    t.pensize(MAIN_PEN_SIZE)

    # Torso
    go_to(t, 0, 100)
    t.goto(0, -80)

    # Right Arm (viewer's left)
    go_to(t, 0, 50)
    t.goto(100, 20)
    t.goto(150, 70)

    # Left Arm (viewer's right)
    go_to(t, 0, 50)
    t.goto(-80, 80)
    t.goto(-140, 50)

    # Right Leg (viewer's left)
    go_to(t, 0, -80)
    t.goto(60, -180)
    t.goto(50, -250)

    # Left Leg (viewer's right)
    go_to(t, 0, -80)
    t.goto(-70, -170)
    t.goto(-60, -240)

def draw_head_and_eyes(t):
    """Draws the head and eyes on top of the body."""
    # Head Outline
    # Position the turtle at the bottom of the circle to draw it correctly on the neck
    radius = 80
    go_to(t, 0, 100 - radius)
    t.setheading(0)
    t.color(LINE_COLOR)
    t.pensize(MAIN_PEN_SIZE)
    t.circle(radius)

    # Eyes
    t.color(LINE_COLOR, EYE_COLOR)
    
    # Left Eye
    go_to(t, -15, 150)
    t.begin_fill()
    t.goto(-55, 120)
    t.goto(-50, 90)
    t.goto(-15, 110)
    t.goto(-15, 150)
    t.end_fill()

    # Right Eye
    go_to(t, 15, 150)
    t.begin_fill()
    t.goto(55, 120)
    t.goto(50, 90)
    t.goto(15, 110)
    t.goto(15, 150)
    t.end_fill()

def draw_webbed_accessory(t, width, height):
    """A reusable function to draw a filled blue box with a web pattern."""
    start_pos = t.pos()
    start_heading = t.heading()

    # Draw and fill the blue rectangle
    t.color(LINE_COLOR, BLUE_COLOR)
    t.pensize(MAIN_PEN_SIZE)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()

    # Add the black web pattern
    t.color(LINE_COLOR)
    t.pensize(DETAIL_PEN_SIZE)
    
    # Vertical lines
    for i in range(1, 3):
        go_to(t, start_pos[0], start_pos[1])
        t.setheading(start_heading)
        t.forward(i * width / 3)
        t.right(90)
        t.pendown()
        t.forward(height)
    
    # Horizontal line
    go_to(t, start_pos[0], start_pos[1])
    t.setheading(start_heading)
    t.right(90)
    t.forward(height / 2)
    t.left(90)
    t.pendown()
    t.forward(width)

def draw_costume_details(t):
    """Draws the backpack, gloves, and boots."""
    # Backpack (drawn first to be behind the arm)
    go_to(t, -10, 30)
    t.setheading(180)
    draw_webbed_accessory(t, 50, 90)
    
    # Right Glove
    go_to(t, 135, 95)
    t.setheading(315)
    draw_webbed_accessory(t, 60, 35)

    # Left Glove
    go_to(t, -165, 30)
    t.setheading(225)
    draw_webbed_accessory(t, 60, 35)
    
    # Right Boot
    go_to(t, 30, -275)
    t.setheading(200)
    draw_webbed_accessory(t, 70, 40)

    # Left Boot
    go_to(t, -80, -265)
    t.setheading(160)
    draw_webbed_accessory(t, 70, 40)

# ----------------- MAIN EXECUTION -----------------
def main():
    """Main function to set up and run the drawing."""
    screen = turtle.Screen()
    screen.bgcolor(BG_COLOR)
    screen.title("Cartoon Spider-Man")
    
    spidey = turtle.Turtle()
    spidey.speed(0)
    spidey.hideturtle()

    # The drawing order is critical for correct layering.
    # 1. Draw the background details first.
    draw_costume_details(spidey)
    
    # 2. Draw the main body on top of the backpack.
    draw_body_and_limbs(spidey)
    
    # 3. Draw the head and eyes last so they are on the very top layer.
    draw_head_and_eyes(spidey)
    
    screen.exitonclick()

if __name__ == "__main__":
    main()                     