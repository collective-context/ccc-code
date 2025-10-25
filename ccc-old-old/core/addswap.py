"""CCC CODE Swap Creation"""
import os

import psutil

from ccc.core.aptget import CCCAptGet
from ccc.core.fileutils import CCCFileUtils
from ccc.core.logging import Log
from ccc.core.shellexec import CCCShellExec


class CCCSwap():
    """Manage Swap"""

    def __init__():
        """Initialize """
        pass

    def add(self):
        """Swap addition with CCC CODE"""
        # Get System RAM and SWAP details
        ccc_ram = psutil.virtual_memory().total / (1024 * 1024)
        ccc_swap = psutil.swap_memory().total / (1024 * 1024)
        if ccc_ram < 512:
            if ccc_swap < 1000:
                Log.info(self, "Adding SWAP file, please wait...")

                # Install dphys-swapfile
                CCCAptGet.update(self)
                CCCAptGet.install(self, ["dphys-swapfile"])
                # Stop service
                CCCShellExec.cmd_exec(self, "service dphys-swapfile stop")
                # Remove Default swap created
                CCCShellExec.cmd_exec(self, "/sbin/dphys-swapfile uninstall")

                # Modify Swap configuration
                if os.path.isfile("/etc/dphys-swapfile"):
                    CCCFileUtils.searchreplace(self, "/etc/dphys-swapfile",
                                              "#CONF_SWAPFILE=/var/swap",
                                              "CONF_SWAPFILE=/ccc-swapfile")
                    CCCFileUtils.searchreplace(self, "/etc/dphys-swapfile",
                                              "#CONF_MAXSWAP=2048",
                                              "CONF_MAXSWAP=1024")
                    CCCFileUtils.searchreplace(self, "/etc/dphys-swapfile",
                                              "#CONF_SWAPSIZE=",
                                              "CONF_SWAPSIZE=1024")
                else:
                    with open("/etc/dphys-swapfile", 'w') as conffile:
                        conffile.write("CONF_SWAPFILE=/ccc-swapfile\n"
                                       "CONF_SWAPSIZE=1024\n"
                                       "CONF_MAXSWAP=1024\n")
                # Create swap file
                CCCShellExec.cmd_exec(self, "service dphys-swapfile start")
