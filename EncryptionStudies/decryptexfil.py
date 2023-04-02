from cryptor import decrypt
with open('matplotlib.pdf.txt', 'rb') as f:
    contents = f.read()
with open('ExfilMatplotlib.pdf', 'wb') as f:
    f.write(decrypt(contents))