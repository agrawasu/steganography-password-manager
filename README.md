# To run:
To run this program, please clone this repository, then open the <code>main.py</code> file in the <code>src</code> folder and run it.

# Before running:
1. In order for the program to work, there must be a <code>PNG</code> file in the <code>raw image</code> folder
2. Have a password in mind before running

# Running:
When running the code, the first prompt will ask for the <code>Password</code> you wish to encrypt. The second will ask for the <code>account application</code>, which in this case should be the name of the file **EXCLUDING THE FILETYPE**.

# Output:
A new <code>PNG</code> file will be created in the <code>encrypted image</code> with the same name as the <code>PNG</code> in the <code>raw image</code> with <code>-epass</code> at the end (i.e. <code>youtube.png</code> -> <code>youtube-epass.png</code>.
The code will print the decrypted password, which will just be the password you entered. If you read through the code, you will see, however, that this is retrieved by decrypting the encrypted steganography-secured password.
