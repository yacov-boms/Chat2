# Chat2 - Phase 1
All about Trump - A light Chatbot with agile approach
This chatbot is for human language messaging  interacion. 
It provides factual answers for various users queries about President Donald Trump.
The heart of the chatbot is a Python program with NLTK package residing (currently) on a local computer.
It is also comprised of:
•	Flask - A python local web server which listens to messages from Facebook Messenger. 
•	Requests - A python package for sending messages back to users.
•	Ngrok- A safe https connection from the local web server to Facekook Messenger.
•	It uses Facekook Messenger connectivity, which has over 1 billion users.

Chatbot Funcionality:
At startup:
•	Establishes connection with Messenger
•	Reads a text file
•	Word tokenize and sentence tokenize
•	Does cleaning and lemmatazaion

In response to a users query:
•	Possible basic greetings
•	Ceates a TfIdf table 
•	Checks cosine similarity between the query and each of the file's sentences 
(it is a simple method that outperforms more advanced algorithms for small datadets)
•	Picks the best similar sentence and sends it to the user.



