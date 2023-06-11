# ACE_2023_ChallengeProblem
Malazan &amp; Farsight-1 Challenge Team

The requirements.txt file contains all necessary packages to run our code.

To test our code, first create a certificate authroity instnace within the EncrpytionScheme.py file.
The certificate authroity class does not take any parameters.

Next, create two instances of the EncryptionScheme class, these represent the two clients using the scheme.
The EncryptionScheme class takes two parameters, a string representing the name the certificate authroity created above.
You should pass the same certificate authority instance to each user or they can not communicate.

To send a message call the send_message function from teh instance you want to send from. Pass in the message text
and the string user name of the recipient. This returns an encrypted message. Pass teh encrypted emssage into the recipients decrypt  
messge along with the string user name of the sender. There is already a small example in the EncrpytionScheme.py file.

Due to the large key sizes used the code deos take a while to run.
