Hooks.once('init', () => {

	if(typeof Babele !== 'undefined') {
		
		Babele.get().register({
			module: 'z_pf2eja',
			lang: 'ja',
			dir: 'compendium'
		});
	}
});
