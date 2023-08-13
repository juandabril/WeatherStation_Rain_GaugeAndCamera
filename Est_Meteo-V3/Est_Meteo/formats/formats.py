import os

def creartxt(namefile,dirfile):
    if not os.path.exists(dirfile): os.makedirs(dirfile)
    filename=os.path.join(dirfile,namefile)
    with open(filename,'a') as outfile:
        outfile.close()
    return
def grabartxt(dirname,filename,dataline):
    namefilew=os.path.join(dirname,filename)
    with open(namefilew,'a') as archi:
        archi.write(dataline+ '\n')
    return
