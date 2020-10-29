"""
 *****************************************************************************
   FILE:        Game.py

   AUTHOR:      Lucas Barusek

   ASSIGNMENT:  Final Project

   DATE:        November 20, 2018

   DESCRIPTION: This program is a functioning version of the board game 
                boggle. It supports up to five players with each round lasting
                twenty seconds. As many rounds as desired can be played and 
                a winner is declared when the game is stopped.The game 
                utilizes the cs110 graphics package for all the graphical 
                components and uses obeject oriented programming for the 
                logic of the game.

 *****************************************************************************
"""


from random import choice
from cs110graphics import *


class Board:
    """ Creates the Board"""

    def __init__(self, win, length, center, num_players, player_scores, words):
        """ The constructor for the Board """
        
        self._win = win                        # the graphics window
        self._length = length                  # the length of the board
        self._center = center                  # the center of the board
        self._num_players = num_players        # the number of playersS
        self._player_scores = player_scores    # the scores of the players
        self._words = words                    # the list of all real words

        # creates the variable for sumbitted words
        self._possible_word = ''

        # creates the variable to keep track of the previous tile
        self._previous_tile = '' 

        # creates the variable to keep track of which pkayer is going    
        self._player = 0 

        # creates the board   
        self._board = Rectangle(self._win, self._length + 400,
                                self._length + 400, self._center)
        self._board.set_fill_color('deepskyblue')
        self._win.add(self._board)

        # crates the text diplaying which player is going          
        self._player_turn = Text(self._win, "Player One's Turn!", 30,
                                 (400, 50))
        self._player_turn.set_depth(0)
        self._win.add(self._player_turn)

        # keeps track of whether a boggle press should change the letters
        # or just issue a player change
        self._is_same_round = False

        # stores the list of words for each player
        self._word_list = []

        # stores the list of words for each player and the players index
        self._word_dict = {}

        # list that will store the tiles
        self._tiles = []

        # creats a welcome display on the boggle board
        welcome = [['W', 'E', 'L', 'C'], ['O', 'M', 'E', 'T'],
                   ['O', 'B', 'O', 'G'], ['G', 'L', 'E', '!']]

        # Cite: Prof. Perkins' Lights code

        # creates the 16 tiles on the boggle board and appends them 
        # to the tile list (tile class is on line 312)
        for x in range(4):
            new_row = []
            y_value = int(100 + (self._length // 4) // 2 + x *
                          (self._length // 4))
            for y in range(4):
                x_value = (75 + (self._length // 4) // 2 + y *
                           (self._length // 4))
                tile = Tile(self, self._win, (self._length // 4),
                            (x_value, y_value), (x, y), (welcome[x][y]))
                new_row.append(tile)
            self._tiles.append(new_row)

        # creates the boggle button (Boggle class on line 439)
        self._boggle_button = Boggle(self._win, self)

        # creates the button that lets you submit words 
        # (Submit class on line 499)
        self._submit = Submit(self, self._win)

        # creates the box that diplays the word you are currently typing
        # (WordDisplay class on 543)
        self._word_display = WordDisplay(self, self._win)

        # creates the box that will display the countdown timer
        self._timer = Rectangle(self._win, 125, 100, (775, 190))
        self._timer.set_depth(1)
        self._timer.set_fill_color('limegreen')
        self._win.add(self._timer)

        # creates the the number that will be in the countdown display
        self._timer_num = Text(self._win, '', 60, (775, 190))
        self._timer_num.set_depth(0)
        self._win.add(self._timer_num)

        
    def timer(self):
        """ Keeps track of the time for each round """

        # calls on the code that will end the player's turn after time is up
        RunWithYieldDelay(self._win, self.end_round())

        # calls on the code that will display the countdown timer
        RunWithYieldDelay(self._win, self.set_timer())
        
        
    def end_round(self):
        """ Ends each player's turn after twenty seconds and ends the round
        if the last player has gone"""

        # keeps track of which player is going
        self._player += 1

        # makes it so the boggle button can't be pressed
        self._boggle_button.set_is_active()

        # waits for a little over twenty seconds to account for lag
        yield 23000

        # resets all the tiles to active
        for x in self._tiles:
            for y in x:
                y.set_all_inactive()
        
        # allows the submit button to be pressed
        self.set_submit_active()

        # appends the word list to the dictionary containing the lists of words
        self._word_dict[self._player] = self._word_list

        # resets the word list for the new turn
        self._word_list = []

        # resets the word display
        self._word_display.reset_display()

        # makes it so the boggle button can be pressed
        self._boggle_button.set_is_active()

        # resets the current word to nothing
        self.new_word()

        # sets the player player to show whose turn it is
        self.set_player_turn()
        
        # checks if the last player has gone
        if self._player == self._num_players:
            
            # removes everything on the boggle board from the window
            self._boggle_button.remove()
            self._word_display.remove()
            self._win.remove(self._player_turn)
            self._win.remove(self._timer)
            self._win.remove(self._timer_num)
            for row in self._tiles:
                for tile in row:
                    tile.remove()

            # calls on the method that initiates the score screen
            self.score_screen()


    def boggle(self):
        """ Adds new random letters to each tile if the round is over """

        # checks if the round is over, if it is, randomly assigns a 
        # new letter to each tile
        if self._is_same_round is False:
            for row in self._tiles:
                for tile in row:
                    tile.boggle()

        # resets variable to true to indicate that the next time boggle 
        # is pressed, not to reset the letters because it is not the
        # end of the round
        self._is_same_round = True


    def reset_tiles(self):
        """ For each tile, resets them to as if the board was just created """
        
        for row in self._tiles:
            for tile in row:
                tile.reset()


    def compile_letters(self, letter):
        """ Complies each pressed letter into a string """
        
        self._possible_word += letter

    
    def new_word(self):
        """ Resets the word tracker and the tile tracker to blank """
        
        self._possible_word = ''
        self._previous_tile = ''
        

    def append_possible_word(self):
        """ Appends the compiled word to the word list when a word
        is submitted  """

        # resets the word display
        self._word_display.reset_display()
        
        # appends the compiled word to the word list
        if self._possible_word not in self._word_list:
            self._word_list.append(self._possible_word)


    def display_word(self, letter):
        """ Passes the pressed letter to the word display so the 
        word that is being created can be displayed """

        self._word_display.display_word(letter)

    
    def set_previous_tile(self, loc):
        """ sets the location of the previous tile to keep track of
        whether the new tile is a neighbor of the previously clicked tile """

        self._previous_tile = loc


    def is_neighbor(self, current_loc):
        """ checks if the clicked on tile is a neighbor of 
        the previously clicked on tile """

        # defines the directions of all possible neighbors
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        # if statement checks if no tile has been pressed yes; if so
        # returns true
        if self._previous_tile == '':
            return True

        # returns true if the clicked on tile is a neighbor of the 
        # previously clicked tile
        for direc in directions:
            if (self._previous_tile[0] + direc[0], \
                self._previous_tile[1] + direc[1]) == current_loc:
                return True

        # returns False if the clicked on tile is not a neighbor of 
        # the previously clicked tile
        return False

    
    def set_timer(self):
        """ displays the countdown timer """

        # starts the timer at 20
        timer = 20

        # for loop iterates twenty times wating a second each time,
        # subtracts 1 from the timer and displays that number
        for _ in range(0, 21):
            yield 1000
            self._timer_num.set_text(str(timer))
            timer -= 1


    def set_player_turn(self):
        """ Sets display for whose turn it is at the top of the screen """

        # creates a list of all players. (PLayer one is omitted because
        # the display is created with player one)
        players = ["Player Two's", "Player Three's", 
                   "Player Four's", "Player Five's"]

        # checks if the last player has gone, if not, sets the player 
        # display to the next player whose turn it is
        if self._player < self._num_players:
            self._player_turn.set_text(players[self._player - 1] + ' Turn!')

    
    def set_submit_active(self):
        """ toggles whether the submit button can be pressed """

        self._submit.set_is_active()

    
    def score_screen(self):
        """ Once the round is over created the Score Screen """

        # (ScoreScreen class on line 590)
        ScoreScreen(self._win, self._word_dict, self._num_players,
                    self._player_scores, self._words)


class Tile(EventHandler):
    """ Handles the events for the tiles """
    
    def __init__(self, board, win, side, center, loc, start_letter):
        """ The Constructor for each tile """
        
        self._board = board                # the board
        self._win = win                    # the graphical window
        self._side = side                  # the length of tile
        self._center = center              # the center of the tile
        self._loc = loc                    # the grid location of the tile
        self._start_letter = start_letter  # the start letter of each tile

        # creates a variable to store the letter of the tile
        self._cur_let = ''       

        # Keeps track of whether the tiles can be clicked or not          
        self._is_active = False

        # creates the square outline of each tile and adds it to
        # the handler
        self._tile = Square(self._win, self._side, self._center)
        self._tile.set_border_width(1)
        self._tile.set_fill_color('navajowhite')
        self._tile.set_border_color('blue')
        self._tile.set_depth(2)
        self._tile.add_handler(self) 
        self._win.add(self._tile)

        # creates the inscribed circle and adds it to the handler
        self._circle = Circle(self._win, (self._side // 2) - 2, self._center)
        self._circle.set_depth(1)
        self._circle.set_fill_color('blanchedalmond')
        self._circle.add_handler(self)
        self._circle.set_border_color('blanchedalmond')
        self._win.add(self._circle)

        # creates the text that will be displayed on each tile (The tiles
        # initially display 'Welcome to Boggle!')
        self._text = Text(self._win, self._start_letter, 60, self._center)
        self._text.set_depth(0)
        self._text.add_handler(self)
        self._win.add(self._text)

        # defines the letters on each cube to be randomly selected from
        self._cubes = ['R', 'I', 'F', 'O', 'B', 'X',
                       'I', 'F', 'E', 'H', 'E', 'Y',
                       'D', 'E', 'N', 'O', 'W', 'S',
                       'U', 'T', 'O', 'K', 'N', 'D',
                       'H', 'M', 'S', 'R', 'A', 'O',
                       'L', 'U', 'P', 'E', 'T', 'S',
                       'A', 'C', 'I', 'T', 'O', 'A',
                       'Y', 'L', 'G', 'K', 'U', 'E',
                       'QU', 'B', 'M', 'J', 'O', 'A',
                       'E', 'H', 'I', 'S', 'P', 'N',
                       'V', 'E', 'T', 'I', 'G', 'N',
                       'B', 'A', 'L', 'I', 'Y', 'T',
                       'E', 'Z', 'A', 'V', 'N', 'D',
                       'R', 'A', 'L', 'E', 'S', 'C',
                       'U', 'W', 'I', 'L', 'R', 'G',
                       'P', 'A', 'C', 'E', 'M', 'D']
        EventHandler.__init__(self)


    def boggle(self):
        """ From it's own cube, picks one random letter to display"""

        self._cur_let = choice(self._cubes)
        self._text.set_text(self._cur_let)
        self._text.set_depth(0)
        self._win.add(self._text)

   
    def handle_mouse_press(self, _):
        """ This code will activate when the user clicks on the tile """

        # only allows the tile to be clicked on if the tile is active
        # and is a neighbor of the previously clicked tile
        if self._is_active:
            if self._board.is_neighbor(self._loc):

                # passses the pressed letter to the word display
                self._board.display_word(self._cur_let)

                # passes the pressed letter to board method that compiles
                # the possible word
                self._board.compile_letters(self._cur_let)

                # sets the location of the previous tile
                self._board.set_previous_tile(self._loc)

                # sets the tile's fill color to yellow and makes it so 
                # that tile cannot be pressed again 
                self._tile.set_fill_color('yellow')
                self._is_active = False


    def set_is_active(self):
        """ Sets whether the tile can be clicked on or not """

        # sets the tile to the opposite status of what it is currently
        self._is_active = True if self._is_active is False else False
    
        return self._is_active

    
    def set_all_inactive(self):
        """ sets the tile to be active """

        self._is_active = False


    def reset(self):
        """ resets the tiles active status to true and resets the tile's 
        fill color to its original color """

        self._is_active = True
        self._tile.set_fill_color('navajowhite')

    
    def remove(self):
        """ removes all graphical components of the tile from the window """
      
        self._win.remove(self._tile)
        self._win.remove(self._circle)
        self._win.remove(self._text)


class Boggle(EventHandler):
    """ Handles the events of the boggle button """

    def __init__(self, win, board):
        """ The Constructor for the boggle button """

        self._win = win         # the graphical window
        self._board = board     # the board

        # creates the 'Boggle' text on the boggle button and adds it
        # to handler 
        self._text = Text(self._win, 'Boggle', 24, (775, 600))
        self._text.set_depth(0)
        self._text.add_handler(self)
        self._win.add(self._text)

        # creates the boggle button and adds it to handler
        self._boggle = Rectangle(self._win, 125, 100, (775, 600))
        self._boggle.set_depth(1)
        self._boggle.set_fill_color('orange')
        self._boggle.add_handler(self)
        self._win.add(self._boggle)

        # creates a variable that keeps track of whether the boggle 
        # button can be pressed
        self._is_active = True
        EventHandler.__init__(self)


    def handle_mouse_press(self, _):
        """ This code activates when the boggle button is pressed """

        # if the boggle button can be pressed, calls on the timer class,
        # boggles all the tiles, resets all the tiles, and makes it
        # so the submit button can be pressed
        if self._is_active:
            self._board.timer()
            self._board.boggle()
            self._board.reset_tiles()
            self._board.set_submit_active()

    
    def remove(self):
        """ removes all graphical components of the boggle button 
        from the window """

        self._win.remove(self._text)
        self._win.remove(self._boggle)

    
    def set_is_active(self):
        """ sets the active status of the boggle button """

        # sets the boggle button to the opposite status of what it is currently
        self._is_active = True if self._is_active is False else False
        return self._is_active


class Submit(EventHandler):
    """ Handles the events for the submit button """

    def __init__(self, board, win):
        """ The constructor for the submit button """

        self._board = board      # the board
        self._win = win          # the graphical window

        # creates the submit button off of the window and adds it to handler
        self._submit = Square(self._win, 100, (1000, 450))
        self._submit.set_depth(1)
        self._submit.set_fill_color('purple')
        self._submit.add_handler(self)
        self._win.add(self._submit)

        # creates a variable that keeps track of whether the submit
        # button can be pressed
        self._is_active = False
        EventHandler.__init__(self)

    
    def handle_key_release(self, event):
        """ This code activates when the enter key is pressed """

        # when the enter key is pressed, if the submit button is active,
        # appends the possible word to the word list, resets all the tiles,
        # and inidicates that a new word is being pressed
        if event.get_key() == 'Return':
            if self._is_active:
                self._board.append_possible_word()
                self._board.reset_tiles()
                self._board.new_word()


    def set_is_active(self):
        """ sets the active status of the submit button """

        # sets the submit button to the opposite status of what it is currently
        self._is_active = True if self._is_active is False else False
        return self._is_active

            
class WordDisplay:
    """ Class for the word display """

    def __init__(self, board, win):
        """ The constructor for the word display """ 

        self._win = win          # the graphical window
        self._board = board      # the board

        # creates an empty variable that keeps track of the word
        # that is being created
        self._letters = ''

        # creates the box that displays the word that is being created
        self._display = Rectangle(self._win, 125, 100, (775, 400))
        self._display.set_fill_color('mistyrose')
        self._display.set_depth(1)
        self._win.add(self._display)

        # creates graphical display of the word that is being created
        self._text = Text(self._win, self._letters, 12, (775, 400))
        self._text.set_depth(0)
        self._win.add(self._text)


    def display_word(self, letters):
        """ Compiles the word being created and sets the text to
        that word as it's being compiled """
    
        self._letters += letters
        self._text.set_text(self._letters)

    
    def reset_display(self):
        """ Reset the word display to displaying nothing """ 

        self._letters = ''
        self._text.set_text(self._letters)

    
    def remove(self):
        """ Removes all the graphical components of the word display """

        self._win.remove(self._display)
        self._win.remove(self._text)

    
class ScoreScreen:
    """ Class for the Score Screen at the end of the each round"""

    def __init__(self, win, word_dict, num_players, player_scores, words):
        """ The constructor for Score Screen """

        self._win = win              # the graphical window
        self._word_dict = word_dict  # the dictionary with the word lists
        self._num_players = num_players   # the number of players
        self._player_scores = player_scores   # a list of each player's scores
        self._real_words = words           # the list of all real words

        # creates a list to check for duplicate words
        self._duplicate_check = []    

        # creates a list to store the duplicate words
        self._duplicates = []

        # creates a list to store all the words once
        self._no_duplicates = []

        # creates a list of the scorable words
        self._scorable_words = []

        # creates a dictionary of the lists of the scorable words
        self._scorable_dict = {}

        # list of the players
        player_list = ['Player One', 'Player Two', 'Player Three',
                       'Player Four', 'Player Five']

        # creates a dictionary of all the correct words to be displayed
        self._printable_words = self.compile_scorable_words_dict()

        # creates an empty to list to compile the graphical component
        # of each player's word lists
        self._all_words = []

        # for each word list in the dictionary, creates a graphical display 
        # of the word list and appends each list to self._all_words
        # (WordList class on line 735)
        for x in range(num_players):
            self._words = WordList(self, self._win,
                                   self._printable_words[x + 1],
                                   player_list[x], x + 1)
            self._all_words.append(self._words)

        # creates a graphical button that allows the players to play 
        # another round (continues class on line 773)
        self._continue = Continue(self, self._win, self._num_players, 
                                  self._player_scores, self._real_words)

        # creates a graphical button that allows the players to end 
        # the game (End class on line 825)
        self._end = End(self, self._win, self._player_scores)

        # creates a Text object that asks whether the users want to 
        # play another round
        self._next_round = Text(self._win,
                                'Would You Like To Play Another Round?',
                                20, (300, 725))
        self._next_round.set_depth(0)
        self._win.add(self._next_round)

        # creates a graphical separator of dashes at the top and bottom 
        # of screen to make it look nice
        self._top_separator = Text(self._win, '-' * 125, 20, (450, 75))
        self._top_separator.set_depth(0)
        self._win.add(self._top_separator)
        self._bottom_separator = Text(self._win, '-' * 125, 20, (450, 650))
        self._bottom_separator.set_depth(0)
        self._win.add(self._bottom_separator)

        # checks the length of each word in each list and adds the approriate
        # approriate amount of points to the player's score depending on
        # how long the word is 
        for player in range(len(self._player_scores)):
            for word in self._printable_words[player + 1]:
                if len(word) == 3:
                    self._player_scores[player] += 1
                if len(word) == 4:
                    self._player_scores[player] += 2
                if len(word) == 5:
                    self._player_scores[player] += 3
                if len(word) == 6:
                    self._player_scores[player] += 5
                if len(word) == 7:
                    self._player_scores[player] += 7
                if len(word) >= 8:
                    self._player_scores[player] += 10
                else:
                    self._player_scores[player] += 0

    
    def compile_scorable_words_dict(self):
        """ compiles a dictionary of all the words that pass all
        the rules of boggle """

        # creates a flattened list of every word each player submitted
        for key in self._word_dict:
            for word in self._word_dict[key]:
                self._duplicate_check.append(word)

        # creates a list of all the words that appear twice 
        # in the flattened list (self._duplicates) and a list
        # of all the words but each word only appears once (self._originals)
        for word in self._duplicate_check:
            if word not in self._no_duplicates:
                self._no_duplicates.append(word)
            else:
                self._duplicates.append(word)
        
        # iterates through the no duplicates list and checks if
        # each word in that list is not a duplicate, is a real 
        # english word, and is longer than two characters. If so,
        # appends that word to self._scorable_words
        for word in self._no_duplicates:
            if word not in self._duplicates:
                if word in self._real_words and len(word) > 2:
                    self._scorable_words.append(word)

        # for each scorable word, checks what player submitted
        # that word and creates a dictiionary (self._scorable_dict) that
        # stores each word at the key of player that sumbitted it 
        for key in self._word_dict:
            word_list = []
            for scorable_word in self._scorable_words:
                if scorable_word in self._word_dict[key]:
                    word_list.append(scorable_word)
            self._scorable_dict[key] = word_list

        return self._scorable_dict

            
    def remove(self):
        """ removes all graphical components of the score
        screen from the window """

        self._win.remove(self._top_separator)
        self._win.remove(self._bottom_separator)
        self._win.remove(self._next_round)
        self._continue.remove()
        self._end.remove()
        for words in self._all_words:
            words.remove()


class WordList:
    """ Creates a graphical display of each player's word list """

    def __init__(self, score_screen, win, word_list, player, x_loc):
        """ The constructor for word list """

        self._score_screen = score_screen  # the score screen
        self._win = win                    # the graphical window
        self._word_list = word_list        # the player's list of words
        self._x_loc = (x_loc * 175) - 75   # the X-loc of each word
        self._words = []        # an empty list to append each graphical word to
        self._player = player   # the  player whose list is being displayed

        # Creates a Text object above the word list that displays
        # whose player's words are being displayed
        self._player_display = Text(self._win, self._player, 22, 
                                    (self._x_loc, 50))
        self._player_display.set_depth(0)
        self._win.add(self._player_display)

        # Creates a vertical display of all the all the words in 
        # the word list and add each word to self._words
        for y_loc in range(len(self._word_list)):
            self._word = Text(self._win, str(self._word_list[y_loc]),
                              20, (self._x_loc, (y_loc + 1) * 30 + 75))
            self._win.add(self._word)
            self._word.set_depth(0)
            self._words.append(self._word)

        
    def remove(self):
        """ removes all the words and the player display from the window """

        for word in self._words:
            self._win.remove(word)
        self._win.remove(self._player_display)


class Continue(EventHandler):
    """  The class for the button that allows another round to be played """ 

    def __init__(self, score_screen, win, num_players, player_scores, words):
        """ The constructor for the continue button """

        self._score_screen = score_screen    # the score screen
        self._win = win                      # the grapical window
        self._num_players = num_players      # the number of players
        self._player_scores = player_scores  # the list of the player's scores
        self._words = words                  # the list of all real words

        # creates the graphical button to trigger another round
        self._continue = Square(self._win, 100, (650, 725))
        self._continue.set_depth(1)
        self._continue.set_fill_color('darkgreen')
        self._win.add(self._continue)

        # adds the text to the graphical button saying 'Yes'
        self._yes = Text(self._win, 'YES', 30, (650, 725))
        self._yes.set_depth(0)
        self._win.add(self._yes)

        # adds both graphical objects to the handler
        self._continue.add_handler(self)
        self._yes.add_handler(self)

        EventHandler.__init__(self)

    
    def handle_mouse_press(self, _):
        """ this code is activated when the user clicks on the 
        graphical objects """

        # calls on a mathed in the score screen that removes all
        # graphical objects 
        self._score_screen.remove()

        # calls on the board class passing the new scores creating
        # a new round while keeping track of the scores
        Board(self._win, 600, (450, 400), self._num_players, 
              self._player_scores, self._words)


    def remove(self):
        """ removes all graphical objects in the continue 
        button from the window """

        self._win.remove(self._continue)
        self._win.remove(self._yes)


class End(EventHandler):
    """ The class for the button that ends the game """

    def __init__(self, score_screen, win, player_scores):
        """ The constructor for the end game button  """

        self._score_screen = score_screen    # the score screen
        self._win = win                      # the graphical window
        self._player_scores = player_scores  # the player scores

        # creates the graphical button to end the game
        self._end = Square(self._win, 100, (800, 725))
        self._end.set_depth(1)
        self._end.set_fill_color('red')
        self._win.add(self._end)

        # creates a text object on the button that says 'no'
        self._no = Text(self._win, 'NO', 30, (800, 725))
        self._no.set_depth(0)
        self._win.add(self._no)

        # adds both graphical objects to the handler
        self._end.add_handler(self)
        self._no.add_handler(self)

        EventHandler.__init__(self) 

    
    def handle_mouse_press(self, _):
        """ This code activates when the user clicks on 
        the button"""

        # calls on a methed in the score screen that removes all
        # graphical objects (EndScreen class on line 871)
        self._score_screen.remove()
        EndScreen(self._win, self._player_scores)

    
    def remove(self):
        """ removes all graphical objects in the end
        button from the window """

        self._win.remove(self._end)
        self._win.remove(self._no)


class EndScreen:
    """ class that diplays the end of game screen """

    def __init__(self, win, player_scores):
        """ The constructor for the End Screen """

        self._win = win                      # the graphical window
        self._player_scores = player_scores  # the player scores

        # creates a text object that will display the winner
        self._winner = Text(self._win, '', 29, (450, 150))
        self._winner.set_depth(0)
        self._win.add(self._winner)

        # creates a final image
        self._image = Image(self._win, 'Thanks.png', 900, 800, (450, 400))
        self._image.set_depth(1)

        # creates a text object that thanks the users for players
        # self._thanks = Text(self._win, 'Thanks For Playing!', 40, (450, 400))
        # self._thanks.set_depth(0)
        # self._win.add(self._thanks)

        # calls on the method that declares the winner
        self.declare_winner()

    
    def declare_winner(self):
        """ Defines the high score of all the players and determines
        whether there was a tie or single winner """

        # creates a copy of self._player_scores that I can modify 
        # without modifying self._player_scores itself
        check_player_scores = []
        for score in self._player_scores:
            check_player_scores.append(score)

        # finds the highest score in the list
        high_score = max(self._player_scores)

        # creates an empty list to store the indexes of where the 
        # high score is found
        high_scores_index = []

        # finds each index for where the high score is found and 
        # appends it to high_scores_index
        for score in check_player_scores:
            if score == high_score:
                index = check_player_scores.index(score)
                high_scores_index.append(index)
                check_player_scores[index] = -1

        # checks if multiple players have the same high score, if so
        # calls the tie screen
        if len(high_scores_index) != 1:
            self.display_tie(high_scores_index, high_score)

        # if the high score was only found once, displays the winner screen
        else:
            self.display_winner(self._player_scores.index(high_score) + 1,
                                high_score)


    def display_tie(self, winner_indexes, high_score):
        """ Displays the tie text """

        # creates a string of all the players that have the high score
        winners = ''
        for winner in winner_indexes:
            winners += str(winner + 1) + ', '
        # splices off the last comma and space
        winners = winners[:-2]

        # sets the text to display the winners and their score 
        self._winner.set_text('The winners are players {} with a Score \
of {}'.format(winners, high_score))

        # adds thank you image to screen
        self._win.add(self._image)


    def display_winner(self, winner_index, high_score):
        """ Displays the winner text """

        self._winner.set_text('The Winner is Player {} with a Score \
of {}'.format(winner_index, high_score))

        # adds thank you image to screen
        self._win.add(self._image)


class PlayerButtons(EventHandler):
    """ Handles the events for each player select button """

    def __init__(self, player_select_screen, win, number, color):
        """ The Constructor for each player select button """
        
        self._player_select_screen = player_select_screen  # the board
        self._win = win                    # the graphical window
        self._number = str(number)         # the number on the button
        self._num_players = int(number)    # the amount of players if selected
        self._color = color                # the color of the player button

        # the x pixel location of the player button
        self._loc = (self._num_players - 1) * 175

        # creates the button that the user can click to
        # select the number of players
        self._tile = Square(self._win, 100, (self._loc, 580))
        self._tile.set_fill_color(self._color)
        self._tile.set_depth(1)

        # Creates a text object that displays the amount of players option
        self._text = Text(self._win, self._number, 60, (self._loc, 580))
        self._text.set_depth(0)

        # adds both graphical components to the handler and the window
        self._tile.add_handler(self)
        self._text.add_handler(self)
        self._win.add(self._text)
        self._win.add(self._tile)

        EventHandler.__init__(self)

    
    def handle_mouse_press(self, _):
        """ This code activates when one of the player amount 
        options is clicked """

        # calls on a methed in the player select screen 
        # that removes all graphical objects
        self._player_select_screen.remove()

        # passes the window and the number of players
        # selected to play_game (play_game on line 1071)
        play_game(self._win, self._num_players)

    
    def remove(self):
        """ moves the tile and number off the board """

        self._tile.move_to((1000, 1000))
        self._text.move_to((1000, 1000))


class PlayerSelectScreen:
    """ Creates the player select screen """

    def __init__(self, win):
        """ The constructor for the player select screen """

        self._win = win       # the graphical window
        self._tiles = []      # empty list to store all the tiles

        # the list of colors that will be each tile
        self._tile_colors = ['cornflowerblue', 'red', 'forestgreen', 'orange']

        # puts the boggle logo on the player select screen
        self._image = Image(self._win, 'Boggle.jpg', 400, 275, (450, 175))
        self._image.set_depth(0)
        self._win.add(self._image)

        # creates a player select button for 2, 3, 4, and 5 players
        # (PlayerButtons class on line 962)
        for i in range(2, 6):
            tile = PlayerButtons(self, self._win, i, self._tile_colors[i - 2])
            self._tiles.append(tile)

        # creates a Text object that gives the user directions 
        self._directions = Text(self._win, "Select the Number of Players",
                                36, (450, 400))
        self._directions.set_depth(0)
        self._win.add(self._directions)


    def remove(self):
        """ Gets rid of the player select screen and initiates 
        the boggle board """

        for tile in self._tiles:
            tile.remove()
        self._win.remove(self._directions)
        self._win.remove(self._image)


def dictionary():
    """ compiles a list of all real english words """

    # opens the date file and puts all the words in a list
    with open('English Words.txt') as data_file:
        words = data_file.readlines()
    
    # removes the new line characters from all the words in the 
    # list except the last one
    for word in range(len(words) - 1):
        words[word] = words[word][:-1]

    return words


def play_game(win, num_players):
    """ Creates the boggle board """

    # creates a nested list with the amount of 
    # lists in the list corresponding to the number
    # of players selected to keep track of each score
    player_scores = []
    for _ in range(num_players):
        player_scores.append(0)

    word_list = dictionary()

    # creates the board game (Board class on line 26)
    Board(win, 600, (450, 400), num_players, player_scores, word_list)
    

def program(win):
    """ sets the length and width of the window
    and initializes the player select screen """

    win.set_width(900)
    win.set_height(800)

    # (PlayerSelectScreen Class on line 1016)
    PlayerSelectScreen(win)


def main():
    """The main function """

    StartGraphicsSystem(program)

if __name__ == "__main__":
    main()
