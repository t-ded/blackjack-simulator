import random
import numpy as np
import matplotlib.pyplot as plt

J = 10
Q = 10
K = 10
A = 11
A1 = 1

H = "Hit"
D = "Double"
S = "Stand"
Sur = "Surrender"
Sp = "Split"

class Deck:
	def __init__(self, number_of_decks=1):
		self.deck = number_of_decks*[2, 2, 2, 2, 
									3, 3, 3, 3, 
									4, 4, 4, 4, 
									5, 5, 5, 5, 
									6, 6, 6, 6, 
									7, 7, 7, 7, 
									8, 8, 8, 8, 
									9, 9, 9, 9, 
									10, 10, 10, 10, 
									J, J, J, J, 
									Q, Q, Q, Q, 
									K, K, K, K, 
									A, A, A, A]
									
	#Used when players need to draw cards from the deck
	def draw(self):
		crd = random.choice(self.deck)
		self.deck.remove(crd)
		return crd
		
	#Returns numerical value which says how many cards are left in the deck
	def __len__(self):
		return len(self.deck)
	



class Hand:
	#Hand is created by drawing 2 cards from the deck
	def __init__(self, deck):
		self.hand = [deck.draw(), deck.draw()]
		
	#Return sum of values of player´s cards
	def hand_val(self):
		return sum(self.hand)
		
	#Draw a card from the Deck object
	def draw(self, deck):
		self.hand.append(deck.draw())
		
	#When Player exceeds 21 and has Ace
	def reduce_A(self):
		A_i = self.hand.index(A)
		self.hand[A_i] = A1
	
	#Creating Dealer´s drawing algorithm for both the Player and the Delaer
	def dealer_alg(self, deck, hit_soft_17):
		while True:
			if self.hand_val() > 17:
				if self.hand_val() > 21:
					if A in self.hand:
						self.reduce_A()
						continue
				break
			else:
				if self.hand_val() == 17:
					if hit_soft_17 and A in self.hand:
						self.draw(deck)
					else:
						break
				else:
					self.draw(deck)	




class Dealer(Hand):
	#Returns the card of the dealer which is visible
	def upcard(self):
		return self.hand[0]




class Player(Hand):
	#Returns the Move which should be made according to the Basic Strategy
	def FindMove(self, dealers_upcard, split=False, soft=False, 
				first=True, num_decks=1, dealer_hit_soft_17=False, 
				surr=True, double_after_split=True):
	
		if A in self.hand:
			soft = True
		pair = False
		if split:
			if not double_after_split:
				first = False
			if len(self.hand) > 1:
				first = False
		else:
			if len(self.hand) > 2:
				first = False
			else:
				if self.hand[0] == self.hand[1]:
					pair = True
				elif self.hand[0] in [A, A1] and self.hand[1] in [A, A1]:
					pair = True
		surr = surr if first and not split else False
				
		d = dealers_upcard
		s = self.hand_val()
		
		if num_decks == 1:
			if not dealer_hit_soft_17:
			
				if not pair:
					if soft:
					#Hand is soft
						
						if s <= 16:
							if 4 <= d <= 6:
								return D if first else H
							return H
						
						if s == 17:
							if d <= 6:
								return D if first else H
							return H
						
						if s == 18:
							if 3 <= d <=6:
								return D if first else S
							elif 9 <= d <= 10:
								return H
							return S
						
						if s == 19:
							if d == 6:
								return D if first else S
							return S
						
						else:
							return S
					
					else:
					#Hand is not soft
						
						if s <= 7:
							return H
						
						if s == 8:
							if 5 <= d <= 6:
								return D if first else H
							return H
						
						if s == 9:
							if d <= 6:
								return D if first else H
							return H
						
						if s == 10:
							if d <= 9:
								return D if first else H
							return H
						
						if s == 11:
							return D if first else H
						
						if s == 12:
							if 4 <= d <= 6:
								return S
							return H
						
						if s == 13:
							if d <= 6:
								return S
							return H
						
						if s == 14:
							if d <= 6:
								return S
							return H
						
						if s == 15:
							if d <= 6:
								return S
							return H
						
						if s == 16:
							if d <= 6:
								return S
							elif 10 <= d:
								return Sur if surr else H
							return H
						
						else:
							return S
				
				else:
				#Hand is pair
				
					if s == 4:
						if d == 2:
							return Sp if double_after_split else H
						if 3 <= d <= 7:
							return Sp
						return H
					
					if s == 6:
						if d <= 3 or d == 8:
							return Sp if double_after_split else H
						if 4 <= d <= 7:
							return Sp
						return H
					
					if s == 8:
						if 4 == d:
							return Sp if double_after_split else H
						if 5 <= d <= 6:
							return Sp if double_after_split else D
						return H
					
					if s == 10:
						if d <= 9:
							return D if first else H
						return H
					
					if s == 12:
						if d == 7:
							return Sp if double_after_split else H
						if d <= 6:
							return Sp
						return H
					
					if s == 14:
						if d == 8:
							return Sp if double_after_split else H
						if d <= 7:
							return Sp
						if d == 10:
							return Sur if surr else S
						return H
					
					if s == 16:
						return Sp
					
					if s == 18:
						if d == 7 or d >= 10:
							return S
						return Sp
					
					if s == 20:
						return S
					
					if s == 22:
						return Sp

			else:
			#Dealer hits on Soft 17
			
				if not pair:
					if soft:
					#Hand is soft
						
						if s <= 16:
							if 4 <= d <= 6:
								return D if first else H
							return H
						
						if s == 17:
							if d <= 6:
								return D if first else H
							return H
						
						if s == 18:
							if 3 <= d <=6:
								return D if first else S
							elif 9 <= d:
								return H
							return S
						
						if s == 19:
							if d == 6:
								return D if first else S
							return S
						
						else:
							return S
					
					else:
					#Hand is not soft
						
						if s <= 7:
							return H
						
						if s == 8:
							if 5 <= d <= 6:
								return D if first else H
							return H
						
						if s == 9:
							if d <= 6:
								return D if first else H
							return H
						
						if s == 10:
							if d <= 9:
								return D if first else H
							return H
						
						if s == 11:
							return D if first else H
						
						if s == 12:
							if 4 <= d <= 6:
								return S
							return H
						
						if s == 13:
							if d <= 6:
								return S
							return H
						
						if s == 14:
							if d <= 6:
								return S
							return H
						
						if s == 15:
							if d <= 6:
								return S
							elif 10 < d:
								return Sur if surr else H
							return H
						
						if s == 16:
							if d <= 6:
								return S
							elif 10 <= d:
								return Sur if surr else H
							return H
						
						if s == 17:
							if 10 < d:
								return Sur if surr else S
							return S
						
						else:
							return S
				
				else:
				#Hand is pair
				
					if s == 4:
						if d == 2:
							return Sp if double_after_split else H
						if 3 <= d <= 7:
							return Sp
						return H
					
					if s == 6:
						if d <= 3 or d == 8:
							return Sp if double_after_split else H
						if 4 <= d <= 7:
							return Sp
						return H
					
					if s == 8:
						if 4 == d:
							return Sp if double_after_split else H
						if 5 <= d <= 6:
							return Sp if double_after_split else D
						return H
					
					if s == 10:
						if d <= 9:
							return D if first else H
						return H
					
					if s == 12:
						if d == 7:
							return Sp if double_after_split else H
						if d <= 6:
							return Sp
						return H
					
					if s == 14:
						if d == 8:
							return Sp if double_after_split else H
						if d <= 7:
							return Sp
						if d == 10:
							return Sur if surr else S
						if 10 < d:
							return Sur if surr else H
						return H
					
					if s == 16:
						return Sp
					
					if s == 18:
						if d == 7 or d == 10:
							return S
						if 10 < d:
							return Sp if double_after_split else S
						return Sp
					
					if s == 20:
						return S
					
					if s == 22:
						return Sp
				

	#For card counting
	def count(self, dealer):
		c = 0
		for card in self.hand:
			if card < 7:
				if card == A1:
					c -= 1
				else:
					c += 1
			elif card > 9:
				c -= 1
		for card in dealer.hand:
			if card < 7:
				if card == A1:
					c -= 1
				else:
					c += 1
			elif card > 9:
				c -= 1
		return c




#For player hands created by splitting
class SpPlayer(Player):
	def __init__(self, player):
		self.hand = [player.hand.pop()]
	
	def count(self, p2, dealer):
		c = 0
		for player_hand in [self, p2]:
			for card in player_hand.hand:
				if card < 7:
					if card == A1:
						c -= 1
					else:
						c += 1
				elif card > 9:
					c -= 1
		for card in dealer.hand:
			if card < 7:
				if card == A1:
					c -= 1
				else:
					c += 1
			elif card > 9:
				c -= 1
		return c




class Game:
	
	def __init__(self, number_of_decks=1, dealer_hit_soft_17=False, surr=True, double_after_split=True, 
				BJ=[3, 2], insurance=True, insurance_rate=[2, 1], strategy=2, 
				budget=np.inf, min_bet=5, max_bet=100, deck_to_shuffle=0.5, games_to_shuffle=5):
		
		#Set Rules
		self.number_of_decks = number_of_decks
		self.dealer_hit_soft_17 = dealer_hit_soft_17
		self.surr = surr
		self.double_after_split = double_after_split
		self.BJ = BJ
		self.insurance = insurance
		self.insurance_rate = insurance_rate
		self.strategy = strategy
		self.budget = budget
		self.min_bet = min_bet
		self.max_bet = max_bet
		self.deck_to_shuffle = 52*deck_to_shuffle*number_of_decks
		self.games_to_shuffle = games_to_shuffle
		self.wins = 0
		self.losses = 0
		self.draws = 0
		self.game_count = 0
		self.deck = Deck(self.number_of_decks)
		self.count = 0
		self.true_count = 0
		self.shuffle_game_count = 0
		
		
	def New(self):
		#Create Dealer and Player
		self.dealer = Dealer(self.deck)
		self.player = Player(self.deck)
		
		#Check Hands
		if self.dealer.hand_val() > 21:
			self.dealer.hand[1] = A1
		if self.player.hand_val() > 21:
			self.player.reduce_A()
		
				
	def win(self, bet, rate=2):
		self.wins += 1
		self.budget += rate*bet
	
	
	def draw(self, bet):
		self.draws += 1
		self.budget += bet
	
	
	def loss(self):
		self.losses += 1
	
	
	def compare(self, bet, hand):
		if hand.hand_val() > 21:
			if A in hand.hand:
				hand.reduce_A()
			else:
				self.loss()
				return
		if self.dealer.hand_val() > 21:
			self.win(bet=bet)
			return
		else:
			if self.dealer.hand_val() > hand.hand_val():
				self.loss()
				return
			elif self.dealer.hand_val() < hand.hand_val():
				self.win(bet=bet)
				return
			else:
				self.draw(bet=bet)
				return
		

	def Round(self):
		#Check Deck
		self.bet = self.min_bet
		self.game_count += 1
		self.shuffle_game_count += 1
		if len(self.deck) < self.deck_to_shuffle or self.shuffle_game_count > self.games_to_shuffle:
			self.deck = Deck(self.number_of_decks)
			self.shuffle_game_count = 0
			self.count = self.true_count = 0
		self.New()
		
		#Get True Count
		self.true_count = self.count*52//len(self.deck)
				
		#Bet Calculation
		"""DOPLNIT HOUSE ADVANTAGE A SKRZ TO KALKULOVAT NUTNEJ POČET TRUE COUNT PRO ZVYŠOVÁNÍ SÁZKY"""
		if self.strategy == 2:
			if self.true_count < 0:
				self.bet = self.min_bet
			else:
				self.bet = abs(0.08*self.budget*((-0.045+self.true_count*0.5)/100))
				self.bet = min(round(self.bet), self.max_bet)
				self.bet = max(self.bet, self.min_bet)
		self.budget -= self.bet
		
		#Offer Insurance
		I = 0
		if self.insurance and self.strategy == 2:
			if self.dealer.upcard() == A:
				if self.deck.deck.count(10) >= len(self.deck)/((self.insurance_rate[0]/self.insurance_rate[1])+1):
					I = 1
					self.budget -= self.bet/2
		
		#Check Blackjacks
		if self.player.hand_val() == 21:
			if self.dealer.hand_val() == 21:
				self.draw(bet=self.bet)
				if I:
					self.budget += ((self.insurance_rate[0]/self.insurance_rate[1])+1)*(self.bet/2)
				if self.strategy == 2:
					self.count += self.player.count(self.dealer)
				return
			else:
				self.win(bet=self.bet, rate=(self.BJ[0]/self.BJ[1])+1)
				if self.strategy == 2:
					self.count += self.player.count(self.dealer)
				return
		
		elif self.dealer.hand_val() == 21:
			self.loss()
			if I:
				self.budget += ((self.insurance_rate[0]/self.insurance_rate[1])+1)*(self.bet/2)
			if self.strategy == 2:
				self.count += self.player.count(self.dealer)
			return
			
		#Actual Play
		else:
			#Player mirroring Dealer´s strategy
			p1, p2 = None, None
			bust1, bust2 = False, False
			split = False
			if self.strategy == 0:
				self.player.dealer_alg(self.deck, self.dealer_hit_soft_17)
				if self.player.hand_val() > 21:
					self.loss()
					return
			
			#Basic Strategy and Card Counting
			elif self.strategy in [1, 2]:

				while True and not split:
					if self.player.hand_val() > 21:
						if A in self.player.hand:
							self.player.reduce_A()
						else:
							break
							
					else:
						move = self.player.FindMove(self.dealer.upcard(), first=True, surr=self.surr,
													num_decks=self.number_of_decks, dealer_hit_soft_17=self.dealer_hit_soft_17)
						if move == S:
							break
						elif move == Sur:
							self.budget += self.bet/2
							self.loss()
							if self.strategy == 2:
								self.count += self.player.count(self.dealer)
							return
						elif move == D:
							self.budget -= self.bet
							self.bet *= 2
							self.player.draw(self.deck)
							break
						elif move == H:
							self.player.draw(self.deck)

						#Split
						elif move == Sp:
							split = True
							self.budget -= self.bet
							p1 = SpPlayer(self.player)
							b1 = self.bet
							if self.player.hand[0] == A1:
								self.player.hand[0] = A
							while True:
								if p1.hand_val() > 21:
									if A in p1.hand:
										p1.reduce_A()
									else:
										bust1 = True
										self.loss()
										break
										
								else:
									move = p1.FindMove(self.dealer.upcard(), split=True, first=True, surr=self.surr,
														num_decks=self.number_of_decks, dealer_hit_soft_17=self.dealer_hit_soft_17)
									if move == S:
										break
									elif move == D:
										self.budget -= b1
										b1 *= 2
										p1.draw(self.deck)
										break
									elif move == H:
										p1.draw(self.deck)
																	
							p2 = SpPlayer(self.player)
							b2 = self.bet
							while True:
								if p2.hand_val() > 21:
									if A in p2.hand:
										p2.reduce_A()
									else:
										bust2 = True
										self.loss()
										break
										
								else:
									move = p2.FindMove(self.dealer.upcard(), split=True, first=True, surr=self.surr,
														num_decks=self.number_of_decks, dealer_hit_soft_17=self.dealer_hit_soft_17)
									if move == S:
										break
									elif move == D:
										self.budget -= b2
										b2 *= 2
										p2.draw(self.deck)
										break
									elif move == H:
										p2.draw(self.deck)
							
			#Check Busts and Compare the Hands
			if self.player.hand_val() > 21:
				if A in self.player.hand:
					self.player.reduce_A()
				else:
					self.loss()
					if self.strategy == 2:
						self.count += self.player.count(self.dealer)
					return
					
			self.dealer.dealer_alg(self.deck, self.dealer_hit_soft_17)
			if p1 and p2:
				if not bust1:
					self.compare(bet=b1, hand=p1)
				if not bust2:
					self.compare(bet=b2, hand=p2)
				if self.strategy == 2:
					self.count += p1.count(p2, self.dealer)
				return
					
			else:
				self.compare(bet=self.bet, hand=self.player)
				if self.strategy == 2:
					self.count += self.player.count(self.dealer)
				return
				
							
		

					
###JUST WORKING VERSION --- NEEDS TO BE USER-FRIENDLY 					
				
def simulate(num_of_games, color=0, number_of_decks=1, dealer_hit_soft_17=False, surr=True, double_after_split=True, 
			BJ=[3, 2], insurance=True, insurance_rate=[2, 1], strategy=2, 
			budget=np.inf, min_bet=5, max_bet=100, deck_to_shuffle=0.5, games_to_shuffle=7):
	
	G = Game(number_of_decks=number_of_decks, dealer_hit_soft_17=dealer_hit_soft_17, surr=surr, double_after_split=double_after_split, 
			BJ=BJ, insurance=insurance, insurance_rate=insurance_rate, strategy=strategy, 
			budget=budget, min_bet=min_bet, max_bet=max_bet, deck_to_shuffle=deck_to_shuffle, games_to_shuffle=games_to_shuffle)	
	
	x = []
	y = []
	while G.game_count < num_of_games:
		if not G.game_count%1000:
			x.append(G.game_count)
			y.append(G.budget)
		G.Round()
	x.append(G.game_count)
	y.append(G.budget)
	#print("Wins:", G.wins/G.game_count*100, "%")
	#print("Draws:", G.draws/G.game_count*100, "%")
	#print("Losses:", G.losses/G.game_count*100, "%")
	return x, y


n = int(input("Enter requested number of games to simulate: "))
colors = 10*["b", "r", "g"]
strats = ["Mirror Dealer", "Basic Strategy", "Card Counting"]
for i in range(3):
	print(strats[i])
	for j in range(3):
		xs, y = simulate(n, BJ=[6, 5], budget=310000, strategy=i, max_bet=100, games_to_shuffle=np.inf, dealer_hit_soft_17=True)
		if j == 0:
			dy = {x: y[ind] for ind, x in enumerate(xs)}
		else:
			for ind, num in enumerate(xs):
				dy[num] = (dy[num]+y[ind])/2
				
	print(dy)
	plt.plot(list(dy.keys()), list(dy.values()), label=strats[i], color=colors[i])
				

xmin, xmax, ymin, ymax = plt.axis([0, 1000000, -50000, 700000])
plt.xlabel("Number of games")
plt.xticks(ticks=range(0, 1000001, 200000))
plt.ylabel("Player´s budget")
plt.title("Blackjack strategies comparison - 1 000 000 games")
plt.legend()
plt.show()