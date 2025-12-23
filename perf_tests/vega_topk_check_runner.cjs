'use strict';

// Simple Node runner that bootstraps ts-node for TypeScript/TSX imports
// Usage: node perf_tests/vega_topk_check_runner.cjs

require('ts-node').register({
  transpileOnly: true,
  compilerOptions: {
    module: 'commonjs',
    jsx: 'react-jsx',
  },
});

require('./vega_topk_check.ts');
