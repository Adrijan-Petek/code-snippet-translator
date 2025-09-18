// tools/parse_js.js
const parser = require('@babel/parser');
const fs = require('fs');

try {
    const code = fs.readFileSync(0, 'utf8');
    const ast = parser.parse(code, {
        sourceType: 'module',
        plugins: ['jsx', 'classProperties']
    });
    console.log(JSON.stringify(ast, null, 2));
} catch (error) {
    console.error(JSON.stringify({ error: error.message }));
    process.exit(1);
}