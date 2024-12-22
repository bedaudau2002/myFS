import os
import sys
import hashlib
import time
import random
import json
import struct
from cryptography.fernet import Fernet
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

class MyFSMetadata:
    def __init__(self):
        self.machine_id: str = self._get_machine_id()
        self.creation_date: str = datetime.now().isoformat()
        self.file_count: int = 0
        self.files: Dict[str, Dict] = {}
        self.master_key: Optional[bytes] = None
    
    def _get_machine_id(self) -> str:
        # Get unique machine identifier
        if sys.platform == 'win32':
            return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        return ''

class FileEntry:
    def __init__(self, name: str, size: int, original_path: str):
        self.name = name
        self.size = size
        self.original_path = original_path
        self.creation_time = datetime.now().isoformat()
        self.is_encrypted = False
        self.file_key: Optional[bytes] = None
        self.offset: int = 0
        self.attributes = {}

class MyFS:
    HEADER_SIZE = 1024
    MAX_FILES = 99
    IMPORTANT_FILE_THRESHOLD = 104857600  # 100MB

    def __init__(self, fs_path: str, metadata_path: str):
        self.fs_path = fs_path
        self.metadata_path = metadata_path
        self.metadata = MyFSMetadata()
        self.is_initialized = False
        self.password_attempts = 0
        self.last_otp_time = 0
        
    def format_fs(self, password: str) -> bool:
        """Initialize a new MyFS filesystem"""
        try:
            # Generate master encryption key
            key = Fernet.generate_key()
            self.metadata.master_key = key
            
            # Create empty filesystem file
            with open(self.fs_path, 'wb') as fs_file:
                fs_file.write(b'\0' * self.HEADER_SIZE)
            
            # Save encrypted metadata to separate volume
            self._save_metadata(password)
            self.is_initialized = True
            return True
        except:
            return False

    def _save_metadata(self, password: str) -> None:
        """Save encrypted metadata to separate volume"""
        metadata_dict = {
            'machine_id': self.metadata.machine_id,
            'creation_date': self.metadata.creation_date,
            'file_count': self.metadata.file_count,
            'files': self.metadata.files,
            'master_key': self.metadata.master_key.hex() if self.metadata.master_key else None
        }
        
        # Encrypt metadata with password
        key = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode(), 
            b'salt', 
            100000
        )
        f = Fernet(key)
        encrypted_data = f.encrypt(json.dumps(metadata_dict).encode())
        
        with open(self.metadata_path, 'wb') as f:
            f.write(encrypted_data)

    def verify_otp(self, challenge: int, response: int, timeout: int = 20) -> bool:
        """Verify OTP response within timeout period"""
        current_time = time.time()
        if current_time - self.last_otp_time > timeout:
            return False
        
        # Implement OTP verification logic here
        # This is a placeholder - actual implementation would be more complex
        return (response % 10000) == challenge

    def is_valid_machine(self) -> bool:
        """Check if current machine is the one that created the FS"""
        return self.metadata.machine_id == self._get_machine_id()

    def verify_program_integrity(self) -> bool:
        """Check program integrity"""
        # Calculate hash of current executable
        with open(sys.argv[0], 'rb') as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
            
        # Compare with stored hash (implementation needed)
        return True  # Placeholder

def import_file(self, file_path: str, encrypt: bool = False) -> bool:
    """Import a file into MyFS"""
    if self.metadata.file_count >= self.MAX_FILES:
        return False
        
    try:
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Create file entry
        entry = FileEntry(file_name, file_size, file_path)
        
        # Generate file key if encryption requested
        if encrypt:
            entry.file_key = Fernet.generate_key()
            entry.is_encrypted = True
            
        # Read and write file data
        with open(self.fs_path, 'ab') as fs_file, open(file_path, 'rb') as source_file:
            entry.offset = fs_file.tell()
            data = source_file.read()
            
            if encrypt:
                f = Fernet(entry.file_key)
                data = f.encrypt(data)
                
            fs_file.write(data)
            
        # Update metadata
        self.metadata.files[file_name] = entry.__dict__
        self.metadata.file_count += 1
        self._save_metadata(self.current_password)
        return True
    except:
        return False

def export_file(self, file_name: str, dest_path: str) -> bool:
    """Export a file from MyFS"""
    if file_name not in self.metadata.files:
        return False
        
    try:
        entry = self.metadata.files[file_name]
        with open(self.fs_path, 'rb') as fs_file, open(dest_path, 'wb') as dest_file:
            fs_file.seek(entry['offset'])
            data = fs_file.read(entry['size'])
            
            if entry['is_encrypted']:
                f = Fernet(bytes.fromhex(entry['file_key']))
                data = f.decrypt(data)
                
            dest_file.write(data)
        return True
    except:
        return False

def delete_file(self, file_name: str) -> bool:
    """Delete a file from MyFS"""
    if file_name not in self.metadata.files:
        return False
        
    del self.metadata.files[file_name]
    self.metadata.file_count -= 1
    self._save_metadata(self.current_password)
    return True

def list_files(self) -> List[Dict]:
    """List all files in MyFS"""
    return [
        {
            'name': name,
            'size': info['size'],
            'encrypted': info['is_encrypted'],
            'created': info['creation_time']
        }
        for name, info in self.metadata.files.items()
    ]

def set_file_password(self, file_name: str, password: str) -> bool:
    """Set password for specific file"""
    if file_name not in self.metadata.files:
        return False
        
    try:
        entry = self.metadata.files[file_name]
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)
        entry['file_key'] = key.hex()
        self._save_metadata(self.current_password)
        return True
    except:
        return False

def change_fs_password(self, old_password: str, new_password: str) -> bool:
    """Change filesystem password"""
    try:
        # Verify old password
        key = hashlib.pbkdf2_hmac('sha256', old_password.encode(), b'salt', 100000)
        f = Fernet(key)
        
        with open(self.metadata_path, 'rb') as file:
            f.decrypt(file.read())
            
        self.current_password = new_password
        self._save_metadata(new_password)
        return True
    except:
        return False

def main():
    # Create MyFS instance
    fs = MyFS('myfs.dat', 'metadata.dat')
    
    # Initialize with password
    password = input("Enter password to create filesystem: ")
    if not fs.format_fs(password):
        print("Failed to create filesystem")
        return
        
    # Basic command loop
    while True:
        cmd = input("\nEnter command (import/export/delete/list/exit): ").lower()
        
        if cmd == 'exit':
            break
        elif cmd == 'import':
            path = input("Enter file path: ")
            encrypt = input("Encrypt file? (y/n): ").lower() == 'y'
            if fs.import_file(path, encrypt):
                print("File imported successfully")
            else:
                print("Import failed")
        elif cmd == 'export':
            name = input("Enter filename: ")
            dest = input("Enter destination path: ")
            if fs.export_file(name, dest):
                print("File exported successfully")
            else:
                print("Export failed")
        elif cmd == 'delete':
            name = input("Enter filename: ")
            if fs.delete_file(name):
                print("File deleted successfully")
            else:
                print("Delete failed")
        elif cmd == 'list':
            files = fs.list_files()
            for f in files:
                print(f"\n{f['name']}")
                print(f"Size: {f['size']} bytes")
                print(f"Encrypted: {f['encrypted']}")
                print(f"Created: {f['created']}")
        else:
            print("Invalid command")

if __name__ == '__main__':
    main()

