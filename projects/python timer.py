#!/usr/bin/env python3
"""
Pomodoro Timer Automation using Selenium and vClock.com
Configured for Brave Browser
Alternates between 25-minute work sessions and 5-minute breaks
"""

import time
import sys
import os
import platform
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class PomodoroAutomation:
    """Main class for Pomodoro timer automation using Brave Browser"""
    
    def __init__(self):
        self.driver = None
        self.work_tab = None
        self.break_tab = None
        self.work_duration = 25  # minutes
        self.break_duration = 5  # minutes
        self.timer_url = "https://vclock.com/timer/"
        self.browser_type = "Brave"
        
    def find_brave_path(self):
        """Find Brave browser installation path"""
        system = platform.system()
        
        possible_paths = []
        
        if system == "Windows":
            possible_paths = [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
                os.path.expandvars(r"%PROGRAMFILES%\BraveSoftware\Brave-Browser\Application\brave.exe"),
                os.path.expandvars(r"%PROGRAMFILES(X86)%\BraveSoftware\Brave-Browser\Application\brave.exe"),
                os.path.join(os.path.expanduser("~"), r"AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"),
            ]
        elif system == "Darwin":  # macOS
            possible_paths = [
                "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
                os.path.expanduser("~/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
            ]
        else:  # Linux
            possible_paths = [
                "/usr/bin/brave-browser",
                "/usr/bin/brave",
                "/usr/local/bin/brave-browser",
                "/usr/local/bin/brave",
                "/opt/brave.com/brave/brave-browser",
                "/opt/brave.com/brave/brave",
                "/snap/bin/brave",
                os.path.expanduser("~/.local/bin/brave"),
                os.path.expanduser("~/.local/bin/brave-browser"),
            ]
        
        # Check each possible path
        for path in possible_paths:
            if os.path.exists(path):
                print(f"[{self.get_timestamp()}] Found Brave at: {path}")
                return path
        
        # If not found, print helpful message
        print(f"[{self.get_timestamp()}] Brave browser not found in standard locations")
        print(f"[{self.get_timestamp()}] Searched paths:")
        for path in possible_paths[:3]:  # Show first 3 paths as examples
            print(f"  - {path}")
        
        return None
    
    def setup_brave_browser(self):
        """Setup Brave browser with Selenium"""
        try:
            print(f"[{self.get_timestamp()}] Initializing Brave browser...")
            
            # Chrome options work for Brave since it's Chromium-based
            chrome_options = Options()
            
            # Find Brave executable
            brave_path = self.find_brave_path()
            
            if not brave_path:
                print(f"\n[{self.get_timestamp()}] ERROR: Brave browser not found!")
                print("\nPlease install Brave browser from: https://brave.com/download/")
                print("\nIf Brave is installed in a custom location, please check the script paths.")
                return False
            
            # Set Brave as the binary
            chrome_options.binary_location = brave_path
            
            # Browser options for stability
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--log-level=3")  # Suppress console messages
            
            # Disable Brave-specific features that might interfere
            chrome_options.add_argument("--disable-brave-update")
            chrome_options.add_argument("--disable-brave-rewards")
            chrome_options.add_argument("--disable-brave-wallet")
            
            # Create Chrome driver (works with Brave)
            print(f"[{self.get_timestamp()}] Downloading/updating ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            
            print(f"[{self.get_timestamp()}] Starting Brave browser...")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Maximize window
            self.driver.maximize_window()
            
            print(f"[{self.get_timestamp()}] Brave browser initialized successfully!")
            return True
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] Error setting up Brave browser: {e}")
            print("\nTroubleshooting tips:")
            print("1. Ensure Brave browser is installed")
            print("2. Try closing all Brave windows and run again")
            print("3. Check if antivirus is blocking the connection")
            return False
    
    def setup_browser(self):
        """Initialize Brave browser"""
        return self.setup_brave_browser()
    
    def setup_tabs(self):
        """Create and setup two tabs for work and break timers"""
        try:
            print(f"[{self.get_timestamp()}] Setting up timer tabs...")
            
            # Tab A - Work Timer
            print(f"[{self.get_timestamp()}] Loading work timer tab...")
            self.driver.get(self.timer_url)
            time.sleep(5)  # Give time for page to fully load
            self.work_tab = self.driver.current_window_handle
            print(f"[{self.get_timestamp()}] Work timer tab created")
            
            # Tab B - Break Timer
            print(f"[{self.get_timestamp()}] Creating break timer tab...")
            self.driver.execute_script("window.open('');")
            time.sleep(1)
            
            # Switch to new tab
            all_tabs = self.driver.window_handles
            for tab in all_tabs:
                if tab != self.work_tab:
                    self.break_tab = tab
                    break
            
            self.driver.switch_to.window(self.break_tab)
            print(f"[{self.get_timestamp()}] Loading break timer tab...")
            self.driver.get(self.timer_url)
            time.sleep(5)  # Give time for page to fully load
            print(f"[{self.get_timestamp()}] Break timer tab created")
            
            # Switch back to work tab
            self.driver.switch_to.window(self.work_tab)
            
            print(f"[{self.get_timestamp()}] Both timer tabs ready!")
            return True
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] Error setting up tabs: {e}")
            return False
    
    def get_timestamp(self):
        """Get current timestamp for logging"""
        return datetime.now().strftime("%H:%M:%S")
    
    def switch_tab(self, tab_handle):
        """Switch to specified browser tab"""
        try:
            self.driver.switch_to.window(tab_handle)
            time.sleep(1.5)  # Small delay to ensure smooth switching
            return True
        except Exception as e:
            print(f"[{self.get_timestamp()}] Error switching tabs: {e}")
            return False
    
    def set_timer_duration(self, minutes):
        """Set timer duration on vClock.com"""
        try:
            # Wait for page to be ready
            time.sleep(2)
            
            # Use JavaScript to set timer values directly
            script = f"""
                // Set timer values
                var hourInput = document.getElementById('hours') || document.querySelector('input[name="hours"]');
                var minuteInput = document.getElementById('minutes') || document.querySelector('input[name="minutes"]');
                var secondInput = document.getElementById('seconds') || document.querySelector('input[name="seconds"]');
                
                if (hourInput) {{
                    hourInput.value = '0';
                    hourInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                
                if (minuteInput) {{
                    minuteInput.value = '{minutes}';
                    minuteInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                
                if (secondInput) {{
                    secondInput.value = '0';
                    secondInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                
                // Alternative method for vClock
                if (typeof setTimer === 'function') {{
                    setTimer(0, {minutes}, 0);
                }}
            """
            
            self.driver.execute_script(script)
            time.sleep(1)
            
            print(f"[{self.get_timestamp()}] Timer set to {minutes} minutes")
            return True
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] Error setting timer duration: {e}")
            
            # Fallback method: Try using Selenium selectors
            try:
                wait = WebDriverWait(self.driver, 5)
                
                # Try to find input fields
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    inp_id = inp.get_attribute("id") or ""
                    inp_name = inp.get_attribute("name") or ""
                    
                    if "hour" in inp_id.lower() or "hour" in inp_name.lower():
                        inp.clear()
                        inp.send_keys("0")
                    elif "minute" in inp_id.lower() or "minute" in inp_name.lower():
                        inp.clear()
                        inp.send_keys(str(minutes))
                    elif "second" in inp_id.lower() or "second" in inp_name.lower():
                        inp.clear()
                        inp.send_keys("0")
                
                time.sleep(1)
                return True
                
            except:
                return False
    
    def start_timer(self):
        """Start the timer on current tab"""
        try:
            time.sleep(1)
            
            # JavaScript to click start button
            script = """
                // Find and click start button
                var startButton = document.querySelector('button:not([disabled])') || 
                                 document.querySelector('input[type="button"]:not([disabled])');
                
                // Look for button with "Start" text
                var buttons = document.querySelectorAll('button, input[type="button"], input[type="submit"]');
                for (var i = 0; i < buttons.length; i++) {
                    var btn = buttons[i];
                    if ((btn.textContent && btn.textContent.toLowerCase().includes('start')) ||
                        (btn.value && btn.value.toLowerCase().includes('start'))) {
                        if (!btn.disabled) {
                            btn.click();
                            return true;
                        }
                    }
                }
                
                // Alternative: trigger start function directly if available
                if (typeof startTimer === 'function') {
                    startTimer();
                    return true;
                }
                if (typeof start === 'function') {
                    start();
                    return true;
                }
                
                return false;
            """
            
            result = self.driver.execute_script(script)
            
            if result:
                print(f"[{self.get_timestamp()}] Timer started")
                return True
            
            # Fallback: Try Selenium click
            wait = WebDriverWait(self.driver, 5)
            selectors = [
                "//button[contains(translate(text(), 'START', 'start'), 'start')]",
                "//input[@type='button' and contains(translate(@value, 'START', 'start'), 'start')]",
                "//button[contains(@class, 'start')]",
                "//button[contains(@id, 'start')]"
            ]
            
            for selector in selectors:
                try:
                    button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    button.click()
                    print(f"[{self.get_timestamp()}] Timer started")
                    return True
                except:
                    continue
            
            print(f"[{self.get_timestamp()}] Could not find start button, timer may already be running")
            return True  # Continue anyway
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] Error starting timer: {e}")
            return False
    
    def stop_timer(self):
        """Stop/Reset the timer on current tab"""
        try:
            # Refresh the page to reset timer
            self.driver.refresh()
            time.sleep(4)
            return True
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] Error stopping timer: {e}")
            return False
    
    def start_work_timer(self):
        """Start a 25-minute work session"""
        print(f"\n[{self.get_timestamp()}] ====== WORK SESSION STARTING ======")
        
        # Switch to work tab
        if not self.switch_tab(self.work_tab):
            return False
        
        time.sleep(2)
        
        # Reset timer first
        self.stop_timer()
        time.sleep(2)
        
        # Set duration
        if not self.set_timer_duration(self.work_duration):
            print(f"[{self.get_timestamp()}] Warning: Could not set timer duration, using default")
        
        time.sleep(1)
        
        # Start timer
        if not self.start_timer():
            print(f"[{self.get_timestamp()}] Warning: Could not start timer automatically")
        
        print(f"[{self.get_timestamp()}] Work session active ({self.work_duration} minutes)")
        print(f"[{self.get_timestamp()}] Expected completion: {self.get_completion_time(self.work_duration)}")
        
        # Progress indicator
        print(f"[{self.get_timestamp()}] Progress: ", end="")
        for i in range(self.work_duration):
            print(".", end="", flush=True)
            time.sleep(60)  # Wait 1 minute
        print(" Done!")
        
        print(f"[{self.get_timestamp()}] Work session completed!")
        return True
    
    def start_break_timer(self):
        """Start a 5-minute break session"""
        print(f"\n[{self.get_timestamp()}] ====== BREAK SESSION STARTING ======")
        
        # Switch to break tab
        if not self.switch_tab(self.break_tab):
            return False
        
        time.sleep(2)
        
        # Reset timer first
        self.stop_timer()
        time.sleep(2)
        
        # Set duration
        if not self.set_timer_duration(self.break_duration):
            print(f"[{self.get_timestamp()}] Warning: Could not set timer duration, using default")
        
        time.sleep(1)
        
        # Start timer
        if not self.start_timer():
            print(f"[{self.get_timestamp()}] Warning: Could not start timer automatically")
        
        print(f"[{self.get_timestamp()}] Break session active ({self.break_duration} minutes)")
        print(f"[{self.get_timestamp()}] Expected completion: {self.get_completion_time(self.break_duration)}")
        
        # Progress indicator
        print(f"[{self.get_timestamp()}] Progress: ", end="")
        for i in range(self.break_duration):
            print(".", end="", flush=True)
            time.sleep(60)  # Wait 1 minute
        print(" Done!")
        
        print(f"[{self.get_timestamp()}] Break session completed!")
        return True
    
    def get_completion_time(self, minutes):
        """Calculate and return expected completion time"""
        from datetime import timedelta
        completion = datetime.now() + timedelta(minutes=minutes)
        return completion.strftime("%H:%M:%S")
    
    def main_loop(self):
        """Main Pomodoro loop - alternates between work and break"""
        session_count = 0
        
        print(f"\n[{self.get_timestamp()}] Starting Pomodoro automation loop...")
        print(f"[{self.get_timestamp()}] Browser: {self.browser_type}")
        print(f"[{self.get_timestamp()}] Work: {self.work_duration} min | Break: {self.break_duration} min")
        print(f"[{self.get_timestamp()}] Press Ctrl+C to stop\n")
        
        try:
            while True:
                session_count += 1
                print(f"\n{'='*60}")
                print(f"[{self.get_timestamp()}] POMODORO CYCLE #{session_count}")
                print(f"{'='*60}")
                
                # Work session
                if not self.start_work_timer():
                    print(f"[{self.get_timestamp()}] Error in work timer, retrying...")
                    time.sleep(5)
                    continue
                
                # Break session
                if not self.start_break_timer():
                    print(f"[{self.get_timestamp()}] Error in break timer, retrying...")
                    time.sleep(5)
                    continue
                
                print(f"\n[{self.get_timestamp()}] ✓ Cycle #{session_count} completed successfully!")
                
        except KeyboardInterrupt:
            print(f"\n\n[{self.get_timestamp()}] Pomodoro automation stopped by user")
            print(f"[{self.get_timestamp()}] Total sessions completed: {session_count}")
        
        except Exception as e:
            print(f"\n[{self.get_timestamp()}] Unexpected error: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources and close browser"""
        try:
            print(f"\n[{self.get_timestamp()}] Cleaning up...")
            if self.driver:
                self.driver.quit()
            print(f"[{self.get_timestamp()}] Brave browser closed. Goodbye!")
        except:
            pass
    
    def run(self):
        """Main entry point for the automation"""
        print("="*60)
        print(" POMODORO TIMER AUTOMATION - BRAVE BROWSER EDITION")
        print("="*60)
        
        # Setup browser
        if not self.setup_browser():
            print("\n[ERROR] Failed to initialize Brave browser.")
            print("\nPlease ensure:")
            print("1. Brave browser is installed (https://brave.com/download/)")
            print("2. The browser path in the script matches your installation")
            sys.exit(1)
        
        # Setup tabs
        if not self.setup_tabs():
            print("[ERROR] Failed to setup timer tabs.")
            self.cleanup()
            sys.exit(1)
        
        # Start main loop
        self.main_loop()


def main():
    """Main function"""
    try:
        # Check for required packages
        try:
            import selenium
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            print("Missing required packages. Please install:")
            print("pip install selenium webdriver-manager")
            sys.exit(1)
        
        # Create and run automation
        pomodoro = PomodoroAutomation()
        pomodoro.run()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()