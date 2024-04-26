import os
import sys
import pygame


def scale_image_keeping_ratio(image, new_width):
    # Get the original dimensions
    width, height = image.get_size()
    # Maintain the aspect ratio
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio)
    # Scale the image
    return pygame.transform.scale(image, (new_width, new_height))


def scale_image(image, new_width, new_height):
    # Scale the image to the specified new width and new height
    return pygame.transform.scale(image, (new_width, new_height))



#returns true if the square is filled
def checkSquareFilled(board, row, col):
    if board[row][col] == "":
        return False
    return True


#function to check if the game has ended, returns "X" or "O"
def checkIfWon(board):
    # Check horizontal and vertical lines
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]  # A winner in a row
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]  # A winner in a column

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]  # A winner on the primary diagonal
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]  # A winner on the secondary diagonal

    for i in board:
        for j in i:
            if j == "":
                return ""
            
    return "No One"

    # # If no winner is found
    # return ""


#function to draw text
def draw_text(text, color, surface, x, y):
    font = pygame.font.Font(None, 45)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
        

#main game function
def main():
    board = [["" for _ in range(3)] for _ in range(3)]

    # Initialize Pygame
    pygame.init()

    # Set up the display
    window_size = (600, 600)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('My Game')

    clock = pygame.time.Clock()


    #set up dependencies
    boardImg = pygame.image.load(os.path.join('imgs','tiktoe3x3.jpg')).convert()
    boardImg = scale_image_keeping_ratio(boardImg, 600)

    Ximg = pygame.image.load(os.path.join('imgs','redX.jpg')).convert()
    Ximg = scale_image(Ximg, 170, 170)

    Oimg = pygame.image.load(os.path.join('imgs','blackO.jpg')).convert()
    Oimg = scale_image(Oimg, 170, 170)


    #dynamic variables ===============
    turn = 0
    whowon = ""

    #initialize screen and board ======================================

    #outter loop for blitting
    screen.fill((255, 255, 255))  # Fill the screen with black

    # Blit the image to the screen at coordinates (50, 50)
    screen.blit(boardImg, (0, 0))

    # Update the display
    pygame.display.flip()

    # Main game loop ======================================================
    running = True
    #outter loop for flipping
    while running:

        screen.fill((255, 255, 255))  # Fill the screen with black

        # Blit the image to the screen at coordinates (50, 50)
        screen.blit(boardImg, (0, 0))


        #inner checking for inputs
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Game logic goes here ===========================================================================
            # Inside your game loop:
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position
            mouse_buttons = pygame.mouse.get_pressed()  # Returns a tuple representing mouse button state

            if mouse_buttons[0]:  # If the left mouse button is pressed

                mouseSquare = (int(mouse_pos[0] / 200), int(mouse_pos[1] / 200))

                #if we can actually add that to the square
                if not checkSquareFilled(board, mouseSquare[1], mouseSquare[0]):

                    if turn % 2 == 0:
                        board[mouseSquare[1]][mouseSquare[0]] = "X"
                    else:
                        board[mouseSquare[1]][mouseSquare[0]] = "O"
                    
                    turn += 1

                    break


            clock.tick(60)


        #loop to print out the current board state
        for i in range(3):
            for j in range(3):
                if board[i][j] == "X":
                    screen.blit(Ximg, (j*200 + 15, i*200 + 15))
                if board[i][j] == "O":
                    screen.blit(Oimg, (j*200 + 15, i*200 + 15))

        # Update the display 
        pygame.display.flip()

        whowon = checkIfWon(board)

        if whowon == "X" or whowon == "O" or whowon == "No One":
            running = False
            break


    #loop until user chooses an option
    tooltipLoop = True
    while tooltipLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:

                    # Quit Pygame
                    pygame.quit()
                    main()  # Player wants to play again
                    tooltipLoop = False
                    break

                elif event.key == pygame.K_n:
                    # Quit Pygame
                    pygame.quit()
                    sys.exit()

        # Draw the popup background
        popup_surf = pygame.Surface((500, 100))
        popup_surf.fill((35, 239, 250))
        draw_text(f"{whowon} won! Play again? (Y/N)", (0, 0, 0), popup_surf, 0, 0)

        # Position the popup on the screen center
        screen.blit(popup_surf, (50, 200))
        pygame.display.flip()
        clock.tick(30)

    


if __name__ == "__main__":
    main()