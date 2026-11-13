/**
 * Package entry point for the TypeScript Active Inference implementation.
 *
 * Importing this module exposes the agent API. Running it directly executes
 * the demo suite, which is what `npm start` and `run.sh` expect.
 */

import { pathToFileURL } from 'node:url';
import { main } from './demos/ant-colony-demo.js';

export { ActiveInferenceAgent } from './ActiveInferenceAgent.js';
export * from './types.js';
export { runAntColonyDemo, runSingleAgentDemo, runErrorHandlingDemo, main } from './demos/ant-colony-demo.js';

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
    main();
}
