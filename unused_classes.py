# class Interactions:
#     prev_character_x_coordinate = 0
#     def interactions(self, character, ball):
#         if character.grabBall:
#             self.grabBall(character, ball)
#     def inter(self, character, platform):
#         if character.get_x_coordinate() > self.prev_character_x_coordinate:
#             self.prev_character_x_coordinate = character.get_x_coordinate()
#             platform.change_x_coordinate(platform.get_x_coordinate() - 2)
#         if character.get_x_coordinate() < self.prev_character_x_coordinate:
#             self.prev_character_x_coordinate = character.get_x_coordinate()
#             platform.change_x_coordinate(platform.get_x_coordinate() + 2)
#     def grabBall(self, charcter, ball):
#         ball_y_coordinate = charcter.get_y_coordinate() + (charcter.getHeight() / 2)
#         ball_x_coordinate = charcter.get_x_coordinate() - 10
#         ball.change_y_coordinate(ball_y_coordinate)
#         ball.change_x_coordinate(ball_x_coordinate)


# class Ball:
#     color = (0, 0, 250)
#     x_coordinate = 90
#     y_coordinate = 90
#     length = 10
#     height = 10
#     def draw(self):
#         pygame.draw.rect(win, (self.color), (self.x_coordinate, self.y_coordinate, self.length, self.height))
#     def getHeight(self):
#         return self.height
#     def getLength(self):
#         return self.length
#     def get_x_coordinate(self):
#         return self.x_coordinate
#     def get_y_coordinate(self):
#         return self.y_coordinate
#     def change_x_coordinate(self, x_coordinate):
#         self.x_coordinate = x_coordinate
#     def change_y_coordinate(self, y_coordinate):
#         self.y_coordinate = y_coordinate
#     def update(self):
#         pass

# def show_enemy_health(self, x_coordinate, y_coordinate, full_health, health_remaining):
#     lost_health = full_health - health_remaining
#     color = (0, 250, 0)
#     health_remaining_length = (health_remaining / full_health) * 100 * (screen_height * .0001)
#     lost_health_length = (lost_health /full_health) * 100 * (screen_height * .0001)
#     pygame.draw.rect(win, (color), (x_coordinate, y_coordinate + screen_height * .02, health_remaining_length, screen_height * .04))
#     color = (250, 0, 0)
#     pygame.draw.rect(win, (color), (x_coordinate + health_remaining_length, y_coordinate + screen_height * .02, lost_health_length, screen_height * .04))

# print(0.0008919363273713182 * 200)
