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
  
	=======================
	Steps
	=======================
       I. Install necessary requirements with pip3 install -r requirements.txt
       II.run server.py
       		a. open a browser
       		b. go to <server-ip>:5000/PicofTheDay to verify the server is working
       III. have a png image in the same location as the other files (or use test.png)
       IV. run stego.py
       V. respond to the prompts (using 1 as to steg and send an image).
		- Note that any spaces in you oiginal message will be replaced by underscores
  		- When you see <Response [200]> you know the image has been successfully uploaded
  		- This may take a few seconds depending on size of image
       VI. Run stego.py again (2 to download and perform steganalysis on the server's current image)
       VII. The output should result in the same message typed in response to step IV's message prompt.

