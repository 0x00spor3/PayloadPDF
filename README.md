# PayloadPDF

A Python-based steganography tool that enables hiding and extracting secret data within PDF files without altering their visual appearance or functionality using advanced PDF structure manipulation techniques.

## 🔍 Overview

PayloadPDF implements sophisticated steganographic methods to conceal payloads within PDF documents. The tool employs the **orphan object technique** as its core method, creating unreferenced PDF objects that remain invisible to standard readers while preserving embedded data.

## ✨ Features

- **Payload Injection**: Embed executables, scripts, or binary data using `inject.py`
- **Payload Extraction**: Retrieve hidden content using `extract.py`
- **Encryption Support**: Optional payload encryption via cryptography module (AES-256)
- **Format Conversion**: PDF manipulation utilities in converter module
- **Cross-platform**: Windows, macOS, and Linux compatibility

## 🏗️ Architecture

The tool follows a modular design with specialized components:
The tool follows a modular design with specialized components:

PayloadPDF/
- converter/          # PDF format conversion utilities
- cryptography/       # Encryption/decryption modules  
- extractor/          # Payload extraction logic
- injector/           # Payload embedding mechanisms
- logger/             # Logging and debugging tools
- extract.py          # Main extraction script
- inject.py           # Main injection script
- parser.py           # Argument parser

## 🔬 Steganographic Method: Orphan Objects
The core technique creates orphan objects - PDF objects that exist in the file structure but are not referenced in the cross-reference table (xref). This approach offers several advantages:

- **Invisibility**: PDF readers ignore unreferenced objects completely
- **Preservation**: Original PDF functionality remains intact
- **Detection Resistance**: Standard analysis tools miss orphaned content
- **Capacity:** Can store substantial payloads without size limitations
### Technical Implementation

Standard PDF:
```
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] >> endobj
3 0 obj << /Type /Page ... >> endobj
```
Modified with Orphan:
```
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] >> endobj
4 0 obj << /Payload [HIDDEN_DATA encoded in base64] >> endobj ← ORPHAN
3 0 obj << /Type /Page ... >> endobj

xref
0 4
0000000000 65535 f
0000000010 00000 n ← obj 1
0000000156 00000 n ← obj 2 + 4 (ORPHAN) Offset
0000000223 00000 n ← obj 3
```

## 📦 Installation

```bash
git clone https://github.com/0x00spor3/PayloadPDF
cd PayloadPDF
pip install -r requirements.txt
```
## 🚀 Usage
### Inject Payload
#### File
```bash
python3 inject.py --i input.pdf --o output.pdf --m file --f test.exe --e Password 
```
#### Text
```bash
python3 inject.py --i input.pdf --o output.pdf --m text --t "Secret Text" --e Password 
```
### Extract Payload
#### File
```bash
python3 extract.py --i output.pdf --m file --e Password 
```
#### Text
```bash
python3 extract.py --i output.pdf --m text --e Password 
```
## 🎯 Use Cases
- **Security Research**: PDF malware analysis and detection evasion studies
- **Red Team Operations**: Covert payload delivery mechanisms
- **Digital Forensics**: Advanced data hiding investigations
- **Penetration Testing**: Bypassing content filtering systems
- **Academic Research**: Steganography algorithm development

## 🛡️ Detection Evasion Capabilities
- **Visual Integrity**: No changes to PDF appearance or layout
- **Functional Preservation**: All original PDF features remain operational
- **Metadata Consistency**: File properties appear unchanged
- **Scanner Bypass**: Evades standard antivirus and content filters
- **Forensic Resistance**: Requires specialized analysis to detect

## 📄 License
MIT License - See LICENSE file for full details.