Hooks.once('init', () => {
	if(typeof Babele !== 'undefined') {
		Babele.get().register({
			module: 'z_pf2eja',
			lang: 'ja',
			dir: 'compendium'
		});

		Babele.get().registerConverters({
			"bestiaryItems": (entities, translations) => {
        const dynamicMapping = new CompendiumMapping('Item');
        return entities.map((data) => {
          if (translations) {
              let translation;
              if (Array.isArray(translations)) {
                  translation = translations.find(t => t.id === data._id || t.id === data.name);
              } else {
                  translation = translations[data._id] || translations[data.name];
              }

              if (translation) {
                  const translatedData = dynamicMapping.map(data, translation);
                  return mergeObject(data, mergeObject(translatedData, { translated: true }));
              }
          }
          const pack = game.babele.packs.filter(
              pack => pack.metadata.id === "pf2e.bestiary-ability-glossary-srd"
          )
          return pack ? pack[0].translate(data) : data;
        });
      }
    });
  }
});

