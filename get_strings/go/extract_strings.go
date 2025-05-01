package main

import (
	"encoding/json"
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"os"
	"strings"
	"unicode/utf8"
)

func main() {
	// 检查是否提供了文件路径作为命令行参数
	if len(os.Args) != 2 {
		fmt.Println("请提供要解析的Go代码文件路径作为命令行参数")
		return
	}

	filePath := os.Args[1]

	// 从文件中读取Go代码
	code, err := readCodeFromFile(filePath)
	if err != nil {
		fmt.Println("读取文件时发生错误:", err)
		return
	}

	// 使用parser解析代码
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, filePath, code, 0)
	if err != nil {
		fmt.Println("解析代码时发生错误:", err)
		return
	}

	// 用于存储提取的字符串信息的结构体
	var extractedStrings []ExtractedString

	// 遍历AST，找到所有的字符串
	ast.Inspect(f, func(n ast.Node) bool {
		switch x := n.(type) {
		case *ast.BasicLit:
			// 检查是否为字符串
			if x.Kind == token.STRING {
				// 提取字符串和位置信息
				str := strings.Trim(x.Value, `"`)
				startPos := fset.Position(x.Pos())
				endPos := fset.Position(x.End())

				// 计算字符数
				charCount := utf8.RuneCountInString(str)

				// 创建ExtractedString对象
				extracted := ExtractedString{
					Value:      str,
					Length:     charCount,
					LineStart:  startPos.Line,
					LineEnd:    endPos.Line,
					ColStart:   startPos.Column,
					ColEnd:     startPos.Column + charCount,
				}

				// 将提取的字符串信息添加到列表中
				extractedStrings = append(extractedStrings, extracted)
			}
		}
		return true
	})

	// 将提取的字符串信息转换为JSON格式并打印
	jsonData, err := json.MarshalIndent(extractedStrings, "", "    ")
	if err != nil {
		fmt.Println("转换为JSON时发生错误:", err)
		return
	}

	fmt.Println(string(jsonData))
}

// ExtractedString 结构体用于存储提取的字符串信息
type ExtractedString struct {
	Value     string `json:"value"`
	Length    int    `json:"length"`
	LineStart int    `json:"line_start"`
	LineEnd   int    `json:"line_end"`
	ColStart  int    `json:"col_start"`
	ColEnd    int    `json:"col_end"`
}

// 从文件中读取Go代码
func readCodeFromFile(filePath string) (string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	stat, err := file.Stat()
	if err != nil {
		return "", err
	}

	size := stat.Size()
	content := make([]byte, size)
	_, err = file.Read(content)
	if err != nil {
		return "", err
	}

	return string(content), nil
}
