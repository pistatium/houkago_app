#coding: utf-8

class Category:
	def __init__(self, cid, label, parent):
		self.id      = cid
		self.label   = label 
		self.parent  = parent
		
	def __repr__(self):
        return "{id = %d, label = %s}" % (self.id, self.label)

	@classmethod
	def load(cls, cid = None):
		categories_data = [
			("Game", 0),
			("App",  0),
		]
		if cid:
			if 0 < cid < len(categories_data):
				return cls(cid, *categories_data[cid])
			else:
				return None
		else:
			categories = []
			for i, cat in enumerate(categories_data):
				categories.append(cls(i, *cat))
			return categories
