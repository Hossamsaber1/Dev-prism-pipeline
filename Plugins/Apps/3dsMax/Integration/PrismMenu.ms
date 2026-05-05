version = getFileVersion "$max/3dsmax.exe"
versionData = filterString version ","
if versionData[1] as Integer >= 27 then (
	function prismMenuCallback =
	(
		local menuMgr = callbacks.notificationParam()
		local mainMenuBar = menuMgr.mainMenuBar
		local helpMenuId = "cee8f758-2199-411b-81e7-d3ff4a80d143"
		local newSubMenu = mainMenuBar.CreateSubMenu "F8FFB827-741C-4A81-8C89-BBF856DCF56D" "Prism" beforeId:helpMenuId
		newSubMenu.CreateAction "bb767ab4-b239-414f-80dd-d55b0a991ce1" 647394 "PrismSave`Prism"
		newSubMenu.CreateAction "bb767ab4-b239-414f-80dd-d55b0a991ce2" 647394 "PrismCommentsave`Prism"
		newSubMenu.CreateAction "bb767ab4-b239-414f-80dd-d55b0a991ce3" 647394 "OpenProjectBrowser`Prism"
		newSubMenu.CreateAction "bb767ab4-b239-414f-80dd-d55b0a991ce4" 647394 "PrismStateManager`Prism"
		newSubMenu.CreateAction "bb767ab4-b239-414f-80dd-d55b0a991ce5" 647394 "PrismSettings`Prism"
	)
	callbacks.removeScripts id:#prismMenu
	callbacks.addScript #cuiRegisterMenus prismMenuCallback id:#prismMenu
	mng = maxops.GetICuiMenuMgr()
	mng.LoadConfiguration("")
) else (
	if menuMan.findMenu "Prism" != undefined then
	(
		menuMan.unRegisterMenu (menuMan.findMenu "Prism")
	)
	(
		local mainMenuBar = menuMan.getMainMenuBar()
		local subMenu = menuMan.createMenu "Prism"
		local psaveItem = menuMan.createActionItem "PrismSave" "Prism"
		subMenu.addItem psaveItem -1
		local pcommentsaveItem = menuMan.createActionItem "PrismCommentsave" "Prism"
		subMenu.addItem pcommentsaveItem -1
		local browserItem = menuMan.createActionItem "OpenProjectBrowser" "Prism"
		subMenu.addItem browserItem -1
		local pmanagerItem = menuMan.createActionItem "PrismStateManager" "Prism"
		subMenu.addItem pmanagerItem -1
		local settingsItem = menuMan.createActionItem "PrismSettings" "Prism"
		subMenu.addItem settingsItem -1
		local subMenuItem = menuMan.createSubMenuItem "Prism" subMenu
		local subMenuIndex = mainMenuBar.numItems()
		mainMenuBar.addItem subMenuItem subMenuIndex
		menuMan.updateMenuBar()
		menuMan.saveMenuFile (menuMan.getMenuFile())
		--menuMan.unRegisterMenu (menuMan.findMenu "Prism")
	)
)