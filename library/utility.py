import ctypes
from library import winapi

def GetProcId(processName):
    procId = None
    hSnap = winapi.CreateToolhelp32Snapshot(winapi.TH32CS_SNAPPROCESS, 0)

    if (hSnap != winapi.INVALID_HANDLE_VALUE):
        procEntry = winapi.PROCESSENTRY32()
        procEntry.dwSize = ctypes.sizeof(winapi.PROCESSENTRY32)

        if (winapi.Process32First(hSnap, ctypes.byref(procEntry))):
            # Do While loops do not exist in python, to emulate this logic we will use a nested function.
            def processCmp(procEntry):
                if (procEntry.szExeFile.decode("utf-8") == processName):
                    nonlocal procId
                    procId = int(procEntry.th32ProcessID)

            processCmp(procEntry)
            while (winapi.Process32Next(hSnap, ctypes.byref(procEntry))):
                processCmp(procEntry)

    winapi.CloseHandle(hSnap)
    return(procId)

def GetModuleBaseAddress(pid, moduleName):
    baseAddress = None
    hSnap = winapi.CreateToolhelp32Snapshot(winapi.TH32CS_SNAPMODULE | winapi.TH32CS_SNAPMODULE32, pid)

    if (hSnap != winapi.INVALID_HANDLE_VALUE):
        modEntry = winapi.MODULEENTRY32()
        modEntry.dwSize = ctypes.sizeof(winapi.MODULEENTRY32)

        if (winapi.Module32First(hSnap, ctypes.byref(modEntry))):
            # Do While loops do not exist in python, to emulate this logic we will use a nested function.
            def moduleCmp(modEntry):
                if (modEntry.szModule.decode("utf-8") == moduleName):
                    nonlocal baseAddress
                    baseAddress = int(hex(ctypes.addressof(modEntry.modBaseAddr.contents)), 16)

            moduleCmp(modEntry)
            while (winapi.Module32Next(hSnap, ctypes.byref(modEntry))):
                moduleCmp(modEntry)

    winapi.CloseHandle(hSnap)
    return(baseAddress)

def FindDMAAddy(hProc, base, offsets, arch=64):

    size=8
    if (arch == 32): size = 4

    address = ctypes.c_uint64(base)

    for offset in offsets:
        winapi.ReadProcessMemory(hProc, address, ctypes.byref(address), size, 0)
        address = ctypes.c_uint64(address.value + offset)

    return(address.value)

def patchBytes(handle, src, destination, size):
    src = bytes.fromhex(src)
    size = ctypes.c_size_t(size)
    destination = ctypes.c_ulonglong(destination)
    oldProtect = ctypes.wintypes.DWORD()

    winapi.VirtualProtectEx(handle, destination, size, winapi.PAGE_EXECUTE_READWRITE, ctypes.byref(oldProtect))
    winapi.WriteProcessMemory(handle, destination, src, size, None)
    winapi.VirtualProtectEx(handle, destination, size, oldProtect, ctypes.byref(oldProtect))

def nopBytes(handle, destination, size):
    hexString = ""

    for i in range(size):
        hexString += "90"

    patchBytes(handle, hexString, destination, size)