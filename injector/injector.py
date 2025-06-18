import re
import base64
from cryptography.AES import AESCipher

class PDFHiddenObjectInjector:
    def __init__(self):
        self.content_str = ""
        self.objects = []
        self.max_obj_num = 0
        self.total_objects = 0
        self.half_objects = 0
        self.new_obj_num = 0
        self.hidden_object = ""
        self.obj_length = 0
        
    def read_pdf(self, pdf_path):
        """Read PDF file and convert to string"""
        with open(pdf_path, 'rb') as f:
            content = f.read()
        
        # Convert to string for parsing (assuming ASCII/Latin-1)
        self.content_str = content.decode('latin-1')
        print(f"PDF file loaded: {pdf_path}")
    
    def analyze_objects(self):
        """Find and analyze all objects in the PDF"""
        obj_pattern = r'(\d+)\s+0\s+obj'
        self.objects = re.findall(obj_pattern, self.content_str)
        self.max_obj_num = max([int(obj) for obj in self.objects]) if self.objects else 0
        self.total_objects = len(self.objects)
        
        print(f"Objects found: {self.total_objects}")
        print(f"Maximum object number: {self.max_obj_num}")
        
        # Calculate half objects (floor division)
        self.half_objects = self.total_objects // 2
        print(f"Half objects (floor): {self.half_objects}")
    
    def create_hidden_object(self, payload, encryption, encryption_key):
        """Create the hidden orphan object"""
        self.new_obj_num = self.max_obj_num + 1
        if encryption:
            aes = AESCipher(encryption_key)
            enc = aes.encrypt(payload).decode("ascii")
            self.hidden_object = f"{self.new_obj_num} 0 obj << /Asd {enc} >> endobj"
        else:
            self.hidden_object = f"{self.new_obj_num} 0 obj << /Asd {base64.b64encode(payload.encode('ascii')).decode('ascii')} >> endobj"
        
        # Calculate byte length of object (with newlines)
        obj_with_newlines = "\n" + self.hidden_object + "\n"
        self.obj_length = len(obj_with_newlines.encode('latin-1'))
        print(f"New object length (with newlines): {self.obj_length} bytes")

    def create_hidden_object_file(self, payload, file_name, encryption, encryption_key):
        """Create the hidden orphan object"""
        self.new_obj_num = self.max_obj_num + 1
        if encryption:
            aes = AESCipher(encryption_key)
            enc = aes.encrypt_byte(payload).decode("ascii")
            self.hidden_object = f"{self.new_obj_num} 0 obj << /{file_name} {enc} >> endobj"
        else:
            self.hidden_object = f"{self.new_obj_num} 0 obj << /{file_name} {base64.b64encode(payload).decode('ascii')} >> endobj"
        
        # Calculate byte length of object (with newlines)
        obj_with_newlines = "\n" + self.hidden_object + "\n"
        self.obj_length = len(obj_with_newlines.encode('latin-1'))
        print(f"New object length (with newlines): {self.obj_length} bytes")
    
    def find_insertion_position(self):
        """Find the position to insert the hidden object"""
        obj_pattern = r'(\d+)\s+0\s+obj'
        obj_positions = []
        
        for match in re.finditer(obj_pattern, self.content_str):
            obj_num = int(match.group(1))
            obj_positions.append((obj_num, match.start()))
        
        obj_positions.sort()
        
        # Find insertion position (after object at position half_objects-1)
        if self.half_objects > 0 and self.half_objects <= len(obj_positions):
            target_obj_num = obj_positions[self.half_objects-1][0]
            # Find end of target object
            end_pattern = rf'{target_obj_num}\s+0\s+obj.*?endobj'
            match = re.search(end_pattern, self.content_str, re.DOTALL)
            if match:
                insert_pos = match.end()
            else:
                insert_pos = len(self.content_str) // 2  # fallback
        else:
            insert_pos = len(self.content_str) // 2
        
        return insert_pos
    
    def insert_hidden_object(self, insert_pos):
        """Insert the hidden object at the specified position"""
        self.content_str = (self.content_str[:insert_pos] + "\n" + 
                           self.hidden_object + "\n" + 
                           self.content_str[insert_pos:])
        print(f"Hidden object {self.new_obj_num} inserted at position {insert_pos}")
    
    def update_xref_table(self):
        """Update the xref table with new offsets"""
        xref_pattern = r'xref\s*\n(.*?)\ntrailer'
        xref_match = re.search(xref_pattern, self.content_str, re.DOTALL)
        
        if xref_match:
            xref_content = xref_match.group(1)
            lines = xref_content.strip().split('\n')
            
            # First line should be "0 N" where N is the number of objects
            header_line = lines[0].strip()
            updated_lines = [header_line]
            
            # Process each xref entry
            for i, line in enumerate(lines[1:], 1):
                if re.match(r'\d{10}\s+\d{5}\s+[fn]', line.strip()):
                    # It's a valid xref entry
                    parts = line.strip().split()
                    offset = int(parts[0])
                    
                    # If this object comes after the insertion point
                    if i >= self.half_objects:  # Objects from half onwards
                        new_offset = offset + self.obj_length
                        updated_line = f"{new_offset:010d} {parts[1]} {parts[2]}"
                    else:
                        updated_line = line.strip()
                    
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line.strip())
            
            # Rebuild xref
            new_xref_content = '\n'.join(updated_lines)
            self.content_str = re.sub(xref_pattern, f'xref\n{new_xref_content}\ntrailer', 
                                    self.content_str, flags=re.DOTALL)
            print("Xref table updated successfully")
        else:
            print("Warning: Xref table not found")
    
    def update_startxref(self):
        """Update the startxref value"""
        startxref_pattern = r'startxref\s*\n(\d+)'
        startxref_match = re.search(startxref_pattern, self.content_str)
        
        if startxref_match:
            old_startxref = int(startxref_match.group(1))
            new_startxref = old_startxref + self.obj_length
            self.content_str = re.sub(startxref_pattern, f'startxref\n{new_startxref}', 
                                    self.content_str)
            print(f"Startxref updated: {old_startxref} -> {new_startxref}")
        else:
            print("Warning: Startxref not found")
    
    def save_pdf(self, output_path):
        """Save the modified PDF to file"""
        with open(output_path, 'wb') as f:
            f.write(self.content_str.encode('latin-1'))
        
        print(f"\nFile saved to: {output_path}")
        print(f"Hidden object {self.new_obj_num} injected successfully!")
        print(f"Offsets updated for objects from position {self.half_objects} onwards")
    
    def inject_hidden_object(self, pdf_path, output_path, payload, encryption=False, encryption_key=None):
        """Main method to inject hidden object into PDF"""
        try:
            print("Starting PDF hidden object injection...")
            
            # Step 1: Read PDF
            self.read_pdf(pdf_path)
            
            # Step 2: Analyze existing objects
            self.analyze_objects()
            
            # Step 3: Create hidden object
            self.create_hidden_object(payload, encryption, encryption_key)
            
            # Step 4: Find insertion position
            insert_pos = self.find_insertion_position()
            
            # Step 5: Insert hidden object
            self.insert_hidden_object(insert_pos)
            
            # Step 6: Update xref table
            self.update_xref_table()
            
            # Step 7: Update startxref
            self.update_startxref()
            
            # Step 8: Save modified PDF
            self.save_pdf(output_path)
            
            print("Injection completed successfully!")
            
        except Exception as e:
            print(f"Error during injection: {str(e)}")
            raise


    def inject_hidden_object_file(self, pdf_path, output_path, payload, file_name, encryption=False, encryption_key=None):
        """Main method to inject hidden object into PDF"""
        try:
            print("Starting PDF hidden object injection...")
            
            # Step 1: Read PDF
            self.read_pdf(pdf_path)
            
            # Step 2: Analyze existing objects
            self.analyze_objects()
            
            # Step 3: Create hidden object
            self.create_hidden_object_file(payload, file_name, encryption, encryption_key)
            
            # Step 4: Find insertion position
            insert_pos = self.find_insertion_position()
            
            # Step 5: Insert hidden object
            self.insert_hidden_object(insert_pos)
            
            # Step 6: Update xref table
            self.update_xref_table()
            
            # Step 7: Update startxref
            self.update_startxref()
            
            # Step 8: Save modified PDF
            self.save_pdf(output_path)
            
            print("Injection completed successfully!")
            
        except Exception as e:
            print(f"Error during injection: {str(e)}")
            raise
