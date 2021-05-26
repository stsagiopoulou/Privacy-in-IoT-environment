import pai
import pickle
keys=pai.generate_keypair(64)
picklefile = open ('keys','wb')
pickle.dump(keys, picklefile)
picklefile.close()
