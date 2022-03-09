import constants

from game.casting.cast import Cast
from game.casting.food import Food
from game.casting.score import Score
from game.casting.snake import Snake
from game.scripting.script import Script
from game.scripting.control_actors_action import ControlActorsAction
from game.scripting.move_actors_action import MoveActorsAction
from game.scripting.handle_collisions_action import HandleCollisionsAction
from game.scripting.draw_actors_action import DrawActorsAction
from game.directing.director import Director
from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService
from game.shared.color import Color
from game.shared.point import Point

from game.casting.actor import Actor


def main():
    
    # create the cast
    cast = Cast()
    cast.add_actor("foods", Food())
    cast.add_actor("snakes", Snake())
    cast.add_actor("scores", Score())
    
    # try adding a second snake
    cast.add_actor("snake2", Snake())


    # This sets an x and y for the position of snake2
    x = int(3*(constants.MAX_X / 4))
    y = int(constants.MAX_Y / 2)
    # this is a different x position for snake1
    x2 = int((constants.MAX_X / 4))

    # set position and velocity of snake2
    for i in range(constants.SNAKE_LENGTH):
        position = Point(x, y + i * constants.CELL_SIZE)
        velocity = Point(0, -1 * constants.CELL_SIZE)
            
        cast._actors["snake2"][0]._segments[i].set_position(position)
        cast._actors["snake2"][0]._segments[i].set_velocity(velocity)

    # I did this to change the position and velocity of snake1
            
        position = Point(x2, y + i * constants.CELL_SIZE)
        velocity = Point(0, -1 * constants.CELL_SIZE)
        cast._actors["snakes"][0]._segments[i].set_position(position)
        cast._actors["snakes"][0]._segments[i].set_velocity(velocity)



   
    # start the game
    keyboard_service = KeyboardService()
    video_service = VideoService()

    script = Script()
    script.add_action("input", ControlActorsAction(keyboard_service))
    script.add_action("update", MoveActorsAction())
    script.add_action("update", HandleCollisionsAction())
    script.add_action("output", DrawActorsAction(video_service))
    
    director = Director(video_service)
    director.start_game(cast, script)


if __name__ == "__main__":
    main()