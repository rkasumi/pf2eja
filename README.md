# PF2e用 日本語化モッド

以下から訳語を使用。個人使用のバックアップ
https://w.atwiki.jp/p2rdj/

# legacy版のデータを使用する
* pf2e-legacy-contentモジュールに対してbabeleが反映されない (理由未調査)
* pf2e-legacy-contentをインストールして、main.pyを実行することでpf2e systemへ必要な辞書を上書きする
  * spells-legacyは呪文体系のJSONの持ち方が変わっていたのでmain.pyで合わせて変換する

# compendium browserをデフォルト絞り込み
* デフォルトだと全ソースが表示される => 翻訳していないソースが表示されてしまう
* 対象："pathfinder-core-rulebook", "pathfinder-player-core", "pathfinder-advanced-players-guide"
* systems/pf2e/pf2e.mjsを編集することで強制的に絞り込みをかける
  * PF2E.ActionActionTypeLabel の直後のsource内の selected: [""]
      "pathfinder-core-rulebook", "pathfinder-player-core", "pathfinder-advanced-players-guide"
  * PF2E.BrowserFilterWeaponFilters の直後のsource内の selected: [""]
    * "pathfinder-core-rulebook", "pathfinder-player-core", "pathfinder-advanced-players-guide", "pathfinder-gm-core"
  * PF2E.BrowserFilterSkills の直後のsource内の selected: [""]
      "pathfinder-core-rulebook", "pathfinder-player-core", "pathfinder-advanced-players-guide","pathfinder-secrets-of-magic"
  * PF2E.BrowserFilterSpellCategories の直後のsource内の selected: [""]
      "pathfinder-core-rulebook", "pathfinder-player-core", "pathfinder-advanced-players-guide"
