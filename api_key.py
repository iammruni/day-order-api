import pandas as pd
from csv import writer
from passlib.hash import sha256_crypt


key_path = './data/hashdb.csv'


def store_api_key(key, permissions):
	"""Saves the given API Key
	"""
	templ = ['1', '2']
	templ[0] = str(key)
	templ[1] = int(permissions)

	with open(key_path,'a') as f_object:
		writer_object = writer(f_object)
		writer_object.writerow(templ)
		f_object.close()


def generate(user, save=False, permissions=1):
	"""Generate an API Key
	"""
	pas = sha256_crypt.encrypt(user)
	if(save):
		store_api_key(pas, permissions)
	return pas


def ver(pas, metho):
	"""Verify the API Key
	"""

	# Permissions: 1 = GET; 2 = POST; 3 = GET&POST; 0 = BLACKLIST
	data = pd.read_csv(key_path, header=0)
	data = data.to_dict('list')
	count = len(data['hash'])
	flag = False
	message = "This API Key does not have permission to use this method"
	err_code = 200

	for i in data['hash']:
		if sha256_crypt.verify(pas, i):
			flag =True
			pert = data['hash'].index(str(i))
			perm = data['permissions'][pert]
			if int(perm) == 1:
				if metho == "get":
					flag = True
					err_code = 200
					return flag, "", err_code
					break
				else:
					flag = False
					return flag, "This API Key does not have permission to use this method", 401

			elif int(perm) == 2:
				if metho == "post":
					flag = True
					err_code= 200
					return flag, "", err_code
					break
				else:
					flag = False
					return flag, "This API Key does not have permission to use this method", 401
			elif int(perm) == 3:
				if metho == "get" or metho == "post":
					flag = True
					err_code= 200
					return flag, "", err_code
					break
				else:
					flag = False
			elif int(perm) == 0:
				# Blacklist
				flag = False
				err_code = 403
				return flag, "This API Key has been blacklisted. See you in hell, b*!", err_code
		else:
			flag = False
			message = "Invalid API Key!"
			err_code = 403

	return flag, message, err_code
