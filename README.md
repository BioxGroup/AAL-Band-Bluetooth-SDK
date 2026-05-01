## AALBand Firmware 1.0-Bluetooth Branch

This branch contains the Bluetooth firmware for AALBand 1.0 devices.

### How to flash your device

1. **Download this branch**
  - Recommended: Click "Code" > "Download ZIP" on GitHub, then extract the files.
  - Or: Use `git clone` if you prefer.
  ```bash 
  git clone --branch 1.0-Bluetoth --single-branch https://github.com/BioxGroup/AALBand-Firmware-Flasher
  ```
2. **Connect your AALBand device**
  - Use a micro USB cable to connect the device to your Windows computer.

3. **Install the CP210x USB driver (required for Windows 11)**
  - Download the official driver from Silicon Labs:
    [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads)
  - Extract the ZIP file.
  - Right-click and install `silabser.inf` (or run the installer in the package).
  - If prompted, allow driver installation.

  > **Note:** Windows security requires user consent for driver installation. Always download and install the driver manually from the official source above.

4. **Open `flashtool.exe`**
  - Run the provided `flashtool.exe` program.
  - The program will automatically detect your device and flash the firmware.

5. **Wait for completion**
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
+45 5358 2038

-Email:
biox@bioxgroup.dk
