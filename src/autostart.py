import os
import sys
import winreg as reg

def add_to_startup(app_name, app_path):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key, app_name, 0, reg.REG_SZ, app_path)
        reg.CloseKey(key)
        return True
    except WindowsError:
        return False

def remove_from_startup(app_name):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS)
        reg.DeleteValue(key, app_name)
        reg.CloseKey(key)
        return True
    except WindowsError:
        return False