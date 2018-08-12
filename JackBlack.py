import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Bank:
    def __init__(self, balance=100, bet=0):
        self.balance = balance
        self.bet = bet
        
    def __str__(self):
        if self.bet > 0:
            return f"Your balance is ${self.balance} and you're betting ${self.bet}."
        else:
            return f"Your balance is ${self.balance} and you've yet to place a bet."
        
    def set_balance(self):
        while True:
            try:
                while True:
                    set_or_not = input(f"Your balance is ${self.balance}. Would you like to change your balance? (y/n) ")
                    if set_or_not.lower() == 'y':
                        self.balance = int(input("Set your balance: "))
                        break
                    elif set_or_not.lower() == 'n':
                        break
                    else:
                        print("You entered an invalid value.")
                        continue
            except:
                print("You entered an invalid value.")
                continue
            else:
                break
        
    def place_bet(self):
        while True:
            try:
                self.bet = int(input("How much do you want to bet? "))
            except:
                print("You entered an invalid value.")
                continue
            else:
                if self.bet > self.balance:
                    print("You don't have that much in your account.")
                    continue
                else:
                    break
    
    def win_bet(self):
        self.balance += self.bet
        self.bet = 0
        
    def lose_bet(self):
        self.balance -= self.bet
        self.bet = 0

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
        
    def __str__(self):
        deck_string = ''
        for card in self.deck:
            deck_string += f"\n {card.__str__()}"
        return f"Cards left in deck:{deck_string}"
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank =='Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing
    
    while True:
        player_choice = input("Would you like to hit? (y/n)")
        
        if player_choice.lower() == 'y':
            hit(deck, hand)
        
        elif player_choice.lower() == 'n':
            print("Player stands, dealer is playing.")
            playing = False
        
        else:
            print("You entered an invalid value.")
            continue
        break

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <hidden>")
    print(f" {dealer.cards[1]}")
    print("\nPlayer's Hand: ", *player.cards, sep = '\n ')

def show_all(player, dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep = '\n ')
    print(f"Value = {dealer.value}")
    print("\nPlayer's Hand: ", *player.cards, sep = '\n ')
    print(f"Value = {player.value}")

def player_busts(player, dealer, bank):
    print("\nPlayer busts!")
    bank.lose_bet()

def player_wins(player, dealer, bank):
    print("\nPlayer wins!")
    bank.win_bet()

def dealer_busts(player, dealer, bank):
    print("\nDealer busts!")
    bank.win_bet()
    
def dealer_wins(player, dealer, bank):
    print("\nDealer wins!")
    bank.lose_bet()
    
def push(player, dealer):
    print("\nDealer and player tie! It's a push.")

def play_game():
    global playing
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n           Dealer hits until they reach 17. Aces count as 1 or 11.')
    
    player_bank = Bank()
    
    while True:
        player_bank.set_balance()

        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        
        player_bank.place_bet()
        
        show_some(player_hand, dealer_hand)
        
        while playing:
            
            hit_or_stand(deck, player_hand)
            
            show_some(player_hand, dealer_hand)
            
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_bank)
                break
                
        if player_hand.value <= 21:
            
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            
            show_all(player_hand, dealer_hand)
            
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_bank)
            
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_bank)
            
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_bank)
            
            else:
                push(player_hand, dealer_hand)
                
        print(f"\nPlayer's winnings stand at {player_bank.balance}")
        
        new_game = input("Would you like to play another hand? (y/n) ")
        
        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print("Thanks for playing!")
            break

play_game()
