Hooks.once('init', () => {

	if(typeof Babele !== 'undefined') {
		
		Babele.get().register({
			module: 'pf2eja',
			lang: 'ja',
			dir: 'compendium'
		});
	}
});
