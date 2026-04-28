#!/bin/bash
# check_errors.sh
# Usage: bash check_errors.sh [err_dir]

ERR_DIR=${1:-err}   # default to ./err, or pass a custom path

echo "=== Scanning: $ERR_DIR ==="
echo ""

FAILED=0
CLEAN=0

for f in "$ERR_DIR"/*.err; do
    [ -f "$f" ] || { echo "No .err files found in $ERR_DIR"; exit 1; }

    if [ -s "$f" ]; then
        echo "❌ FAILED: $f"
        echo "   $(wc -l < "$f") lines | Last 3:"
        tail -3 "$f" | sed 's/^/   /'
        echo ""
        ((FAILED++))
    else
        ((CLEAN++))
    fi
done

echo "================================"
echo "✅ Clean:  $CLEAN"
echo "❌ Failed: $FAILED"
echo "Total:     $((CLEAN + FAILED))"