# PF2e用 日本語化モッド

以下から訳語を使用。個人使用のバックアップ
https://w.atwiki.jp/p2rdj/

# legacy版のデータを使用する
* pf2e-legacy-contentモジュールに対してbabeleが反映されない (理由未調査)
* pf2e-legacy-contentをインストールして、legacy-convert.py実行でpf2e systemへ必要な辞書を上書きする
  * 呪文・特技はJSON構成が変わっているので、あわせて変換
  * equipmentsは変換が困難だったので、本流のものを使用。(訳語だけ旧版準拠にする)

# babele.js クリーチャーの余計なデータを翻訳しないようにする
modules/babele/babele.js
DEFAULT_MAPPINGS
Actor
items　をまるっとコメントアウト
