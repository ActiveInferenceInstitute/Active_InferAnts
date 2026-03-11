#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Solidity Active Inference contract"
echo "This is a smart contract — it runs on the EVM, not directly."
echo ""
if command -v solc &> /dev/null; then
    echo "Compiling with solc..."
    solc --optimize --bin --abi "$SCRIPT_DIR/ActiveInference.sol" -o "$SCRIPT_DIR/build/" --overwrite 2>&1
    echo "✅ Contract compiled successfully to build/"
    echo "Deploy to a local testnet (Hardhat/Foundry) or Ethereum network."
else
    echo "⚠️  solc not found. Install: https://docs.soliditylang.org/en/latest/installing-solidity.html"
    echo "Displaying contract source..."
    cat "$SCRIPT_DIR/ActiveInference.sol"
fi
