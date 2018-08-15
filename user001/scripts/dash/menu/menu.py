log.print("starting menu renderer")

menu = CSafeMenu()

menu.addSubmenu('First')
menu.addItem('First', ['Main Screen', '/d/DisplayScreen@screen=index', 'menu-item'])
menu.addItem('First', ['Model', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item-active' if args.contains('selected') and args.get('selected') == 'Model' else 'menu-item'])
menu.addItem('First', ['Utilities', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Utilities',  'menu-item-active' if args.contains('selected') and args.get('selected') == 'Utilities' else 'menu-item'])
menu.addItem('First', ['Assets', '/d/DisplayScreen@screen=assets&selected=Assets',  'menu-item-active' if args.contains('selected') and args.get('selected') == 'Assets' else 'menu-item'])
menu.addItem('First', ['About', '/d/DisplayScreen@screen=about&selected=About',  'menu-item-active' if args.contains('selected') and args.get('selected') == 'About' else 'menu-item'])

menu.addSubmenu('Second')
if args.contains('selected'):
    if args.get('selected') == 'Model':
        menu.addItem('Second', ['New', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item'])
        menu.addItem('Second', ['Open', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item'])
        menu.addItem('Second', ['Save', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item'])
        menu.addItem('Second', ['Preferences', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Model',  'menu-item'])
    elif args.get('selected') == 'Utilities':
        menu.addItem('Second', ['Price Scenario Generator', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Utilities',  'menu-item'])
        menu.addItem('Second', ['CSV Editor', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Utilities',  'menu-item'])
        menu.addItem('Second', ['Profile Editor', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Utilities',  'menu-item'])
        menu.addItem('Second', ['Hedge Decomposer', '/d/DisplayScreen@screen='+args.get('screen')+'&selected=Utilities',  'menu-item'])

return menu.getNestedList()