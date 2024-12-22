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
## Core Classes
### MyFSMetadata
```python
class MyFSMetadata:
```
- Stores filesystem metadata including machine ID, creation date, file count, and file information
- Maintains the master encryption key
- Gets unique machine identifier for security binding
### FileEntry
```python
class FileEntry:
```
Represents individual file entries with properties like:
- Name, size, original path
- Creation time
- Encryption status
- File-specific encryption key
- Storage offset
- Custom attributes
## Key Functions
1. Filesystem Creation
```python
def format_fs(self, password: str) -> bool:
```
- Initializes new filesystem
- Generates master encryption key
- Creates empty filesystem file with header
- Saves encrypted metadata
- Returns success/failure status
2. Metadata Management
```python
def _save_metadata(self, password: str) -> None:
```

- Converts metadata to dictionary format
- Encrypts metadata using password-derived key
- Saves encrypted data to separate volume
- Uses PBKDF2 for password-based key derivation
3. Security Verification
```python
def verify_otp(self, challenge: int, response: int, timeout: int = 20) -> bool:
def is_valid_machine(self) -> bool:
def verify_program_integrity(self) -> bool:
```
- Implements OTP (One-Time Password) verification
- Checks machine binding
- Verifies program integrity through hash comparison
4. File Operations
```python
def import_file(self, file_path: str, encrypt: bool = False) -> bool:
def export_file(self, file_name: str, dest_path: str) -> bool:
def delete_file(self, file_name: str) -> bool:
```
- Import: Adds files to filesystem with optional encryption
- Export: Retrieves files with automatic decryption if needed
- Delete: Removes files and updates metadata
5. File Management
```python
def list_files(self) -> List[Dict]:
def set_file_password(self, file_name: str, password: str) -> bool:
def change_fs_password(self, old_password: str, new_password: str) -> bool:
```
- Lists all files with their properties
- Manages file-specific passwords
- Handles filesystem password changes

## Security Features Implemented
```
✅ Encrypted metadata storage
✅ Program integrity verification
✅ Password protection
✅ Machine binding
✅ File-level encryption
✅ OTP verification
```
The implementation creates a secure filesystem with encrypted storage, machine binding, and multiple layers of security verification.