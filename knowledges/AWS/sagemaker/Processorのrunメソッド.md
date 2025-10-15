SageMaker SDKのProcessorクラスが定義しているrunメソッドを実行することで、ProcessingJobの実行をトリガーすることができる。

FrameworkProcessorのrunメソッドのコメントに下記のような内容がある。

```python
Returns:
  None or pipeline step arguments in case the Processor instance is built with
  :class:`~sagemaker.workflow.pipeline_context.PipelineSession`
```

つまり、何も返さない時と、パイプラインのステップ引数を返す時があるということらしい。

これはProcessorインスタンスがSageMakerのPipelineSessionを指定して作成されていたらパイプラインのステップとして扱うので、ProcessingJobの実行は遅延される。