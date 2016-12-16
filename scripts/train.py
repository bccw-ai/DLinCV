import utilities
import posenet
import theano
import numpy as np
outputWeightspath = 'trainedweights.h5'
BETA = 250 #to 2000 for outdoor
directory = "/usr/prakt/w065/posenet/KingsCollege/"
dataset = 'dataset_train.txt'
 
def posenet_loss(y_true, y_pred):
	xyz_true=y_true[0:3]
	wpqr_true = y_true[3:7]
	xyz_pred=y_pred[0:3]
	wpqr_pred = y_pred[3:7]
	return np.linalg.norm(xyz_true-xyz_pred) + BETA *np.linalg.norm(wpqr_true-wpqr_pred/np.linalg.norm(wpqr_pred))

nb_epoch = 3
print "creating the model"
model =posenet.create_posenet('mergedweights.h5')
#sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(optimizer='sgd', loss=posenet_loss)

for e in range(nb_epoch):
	print("epoch %d" % e)
	for X_batch, Y_batch in utilities.BatchGenerator(32,directory,dataset):
		history = model.fit(X_batch, Y_batch, batch_size=32,shuffle=True, nb_epoch=1)
		print history.history['loss']

model.save_weights(outputWeightspath)
