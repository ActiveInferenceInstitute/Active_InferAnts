#!/bin/bash

# Active Inference Shell Implementation Runner

set -e

echo "🐚 Shell Active Inference Demo"
echo "=============================="

# Check for required shell utilities
for cmd in bc awk sed grep sort uniq; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ Error: $cmd not found"
        echo "Please install POSIX utilities"
        exit 1
    fi
done

echo "✅ All required shell utilities found"

# Create config.sh if it doesn't exist (must use scalar export format for Active_Shellference.sh)
if [ ! -f config.sh ]; then
    echo "📝 Creating default configuration..."
    cat > config.sh << 'CONFIG_EOF'
#!/bin/bash

# Simulation configuration for Shell Active Inference
export CONFIG_ENVIRONMENT="food danger safe"
export CONFIG_INITIAL_BELIEFS="0.25 0.25 0.25 0.25"
export CONFIG_PREFERENCES="1.0 0.0 0.5"
export CONFIG_TRANSITION_PROBS="0.9 0.1 0.1 0.8 0.1 0.9 0.7 0.3 0.2 0.8 0.8 0.2"
export CONFIG_TIME_STEPS=15
export CONFIG_PRECISION=4

validate_config() { return 0; }
echo "Configuration loaded successfully"
CONFIG_EOF
fi

# Make config executable
chmod +x config.sh

# Run the simulation
echo "🚀 Running Shell active inference simulation..."
./Active_Shellference.sh

echo ""
echo "✅ Shell simulation completed successfully!"
