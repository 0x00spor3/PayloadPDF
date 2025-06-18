import re
from cryptography.AES import AESCipher
import base64
import os

class PDFHiddenMessageExtractor:
    def __init__(self):
        self.content_str = ""
        self.start_obj = 0
        self.num_objects = 0
        self.max_obj_in_xref = 0
        self.hidden_obj_num = 0
        self.all_objects = set()
        self.referenced_objects = set()
        self.orphan_objects = set()
        
    def read_pdf(self, pdf_path):
        """Read PDF file and convert to string"""
        with open(pdf_path, 'rb') as f:
            content = f.read()
        
        # Convert to string for parsing
        self.content_str = content.decode('latin-1')
        print(f"PDF file loaded: {pdf_path}")
    
    def parse_xref_table(self):
        """Parse xref table and extract object information"""
        xref_pattern = r'xref\s*\n(\d+)\s+(\d+)\s*\n(.*?)\ntrailer'
        xref_match = re.search(xref_pattern, self.content_str, re.DOTALL)
        
        if not xref_match:
            print("❌ Error: xref table not found")
            return False
        
        self.start_obj = int(xref_match.group(1))  # First object (usually 0)
        self.num_objects = int(xref_match.group(2))  # Number of objects in xref
        
        print(f"📊 Xref table found:")
        print(f"   - First object: {self.start_obj}")
        print(f"   - Number of objects: {self.num_objects}")
        
        return True
    
    def calculate_hidden_object_number(self):
        """Calculate the hidden object number"""
        self.max_obj_in_xref = self.start_obj + self.num_objects - 1
        self.hidden_obj_num = self.max_obj_in_xref + 1
        
        print(f"🔍 Looking for hidden object number: {self.hidden_obj_num}")
        return self.hidden_obj_num
    
    def find_hidden_object(self, obj_num):
        """Find hidden object in content"""
        hidden_obj_pattern = rf'{obj_num}\s+0\s+obj\s*<<(.*?)>>\s*endobj'
        hidden_match = re.search(hidden_obj_pattern, self.content_str, re.DOTALL)
        
        if not hidden_match:
            print(f"❌ Hidden object {obj_num} not found")
            return None
        
        print(f"✅ Hidden object {obj_num} found!")
        return hidden_match
    
    def extract_object_content(self, obj_match):
        """Extract content from object match"""
        if not obj_match:
            return None
            
        obj_content = obj_match.group(1).strip()
        print(f"📝 Object content:\n{obj_content}")
        return obj_content
    
    def extract_asd_field(self, obj_content, encryption=False, encryption_key=None):
        """Extract /Asd field from object content"""
        if not obj_content:
            return None

        # Look specifically for /Asd field
        asd_pattern = r'/Asd\s+(?:\((.*?)\)|(\S+))'
        asd_match = re.search(asd_pattern, obj_content)

        if asd_match:
            # If it's in parentheses (string), use first group, otherwise second
            asd_value = asd_match.group(1) if asd_match.group(1) else asd_match.group(2)
            if encryption:
                aes = AESCipher(encryption_key)
                asd_value = aes.decrypt(asd_value.encode('ascii'))
            else:
                asd_value = base64.b64decode(asd_value.encode('ascii')).decode("utf-8")
            print(f"\n🔓 HIDDEN MESSAGE FOUND:")
            print(f"   /Asd field: {asd_value}")
            return asd_value
        else:
            print("❌ /Asd field not found in hidden object")
            return None
    
    def find_all_objects(self):
        """Find all objects in the PDF file"""
        all_obj_pattern = r'(\d+)\s+0\s+obj'
        self.all_objects = set(int(match.group(1)) for match in re.finditer(all_obj_pattern, self.content_str))
        return self.all_objects
    
    def find_referenced_objects(self):
        """Find objects referenced in xref table"""
        if self.num_objects > 0:
            self.referenced_objects = set(range(self.start_obj, self.start_obj + self.num_objects))
        else:
            self.referenced_objects = set()
        return self.referenced_objects
    
    def find_orphan_objects(self):
        """Find orphan objects (not referenced in xref)"""
        self.find_all_objects()
        self.find_referenced_objects()
        self.orphan_objects = self.all_objects - self.referenced_objects
        return self.orphan_objects
    
    def analyze_orphan_object(self, obj_num, encryption=False, encryption_key=None):
        """Analyze a specific orphan object"""
        print(f"\n🔍 Analyzing orphan object {obj_num}:")
        obj_pattern = rf'{obj_num}\s+0\s+obj\s*<<(.*?)>>\s*endobj'
        obj_match = re.search(obj_pattern, self.content_str, re.DOTALL)
        
        if obj_match:
            obj_content = obj_match.group(1).strip()
            print(f"   Content: {obj_content}")
            
            # Look for /Asd field
            asd_pattern = r'/Asd\s+(?:\((.*?)\)|(\S+))'
            asd_match = re.search(asd_pattern, obj_content)
            
            if asd_match:
                asd_value = asd_match.group(1) if asd_match.group(1) else asd_match.group(2)
                if encryption:
                    aes = AESCipher(encryption_key)
                    asd_value = aes.decrypt(asd_value.encode('ascii'))
                else:
                    asd_value = base64.b64decode(asd_value.encode('ascii')).decode("utf-8")
                print(f"   🔓 MESSAGE: {asd_value}")
                return asd_value
        return None

    def analyze_orphan_object_file(self, obj_num, encryption=False, encryption_key=None):
        """Analyze a specific orphan object and extract embedded files"""
        print(f"\n🔍 Analyzing orphan object {obj_num}:")
        obj_pattern = rf'{obj_num}\s+0\s+obj\s*<<(.*?)>>\s*endobj'
        obj_match = re.search(obj_pattern, self.content_str, re.DOTALL)
        
        if obj_match:
            obj_content = obj_match.group(1).strip()
            print(f"   Content: {obj_content}")
            
            file_patterns = [
                r'/(\S+)\s+([A-Za-z0-9+/=]+)',           # Base64 content
                r'/(\S+)\s+([0-9a-fA-F]+)',              # Hex content  
                r'/(\S+)\s+\(([A-Za-z0-9+/=\s]+)\)',     # Base64 in parentheses
                r'/(\S+)\s+\(([0-9a-fA-F\s]+)\)',        # Hex in parentheses
            ]
            file_match = None
            content_type = None
            
            for i, pattern in enumerate(file_patterns):
                file_match = re.search(pattern, obj_content)
                if file_match:
                    # Determine content type based on pattern index
                    content_type = 'base64' if i in [0, 2] else 'hex'
                    break

            if file_match:
                filename = file_match.group(1)
                raw_content = file_match.group(2).replace(' ', '').replace('\n', '')
                
                print(f"   📁 Found embedded file: {filename}")
                print(f"   📊 Content type: {content_type}")
                print(f"   📏 Content length: {len(raw_content)} characters")
                
                try:
                    # Convert base64 to byte
                    file_bytes = raw_content.encode("ascii")
                    if encryption and encryption_key:
                        aes = AESCipher(encryption_key)
                        file_bytes = aes.decrypt_byte(file_bytes)
                    else:
                        file_bytes = base64.b64decode(file_bytes)
                    
                    # Create output directory if it doesn't exist
                    output_dir = "extracted_files"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Create full path for the file
                    output_path = os.path.join(output_dir, filename)
                    
                    # Write file content
                    with open(output_path, 'wb') as f:
                        f.write(file_bytes)
                    
                    print(f"   ✅ File extracted successfully: {output_path}")
                    print(f"   📏 File size: {len(file_bytes)} bytes")
                    
                    return {
                        'filename': filename,
                        'path': output_path,
                        'size': len(file_bytes),
                        'byte_content': file_bytes
                    }
                    
                except ValueError as e:
                    print(f"   ❌ Error converting hex content: {e}")
                    return None
                except Exception as e:
                    print(f"   ❌ Error creating file: {e}")
                    return None
            else:
                print("   ⚠️  No embedded file pattern found")
                return None
        else:
            print(f"   ❌ Object {obj_num} not found")
            return None
    
    def extract_hidden_message(self, pdf_path, encryption=False, encryption_key=None):
        """Main method to extract hidden message from PDF"""
        try:
            # Step 1: Read PDF
            self.read_pdf(pdf_path)
            
            # Step 2: Parse xref table
            if not self.parse_xref_table():
                return None
            
            # Step 3: Calculate hidden object number
            self.calculate_hidden_object_number()
            
            # Step 4: Find hidden object
            hidden_match = self.find_hidden_object(self.hidden_obj_num)
            if not hidden_match:
                return None
            
            # Step 5: Extract object content
            obj_content = self.extract_object_content(hidden_match)

            # Step 6: Extract Asd field
            return self.extract_asd_field(obj_content, encryption, encryption_key)
            
        except Exception as e:
            print(f"Error during extraction: {str(e)}")
            return None
    
    def extract_all_hidden_objects(self, pdf_path, encryption=False, encryption_key=None):
        """Extended version that searches for all unreferenced objects in xref"""
        try:
            # Step 1: Read PDF
            self.read_pdf(pdf_path)
            
            # Step 2: Parse xref table for reference
            self.parse_xref_table()
            
            # Step 3: Find orphan objects
            self.find_orphan_objects()
            
            print(f"📊 Complete analysis:")
            print(f"   - Total objects in file: {len(self.all_objects)}")
            print(f"   - Objects referenced in xref: {len(self.referenced_objects)}")
            print(f"   - Orphan objects: {len(self.orphan_objects)}")
            
            messages = []
            
            if self.orphan_objects:
                print(f"🕵️ Orphan objects found: {sorted(self.orphan_objects)}")
                
                for obj_num in sorted(self.orphan_objects):
                    message = self.analyze_orphan_object(obj_num, encryption, encryption_key)
                    if message:
                        messages.append((obj_num, message))
            else:
                print("No orphan objects found")
            
            return messages
            
        except Exception as e:
            print(f"Error during extraction: {str(e)}")
            return []

    def extract_all_hidden_objects_file(self, pdf_path, encryption=False, encryption_key=None):
        """Extended version that searches for all unreferenced objects in xref"""
        try:
            # Step 1: Read PDF
            self.read_pdf(pdf_path)
            
            # Step 2: Parse xref table for reference
            self.parse_xref_table()
            
            # Step 3: Find orphan objects
            self.find_orphan_objects()
            
            print(f"📊 Complete analysis:")
            print(f"   - Total objects in file: {len(self.all_objects)}")
            print(f"   - Objects referenced in xref: {len(self.referenced_objects)}")
            print(f"   - Orphan objects: {len(self.orphan_objects)}")
            
            messages = []
            
            if self.orphan_objects:
                print(f"🕵️ Orphan objects found: {sorted(self.orphan_objects)}")
                
                for obj_num in sorted(self.orphan_objects):
                    message = self.analyze_orphan_object_file(obj_num, encryption, encryption_key)
                    if message:
                        messages.append((obj_num, message))
            else:
                print("No orphan objects found")
            
            return messages
            
        except Exception as e:
            print(f"Error during extraction: {str(e)}")
            return []