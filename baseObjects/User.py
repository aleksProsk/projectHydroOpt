def get_current_uid():
	return 0	#todo

class CUser(object):
	def __init__(self, uid=None):
		if uid is None:
			self.__uid = get_current_uid()
		else:
			self.__uid = uid
	def getRights(self):return 0
	def getUID(self): return self.__uid