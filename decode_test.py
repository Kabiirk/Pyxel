import subprocess


# Test string for refference and testing without subprocess module
s =b'Folder PATH listing for volume OS\r\nVolume serial number is C80A-38AC\r\nC:.\r\n\xc0\xc4\xc4\xc4ui\r\n'

procc = subprocess.Popen(["tree"], stdout=subprocess.PIPE, shell=True)
out, err = procc.communicate()
procc.kill()

print(out.decode('CP437'))