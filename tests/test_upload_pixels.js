// Run with: node tests/test_upload_pixels.js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const context = { document: { addEventListener() {} } };
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(__dirname, '../app/static/app.js'), 'utf8'), context);
const ink = Array.from({ length: 784 }, (_, i) => {
    const x = i % 28, y = Math.floor(i / 28);
    return x >= 12 && x < 16 && y >= 6 && y < 24 ? 255 : 0;
});
for (const format of ['white_on_black', 'black_on_white', 'black_transparent', 'white_transparent']) {
    const pixels = new Uint8ClampedArray(784 * 4);
    ink.forEach((v, i) => {
        const gray = format === 'black_on_white' ? 255 - v :
            format === 'black_transparent' ? 0 : format === 'white_transparent' ? 255 : v;
        pixels.set([gray, gray, gray, format.endsWith('transparent') ? v : 255], i * 4);
    });
    context.normalizeUploadedPixels({ data: pixels, width: 28, height: 28 });
    ink.forEach((v, i) => {
        assert.equal(pixels[i * 4], v, format);
        assert.equal(pixels[i * 4 + 3], 255, format);
    });
}
console.log('PASS: four image backgrounds normalize to identical digit pixels.');
