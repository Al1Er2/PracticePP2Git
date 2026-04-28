import pygame
import traceback
from db import init_db
from game import username_screen, main_menu, play_game, leaderboard_screen, settings_screen

pygame.init()

def main():
    try:
        init_db()
    except Exception:
        print("Database connection error:")
        traceback.print_exc()
        return

    username = username_screen()

    if username == "quit":
        pygame.quit()
        return

    while True:
        choice = main_menu(username)

        if choice == "play":
            while True:
                result = play_game(username)

                if result == "retry":
                    continue

                if result == "menu":
                    break

                if result == "quit":
                    pygame.quit()
                    return

        elif choice == "leaderboard":
            result = leaderboard_screen()

            if result == "quit":
                pygame.quit()
                return

        elif choice == "settings":
            result = settings_screen()

            if result == "quit":
                pygame.quit()
                return

        elif choice == "quit":
            pygame.quit()
            return

if __name__ == "__main__":
    main()