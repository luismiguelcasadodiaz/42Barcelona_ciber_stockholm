   Fernet provides symmetric encryption and authentication data
   ------------------------------------------------------------
   I selected a symmetrical encryption key because requires **less resources
   for encryption**. Fernet is a part of the **cryptography** library for
   python developed by the unofficial **Python Cryptographic Authority**

   Fernet is a **high-level recipe** that requires developer to make very
   few decisions. it simplifies the usage of 

   It is good for a data size that **fits in memory**. When this is not the
   case a "by chunks apprach becomes necessary"

   Fernet includes:

      128-bit AES in CBC mode  (For encryption)
      an HMAC with SHA-256     (For authentication)

      AES - Advanced Encryption Standard is a fast, symmetric-key encryption
      algorithm
      CBC mode secuences the encryption of the plain text in blocks of 
      AES block size

      HMAC gest a Hash for the plaintext to keep data integrity


   When smaller blocks of 128 bits Fernet pads them according to [PKCS#7] (https://www.ibm.com/docs/en/zos/2.4.0?topic=rules-pkcs-padding-method)

   
1. Download https://gist.github.com/xpn/facb5692980c14df272b16a4ee6a29d5
   cause containing all file extensions affected by WannaCry Randsonware
2. Name such file as 'wannacry_file_extensions.txt'

3. Execute generate_encrypt_key.py
   It generates a symmetrical encryption key wiht Fernet.generate_key.
   This key is saved in ~/.ssh/.encrypt.key"

4. Execute stockholm.py
   Pequeño programa de cifrado. Es un ejercicio del bootcamp de ciberseguridad
   de 42 Barcelona. Solamente afecta a los archivos de la carpeta
   '/Users/lcasado-/infection'

   usage:
        ./stockholm [-h] [-v] [-s] [-r] KEY

      optional arguments:
      -h, --help            show this help message and exit
      -v, --version         Muestra la versión del programa
      -s, --silent          No mostrar nombres de ficheros cifrados
      -r KEY, --reverse KEY
                              introduzca la clave para revertir el cifrado

   Recorre al árbol de archivos y directorios que hay en ~/infection.
   para ello se ayuda de os.walk. Por defecto no sigue los enlaces simbólicos
   
   Antes de iniciar el reverse verifica que la KEY introducida por el usuario
   coincide con la que se ha usado para el cifrado y que está guardada en:
   ~/.ssh/.encrypt.key

To know more about Fernet
https://www.comparitech.com/blog/information-security/what-is-fernet/