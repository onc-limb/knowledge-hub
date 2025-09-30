Pythonのパッケージマネージャーであるuvでpipなど他のパッケージマネージャーで使用できるようなrequirements.txtを出力する方法。

```python
uv export > requirements.txt
```

このコマンドでpyproject.tomlに記載された依存関係をrequirements.txtに出力することができる。

—lockedを使用することでuv.lockを更新せずに依存関係を取得できる。