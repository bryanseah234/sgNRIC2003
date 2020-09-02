import barcode
from barcode.writer import ImageWriter


with open('C:\\Users\\yourname\\Downloads\\validated nric2003.txt', 'r') as f:
    for i in f:
        i = i.strip('\n')
        code39 = barcode.get('code39', i, writer=ImageWriter(), add_checksum=False)
        filename = code39.save(i)

