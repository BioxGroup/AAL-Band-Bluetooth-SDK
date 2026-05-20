## AALBand SDK 2.0-Bluetooth 

This branch provides an SDK for Bluetooth connectivity with the AALBand v2.0, including a Python API and a firmware flashing tool for device programming.


[![Cited in Frontiers in Robotics](https://img.shields.io/badge/Cited-Frontiers%20in%20Robotics-blue)](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2020.567491/full)
[![Hardware](https://img.shields.io/badge/Hardware-AAL--Band%202.0-green)](https://www.bioxgroup.dk/webshop/aal-band-2-0-forearm-sensor/)

> **Institutional Access:** Full SDK documentation, zero-lag calibration scripts, and ROS integration examples are available via our research access portal. 
> 
> [→ Request SDK access with your institutional email here](https://www.bioxgroup.dk/webshop/aal-band-2-0-forearm-sensor/#sdk-gate)

### How to download

1. **Download this Release**
  - Recommended: Click "Code" > "Download ZIP" on GitHub, then extract the files.
  - Or: Use `git clone` if you prefer.
  ```bash 
  git clone --branch 2.0 --single-branch https://github.com/BioxGroup/AAL-Band-Bluetooth-SDK
  ```
### How to flach your device (do this to make sure the Python API works)

1. **Connect your AALBand device**
  - Use a micro USB cable to connect the device to your Windows computer.

2. **Install the CP210x USB driver (required for Windows 11)**
  - Download the official driver from Silicon Labs:
    [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads)
  - Extract the ZIP file.
  - Right-click and install `silabser.inf` (or run the installer in the package).
  - If prompted, allow driver installation.

  > **Note:** Windows security requires user consent for driver installation. Always download and install the driver manually from the official source above.

3. **Open `flashtool.exe`**
  - Run the provided `flashtool.exe` program.
  - The program will automatically detect your device and flash the firmware.

4. **Wait for completion**
  - The tool will notify you when flashing is complete.

---

If you have any issues, check:
- USB cable and port
- Driver installation (Device Manager should show CP210x device)
- Antivirus/firewall settings

## Contact & support

For support, contact us at:

-Address:
NOVI Science Park
Niels Jernes Vej 10
9220 Aalborg
DENMARK

-Phone:
+45 2135 9465

-Email:
biox@bioxgroup.dk
