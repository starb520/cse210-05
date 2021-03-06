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
    play_again = True

    # Create two score objects with a position and color.
    score = Score(Point(600,0),Color(128,0,128))
    score2 = Score(Point(0,0),Color(53,203,233))
    
    # Keep playing with the game with the score continuing to update.
    while play_again:

        # create the cast
        cast = Cast()
        cast.add_actor("snakes", Snake())
        
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

            # This sets the colors of the two snakes.
            cast._actors["snake2"][0]._segments[i].set_color(Color(128,0,128))
            cast._actors["snakes"][0]._segments[i].set_color(Color(53,203,233))
        
        # Create two scores, one for the first snake and one for the second.
        cast.add_actor("scores", score2)
        cast.add_actor("scores", score)
    
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

        # See if users would like to continue playing.
        continue_play = input("Would you like to play again? [y/n]")
        play_again = continue_play.lower()
        if continue_play.lower() == "n":
            scores = cast.get_actors("scores")

            scores[0].reset_points()
            scores[1].reset_points()
            play_again = False
        elif continue_play.lower() == "y":
            play_again = True
        

if __name__ == "__main__":
    main()