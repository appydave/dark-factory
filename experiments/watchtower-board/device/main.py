# Auto-run the Factory Front Desk on boot.
#
# install_apps.py detects this root-level main.py and sets UIFlow NVS
# boot_option=2, so UIFlow's boot.py hands straight to this file instead
# of showing the launcher menu — the device boots directly into the app.
#
# frontdesk.py lives in /flash/apps/ and calls run() at its module bottom,
# so importing it starts the app loop. ESC/Q inside the app does
# machine.reset(), which re-enters here (boot_option=2) and relaunches —
# i.e. the front desk is always-on, which is what we want for a desk device.
import sys
if "/flash/apps" not in sys.path:
    sys.path.insert(0, "/flash/apps")

import frontdesk  # noqa: F401  — module bottom calls run(), starting the app
