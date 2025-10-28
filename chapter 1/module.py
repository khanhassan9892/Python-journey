print("Module mean is using someone's code") #--use ctrl+/ to comment
import arcade

arcade.open_window(400, 300, "Red Circle")
arcade.set_background_color(arcade.color.WHITE)
arcade.start_render()
arcade.draw_circle_filled(200, 150, 60, arcade.color.RED)
arcade.finish_render()
arcade.run()
