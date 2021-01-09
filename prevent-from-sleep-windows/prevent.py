# See
# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate
# for more options.
import ctypes
prev = ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000002)
print('Done, previous: ', hex(prev))
input('Press enter to stop.')
