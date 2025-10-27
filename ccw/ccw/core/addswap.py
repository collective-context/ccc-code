"""CCC CODE Swap Creation"""
import os

import psutil

from ccw.core.aptget import CCWAptGet
from ccw.core.fileutils import CCWFileUtils
from ccw.core.logging import Log
from ccw.core.shellexec import CCWShellExec
class CCWSwap():
    """Manage Swap"""

    def __init__():
        """Initialize """
        pass

    def add(self):
        """Swap addition with CCC CODE"""
        # Get System RAM and SWAP details
        ccw_ram = psutil.virtual_memory().total / (1024 * 1024)
        ccw_swap = psutil.swap_memory().total / (1024 * 1024)
        if ccw_ram < 512:
            if ccw_swap < 1000:
                Log.info(self, "Adding SWAP file, please wait...")

                # Install dphys-swapfile
                CCWAptGet.update(self)
                CCWAptGet.install(self, ["dphys-swapfile"])
                # Stop service
                CCWShellExec.cmd_exec(self, "service dphys-swapfile stop")
                # Remove Default swap created
                CCWShellExec.cmd_exec(self, "/sbin/dphys-swapfile uninstall")

                # Modify Swap configuration
                if os.path.isfile("/etc/dphys-swapfile"):
                    CCWFileUtils.searchreplace(self, "/etc/dphys-swapfile",
                                              "#CONF_SWAPFILE=/var/swap",
                                              "CONF_SWAPFILE=/ccw-swapfile")
                    CCWFileUtils.searchreplace(self, "/etc/dphys-swapfile",
                                              "#CONF_MAXSWAP=2048",
                                              "CONF_MAXSWAP=1024")
                    CCWFileUtils.searchreplace(self, "/etc/dphys-swapfile",
                                              "#CONF_SWAPSIZE=",
                                              "CONF_SWAPSIZE=1024")
                else:
                    with open("/etc/dphys-swapfile", 'w') as conffile:
                        conffile.write("CONF_SWAPFILE=/ccw-swapfile\n"
                                       "CONF_SWAPSIZE=1024\n"
                                       "CONF_MAXSWAP=1024\n")
                # Create swap file
                CCWShellExec.cmd_exec(self, "service dphys-swapfile start")

# Zuletzt bearbeitet: 2025-10-27
