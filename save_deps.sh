#!/usr/bin/env bash
# Save dependency versions on whichever Ubuntu machine executes this.
set -euo pipefail
out="${1:-deps_snapshot.txt}"
{
  echo "# Captured $(date -Is)"
  echo '# Operating system'; cat /etc/os-release || true
  echo '# Architecture'; uname -m
  echo '# Python'; python3 --version
  echo '# ROS'; echo "${ROS_DISTRO:-not sourced}"
  echo '# Jetson L4T (if present)'; cat /etc/nv_tegra_release 2>/dev/null || true
  echo '# Python packages'; python3 -m pip freeze || true
  echo '# ROS/Jetson Ubuntu packages'; dpkg-query -W 'ros-humble-*' 'nvidia-l4t-*' 2>/dev/null || true
} > "$out"
printf 'Saved dependency snapshot: %s\n' "$out"
