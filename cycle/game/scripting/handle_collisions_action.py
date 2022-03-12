import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_food_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_food_collision(self, cast):
        """Updates the score nd moves the food if the snake collides with the food.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        score = cast.get_first_actor("scores")
        food = cast.get_first_actor("foods")
        snake = cast.get_first_actor("snakes")
        head = snake.get_head()


        '''This code needs to be deleted eventually, it used to grow the snakes 
           when they ate the food.'''
        # if head.get_position().equals(food.get_position()):
        #     points = food.get_points()
        #     snake.grow_tail(points)
        #     score.add_points(points)
        #     food.reset()
    
    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        snake = cast.get_first_actor("snakes")
        head = snake.get_segments()[0]
        segments = snake.get_segments()[1:]

        snake2 = cast.get_first_actor("snake2")
        head2 = snake2.get_segments()[0]
        segments2 = snake2.get_segments()[1:]

        # Get a scores list.
        scores = cast.get_actors("scores")
        
        # Loop through the segments in the snake2 body. 
        for segment in segments2:
            # Calculate the distance between the head of snake one and the body
            # segment of snake 2.
            delta= head.get_position().subtract(segment.get_position())

            # If the distance between the head of snake one and the segment of snake2 body is
            # less than 20 pixels, game over is true and snake 2 gets points.
            if abs(delta.get_x()) < 17 and abs(delta.get_y()) < 17:
                self._is_game_over = True
                # Add points to snake2.
                scores[1].add_points(10)

        # Loop through the segments in the snake1 body.
        for segment in segments:
            # Calculate the distance between the head of snake2 and the snake two
            # body.
            delta = head2.get_position().subtract(segment.get_position())
            # If the distance between the head of snake2 and the segment of snake1 body is
            # less than 20 pixels, game over is true and snake1 gets points.
            if abs(delta.get_x()) < 17 and abs(delta.get_y()) < 17:
                self._is_game_over = True
                scores[0].add_points(5)
        
    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            snake = cast.get_first_actor("snakes")
            segments = snake.get_segments()

            # I added the snake 2 so at game over so snake2 can turn white.
            snake2 = cast.get_first_actor("snake2")
            segment2 = snake2.get_segments()

            food = cast.get_first_actor("foods")

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)

            for segment in segments:
                segment.set_color(constants.WHITE)

            # I added this so snake 2 can turn white at game over.
            for segment in segment2:
                segment.set_color(constants.WHITE)
            