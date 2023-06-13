# ACE_2023_ChallengeProblem
Malazan &amp; Farsight-1 Challenge Team

DESCRIPTION:

The zip file submitted for the Week 1 Challenge problem contains...
- a requirements.txt file
- a Python source code named EncryptionScheme.py
- a Python source code named cert_authority.py

The requirements.txt contains all necessary packages to run our code. 
* It is important to note cert_authority.py should be located in the same directory and that packages present in requirements.txt should be present on the user's machine to minimize issues.

The EncryptionScheme.py contains the various algorithms making up the encryption scheme and relevant functions. The main module within also offers lines initializing scheme users and example message-receiver pairs in send_message() and decrypt_messsage() calls. Relevant parameters can be changed to observe functionality with different messages at the user's discretion.

The cert_authority.py contains a class defining the trusted certificate authority for use with the asymmetric algorithms. This module is imported in EncryptionScheme.py.

RUNNING:

* The code included can be run in the terminal using the following line in the relevant directory or using a preferred IDE.

	python3 EncryptionScheme.py

To test our code, first create a certificate authroity instnace within the EncrpytionScheme.py file.
The certificate authroity class does not take any parameters.

Next, create two instances of the EncryptionScheme class, these represent the two clients using the scheme.
The EncryptionScheme class takes two parameters, a string representing the name the certificate authroity created above.
You should pass the same certificate authority instance to each user or they can not communicate.

To send a message call the send_message function from teh instance you want to send from. Pass in the message text
and the string user name of the recipient. This returns an encrypted message. Pass teh encrypted emssage into the recipients decrypt  
messge along with the string user name of the sender. There is already a small example in the EncrpytionScheme.py file.

Due to the large key sizes used the code deos take a while to run.
