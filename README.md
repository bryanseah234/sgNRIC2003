# NRIC03 
Disclaimer: For educational purposes only. Used as a proof of concept.
<p align="center">
  <img src="https://github.com/bryanseah234/nric2003/blob/master/archive/nric2003.JPG" />
</p>

## Requirements
Software
1. [Python 3](https://www.python.org/ftp/python/3.8.5/python-3.8.5.exe)
2. [Barcode Module](https://pypi.org/project/python-barcode/)

Hardware
1. Laptop / Desktop (running windows or mac)

Non-tangibles
1. Time (at least 24hours)
2. Storage space (at least 3GB)
3. Electricity (be prepared to leave your device running overnight)


## Procedure to replicate
Step 1: Use code from 01_generate nric2003.py to generate all the possible NRICs combinations.
Step 2: Validate the NRICs by checking their checksum (last alphabet) using 02_validate nric2003.py
Step 3: Generate barcodes for each NRIC by iterating through the list of validated NRICs using 03_generate barcodes.py

(P.S. Outputs from steps 1, 2 and 3 have been uploaded for convenience)

## Why NRICs
I have always been fascinated about how the government label us with 7 digits and 2 alphabets. But one thing that still puzzles me is how they label us... is it based on our birthdate? Or which hospital we were born from? I know the Singapore government will never reveal their secrets, but this got me to be more interested in the National Registration Identity Card System.

At first I wanted to find out the population size born each year, by trying to find the largest NRIC in a particular year (E.G. T0398765A will tell me that there are 98,765 babies born in year 2003, until I find a NRIC larger than that). But I realised this method is very inaccurate at estimating the population size, plus the government is already publicising this information on their website.

Earlier this year I saw this headline: [Man arrested, suspected of redeeming more than 200 face masks from vending machines](https://www.channelnewsasia.com/news/singapore/covid-19-man-arrested-200-face-masks-vending-machines-12784984) which intrigued me. So I changed the aim of my project, and moved on to proving how easy it is to generate someone else's NRIC, using Python.

## How did you do it
I found out that the NRIC's checksum is publicly available for all on the web. Then, there was a lesson in my computing class which needed us to code a script to validate NRICs. It got me wondering if I could generate everyone's NRIC since there is a way to validate them. But I was told that validated NRICs and legitimate NRICs are different. (Of course the government thought of this.)\
</br>
The NRICs I am able to generate does not mean it is tagged to an individual. The NRIC may simply be not in use by anyone. Not worrying about this set back, I went ahead to code a script that would return me all the NRICs in Singpaore.\
</br>
But hold on, all the NRICs? That would seem a little aggressive and excessive. Hence, I chose to only generate the ones in 2003.\
The script I wrote is also able to generate NRICs from other years with some adjustments, if that is what you are into.\
</br>
I wanted to do more. Generating NRICs isn't a really big achievement; anyone one with a basic python skills could do it. Hence, I challenged myself to generate the barcodes of these NRICs.\
</br>
I googled for a python module that would allow me to generate barcodes by user input. I found one called python-barcode and I used it to generate images containing the barcodes.
Note to who ever who wants to replicate this, there are many types of variable length for barcodes. A quick reference to your own Singapore NRIC will reveal that the government uses Code 39 to encode NRICs.

## Challenges faced
1. My own Reddit account got suspended. At first I didnt know what I was doing, and uploaded all the individual images onto a new subreddit I created. Little did I know that it would cause alot of commotion and many conspiracy theory subreddits started picking it up. Well, my subreddit got banned because someone reported it for 'leaking private credentials'. I my opinion, yes, NRICs are private information, or they are suppoed to be. But like what I demonstrated, anyone is able to generate them, in large amounts too. Hence it isn't as private as before, and may not necessarily be a good thing.
2. Trust. I feel that many people (like my friends and teachers) do not understand what I am trying to do, and taken the nature of such a topic I am working on for this project, people have strong views and opinions about what I do. i dont't disagree with them that these are sensitive data, and that if fallen into the wrong hands, the situation can turn ugly. But I still wanted to make it known and put this information out there, onto the web, for people to know and realise the loophole in our NRICs, and the importance of using other methods of verification on top of checking ICs.
3. Data scrappers. I have been advised against posting the individual pictures online, to prevent data / image scrappers from picking it up. This is a valid concern, which admittedly, I did not think about. I have since complied the photos into short videos (around 30 seconds or so) using video editing software.
4. How do I know the barcode works? Well, I tested my own NRIC barcode (which i generated using Python) to collect my free mask at one of the vending machines. And guess what? It worked. However, I STRONGLY CONDEMN using Python generated barcodes for malicious intents. The Singapore Police will definitely be able to track you down.
5. Someone feedbacked to me that the code and output I uploaded here is technically incorrect. I apologise. There has been a mistake on my part. Using the barcode module from python, there will be a checksum at the end of the input. Lets say I want to generate the barcode of "T0399999A". My current code now will include a checksum at the end, so it becomes "T0399999AX" where X can be any alphabet or number or symbol. In order to fix this, I need to ensure "[add checksum = False](https://pythonhosted.org/pyBarcode/codes.html#code-39)".

## As seen on
https://whatismybarcode.blogspot.com/2020/09/how-to-diy-your-own-nric-barcode-python.html
