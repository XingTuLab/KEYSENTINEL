const traverse = require("@babel/traverse").default;
const parse = require('@babel/parser').parse;
const fs = require('fs');
const path = require('path');

function getFileinfo(filePath){
  var code = fs.readFileSync(filePath).toString();
  const extension = path.extname(filePath).toLowerCase();
  if (extension === '.ts') {
    var ast = parse(code, {
        sourceType: 'module',
        ranges: false,
        plugins: ['typescript']
    });

  } else if (extension === '.js'||extension==='.jsx') {
      var ast = parse(code, { sourceType: 'module', plugins: ['jsx'] });
  } else {
      return 'Unknown';
  }
  const strings = [];

  const visitor = {
    StringLiteral: function(path) {
        const stringValue = path.node.value;
        const loc = path.node.loc;
        dict={
          'value': stringValue,
          "line_start": loc['start']['line'],
          "line_end": loc['end']['line'],
          "col_start":loc['start']['column'],
          "col_end":loc['end']['column'],
      }
        strings.push(dict);
    },
    TemplateLiteral: function (path) {
      const expressions = path.node.expressions;
      const quasis = path.node.quasis;

      quasis.forEach((quasi) => {
        const stringValue = quasi.value.raw;
        const loc = quasi.loc;
        dict={
          'value': stringValue['value'],
          "line_start": loc['start']['line'],
          "line_end": loc['end']['line'],
          "col_start":loc['start']['column'],
          "col_end":loc['end']['column'],
      }
        strings.push(dict);
      });
    }
  };

  traverse(ast, visitor);

  return JSON.stringify(strings);
}
const filePath = process.argv[2];
const result = getFileinfo(filePath);
console.log(result);
