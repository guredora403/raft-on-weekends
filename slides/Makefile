# Makefile

# マークダウンファイルのリスト
MD_FILES = 0-intro.md 1-parallel-pcoessing.md 3-raft.md 5-repo.md 4-handson.md

# 生成するPDFファイル名 (./distディレクトリに出力)
PDF_FILES = $(patsubst %.md, ./dist/%.pdf, $(MD_FILES))

# デフォルトターゲット
all: $(PDF_FILES)

# 出力ディレクトリを確認してPDFに変換するルール
./dist/%.pdf: %.md
	mkdir -p ./dist
	marp $< --pdf --output $@

# クリーンアップ用ルール
clean:
	rm -f ./dist/*.pdf
