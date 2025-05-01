package main

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"strings"
)

func main() {


	// 使用parser解析代码
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, "./dddd.go", code, 0)
	if err != nil {
		fmt.Println("解析代码时发生错误:", err)
		return
	}
	a=`afasfa
	fsafasfvzv`
	// 遍历AST，找到所有的字符串并输出位置信息
	ast.Inspect(f, func(n ast.Node) bool {
		switch x := n.(type) {
		case *ast.BasicLit:
			// 检查是否为字符串
			if x.Kind == token.STRING {
				// 提取字符串和位置信息并打印
				str := strings.Trim(x.Value, `"`)
				pos := fset.Position(x.Pos())
				index := fset.Position(x.Pos()).Offset

				fmt.Printf("提取的字符串: %s\n位置: %s\n行号: %d\n列号: %d\n索引: %d\n", str, pos, pos.Line, pos.Column, index)
			}
		}
		return true
	})
}
