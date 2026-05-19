from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import threading
import time
import json
import os

import security
import network
import secret_key

def get_device_id():
    from kivy.utils import platform
    if platform == 'android':
        from jnius import autoclass
        Secure = autoclass('android.provider.Settings$Secure')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        content_resolver = activity.getContentResolver()
        return Secure.getString(content_resolver, Secure.ANDROID_ID)
    else:
        return "pc_debug_id_12345"

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(MDLabel(text='输入卡密和代理模板', font_style='H5', halign='center'))
        self.key_field = MDTextField(hint_text='卡密', mode='rectangle')
        self.proxy_field = MDTextField(hint_text='代理模板 (user:pass@host:port)', mode='rectangle')
        layout.add_widget(self.key_field)
        layout.add_widget(self.proxy_field)
        self.activate_btn = MDRaisedButton(text='激活', size_hint=(1, 0.2))
        self.activate_btn.bind(on_press=self.start_activation)
        layout.add_widget(self.activate_btn)
        self.status_label = MDLabel(halign='center')
        layout.add_widget(self.status_label)
        self.add_widget(layout)

    def start_activation(self, instance):
        key = self.key_field.text.strip()
        proxy = self.proxy_field.text.strip()
        if not key or not proxy:
            self.status_label.text = '卡密和代理模板不能为空'
            return
        self.activate_btn.disabled = True
        self.status_label.text = '正在激活...'
        threading.Thread(target=self._activate, args=(key, proxy), daemon=True).start()

    def _activate(self, key, proxy):
        secret = secret_key.get_key()
        device = get_device_id()
        result = network.call_activate_api(key, device, proxy, secret)
        Clock.schedule_once(lambda dt: self._handle_result(result))

    def _handle_result(self, result):
        self.activate_btn.disabled = False
        code = result.get('code')
        if code == 200:
            expires = result.get('expires_at')
            try:
                with open('/sdcard/sniper_auth.json', 'w') as f:
                    json.dump({"expires_at": expires}, f)
            except:
                pass
            self.status_label.text = '激活成功！即将进入主界面...'
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'main'), 1)
        else:
            self.status_label.text = result.get('message', '未知错误')

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(MDLabel(text='脉冲IP狙击 (已授权)', font_style='H4', halign='center'))
        btn = MDRaisedButton(text='开始扫描（功能待集成）', size_hint=(1, 0.3))
        layout.add_widget(btn)
        self.add_widget(layout)

class SniperApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        security.run_security_checks()
        if self.check_local_auth():
            return MainScreen()
        else:
            return LoginScreen()

    def check_local_auth(self):
        try:
            with open('/sdcard/sniper_auth.json', 'r') as f:
                data = json.load(f)
                expires = data.get('expires_at', 0)
                if expires > time.time():
                    return True
        except:
            pass
        return False

if __name__ == '__main__':
    SniperApp().run()
