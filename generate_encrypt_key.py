#!/Users/lcasado-/miniconda3/envs/42AI-lcasado-/bin/python
#!/home/luis/anaconda3/envs/42AI-lcasado-/bin/python

from cryptography.fernet import Fernet
import os
 
 
# generate a key for encryption and decryption
# You can use fernet to generate a simmetric key
# the key or use random key generator
# here I'm using fernet to generate key
notice ="""
THIS SCRIPT RELATES TO 42 BARCELONA CYBERSECURITY BOOTCAMP STOCKHOLM EXERCISE

WHEN YOU EXECUTE THIS SCRIPT, THE SEED FOR CREATING SYMMETRICAL ENCRYPTION KEY
WILL CHANGE.

~/.ssh/..encrypt.key WILL CHANGE

IF THAT HAPPENS AFTER THE INFECTION FOLDER ENCRYPTION, STOCKHOLM EXERCISE AIM,
IT WOULD NOT BE POSSIBEL TO DESENCRYPT SUCH FOLDER

ARE YOU SURE YOU WANT CONTINUE?
"""

print(notice)
answer = input("ARE YOU SURE YOU WANT CONTINUE? (Y/N)").lower()
if answer == "y":
        answer = input("It seem you know what you do. Please give your four initials >").upper()
        if answer == "LMCD":

            key = Fernet.generate_key()   # it is a byte array of len 44.
            cifer_key_path = os.path.join(os.environ["HOME"], ".ssh/.encrypt.key" )
            with open(cifer_key_path,'wb') as f:
                    f.write(key)

print(f" I generated {cifer_key_path}")
