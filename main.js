Hooks.once("ready", () => {
    //----- Compendium Browser のデフォルト絞り込みを変更
    // アクション
    game.pf2e.compendiumBrowser.tabs.action.filterData.checkboxes.source.selected = [
        "pathfinder-core-rulebook",
        "pathfinder-player-core",
        "pathfinder-advanced-players-guide",
    ];
    // 装備品
    game.pf2e.compendiumBrowser.tabs.equipment.filterData.checkboxes.source.selected = [
        "pathfinder-core-rulebook",
        "pathfinder-player-core",
        "pathfinder-advanced-players-guide",
        "pathfinder-gm-core", // 戦利品リスト
    ];
    // 特技
    game.pf2e.compendiumBrowser.tabs.feat.filterData.checkboxes.source.selected = [
        "pathfinder-core-rulebook",
        "pathfinder-player-core",
        "pathfinder-advanced-players-guide",
        "pathfinder-secrets-of-magic", // メイガス・サモナー用
    ];
    // 呪文
    game.pf2e.compendiumBrowser.tabs.spell.filterData.checkboxes.source.selected = [
        "pathfinder-core-rulebook",
        "pathfinder-player-core",
        "pathfinder-advanced-players-guide",
    ];
})
