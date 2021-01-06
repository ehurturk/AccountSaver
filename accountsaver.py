import random
import json
import pyperclip

LENGTH = 14
THRESHOLD = 3

PATH = "/Users/emirhurturk/Dev/Projects/Logs/accounts.json"


class Account():

	all_users = {
		"Websites": [],
		"Usernames": [],
		"Passwords": []
	}

	data_dict = {

	}
	def __init__(self, website, username, length, threshold, password=None):
		self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '*', '+']
		self.used_letters = []
		if (password==None): # If there is no password
			self.generated_password = self.generate_password(length, threshold)
		else:
			self.generated_password = password
		self.add_user(username, website, password=self.generated_password)


	def count(self, element, iterable):
		"""
		Returns how much of the element is in an array

		Params: element: the object that is being searched
				iterable: an iterable object that is being used to search the element
		"""
		number = 0
		for iterable_element in iterable:
			if (iterable_element == element):
				number+=1

		return number

	def generate_password(self, length, threshold):
		"""
		Creates a generic password according to params
		"""

		password = []
		for i in range(0, length):
			letter = self.alphabet[random.randint(0, len(self.alphabet) -1)]

			if self.count(letter, self.used_letters) > threshold-1:
				while letter in self.used_letters:
					letter = self.alphabet[random.randint(0, len(self.alphabet) -1)]

			self.used_letters.append(letter)


			password.append(letter)

		return password

	def add_user(self, username, website,  **kwargs):
		Account.all_users["Usernames"].append(username)
		Account.all_users["Websites"].append(website)
		Account.all_users["Passwords"].append(kwargs["password"])

	@classmethod
	def log(cls):
		"""
		Logs the usernames and passwords that is created
		Saves the log into "/Users/emirhurturk/Dev/Projects/Logs/passwords.txt"
		"""

		for i in range(0, len(Account.all_users["Passwords"])):
			if (i==len(Account.all_users["Passwords"]) - 1):
				pyperclip.copy("".join(Account.all_users["Passwords"]))
			website = Account.all_users["Websites"][i]
			Account.data_dict[website] = {"username": Account.all_users["Usernames"][i], "password": "".join(Account.all_users["Passwords"][i])}

		try:
			with open(PATH, "r") as data:
				try:
					df = json.load(data)
				except json.decoder.JSONDecodeError as e:
					df = {}
		except FileNotFoundError:
			with open(PATH, "w") as data:
				json.dump(Account.data_dict, data, indent=4)
		else:
			df.update(Account.data_dict)
			with open(PATH, "w") as data:
				json.dump(df, data, indent=4)


	@classmethod
	def search(cls, website):
		username, password = "", ""
		try:
			with open(PATH) as data:
				data_ = json.load(data)
				for _website in data_:
					if _website == website:
						username = data_[_website]["username"]
						password = data_[_website]["password"]
		except FileNotFoundError as e:
			print(e)
		print(f"{website} | {username} | {password}")

	@classmethod
	def clear(cls):
		with open(PATH, "w") as data:
			json.dump({}, data)


# print(password.generate_password(length=LENGTH, threshold=THRESHOLD))

def get_info():
	stop = False
	print("		 -Menu-    ")
	print("-----------------")
	print("1) Search Account")
	print("2) Add Account")
	print("3) Clear All Accounts")
	selection = input("Please enter your selection: \n")

	try:
		if (selection=="2"):
			website = input("Please enter the website/application: \n")
			username = input("Please enter a username/email: \n")
			password = input("Do you want us to generate a new 14 lettered password with symbols and letters? (y/n)\n")
			if (password=="y"):
				account = Account(website, username, LENGTH, THRESHOLD) ## adds the details to an account
			else:
				passw = input("Please enter your password:\n")
				account = Account(website, username, LENGTH, THRESHOLD, password=passw)


			print("Account is added to: "+ PATH+" and the password is copied to your clipboard")
			Account.log()

		elif (selection=="1"):
			website = input("Please enter the website/application: \n")
			Account.search(website)
		elif (selection =="3"):
			Account.clear()
		else:
			raise ValueError("Wrong Input")

	except ValueError as e:
		print(e)


get_info()
