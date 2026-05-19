from kivy.utils import platform
import os
import sys

def is_emulator():
    if platform != 'android':
        return False
    from jnius import autoclass
    Build = autoclass('android.os.Build')
    f = (Build.FINGERPRINT + Build.BRAND + Build.MODEL + Build.DEVICE + Build.HARDWARE).lower()
    indicators = ["generic", "goldfish", "ranchu", "vbox", "qemu", "tencent", "leidian", "mumu", "bluestacks", "nox", "genymotion", "androVM"]
    for ind in indicators:
        if ind in f:
            return True
    paths = ["/system/lib/libc_malloc_debug_qemu.so", "/sys/qemu_trace", "/system/bin/qemu-props"]
    for p in paths:
        if os.path.exists(p):
            return True
    return False

def is_vpn_active():
    if platform != 'android':
        return False
    from jnius import autoclass, cast
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    ConnectivityManager = autoclass('android.net.ConnectivityManager')
    NetworkCapabilities = autoclass('android.net.NetworkCapabilities')
    activity = PythonActivity.mActivity
    cm = cast(ConnectivityManager, activity.getSystemService(Context.CONNECTIVITY_SERVICE))
    networks = cm.getAllNetworks()
    for net in networks:
        caps = cm.getNetworkCapabilities(net)
        if caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN):
            return True
    return False

def is_proxy_set():
    import urllib.request
    if urllib.request.getproxies():
        return True
    if platform != 'android':
        return False
    from jnius import autoclass
    SystemProperties = autoclass('android.os.SystemProperties')
    http_proxy = SystemProperties.get('net.hostname')
    if http_proxy:
        return True
    return False

def run_security_checks():
    if is_emulator():
        sys.exit("检测到模拟器，程序终止。")
    if is_vpn_active():
        sys.exit("请关闭VPN后使用。")
    if is_proxy_set():
        sys.exit("请关闭系统代理后使用。")