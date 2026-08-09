# Zero-Knowledge Authenticator

An embedded authentication system that leverages Zero-Knowledge Proofs (ZKP) to enable secure, private authentication without revealing sensitive information.

## Overview

This project implements a cryptographic authentication mechanism for embedded systems using Zero-Knowledge Proofs. It allows a system to verify the identity of a user or device without ever exposing the actual secret credentials. This approach provides enhanced security and privacy for embedded applications.

## Key Features

- **Zero-Knowledge Proof Implementation**: Authenticates without exposing secrets
- **Embedded Systems Support**: Designed for resource-constrained environments
- **Cryptographic Security**: Uses proven cryptographic techniques
- **Privacy-Preserving**: Verifies identity without credential disclosure

## Technical Details

This project is written in **C** and is optimized for embedded systems, specifically targeting the **Texas Instruments Tiva microcontroller** platform.

### Dependencies

- **Energia IDE**: Development environment for Tiva boards
- **BigNumber.h Library**: Custom arbitrary precision arithmetic library for cryptographic operations

## Getting Started

### Prerequisites

- Tiva C Series microcontroller (or compatible)
- [Energia IDE](https://energia.nu/) installed
- USB cable for board programming

### Installation

1. **Set up the BigNumber library**:
   - Locate the `BigNumber.h` file in this repository
   - Copy it to your Energia libraries folder:
     - On Windows: `Documents\Energia\libraries\`
     - On macOS: `~/Documents/Energia/libraries/`
     - On Linux: `~/Energia/libraries/`

2. **Load the project**:
   - Open Energia IDE
   - Copy the contents of `foss_tiva` file into a new Energia sketch
   - Ensure the `BigNumber.h` library is imported in your sketch

3. **Upload and Run**:
   - Connect your Tiva board via USB
   - Select the correct board and COM port in Energia
   - Upload the sketch to the board
   - Run the executable to start the authentication system

## Project Structure

- `foss_tiva` - Main authentication implementation for Tiva platform
- `BigNumber.h` - Arbitrary precision arithmetic library for cryptographic calculations
- `HowToRun.txt` - Quick setup instructions
- `Report.docx` - Detailed technical documentation and research findings

## Documentation

For detailed information about the implementation, cryptographic theory, and design decisions, please refer to **Report.docx**.

## License

This project is open source. See the repository for license details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## Contact

For questions or inquiries, please reach out via GitHub issues.

---

**Note**: This is an educational and research project focused on zero-knowledge authentication in embedded systems.
