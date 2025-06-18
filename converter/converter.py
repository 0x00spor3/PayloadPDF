import platform
import subprocess
import sys
import os
import shutil

class PDFTraditionalConverter:
    def __init__(self):
        self.system = ""
        self.qpdf_installed = False
        
    def detect_operating_system(self):
        """Detect operating system"""
        self.system = platform.system().lower()
        print(f"🖥️  Operating system detected: {self.system}")
        return self.system
    
    def check_qpdf_installation(self):
        """Check if qpdf is installed"""
        try:
            result = subprocess.run(['qpdf', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ qpdf already installed: {result.stdout.strip()}")
                self.qpdf_installed = True
                return True
            else:
                print("❌ qpdf not found")
                self.qpdf_installed = False
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            print("❌ qpdf not installed")
            self.qpdf_installed = False
            return False
    
    def detect_linux_distribution(self):
        """Detect Linux distribution"""
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
            
            if 'ubuntu' in os_info or 'debian' in os_info:
                return 'debian'
            elif 'fedora' in os_info or 'rhel' in os_info or 'centos' in os_info:
                return 'redhat'
            else:
                return 'unknown'
        except FileNotFoundError:
            return 'unknown'
    
    def install_qpdf_linux(self):
        """Install qpdf on Linux systems"""
        distro = self.detect_linux_distribution()
        
        if distro == 'debian':
            print("🐧 Detected Debian/Ubuntu system")
            print("💡 Attempting installation without sudo...")
            
            try:
                result = subprocess.run(['apt', 'install', '-y', 'qpdf'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode != 0:
                    print("⚠️  Installation without privileges failed")
                    print("💡 Try manually: sudo apt install qpdf")
                    return False
                return True
            except:
                print("⚠️  Cannot install automatically")
                print("💡 Run manually: sudo apt update && sudo apt install qpdf")
                return False
                
        elif distro == 'redhat':
            print("🐧 Detected RedHat/Fedora system")
            print("💡 Run manually: sudo dnf install qpdf")
            return False
        else:
            print("⚠️  Unrecognized Linux distribution")
            print("💡 Install qpdf manually using your distribution's package manager")
            return False
    
    def install_qpdf_macos(self):
        """Install qpdf on macOS"""
        print("🍎 Detected macOS")
        
        if shutil.which('brew') is None:
            print("❌ Homebrew not found")
            print("💡 Install Homebrew from: https://brew.sh/")
            print("💡 Then run: brew install qpdf")
            return False
        
        try:
            result = subprocess.run(['brew', 'install', 'qpdf'], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                print(f"❌ Brew error: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"❌ Error installing via Homebrew: {e}")
            return False
    
    def try_winget_installation(self):
        """Try installing qpdf via winget"""
        if shutil.which('winget') is not None:
            print("📦 Using winget...")
            try:
                result = subprocess.run(['winget', 'install', 'qpdf', '--accept-source-agreements', '--accept-package-agreements'], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    print("✅ Installed via winget")
                    return True
                else:
                    print(f"⚠️  Winget failed: {result.stderr}")
            except Exception as e:
                print(f"⚠️  Winget error: {e}")
        return False
    
    def try_chocolatey_installation(self):
        """Try installing qpdf via chocolatey"""
        if shutil.which('choco') is not None:
            print("🍫 Using Chocolatey...")
            try:
                result = subprocess.run(['choco', 'install', 'qpdf', '-y'], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    print("✅ Installed via chocolatey")
                    return True
                else:
                    print(f"⚠️  Chocolatey failed: {result.stderr}")
            except Exception as e:
                print(f"⚠️  Chocolatey error: {e}")
        return False
    
    def try_scoop_installation(self):
        """Try installing qpdf via scoop"""
        if shutil.which('scoop') is not None:
            print("🥄 Using Scoop...")
            try:
                result = subprocess.run(['scoop', 'install', 'qpdf'], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    print("✅ Installed via scoop")
                    return True
                else:
                    print(f"⚠️  Scoop failed: {result.stderr}")
            except Exception as e:
                print(f"⚠️  Scoop error: {e}")
        return False
    
    def install_qpdf_windows(self):
        """Install qpdf on Windows"""
        print("🪟 Detected Windows")
        
        # Try different package managers
        if self.try_winget_installation():
            return True
        if self.try_chocolatey_installation():
            return True
        if self.try_scoop_installation():
            return True
        
        # No package manager worked
        print("❌ No package manager found")
        print("💡 Options:")
        print("   1. Install winget (Windows 10 1709+): https://github.com/microsoft/winget-cli")
        print("   2. Install chocolatey: https://chocolatey.org/install")
        print("   3. Install scoop: https://scoop.sh/")
        print("   4. Manual download: https://qpdf.sourceforge.io/")
        return False
    
    def install_qpdf(self):
        """Install qpdf based on operating system"""
        print(f"📦 Attempting to install qpdf on {self.system}...")
        
        try:
            if self.system == "linux":
                return self.install_qpdf_linux()
            elif self.system == "darwin":  # macOS
                return self.install_qpdf_macos()
            elif self.system == "windows":
                return self.install_qpdf_windows()
            else:
                print(f"❌ Operating system '{self.system}' not supported")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during installation: {e}")
            print("💡 Try manual installation")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def show_manual_installation_instructions(self):
        """Show manual installation instructions"""
        print("\n📋 MANUAL INSTALLATION INSTRUCTIONS:")
        
        if self.system == "linux":
            print("🐧 Linux:")
            print("   Ubuntu/Debian: sudo apt update && sudo apt install qpdf")
            print("   Fedora/RHEL:   sudo dnf install qpdf")
            print("   Arch:          sudo pacman -S qpdf")
            print("   openSUSE:      sudo zypper install qpdf")
        elif self.system == "darwin":
            print("🍎 macOS:")
            print("   With Homebrew: brew install qpdf")
            print("   With MacPorts: sudo port install qpdf")
            print("   Download:      https://qpdf.sourceforge.io/")
        elif self.system == "windows":
            print("🪟 Windows:")
            print("   Winget:        winget install qpdf")
            print("   Chocolatey:    choco install qpdf")
            print("   Scoop:         scoop install qpdf")
            print("   Download:      https://qpdf.sourceforge.io/")
        
        print("\n🔄 After installation, run the script again!")
    
    def validate_input_file(self, input_file):
        """Validate input file exists"""
        if not os.path.exists(input_file):
            print(f"❌ Input file not found: {input_file}")
            return False
        return True
    
    def build_conversion_command(self, input_file, output_file):
        """Build qpdf conversion command"""
        if self.system == "windows":
            cmd = [
                'qpdf', '--qdf',
                '--object-streams=disable',
                '--compress-streams=n', 
                '--normalize-content=y',
                '--preserve-unreferenced',
                '--deterministic-id',
                input_file, output_file
            ]
        else:
            cmd = [
                'qpdf', '--qdf',
                '--object-streams=disable',
                '--compress-streams=n', 
                '--normalize-content=y',
                '--preserve-unreferenced=n',
                '--deterministic-id',
                input_file, output_file
            ]
        return cmd
    
    def execute_conversion(self, cmd):
        """Execute the conversion command"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return True, result.stdout, result.stderr
            else:
                return False, result.stdout, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "", "Timeout during conversion (>60s)"
        except Exception as e:
            return False, "", str(e)
    
    def verify_output_file(self, output_file):
        """Verify output file was created successfully"""
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"📄 Output file created: {output_file} ({size} bytes)")
            return True
        return False
    
    def convert_pdf_to_traditional(self, input_file, output_file):
        """Convert PDF to traditional format using qpdf"""
        if not self.validate_input_file(input_file):
            return False
        
        print(f"🔄 Converting {input_file} → {output_file}")
        
        # Build and execute command
        cmd = self.build_conversion_command(input_file, output_file)
        success, stdout, stderr = self.execute_conversion(cmd)
        
        if success:
            print("✅ Conversion completed successfully!")
            return self.verify_output_file(output_file)
        else:
            print(f"❌ Error during conversion:")
            if stdout:
                print(f"   stdout: {stdout}")
            if stderr:
                print(f"   stderr: {stderr}")
            return False
    
    def setup_qpdf(self):
        """Setup qpdf installation"""
        if not self.check_qpdf_installation():
            print("\n⚠️  qpdf is not installed!")
            
            # Try automatic installation
            print("🔧 Attempting automatic installation...")
            if self.install_qpdf():
                # Verify again after installation
                if self.check_qpdf_installation():
                    print("✅ qpdf installed successfully!")
                    return True
                else:
                    print("❌ qpdf not working after installation")
                    self.show_manual_installation_instructions()
                    return False
            else:
                print("❌ Automatic installation failed")
                self.show_manual_installation_instructions()
                return False
        return True
    
    def convert_pdf(self, input_file, output_file):
        """Main method to convert PDF to traditional format"""
        print("🚀 Starting PDF conversion...")
        
        try:
            # Step 1: Detect operating system
            self.detect_operating_system()
            
            # Step 2: Setup qpdf
            if not self.setup_qpdf():
                return False
            
            # Step 3: Execute conversion
            return self.convert_pdf_to_traditional(input_file, output_file)
            
        except Exception as e:
            print(f"❌ Unexpected error in conversion process: {e}")
            return False