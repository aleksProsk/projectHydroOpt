def loadModal(n0, n1, n2, n3, n4, n5, n6, n7, oldStyle):
	if n0 is None:
		n0 = 0
	if n1 is None:
		n1 = 0
	if n2 is None:
		n2 = 0
	if n3 is None:
		n3 = 0
	if n4 is None:
		n4 = 0
	if n5 is None:
		n5 = 0
	if n6 is None:
		n6 = 0
	if n7 is None:
		n7 = 0
	style = CSafeDict(oldStyle)
	if n0 + n1 + n2 + n3 + n4 + n5 + n6 > n7:
		style.set('display', 'block')
	else:
		style.set('display', 'none')
	return style.getDict()

N0 = 0
N1 = 0
N2 = 0
N3 = 0
N4 = 0
N5 = 0
N6 = 0

def buildModalGraph(n0, n1, n2, n3, n4, n5, n6, fig0, fig1, fig2, fig3, fig4, fig5, fig6):
	global N0, N1, N2, N3, N4, N5, N6
	if n0 is None:
		n0 = 0
	if n1 is None:
		n1 = 0
	if n2 is None:
		n2 = 0
	if n3 is None:
		n3 = 0
	if n4 is None:
		n4 = 0
	if n5 is None:
		n5 = 0
	if n6 is None:
		n6 = 0
	fig = fig0
	if n1 != N1:
		fig = fig1
	if n2 != N1:
		fig = fig2
	if n3 != N1:
		fig = fig3
	if n4 != N1:
		fig = fig4
	if n5 != N1:
		fig = fig5
	if n6 != N1:
		fig = fig6
	log.print(fig)
	newFig = CSafeFigure(figure=fig)
	newFig.scale(1.6)
	return newFig.getFigure()

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
			if i == 0:
				selected = 'all'
				j = 0
				cnt = 0
				while j < selectedList.len():
					if selectedList.get(j) == 1:
						cnt = cnt + 1
					j = j + 1
				if cnt == selectedList.len():
					selected = 'noone'
			else:
				selected = i
		i = i + 1
	i = 0
	while i < clicks.len():
		if selected == i:
			selectedList.set(i, selectedList.get(i) ^ 1)
		elif selected == 'all':
			selectedList.set(i, 1)
		elif selected == 'noone':
			selectedList.set(i, 0)
		i = i + 1
	return selectList.select(selectedList.getList())