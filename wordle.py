import random
import os
import msvcrt

with open("words.txt","r") as f:
	lines = f.readlines()

def clear_screen():
	if os.name == "posix":  # for UNIX and Linux
		os.system("clear")
	elif os.name == "nt":  # for Windows
		os.system("cls")

def waitfor_user_input_char():
	input_string = ""
	while True:
		if msvcrt.kbhit():
			key = msvcrt.getch()
			key_char = key.decode('utf-8')
			return key_char


def print_colored(text, color):
	returnstring = ""
	color_code = {
		"black"     : '\033[40m',
		"red"       : '\033[41m',
		"green"     : '\033[42m',
		"yellow"    : '\033[43m',
		"blue"      : '\033[44m',
		"magenta"   : '\033[45m',
		"cyan"      : '\033[46m',
		"white"     : '\033[47m',
		"grey"      : '\033[100m',
	}

	reset = '\033[0m'

	if color not in color_code:
		# print(text,end="")
		returnstring += text
		return returnstring
	# print(f"{color_code[color]} {text} {reset}",end="")
	returnstring += f"{color_code[color]} {text} {reset}"
	return returnstring

def draw_horizontal_line(wordlen,line_characters = "  - "):
	returnstring = ""
	for j in range(wordlen):
		# print(line_characters,end="")
		returnstring += line_characters
	# print(line_characters)
	
	# print("")
	returnstring += "\n"
	return returnstring

class Game:
	def __init__(self,tip_num,filename,word=None,num_of_letters_if_random = None):
		self.filename                       = filename
		self.word_list                      = []
		if word != None:
			self.word                           = word
			self.wordlen                        = len(self.word)
			self.get_word_list(self.wordlen)
		else:
			self.wordlen                        = num_of_letters_if_random
			self.get_word_list(self.wordlen)
			self.word                           = random.choice(self.word_list)

			


		self.tip_num                        = tip_num
		self.tip_list                       = []
		self.used_letters                   = {}#letter:color
		self.letters                        = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
		self.color_list                     = ["black","grey","green","black"]
		self.vertical_separate_character  = "|"
		self.current_user_input             = ""
		self.WIN                            = "win"
		self.LOST                           = "lost"
		self.PLAY                           = "play"
		self.game_state                     =  self.PLAY
		self.system_message                 = ""
	
	def NOT_IN_WORD (self): return self.color_list[0]
	def IN_WORD     (self): return self.color_list[1]
	def RIGHT_SPOT  (self): return self.color_list[2]
	def NOT_SELECTED(self): return self.color_list[3]
	
	def print_letters(self):
		returnstring = " "
		# for letter in self.letters:
		for i in range(len(self.letters)):
			if i % (self.wordlen) == 0:
				returnstring += "\n "
			returnstring += print_colored(self.letters[i],self.used_letters[self.letters[i]] if self.letters[i] in self.used_letters.keys() else "black")
			returnstring += " "
		returnstring += "\n"
		return returnstring
	def add_letter(self,letter,color):
		if letter in self.used_letters.keys():
			if self.color_list.index(color) > self.color_list.index(self.used_letters[letter]):
				self.used_letters[letter] = color
		else:
			self.used_letters[letter] = color

	def get_word_list(self,num_of_letters):
		with open(self.filename,"r") as f:
			lines = f.readlines()
			for line in lines:
				word = line.strip()
				if word.islower():
					word =  word.upper()
				if len(word) == num_of_letters:
					# print(word)
					self.word_list.append(word)
		
	def check_tip(self,word):
		if len(word) < self.wordlen:
			self.system_message = "The word is too short"
			return False
		if len(word) > self.wordlen:
			self.system_message = "The word is too long"
			return False
		if word in self.tip_list:
			self.system_message = "Cannot try the same word twice"
			return False
		if word not in self.word_list:
			self.system_message = "This word is not in the dictionary"
			return False
		return True
	
	def add_tip(self,word):
		tip_check_result = self.check_tip(word)
		if tip_check_result != True:
			return False
		else:
			self.tip_list.append(word)
			for i in range(self.wordlen):
				if word[i] == self.word[i]:
					self.add_letter(word[i],self.RIGHT_SPOT())
				elif word[i] in self.word:
					self.add_letter(word[i],self.IN_WORD())
		return True
	def write_word(self,word,no_color = False):
		returnstring = ""
		for j in range(self.wordlen):
			returnstring += self.vertical_separate_character
			if word != "" and word != None:
				# print_colored(word[j],self.used_letters[word[j]] if word[j] in self.used_letters.keys() else self.NOT_IN_WORD())
				if no_color == True:
					returnstring += print_colored(word[j],self.NOT_SELECTED())
				else:
					if word[j] == self.word[j]:
						returnstring += print_colored(word[j],self.RIGHT_SPOT())
					elif word[j] in self.word:
						returnstring += print_colored(word[j],self.IN_WORD())
					else:
						returnstring += print_colored(word[j],self.NOT_IN_WORD())
			else:
				returnstring += "   "
		returnstring += self.vertical_separate_character
		returnstring += "\n"
		return returnstring

	def draw_board(self):
		returnstring = ""
		tiplist = self.tip_list.copy()
		current_tip = ""
		if len(self.tip_list) < self.tip_num and self.current_user_input != "":
			current_tip = self.current_user_input
			while len(current_tip) != self.wordlen:
				# print(f"word is:{tiplist[-1]}, len is:{len(tiplist[-1])}")
				current_tip += " "


		for i in range(self.tip_num):
			returnstring += draw_horizontal_line(self.wordlen)
			if len(tiplist) < i:
				returnstring += self.write_word("")	
			elif len(tiplist) == i:
				returnstring += self.write_word(current_tip,no_color=True)
			else:
				returnstring += self.write_word(tiplist[i])
		returnstring += draw_horizontal_line(self.wordlen)
		return returnstring

	def is_over_game(self):
		if len(self.tip_list) == 0:
			return False
		if self.tip_list[len(self.tip_list)-1] == self.word:
			self.system_message = "You won"
			return True
		if len(self.tip_list) == self.tip_num:
			self.system_message = "You lost"
			return True

	def read_user_input(self):
		user_input = waitfor_user_input_char()
		self.system_message = ""
		if user_input == "\b":
			if len(self.current_user_input) > 0:
				self.current_user_input = self.current_user_input[0:-1]
		elif user_input == "\r":
			if(self.add_tip(self.current_user_input)):
				self.current_user_input = ""
		else:
			if user_input.islower():
				user_input =  user_input.upper()
			if len(self.current_user_input) < self.wordlen:
				self.current_user_input += user_input
			else:
				self.system_message = "Word is too long"

	def draw_display(self):
		screen_to_display = ""
		# clear_screen()
		screen_to_display = "\033[H\033[J"
		screen_to_display += draw_horizontal_line(self.wordlen+1,line_characters="____")
		screen_to_display += self.draw_board()
		screen_to_display += self.print_letters()
		screen_to_display += self.system_message
		print(screen_to_display,end="")

	def play(self):
		self.draw_display()
		while(True):
			returnstring = ""
			# draw_horizontal_line(self.wordlen)
			self.read_user_input()
			is_over = self.is_over_game()
			self.draw_display()
			if is_over:
				return


			# wordin = input("Write your word: ")
			# self.add_tip(wordin)


# draw_board(["bride","bowel"],"blade",6)


game = Game(6,"words.txt",num_of_letters_if_random=5)
game.play()




