SageMakerを使用して前処理や後処理を行うのに、ProcessingJobを用いる。

ProcessingJobの設定や起動をPython SDKで行う場合に使用するのがProcessorクラス。

大元となるProcessorクラスを継承して、フレームワークやユースケースに合わせたProcessorクラスが用意されている。

継承関係

```less
Processor
|- ScriptProcessor
	|- SKLearnProcessor
	|- FrameworkProcessor
		|- PytorchProcessor
		|- TensorFlowProcessor
```

Processorは指定したDocker imageを実行するのみ。

ScriptProcessorは指定したDocker imageを元にしたコンテナに、スクリプトを挿入して実行できる。

FrameworkProcessorは使用するフレームワークの種類やバージョンを指定することで、AWSが用意している適したDocker imageでコンテナを起動して、スクリプトを挿入して実行する。

注意が必要なのは、コンテナに挿入するスクリプトに依存関係がある場合である

ProcessingJobの実行時(run)にsource_dirでディレクトリ自体を指定したり、dependenciesで複数の依存ファイルを指定することができる機能が、FrameworkProcessorに定義されているということ。

そのため、ScriptProcessorを継承しているSKLearnProcessorではこのような依存関係の解決ができない。

FrameworkProcessorの内部では依存関係をまとめてS3に格納しているので、自前でパッキングしてS3に保存しProcessingInputで指定してあげたら実現自体は可能だが、サポートしてくれてもいいと思う。

[https://github.com/aws/sagemaker-python-sdk/issues/4968](https://github.com/aws/sagemaker-python-sdk/issues/4968)

[https://github.com/aws/sagemaker-python-sdk/issues/3599](https://github.com/aws/sagemaker-python-sdk/issues/3599)

[https://github.com/aws/sagemaker-python-sdk/issues/1248](https://github.com/aws/sagemaker-python-sdk/issues/1248)