log.print("starting menu renderer")

menu = CSafeMenu()

menu.addSubmenu('Screens')
menu.addItem('Screens', ['Result overview', '/d/DisplayScreen@screen=ResultOverview&asset='+args.get('asset'),  'menu-item-active' if args.get('screen') == 'ResultOverview' else 'menu-item'])
menu.addItem('Screens', ['Engine results', '/d/DisplayScreen@screen=EngineResults&asset='+args.get('asset'),  'menu-item-active' if args.get('screen') == 'EngineResults' else 'menu-item'])

menu.addSubmenu('Assets')
menu.addItem('Assets', ['Valle Selva Meloni', '/d/DisplayScreen@asset=Alperia-VSM&screen='+args.get('screen'),  'menu-item-active' if args.get('asset') == 'Alperia-VSM' else 'menu-item'])
menu.addItem('Assets', ['Hongrin-Léman', '/d/DisplayScreen@asset=Alpiq-FMHL&screen='+args.get('screen'),  'menu-item-active' if args.get('asset') == 'Alpiq-FMHL' else 'menu-item'])
menu.addItem('Assets', ['Testmodell', '/d/DisplayScreen@asset=TAH-TM&screen='+args.get('screen'),  'menu-item-active' if args.get('asset') == 'TAH-TM' else 'menu-item'])

return menu.getNestedList()