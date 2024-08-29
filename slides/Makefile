# Makefile

# マークダウンファイルのリスト
MD_FILES = 0-intro.md 1-parallel-pcoessing.md 2-consistency.md 3-raft.md 4-repo.md 5-handson.md

# 生成するPDFファイル名 (./distディレクトリに出力)
PDF_FILES = $(patsubst %.md, ./dist/%.pdf, $(MD_FILES))

# 結合後のPDFファイル名
MERGED_PDF = ./dist/merged_slides.pdf


# デフォルトターゲット
all: $(PDF_FILES) $(MERGED_PDF)

# 出力ディレクトリを確認してPDFに変換するルール
./dist/%.pdf: %.md
	mkdir -p ./dist
	marp $< --pdf --allow-local-files --theme ./marp_themes/delight.css --output $@

# PDFを結合するルール
$(MERGED_PDF): $(PDF_FILES)
	pdfunite $(PDF_FILES) $(MERGED_PDF)

# クリーンアップ用ルール
clean:
	rm -f ./dist/*.pdf
