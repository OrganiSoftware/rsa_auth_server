import os
import argparse

class gen_key:
    def gen_key(self):
        parser = argparse.ArgumentParser(description='server args parser')
        parser.add_argument('username', help='username for key gen')
        parser.add_argument('password', help='password for key gen')
        args = parser.parse_args()
        os.system("cat >~/auth_gen_key_file <<EOF\n"
                  + "%echo Generating a basic OpenPGP key\n"
                  + "Key-Type: RSA\n"
                  + "Key-Length: 4096\n"
                  + "Subkey-Type: RSA\n"
                  + "Subkey-Length: 4096\n"
                  + "Name-Real: "+str(args.username)+"\n"
                  + "Name-Comment: with stupid passphrase\n"
                  + "Name-Email: "+str(args.username)+"@rsa_auth.com\n"
                  + "Expire-Date: 0\n"
                  + "Passphrase: "+str(args.password)+"\n"
                  + "%commit\n"
                  + "%echo done\n"
                  + "EOF")

        os.system("gpg --batch --generate-key " + "~/auth_gen_key_file")
        os.system("echo "+str(args.password)+" > ~/raw_server_side_pass.txt")
        os.system("gpg -e -a -r "+args.username+" ~/raw_server_side_pass.txt")
        os.system ("cp ~/raw_server_side_pass.txt.asc ~/"+args.username+"_password_file.txt.asc")
        os.system("rm ~/raw_server_side_pass.txt; rm ~/auth_gen_key_file; rm ~/raw_server_side_pass.txt ;  rm ~/raw_server_side_pass.txt.asc")


if __name__ == '__main__':
    gen_key = gen_key()
    gen_key.gen_key()