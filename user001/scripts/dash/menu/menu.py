log.print("starting menu renderer")

menu = CSafeMenu()

menu.addSubmenu('First')
if args.contains('selected') and (args.get('selected') == 'Model' or args.get('selected') == 'Utilities'):
    menu.addItem('First', ['Main Screen', '/d/DisplayScreen@screen=index&selected='+args.get('selected'), 'menu-item-active' if args.get('screen') == 'index' else 'menu-item'])
else:
    menu.addItem('First', ['Main Screen', '/d/DisplayScreen@screen=index', 'menu-item-active' if args.get('screen') == 'index' else 'menu-item'])
if args.contains('selected') and (args.get('selected') == 'Model' or args.get('selected') == 'Utilities'):
    menu.addItem('First', ['Assets', '/d/DisplayScreen@screen=assets&selected='+args.get('selected'),  'menu-item-active' if args.get('screen') == 'assets' else 'menu-item'])
else:
    menu.addItem('First', ['Assets', '/d/DisplayScreen@screen=assets',  'menu-item-active' if args.get('screen') == 'assets' else 'menu-item'])
if args.contains('selected') and (args.get('selected') == 'Model' or args.get('selected') == 'Utilities'):
    menu.addItem('First', ['About', '/d/DisplayScreen@screen=about&selected='+args.get('selected'),  'menu-item-active' if args.get('screen') == 'about' else 'menu-item'])
else:
    menu.addItem('First', ['About', '/d/DisplayScreen@screen=about',  'menu-item-active' if args.get('screen') == 'about' else 'menu-item'])

menu.addSubmenu('Second')
menu.addItem('Second', ['Model', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item-active' if args.contains('selected') and args.get('selected') == 'Model' else 'menu-item'])
menu.addItem('Second', ['Utilities', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Utilities',  'menu-item-active' if args.contains('selected') and args.get('selected') == 'Utilities' else 'menu-item'])


menu.addSubmenu('Third')
if args.contains('selected'):
    if args.get('selected') == 'Model':
        menu.addItem('Third', ['New', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item', 'new'])
        menu.addItem('Third', ['Open', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item', 'open'])
        menu.addItem('Third', ['Save', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item', 'save'])
        menu.addItem('Third', ['Add assets', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item', 'add'])
        menu.addItem('Third', ['Preferences', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item'])
    elif args.get('selected') == 'Utilities':
        menu.addItem('Third', ['Price Scenario Generator', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Utilities', 'menu-item'])
        menu.addItem('Third', ['CSV Editor', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Utilities', 'menu-item'])
        menu.addItem('Third', ['Profile Editor', '/d/DisplayScreen@screen=profileEditor&selected=Utilities', 'menu-item-active' if args.get('screen') == 'profileEditor' else 'menu-item'])
        menu.addItem('Third', ['Hedge Decomposer', '/d/DisplayScreen@screen=hedgeDecomposer&selected=Utilities', 'menu-item-active' if args.get('screen') == 'hedgeDecomposer' else 'menu-item'])

return menu.getNestedList()