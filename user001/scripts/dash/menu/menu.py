log.print("starting menu renderer")

menu = CSafeMenu()

menu.addSubmenu('First')

menu.addItem('First', ['Result overview', '/d/DisplayScreen@screen=ResultOverview'+args.get('asset'),  'menu-item-active' if args.get('screen') == 'ResultOverview' else 'menu-item'])
menu.addItem('First', ['Engine results', '/d/DisplayScreen@screen=EngineResults&asset='+args.get('asset'),  'menu-item-active' if args.get('screen') == 'EngineResults' else 'menu-item'])

menu.addSubmenu('Second')
menu.addItem('Second', ['Valle Selva Meloni', '/d/DisplayScreen@asset=Alperia-VSM&screen='+args.get('screen'),  'menu-item-active' if args.get('asset') == 'Alperia-VSM' else 'menu-item'])
menu.addItem('Second', ['Hongrin-Léman', '/d/DisplayScreen@asset=Alpiq-FMHL&screen='+args.get('screen'),  'menu-item-active' if args.get('asset') == 'Alpiq-FMHL' else 'menu-item'])
menu.addItem('Second', ['Testmodell', '/d/DisplayScreen@asset=TAH-TM&screen='+args.get('screen'),  'menu-item-active' if args.get('asset') == 'TAH-TM' else 'menu-item'])

return menu.getNestedList()