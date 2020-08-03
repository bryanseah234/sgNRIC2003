# NRIC03

Disclaimer: For educational purposes only.

## Procedure to replicate
1. Generate all the possible NRICs combinations using 01_generate nric2003.py
2. Validate the NRICs by checking their checksum (last alphabet) using 02_validate nric2003.py
3. Generate the barcodes for each NRIC by iterating through the list of validated NRICs using 03_generate barcodes.py

P.S. Outputs from steps 1 and 2 have been uploaded for convenience 

## Why NRICs

I have always been fascinated about how the government label us with 7 digits and 2 alphabets. Will they ever run out of letters? Will they change their system?
But one thing that still puzzles me is how they label us... is it based on our birthdate? Or which hospital we were born from? I know the government will never reveal their secrets, but this got me to be more interested in the National Registration Identity Card System in Singapore.

## How did you do it

I found out that the NRIC's checksum is publicly available for all on the web. Then, there was a lesson in my computing class which needed us to code a script to validate NRICs. It got me wondering if I could generate everyone's NRIC since there is a way to validate them. But I was told that validated NRICs and legitimate NRICs are different. (Of course the government thought of this.)\
</br>
The NRICs I am able to generate does not mean it is tagged to an individual. The NRIC may simply be not in use by anyone. Not worrying about this set back, I went ahead to code a script that would return me all the NRICs in Singpaore.\
</br>
But hold on, all the NRICs? That would seem a little aggressive and excessive. Hence, I chose to only generate the ones in 2003.\
The script I wrote is also able to generate NRICs from other years with some adjustments, if that is what you are into.\
</br>
I wanted to do more. Generating barcodes isn't a really big acheievement; anyone one with a basic python skills could do it. Hence, I challenged myself to generate the barcodes of these NRICs.\
</br>
I googled for a python module that would allow me to generate barcodes by user input. I found one called python-barcode and I used it to generate images containing the barcodes.
Note to who ever who wants to replicate this, there are many types of variable length for barcodes. A quick reference to your own Singapore NRIC will reveal that the government uses Code 39 to encode NRICs.

## Challenges faced

There are many, many challenges I faced when doing this project. Contact me for more information.
