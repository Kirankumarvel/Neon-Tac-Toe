import os
import time
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

class EnhancedBoard:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset the board to empty state"""
        self.cells = [" " for _ in range(9)]
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
    def display(self):
        """Display the current board state with colors and borders"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.YELLOW + "\n   TIC-TAC-TOE   \n")
        print(Fore.CYAN + "    1 | 2 | 3 ")
        print("   -----------")
        print(Fore.CYAN + "    4 | 5 | 6 ")
        print("   -----------")
        print(Fore.CYAN + "    7 | 8 | 9 \n")
        
        print(Fore.WHITE + "  Current Board:")
        for i in range(0, 9, 3):
            row = []
            for cell in self.cells[i:i+3]:
                if cell == "X":
                    row.append(Fore.RED + " X " + Style.RESET_ALL)
                elif cell == "O":
                    row.append(Fore.BLUE + " O " + Style.RESET_ALL)
                else:
                    row.append("   ")
            print(Fore.WHITE + "  " + "|".join(row))
            if i < 6:
                print("  ----------")
        print()
        
    def update(self, position, symbol):
        """Update the board with player's move"""
        if self.is_valid_move(position):
            self.cells[position-1] = symbol
            return True
        return False
        
    def is_valid_move(self, position):
        """Check if the move is valid"""
        return 1 <= position <= 9 and self.cells[position-1] == " "
        
    def is_full(self):
        """Check if the board is full"""
        return " " not in self.cells
        
    def check_winner(self, symbol):
        """Check if the current player has won"""
        for combo in self.winning_combinations:
            if all(self.cells[i] == symbol for i in combo):
                # Highlight winning combination
                for i in combo:
                    if symbol == "X":
                        self.cells[i] = Fore.RED + Style.BRIGHT + "X" + Style.RESET_ALL
                    else:
                        self.cells[i] = Fore.BLUE + Style.BRIGHT + "O" + Style.RESET_ALL
                return True
        return False

class EnhancedPlayer:
    def __init__(self, name, symbol, color):
        self.name = name
        self.symbol = symbol
        self.color = color
        self.score = 0
        
    def get_move(self):
        """Get player's move from input with validation"""
        while True:
            try:
                move = input(f"{self.color}{self.name}'s turn ({self.symbol}): " + 
                            Fore.YELLOW + "Enter position (1-9)" + Style.RESET_ALL + ": ")
                if move.lower() == 'q':
                    return 'quit'
                move = int(move)
                if 1 <= move <= 9:
                    return move
                print(Fore.RED + "Please enter a number between 1-9!")
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter a number.")

class EnhancedTicTacToe:
    def __init__(self):
        self.board = EnhancedBoard()
        self.players = []
        self.current_player = None
        self.game_count = 1
        
    def display_header(self):
        """Display game header with scores"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.GREEN + Style.BRIGHT + "="*40)
        print(f"  TIC-TAC-TOE | GAME {self.game_count}")
        print("="*40)
        print(Fore.CYAN + f"  {self.players[0].name}: {self.players[0].score} " + 
              Fore.WHITE + "vs " + 
              Fore.CYAN + f"{self.players[1].name}: {self.players[1].score}")
        print(Fore.GREEN + "="*40 + Style.RESET_ALL)
        
    def setup_players(self):
        """Setup players with names and symbols"""
        print(Fore.YELLOW + "\nPLAYER SETUP\n" + Style.RESET_ALL)
        player1_name = input(Fore.RED + "Enter Player 1 name (X): " + Style.RESET_ALL)
        player2_name = input(Fore.BLUE + "Enter Player 2 name (O): " + Style.RESET_ALL)
        
        self.players = [
            EnhancedPlayer(player1_name, "X", Fore.RED),
            EnhancedPlayer(player2_name, "O", Fore.BLUE)
        ]
        self.current_player = self.players[0]
        
    def switch_player(self):
        """Switch to the other player"""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
        
    def play_turn(self):
        """Handle a single turn"""
        self.display_header()
        self.board.display()
        
        move = self.current_player.get_move()
        if move == 'quit':
            return False
            
        if not self.board.update(move, self.current_player.symbol):
            print(Fore.RED + "\nThat position is already taken or invalid!")
            time.sleep(1.5)
            return True
            
        if self.board.check_winner(self.current_player.symbol):
            self.display_header()
            self.board.display()
            self.current_player.score += 1
            print(Fore.MAGENTA + Style.BRIGHT + f"\nCONGRATULATIONS {self.current_player.name}! YOU WON! 🎉")
            return False
            
        if self.board.is_full():
            self.display_header()
            self.board.display()
            print(Fore.YELLOW + Style.BRIGHT + "\nIT'S A TIE! 🤝")
            return False
            
        self.switch_player()
        return True
        
    def play(self):
        """Main game loop"""
        self.setup_players()
        
        while True:
            self.board.reset()
            self.display_header()
            
            continue_playing = True
            while continue_playing:
                continue_playing = self.play_turn()
                
            if not self.play_again():
                break
                
            self.game_count += 1
            self.switch_player()  # Alternate who starts
            
    def play_again(self):
        """Ask players if they want to play again"""
        print(Fore.WHITE + "\nGame Over!")
        while True:
            choice = input(Fore.CYAN + "Play again? (y/n): " + Style.RESET_ALL).lower()
            if choice == 'n':
                self.display_final_scores()
                return False
            elif choice == 'y':
                return True
            print(Fore.RED + "Invalid choice! Please enter 'y' or 'n'.")
                
    def display_final_scores(self):
        """Show final scores when game ends"""
        print(Fore.GREEN + "\nFINAL SCORES:")
        print(Fore.CYAN + f"{self.players[0].name}: {self.players[0].score}")
        print(Fore.CYAN + f"{self.players[1].name}: {self.players[1].score}")
        if self.players[0].score > self.players[1].score:
            print(Fore.MAGENTA + f"\n{self.players[0].name} WINS THE SERIES! 🏆")
        elif self.players[1].score > self.players[0].score:
            print(Fore.MAGENTA + f"\n{self.players[1].name} WINS THE SERIES! 🏆")
        else:
            print(Fore.YELLOW + "\nTHE SERIES ENDED IN A TIE! 🤝")

if __name__ == "__main__":
    try:
        game = EnhancedTicTacToe()
        game.play()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nGame interrupted. Thanks for playing!")
    finally:
        print(Style.RESET_ALL)
