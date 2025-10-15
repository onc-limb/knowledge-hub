# Research: knowledges ディレクトリメタデータ生成機能

## 技術選択の調査結果

### プログラミング言語・ランタイム

**Decision**: TypeScript/Node.js  
**Rationale**:

- 既存の knowledge-hub プロジェクトが TypeScript/Node.js で構築されている
- scripts/generate-metadata.ts が既に存在し、拡張ベースで実装可能
- ファイルシステム操作は Node.js 標準ライブラリで十分

**Alternatives considered**:

- Python: 新しい依存関係追加が必要
- Bash/Shell: 複雑な JSON 操作が困難
- Go: 既存プロジェクトとの整合性に欠ける

### ファイルシステム操作

**Decision**: Node.js 標準ライブラリ (fs, path)  
**Rationale**:

- `fs.readdirSync()`, `fs.statSync()` で同期的なディレクトリスキャンが可能
- `path.join()`, `path.extname()` でクロスプラットフォーム対応
- 外部依存なしでシンプルな実装が可能

**Alternatives considered**:

- glob library: 過度に複雑、標準 API で十分
- fast-glob: パフォーマンス向上は現在のスケールでは不要

### データ構造・形式

**Decision**: 既存の meta.json 形式を維持  
**Rationale**:

- 後方互換性の確保が要件に明記されている
- categories 配列、category/point/subCategories/names 構造は十分
- 階層の深度制限撤廃により再帰構造に対応

**Alternatives considered**:

- 新しい JSON schema: 破壊的変更となり要件違反
- YAML 形式: 既存利用者への影響大

### アーキテクチャパターン

**Decision**: 関数型アプローチ  
**Rationale**:

- ディレクトリスキャンは純粋関数として実装可能
- 状態管理不要でテストが簡単
- 再帰処理に適している

**Alternatives considered**:

- オブジェクト指向: 過度に複雑、状態管理が不要
- イベント駆動: ファイル監視は現在の要件外

### テスト戦略

**Decision**: 実ファイルシステムベースのテスト  
**Rationale**:

- ファイル操作の正確性確保が重要
- テスト用のディレクトリ構造作成は軽量
- 統合テストで実際の動作確認が可能

**Alternatives considered**:

- モックファイルシステム: 実際の動作との乖離リスク
- インメモリ: パス操作の検証困難

### パフォーマンス考慮

**Decision**: 同期処理  
**Rationale**:

- ファイル数が現在 20 程度、将来も数百程度
- CLI ツールのため順次処理で十分
- 実装の複雑性を避けることを優先

**Alternatives considered**:

- 非同期処理: 現在のスケールでは過度に複雑
- 並列処理: I/O ボトルネックよりもメモリ効率を重視

## 実装方針

### ライブラリ構成

```
src/metadata-generator/
├── index.ts      # メインエクスポート
├── scanner.ts    # ディレクトリスキャン処理
└── types.ts      # 型定義
```

### 処理フロー

1. knowledges ディレクトリをルートとしてスキャン開始
2. 各ディレクトリで`.md`ファイルを検出・カウント
3. サブディレクトリを再帰的に処理
4. カテゴリのポイント = 直下ファイル数 + サブカテゴリポイント合計
5. 既存の meta.json 形式で JSON を生成・出力

### エラーハンドリング

- ディレクトリアクセス権限エラー
- ファイル書き込みエラー
- JSON parsing/stringify エラー
- 不正なディレクトリ構造

## 依存関係

- Node.js 標準ライブラリのみ
- TypeScript (開発時)
- テストランナー (Node.js built-in または Jest)

## 非機能要件

- **パフォーマンス**: 1000 ファイル未満を 1 秒以内
- **互換性**: 既存 meta.json 形式 100%維持
- **保守性**: 単一責任の関数分割
- **拡張性**: 将来的なフィルタリング機能追加を考慮
