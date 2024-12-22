# myFS

## Overview
A secure file storage system with encryption capabilities and machine-specific binding.

## Features
- File encryption using Fernet symmetric encryption
- Machine-specific filesystem binding
- Password protection for individual files
- One-time password (OTP) verification
- File import/export functionality
- Maximum 99 files per filesystem

## Usage
```bash
# Run the program
python main.py

# Follow the prompts to:
- Create a new filesystem with password
- Import files (with optional encryption)
- Export files to your system
- Delete files from storage
- List all stored files
```

## Security Features
- Encrypted metadata storage
- Program integrity verification
- Password protection
- Machine binding for enhanced security


## Core Classes
### MyFSMetadata
```python
class MyFSMetadata:
```
Stores filesystem metadata including machine ID, creation date, file count, and file information
Maintains the master encryption key
Gets unique machine identifier for security binding
FileEntry
Represents individual file entries with properties like:
Name, size, original path
Creation time
Encryption status
File-specific encryption key
Storage offset
Custom attributes
Key Functions
1. Filesystem Creation
Initializes new filesystem
Generates master encryption key
Creates empty filesystem file with header
Saves encrypted metadata
Returns success/failure status
2. Metadata Management
Converts metadata to dictionary format
Encrypts metadata using password-derived key
Saves encrypted data to separate volume
Uses PBKDF2 for password-based key derivation
3. Security Verification
Implements OTP (One-Time Password) verification
Checks machine binding
Verifies program integrity through hash comparison
4. File Operations
Import: Adds files to filesystem with optional encryption
Export: Retrieves files with automatic decryption if needed
Delete: Removes files and updates metadata
5. File Management
Lists all files with their properties
Manages file-specific passwords
Handles filesystem password changes
Security Features Implemented
✅ Encrypted metadata storage
✅ Program integrity verification
✅ Password protection
✅ Machine binding
✅ File-level encryption
✅ OTP verification
The implementation creates a secure filesystem with encrypted storage, machine binding, and multiple layers of security verification.