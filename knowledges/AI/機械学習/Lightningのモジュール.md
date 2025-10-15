PytorchのLightningにはLightningModuleとLightningDataModuleが存在する。
LightningModuleは学習するモデルの本体であり、機械学習の脳みそとなるモジュール。
下記のメソッドを持って、それぞれを実行することでモデルを学習させることができる。
- init モデルの定義
- forward　入力データの流れの定義（順伝播）
- training_step　一つのバッチデータに対する損失の計算
- validation_step, test_step　モデルの評価
- configure_optimizers　オプティマイザの設定

LightninigDataModuleはデータをモデルに供給するためのパイプラインを定義するモジュール。
下記のメソッドを持っている。
- prepare_data　データの取得
- setup　データの分割や前処理
- hoge_dataloader　データローダーの返却

