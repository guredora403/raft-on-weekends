# Makefile

# マークダウンファイルのリスト
MD_FILES = 0-intro.md 1-parallel-pcoessing.md 2-consistency.md 3-raft.md 4-repo.md 5-handson.md

# 個別のPDFファイル名 (./distディレクトリに出力)
PDF_FILES = $(patsubst %.md, ./dist/%.pdf, $(MD_FILES))

# 結合後のMarkdownファイル名
MERGED_MD = ./dist/merged_output.md

# 結合後のPDFファイル名
MERGED_PDF = ./dist/merged_output.pdf

# デフォルトターゲット
all: $(PDF_FILES) $(MERGED_PDF)

# 個別のMarkdownファイルをPDFに変換するルール
./dist/%.pdf: %.md
	mkdir -p ./dist
	marp $< --pdf --allow-local-files --output $@

# Markdownファイルを結合するルール
$(MERGED_MD): $(MD_FILES)
	mkdir -p ./dist
	cat $(MD_FILES) > $(MERGED_MD)

# 結合されたMarkdownをPDFに変換するルール
$(MERGED_PDF): $(MERGED_MD)
	marp $(MERGED_MD) --pdf --allow-local-files --output $@

# クリーンアップ用ルール
clean:
	rm -f ./dist/*.pdf ./dist/*.md
