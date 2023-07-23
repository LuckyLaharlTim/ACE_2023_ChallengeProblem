=======================
Contents
=======================
This challenge problem consists of 7 files in addition to this README.
1) server.py
2) stego.py
3) post_test.py
4) the templates directory containing ...
	4a - newPic.html
	4b - picNsourceOnly.html
5) requirements.txt
6) test.png

=======================
Running the Submission
=======================
* Before attempting to run anything, the user should note the ip of the machine used to run server.py
* The host parameter to app.run() in server.py should be changed to that ip-address
* The flask python library should also be installed using "pip install flask" as needed
       --------
	Steps
       --------
       I. run server.py
       		a. open a browser
       		b. go to <server-ip>:5000/PicofTheDay to verify the server is working
       II. have a png image in the same location as the other files (or use test.png)
       III. run stego.py
       IV. respond to the prompts (using 1 as to steg and send an image).
       		~ Please note that the message (prompt number 4) cannot contain non-alphabetic characters.
       V. Run stego.py again (2 to download and perform steganalysis on the server's current image)
       VI. The output should result in the same message typed in response to step IV's message prompt.

