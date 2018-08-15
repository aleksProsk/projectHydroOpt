class baseInputElement():
	def __init__(self, uid, id):
		self.id = id
		self.uid = uid
		
class Dropdown(baseInputElement):
	def __init__(self, uid, id, options, multi, placeholder):
		super().__init__(uid, id)
		self.options = options
		self.multi = multi
		self.placeholder = placeholder

class Slider(baseInputElement):
	def __init__(self, uid, id, max, min, step, marks=[]):
		super().__init__(uid, id)
		self.max = max
		self.min = min
		self.step = step
		self.marks = marks
		
class RangeSlider(baseInputElement):
	def __init__(self, uid, id, max, min, step, allowCross=False, marks=[]):
		super().__init__(uid, id)
		self.allowCross = allowCross
		self.max = max
		self.min = min
		self.step = step
		self.marks = marks
		
class Input(baseInputElement):
	def __init__(self, uid, id, max=100, min=0, maxlength=100, minlength=0, multiple=False, placeholder='', type='text'):
		super().__init__(uid, id)
		self.placeholder = placeholder
		self.max = max
		self.min = min
		self.maxlength = maxlength
		self.minlength = minlength
		self.multiple = multiple
		self.type = type

class Textarea(baseInputElement):
	def __init__(self, uid, id, cols, rows, maxLength, placeholder='', title=''):
		super().__init__(uid, id)
		self.cols = cols
		self.rows = rows
		self.maxLength = maxLength
		self.placeholder = placeholder
		self.title = title
		
class Checklist(baseInputElement):
	def __init__(self, uid, id, options):
		super().__init__(uid, id)
		self.options = options
		
class Radioitems(baseInputElement):
	def __init__(self, uid, id, options):
		super().__init__(uid, id)
		self.options = options
		
class DatePickerSingle(baseInputElement):
	def __init__(self, uid, id,  max_date_allowed, min_date_allowed, placeholder=''):
		super().__init__(uid, id)
		self.max_date_allowed = max_date_allowed
		self.min_date_allowed = min_date_allowed
		self.placeholder = placeholder
		
class DatePickerRange(baseInputElement):
	def __init__(self, uid, id,  max_date_allowed, min_date_allowed):
		super().__init__(uid, id)
		self.max_date_allowed = max_date_allowed
		self.min_date_allowed = min_date_allowed