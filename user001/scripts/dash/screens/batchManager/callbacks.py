Clicks = CSafeList()

def selectListInteraction(*clicks):
	global Clicks
	clicks = CSafeList(lst=clicks)
	selectList = screenVariables.get('mySelectList')
	i = 0
	while Clicks.len() < clicks.len():
		Clicks.append(0)
	while i < clicks.len():
		z = clicks.get(i)
		if z is None:
			clicks.set(i, 0)
		i = i + 1
	selected = 'none'
	i = 0
	selectedList = CSafeList(lst=selectList.getSelected())
	while i < clicks.len():
		if clicks.get(i) != Clicks.get(i):
			selected = i
		i = i + 1
	i = 0
	while i < clicks.len():
		if selected == i:
			selectedList.set(i, selectedList.get(i) ^ 1)
		i = i + 1
	return selectList.select(selectedList.getList())

Clicks1 = CSafeList()

def selectListInteraction1(*clicks):
	global Clicks1
	clicks = CSafeList(lst=clicks)
	selectList = screenVariables.get('mySelectList1')
	i = 0
	while Clicks1.len() < clicks.len():
		Clicks1.append(0)
	while i < clicks.len():
		z = clicks.get(i)
		if z is None:
			clicks.set(i, 0)
		i = i + 1
	selected = 'none'
	i = 0
	selectedList = CSafeList(lst=selectList.getSelected())
	while i < clicks.len():
		if clicks.get(i) != Clicks1.get(i):
			selected = i
		i = i + 1
	i = 0
	while i < clicks.len():
		if selected == i:
			selectedList.set(i, 1)
		else:
			selectedList.set(i, 0)
		i = i + 1
	return selectList.select(selectedList.getList())