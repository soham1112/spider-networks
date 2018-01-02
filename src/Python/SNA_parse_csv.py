#==============================================================================
# SM 2/2016
# ReaDATA CSV frame data generated from the excel files using Pandas
# and generates the association matrix for Attacker and Comer data.
# Input  : sheet_ID <frame ID>
# Output : R_DIR > ADJ_A/C_***.csv
#==============================================================================

import numpy as np
import pandas as pd
import os

import SNA_compute_ADJ_matrix as AM
import SNA_metrics as SM

def read(sheet_ID, PARSE='Attacker'):

	C = np.array(pd.read_csv('../../datasets/info/color_coding.csv', usecols=['color ID', 'code']).fillna(0)).T

	INFO = pd.read_csv(sheet_ID, usecols=[0,1])
	if int(INFO.ix[0,0]) < 10:
		FRAME_ID = '%s_F0%r' %(INFO.ix[0,1].split(" ")[0], int(INFO.ix[0,0]))
	else:
		FRAME_ID = '%s_F%r' %(INFO.ix[0,1].split(" ")[0], int(INFO.ix[0,0]))

	if PARSE=='Attacker':
		data_columns = [4, 7, 9, 10]
		DATA = pd.read_csv(sheet_ID, usecols=data_columns).fillna(0)
		DATA = DATA[DATA.ix[:,1] != 1]
		DATA = DATA[DATA.ix[:,2] != 0]

		DATA.ix[:,2] = DATA.ix[:,2].str.strip().fillna(0)
		DATA.ix[:,3] = DATA.ix[:,3].str.strip().fillna(0)

		D = np.array(DATA).T
		ID_A = D[2]
		CF_R = D[3]

		for h, i in enumerate(C[0]):
			np.put(ID_A, np.where(ID_A == i), C[1][h])

		for k in range(0, len(ID_A)):
			if isinstance(ID_A[k], basestring) == True:
				ID_A[k] = -1

		for j, i in enumerate(CF_R):
			if i == 'R':
				CF_R[j] = 10.0
			elif i == 'G':
				CF_R[j] = 14.0
			else:
				CF_R[j] = 0.0

		R = []
		for i, j in enumerate(D[0]):
			if j != 0:
				R.append(i)
		C = np.hstack((np.diff(R),len(D[2]) - np.sum(np.diff(R))))
		A = np.unique(D[0])
		A = A[A > 0]
		B = np.repeat(A, C)

		REC_DATA = np.vstack((B, ID_A, CF_R))
		DATAFRAME = pd.DataFrame({'D0: Trial':REC_DATA[0],'D1: Attackers':REC_DATA[1],'D2: Retreat':REC_DATA[2]})

		if not os.path.exists('../../output/csv/sequence'):
			os.makedirs('../../output/csv/sequence')

		print "Saving parsed attacker data to %s.csv" %(FRAME_ID.split(" ", 1)[0])
		DATAFRAME.to_csv('../../output/csv/sequence/seq_A_%s.csv'%(FRAME_ID.split(" ", 1)[0]), sep = ',')

		# Generate the attacker adjacency matrix from the parsed data.
		AM.generate_attacker_matrix(REC_DATA, FRAME_ID)

	elif PARSE=="Comer":

		data_columns = [4, 13, 14]
		DATA = pd.read_csv(sheet_ID, usecols=data_columns).fillna(0)

		print "Looking for comer data..."
		DATA = DATA[DATA.ix[:,2] != 0]
		if DATA.empty:
			print 'No comer data found. Aborting.'
			return 0, 0

		DATA.ix[:,2] = DATA.ix[:,2].str.strip().fillna(0)
		print 'Found comer data.'

		D = np.array(DATA).T
		T    = D[0]
		NC   = D[1]
		ID_C = D[2]

		for h, i in enumerate(C[0]):
			np.put(ID_C, np.where(ID_C == i), C[1][h])

		for k in range(0, len(ID_C)):
			if isinstance(ID_C[k], basestring) == True:
				ID_C[k] = -1

		R = []
		for i, j in enumerate(D[0]):
			if j != 0:
				R.append(i)

		C = np.hstack((np.diff(R),len(D[2]) - np.sum(np.diff(R))))
		A = np.unique(D[0])
		A = A[A > 0]
		B = np.repeat(A, C)

		REC_DATA = np.vstack((B, ID_C))
		DATAFRAME = pd.DataFrame({'D0: Trial':REC_DATA[0],'D1: Comers':REC_DATA[1]})

		if not os.path.exists('../../output/csv/sequence'):
			os.makedirs('../../output/csv/sequence')

		print "Saving parsed comer data to %s.csv" %(FRAME_ID.split(" ", 1)[0])
		DATAFRAME.to_csv('../../output/csv/sequence/seq_C_%s.csv'%(FRAME_ID.split(" ", 1)[0]), sep = ',')

		# Generate the comer adjacency matrix from the parsed data.
		AM.generate_comer_matrix(REC_DATA, FRAME_ID)
		
	else:
		print "Do not know which data to parse. Aborting."
		return None

	return None