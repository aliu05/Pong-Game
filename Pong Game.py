'''
Name: Andrew Liu
Date: March 25, 2021
Class Code: ICS3U
Teacher: Ms. Franolla
This pong game program allows the user to play with their friend
or against an AI which is of the difficulty they select.
'''

import pygame, random

#Initialize pygame
pygame.init()

#Set clock speed
clock = pygame.time.Clock()
clock.tick(10)

#Setup the screen
SIZE = (800, 600)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pong Game")

#Find centre of screen
screenWidth = screen.get_width()
screenHeight = screen.get_height()
centreX = screenWidth / 2
centreY = screenHeight / 2

#Colours to use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

#Set up fonts to use
fontTitle = pygame.font.SysFont("arial", 30, italic = True)
fontTitleBold = pygame.font.SysFont("arial", 30, bold = True)
fontInstructions = pygame.font.SysFont("arial", 30)
fontScore = pygame.font.SysFont("tahoma", 45, bold = True)

#Initialize the players (in this case paddles)
playerWidth = 10
playerHeight = 120

playerRect1 = pygame.Rect(0, centreY - 60, playerWidth, playerHeight)
playerRect2 = pygame.Rect(785, centreY - 60, playerWidth, playerHeight)

playerSpeed = 7
playerDisplacement1 = 0
playerDisplacement2 = 0

#Initialize AI speed variables
aiSpeed = 0

aiSpeedEasy = 3
aiSpeedMedium = 4
aiSpeedHard = 5

#Initialize ball
diameter = 8
ballRect = pygame.Rect(centreX - 7, centreY - 7, 14, 14)
#Send the ball in a random direction
ballSpeedList = [-5, 5]
ballSpeedX = ballSpeedList[random.randint(0, 1)]
ballSpeedY = ballSpeedList[random.randint(0, 1)]

#Initialize scoreboard variables
score1 = 0
score2 = 0

#Initialize the game Loop
running = True
menu = True
difficultySelect = False
singleplayerGame = False
multiplayerGame = False
instruction = False
final = False

def menu_text():
  #Set menu/start text
  textTitle = fontTitle.render("WELCOME TO PONG GAME", False, WHITE)
  textTitle2 = fontTitle.render("Press '1' for singleplayer, '2' for multiplayer,", False, WHITE)
  textTitle3 = fontTitle.render("'i' for instructions and 'q' to quit", False, WHITE)
  #Use rects to hold text
  textRect = textTitle.get_rect()
  textRect2 = textTitle2.get_rect()
  textRect3 = textTitle3.get_rect()
  #Assign location for text
  textRect.center = (centreX, 175)
  textRect2.center = (centreX, 300)
  textRect3.center = (centreX, 380)
  #Blit text onto screen
  screen.blit(textTitle, textRect)
  screen.blit(textTitle2, textRect2)
  screen.blit(textTitle3, textRect3)

def instruction_text():
  #Game instructions and how to return to menu screen
  textInstructions = fontTitleBold.render("INSTRUCTIONS", False, WHITE)
  textInstructions2 = fontInstructions.render("Pong is a classic 2 player arcade game", False, WHITE)
  textInstructions3 = fontInstructions.render("Player 1 will use 'w' and 's' to control their paddle", False, WHITE)
  textInstructions4 = fontInstructions.render("Player 2 will use the up and down arrow keys", False, WHITE)
  textInstructions5 = fontInstructions.render("The first to 3 points wins", False, WHITE)
  textInstructions6 = fontTitle.render("press 'm' to return to the menu screen", False, WHITE)
  #Use rects to hold text
  textInstructionsRect = textInstructions.get_rect()
  textInstructionsRect2 = textInstructions2.get_rect()
  textInstructionsRect3 = textInstructions3.get_rect()
  textInstructionsRect4 = textInstructions4.get_rect()
  textInstructionsRect5 = textInstructions5.get_rect()
  textInstructionsRect6 = textInstructions6.get_rect()
  #Assign location for text
  textInstructionsRect.center = (centreX, 75)
  textInstructionsRect2.center = (centreX, 175)
  textInstructionsRect3.center = (centreX, 250)
  textInstructionsRect4.center = (centreX, 325)
  textInstructionsRect5.center = (centreX, 400)
  textInstructionsRect6.center = (centreX, 500)
  #Blit text onto screen
  screen.blit(textInstructions, textInstructionsRect)
  screen.blit(textInstructions2, textInstructionsRect2)
  screen.blit(textInstructions3, textInstructionsRect3)
  screen.blit(textInstructions4, textInstructionsRect4)
  screen.blit(textInstructions5, textInstructionsRect5)
  screen.blit(textInstructions6, textInstructionsRect6)

def difficulty_text():
  #Set display text
  textDifficulty = fontTitle.render("Please select a difficulty using your keyboard", False, WHITE)
  textDifficulty2 = fontTitle.render("The difficulty you select will affect the AI's speed", False, WHITE)
  textDifficulty3 = fontTitle.render("Press 'e' for easy, 'm' for medium or 'h' for hard", False, WHITE)
  #Use rects to hold text
  textDifficultyRect = textDifficulty.get_rect()
  textDifficultyRect2 = textDifficulty2.get_rect()
  textDifficultyRect3 = textDifficulty3.get_rect()
  #Assign location for text
  textDifficultyRect.center = (centreX, 175)
  textDifficultyRect2.center = (centreX, 230)
  textDifficultyRect3.center = (centreX, 350)
  #Blit text onto screen
  screen.blit(textDifficulty, textDifficultyRect)
  screen.blit(textDifficulty2, textDifficultyRect2)
  screen.blit(textDifficulty3, textDifficultyRect3)

def final_text():
  #Set final text
  textFinal = fontTitleBold.render("Game over, the final score was " + str(score1) + " : " + str(score2), False, WHITE)
  textFinal2 = fontInstructions.render("Press 'q' to quit or 'm' to return to the menu", False, WHITE)
  #Use rects to hold text
  textFinalRect = textFinal.get_rect()
  textFinalRect2 = textFinal2.get_rect()
  #Assign location for text
  textFinalRect.center = (centreX, 175)
  textFinalRect2.center = (centreX, 300)
  #Blit text onto screen
  screen.blit(textFinal, textFinalRect)
  screen.blit(textFinal2, textFinalRect2)

def reset_game(winner):
  #Set variables to global scope
  global score1, score2, centreX, centreY, ballSpeedX, ballSpeedY, playerRect1, playerRect2
  #Reset the ball after someone scores
  if winner == "player1":
    ballRect.center = (centreX, centreY)
    score1 += 1

    #Send the ball in a random direction
    ballSpeedList = [-5, 5]
    ballSpeedX = ballSpeedList[random.randint(0, 1)]
    ballSpeedY = ballSpeedList[random.randint(0, 1)]

  elif winner == "player2":
    ballRect.center = (centreX, centreY)
    score2 += 1  

    #Send the ball in a random direction
    ballSpeedList = [-5, 5]
    ballSpeedX = ballSpeedList[random.randint(0, 1)]
    ballSpeedY = ballSpeedList[random.randint(0, 1)]

  #Reset the paddles
  playerRect1 = pygame.Rect(0, centreY - 60, playerWidth, playerHeight)
  playerRect2 = pygame.Rect(785, centreY - 60, playerWidth, playerHeight)

#Main loop
while running:
  #Check for any events
  for event in pygame.event.get():
    #Check if 'x' was clicked
    if event.type == pygame.QUIT:
      #End the program
      running = False
  
  #Menu/introduction loop
  while menu:
    #Fill screen
    screen.fill(BLACK)
    #Display menu/start text
    menu_text()

    #Check for some events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        menu = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          menu = False
          difficultySelect = True
        elif event.key == pygame.K_2:
          menu = False
          multiplayerGame = True
        elif event.key == pygame.K_q:
          running = False
          menu = False
        elif event.key == pygame.K_i:
          menu = False
          instruction = True

    #Update display
    pygame.display.update()

  #Instruction loop containing information for user
  while instruction:
    #Fill screen
    screen.fill(BLACK)

    #Display game instructions and how to return to menu screen
    instruction_text()

    #Check for key presses
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        instruction = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          running = False
          instruction = False
        elif event.key == pygame.K_m:
          instruction = False
          menu = True

    #Update display
    pygame.display.update()

  #Select AI difficulty for singleplayer mode
  while difficultySelect:
    #Fill screen
    screen.fill(BLACK)

    #Check for key events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        difficultySelect = False
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          running = False
          difficultySelect = False

        #Adjust the speed of the AI prior to starting the singleplayer game loop
        elif event.key == pygame.K_e:
          aiSpeed = aiSpeedEasy
          difficultySelect = False
          singleplayerGame = True
        elif event.key == pygame.K_m:
          aiSpeed = aiSpeedMedium
          difficultySelect = False
          singleplayerGame = True
        elif event.key == pygame.K_h:
          aiSpeed = aiSpeedHard
          difficultySelect = False
          singleplayerGame = True

    #Display instructions on how to choose difficulty
    difficulty_text()

    #Update the display
    pygame.display.update()

  #Player vs AI loop
  while singleplayerGame:
    #Fill screen
    screen.fill(BLACK)   

    #Draw the centre line
    pygame.draw.line(screen, GRAY, (400, 0), (400, 600), 2)
    #Draw the paddles
    pygame.draw.rect(screen, GRAY, (playerRect1))
    pygame.draw.rect(screen, GRAY, (playerRect2))
    #Draw the ball
    pygame.draw.circle(screen, GRAY, (ballRect.center), 7)

    #Check key events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        singleplayerGame = False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          running = False
          singleplayerGame = False

        #Player paddle movement
        elif event.key == pygame.K_UP:
          playerDisplacement2 = -playerSpeed
        elif event.key == pygame.K_DOWN:
          playerDisplacement2 = playerSpeed

      #End paddle movement
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
          playerDisplacement2 = 0
        
    #Move player paddle
    playerRect2.y += playerDisplacement2

    #Move AI paddle
    #Track the ball center and match the paddle's y coordinate
    if ballRect.x < 400:
      if playerRect1.centery < ballRect.centery:
        playerRect1.centery += aiSpeed
      elif playerRect1.centery > ballRect.centery:
        playerRect1.centery -= aiSpeed

    #Ensure the paddles don't go off the screen
    if playerRect1.top <= 0:
      playerRect1.top = 0
    elif playerRect1.bottom >= 600:
      playerRect1.bottom = 600

    if playerRect2.top <= 0:
      playerRect2.top = 0
    elif playerRect2.bottom >= 600:
      playerRect2.bottom = 600

    #Move the ball
    ballRect.x += ballSpeedX
    ballRect.y += ballSpeedY

    #Check for collision with walls
    if ballRect.top <= 0 or ballRect.bottom >= 600:
      ballSpeedY *= -1

    if ballRect.left <= 0:
      reset_game("player2")
    elif ballRect.right >= 800:
      reset_game("player1")

    #Check for collision with paddles
    if ballRect.colliderect(playerRect1) or ballRect.colliderect(playerRect2):
      ballSpeedX *= -1

    #Display score
    scoreText1 = fontScore.render(str(score1), False, GRAY)
    scoreText2 = fontScore.render(str(score2), False, GRAY)

    screen.blit(scoreText1, (screenWidth / 2 - 56, 30))
    screen.blit(scoreText2, (screenWidth / 2 + 26, 30))

    #End the game if either player scores 3 points
    if score1 == 3 or score2 == 3:
      singleplayerGame = False
      final = True

    #Update display with 60 fps
    pygame.display.update()
    clock.tick(60)

  #Two player game loop
  while multiplayerGame:
    #Fill screen
    screen.fill(BLACK)   
    
    #Draw the centre line
    pygame.draw.line(screen, GRAY, (400, 0), (400, 600), 2)
    #Draw the paddles
    pygame.draw.rect(screen, GRAY, (playerRect1))
    pygame.draw.rect(screen, GRAY, (playerRect2))
    #Draw the ball
    pygame.draw.circle(screen, GRAY, (ballRect.center), 7)

    #Check key events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        multiplayerGame = False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          running = False
          multiplayerGame = False
          
        #Start paddle movement
        elif event.key == pygame.K_w:
          playerDisplacement1 = -playerSpeed
        elif event.key == pygame.K_s:
          playerDisplacement1 = playerSpeed
        elif event.key == pygame.K_UP:
          playerDisplacement2 = -playerSpeed
        elif event.key == pygame.K_DOWN:
          playerDisplacement2 = playerSpeed

      #End paddle movement
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_w or event.key == pygame.K_s:
          playerDisplacement1 = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
          playerDisplacement2 = 0

    #Move the paddles
    playerRect1.y += playerDisplacement1
    playerRect2.y += playerDisplacement2

    #Ensure the paddles don't go off the screen
    if playerRect1.top <= 0:
      playerRect1.top = 0
    elif playerRect1.bottom >= 600:
      playerRect1.bottom = 600

    if playerRect2.top <= 0:
      playerRect2.top = 0
    elif playerRect2.bottom >= 600:
      playerRect2.bottom = 600

    #Move the ball
    ballRect.x += ballSpeedX
    ballRect.y += ballSpeedY

    #Check for collision with walls
    if ballRect.top <= 0 or ballRect.bottom >= 600:
      ballSpeedY *= -1

    if ballRect.left <= 0:
      reset_game("player2")
    elif ballRect.right >= 800:
      reset_game("player1")

    #Check for collision with paddles
    if ballRect.colliderect(playerRect1) or ballRect.colliderect(playerRect2):
      ballSpeedX *= -1

    #Display score
    scoreText1 = fontScore.render(str(score1), False, GRAY)
    scoreText2 = fontScore.render(str(score2), False, GRAY)

    screen.blit(scoreText1, (screenWidth / 2 - 56, 30))
    screen.blit(scoreText2, (screenWidth / 2 + 26, 30))

    #End the game if either player scores 3 points
    if score1 == 3 or score2 == 3:
      multiplayerGame = False
      final = True

    #Update display with 60 fps
    pygame.display.update()
    clock.tick(60)

  #Final loop (when game is over)
  while final:
    #Fill screen
    screen.fill(BLACK)

    #Check for key events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        final = False
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          running = False
          final = False
        elif event.key == pygame.K_m:
          final = False
          menu = True

          #Reset scores
          score1 = 0
          score2 = 0
                   
    #Display end screen text
    final_text()

    #Update dispay
    pygame.display.update()

#Quit pygame
pygame.quit()